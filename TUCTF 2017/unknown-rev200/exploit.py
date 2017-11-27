#gdb -x exploit.py ./unknown

import gdb


pattern = "A"*56 #Password length is 56 
Chars="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!-_{}"
gdb.execute("break *0x0000000000401C84",True,True)

for i in range(len(Chars)):
	counter=0
	while True:
		pattern=pattern[:i:]+Chars[counter]+pattern[(i+1)::]
		print ("[-] failed : "+pattern)
		gdb.execute("r {}".format(pattern),True,True)
		for j in range(i):
                        gdb.execute("c",True,True)
		gdb.execute("ni",True,True)
		a = str(gdb.execute("x/i $rip",True,True))
		if ("add" in a):
			print ("[+] Found : "+pattern)
			counter=0
			break
		counter+=1



#Flag="TUCTF{w3lc0m3_70_7uc7f_4nd_7h4nk_y0u_f0r_p4r71c1p471n6!}"

