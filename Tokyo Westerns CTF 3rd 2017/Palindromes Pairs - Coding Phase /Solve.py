from pwn import *
import time

def palindrome(num):
    return num == num[::-1]


s=remote("ppc1.chal.ctf.westerns.tokyo", 8765)
print s.recvuntil("--\n")
c=0
while True:
	c+=1
	print s.recvuntil("/50\n")
	number=s.recvuntil("\n")
	print number
	data=  s.recvuntil("\n")
	print data
	list=[]
	list=data.split(" ")
	list[len(list)-1]=list[len(list)-1].replace("\n","")
	count=0
	ii=0
	for i in list:
                for j in list:
                        if palindrome(i+j):
                                count+=1
        print "[+] count : " + str(count)
        s.sendline(str(count))
        print s.recvuntil("!")
	if c==50:
		break

time.sleep(0.9)
print s.recv(1024)

