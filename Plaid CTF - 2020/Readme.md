# Plaid CTF 2020 Challenge golf.so 


## Description
> Thinking that Bovik’s flags might be hidden in plain sight, you find on your minimap of the Inner Sanctum that there’s a golf course tucked into the northeast corner. Before other people catch on to the idea, you sneak off towards the rolling grassy hills of the golf course.
> 
> As you walk up to the entrance, a small man with pointy ears pops up out of the ground.
> 
> “Would you like to play? Right now almost nobody is here, so it’ll only be a thousand checkers to play a round.“
> 
> You wave your hand and send the man the required amount. It’s not a lot of money, but your balance dwindles to a paltry sum.
> 
> “Thanks! Enjoy your game.“
> 
> A golf club appears in your hand along with a ball that looks suspiciously too large. The start of the first hole beckons, and you stride over to tee off.
> 
> http://golf.so.pwni.ng

## Solution
This is a team work result between Me, Tnmch and Rekter0.
Consulting the web service reveals two pages:

 - Scoreboard with the teams ranking and file size of each submission
 - Upload page that describes the following :
 > Upload a 64-bit ELF shared object of size at most 1024 bytes. It should spawn a shell (execute `execve("/bin/sh", ["/bin/sh"], ...)`) when used like
> 
> `LD_PRELOAD=<upload> /bin/true`

So our goal is to contruct a shared library that executes `execve("/bin/sh",["/bin/sh"],)` that does not exceeds 1024 as size.

First we started by writing minimal shellcode  that do this for us. here is what it looks like:
```
global _init
section .text
_init:
    xor rdx, rdx
    mov rbx, 0x68732f6e69622fff
    shr rbx, 0x8
    push rbx
    mov rdi, rsp
    xor rax, rax
    push rax
    push rdi
    mov rsi, rsp
    mov al, 0x3b
    syscall
``` 
to compile the shellcode we need `nasm` utility to generate an object file that will be transferred into a shared library using gcc.
```bash
nasm -f elf64 shellcode.asm -o shellcode.o
```
now when it comes to getting our shared library we used gcc options in order to get the minimal possible size through removing protections that are saved later on the ELF header then we used `strip` command in order to delete unnecessary  sections like `.GNU_STACK` `.note*` `.dynsym` `.dynstr` and so many others.
most of the mentioned sections are generally used to map certain function to their corresponsdance in external libraries like libc, ld and others needed by the binary and since in our case we are dealing directly with syscalls we don't need any dynamic interpretations.
here is the final command:
```bash
gcc -nostdlib -Wl,--build-id=none -fno-stack-protector -flto -fPIC 
-shared shellcode.o -o golf.so -nostartfiles -T linker -z no-execstack && 
strip -S --strip-unneeded --remove-section=.note.gnu.gold-version 
--remove-section=.comment --remove-section=.note 
--remove-section=.note.gnu.build-id --remove-section=.note.ABI-tag golf.so
```

the output file has 856 bytes which allow us to try our version against the server through upload functionnality here is the result :
>`You made it to level 0: non-trivial! You have 428 bytes left to be considerable. This effort is worthy of 0/2 flags.`

euuh we need to remove another 428 bytes and looking at other teams ranking, some of them made a binary with 138 btyes only make me feel frustrated xD ! 
before diving into internal ELF headers, i said why don't we try to delete a byte or two each time at random places and check if the binary still functional or not ! 
i made a small python script like the following:
```python

content = open("golf.so").read()
for i in range(0,len(content),2):
    a=content[:i:]+content[i+2::]
    with open("golf_{}.so".format(str(i)),"w") as file:
        file.write(a)
        file.close()
```
repeating the following process until we got a binary with 427 bytes only ! we tried our luck against the server aand : 
>You made it to level 1: considerable! You have 127 bytes left to be thoughtful. This effort is worthy of 0/2 flags.

euuh we made it to level 1 but no flags till now ! and we need another 127 bytes to be removed.
At this moment things are getting more serious because no brute force nor fuzzing is needed we just need to understand how ELF headers are in order to conclude which parts can we remove without corrupting the final file.
we used the following [article](https://linux-audit.com/elf-binaries-on-linux-understanding-and-analysis/) which describes well how ELF file are being constructed and composed of different parts (Header + Data).

using `readelf -a golf.so` we can get the different sections of the file, in our case ony LOAD and DYNAMIC sections are available as well as theirs offets, entries, size and permissions.
LOAD section is generally contains code, data and other informations that needs to be present at runtime also DYNAMIC which is responsible for holding informations about dynamic linking.
according to the following [article](https://refspecs.linuxbase.org/LSB_3.1.1/LSB-Core-generic/LSB-Core-generic/dynamicsection.html)  we can conlude that most of the `ELF64_DYN` are not need at all thus we can save more bytes through deleting those entries carefully using a hexeditor.
now we have a corrypted file with 233 because we should fix  `p_align` value that corresponds to the entry point of the file (because its calculated using `DYN.DT_FINI` that we deleted) now we should fix it. 
And since i'm too lazy to calculate that offset using the manual i went for brute force approach another time (because why not \o/) .
```python
content = open("golf.so","r").read()
from itertools import product

for i in product("abcdef0123456789",repeat=4):
    a = content[:224:]+''.join(i).decode("hex")+content[226::]
    with open("golf_{}.so".format(''.join(i)),"w") as file:
        file.write(a)
        file.close()
```
then a simple bash loop in order to find the correct file that spawn a shell for us :
```bash
`for i in $(ls golf_*) ; do echo $i ; LD_PRELOAD=./$i /bin/true ; done`
```
and we got a fixed file using 0x7d offset and a total file size 233.
we went so fast trying this binary against the web server 
![enter image description here](https://i.imgflip.com/3q4nd0.png)

 and this time we got a flag \o/
>You made it to level 2: thoughtful! You have 9 bytes left to be hand-crafted. This effort is worthy of 1/2 flags. PCTF{th0ugh_wE_have_cl1mBed_far_we_MusT_St1ll_c0ntinue_oNward}

Hopfully our efforts during 10 hours were not in vain !
Now `DYNAMIC` section contains only `DYN.INIT`, `DYN.STRTAB` and `DYN.SYMTAB` and those values are mandatory for running the file but its content are not important so why we don't we put the shellcode there instead of .text section ?

To confirm this hypothesis, we throwed multiples CC opcode which stands for TRAP/Breakpoint instruction in those entries and we run the shared library and we got a beautiful `Trace/breakpoint trap`.
Now the approach consists of dividing the shellcode into three parts, first part contains only 8 bytes so we don't have much choice but putting
```
xor rdx, rdx
xor rax, rax
```
but how can we move the next part hein ? it's here where jmp instruction comes to play through EB XX opcode. (XX is the offset of the next instructon starting from the jmp instruction + 2 bytes of 'EB' instruction).
Calculating that offset leads to the first part being (two XORs + JMP to second part):
`48 31 d2 48 31 c0 eb 08`
with the same analogy we put the mov bin_sh instruction into the 2nd field which can contains 12 bytes and another jmp like the following (MOV bin_sh + JMP to last part ):
`48 bb ff 2f 62 69 6e 2f 73 68 eb 7c`
and the final part is as the following: 
`48 c1 eb 08 53 48 89 e7  50 57 48 89 e6 b0 3b 0f 05`

And based on the above modifications we got a binary with 193 bytes only! 
testing the file gave us a wonderful feeling of satisfaction:
>You made it to level 5: record-breaking! You have 17 bytes left to be astounding. This effort is worthy of 2/2 flags. PCTF{th0ugh_wE_have_cl1mBed_far_we_MusT_St1ll_c0ntinue_oNward} PCTF{t0_get_a_t1ny_elf_we_5tick_1ts_hand5_in_its_ears_rtmlpntyea}

we were too lazy to minimize the file again in order to be among the TOP50 !
 
 I enjoyed alot playing this challenge through team working \o/ ! 

