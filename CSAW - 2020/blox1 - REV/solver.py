import interact
import struct

# Pack integer 'n' into a 8-Byte representation
def p64(n):
    return struct.pack('Q', n)

# Unpack 8-Byte-long string 's' into a Python integer
def u64(s):
    return struct.unpack('Q', s)[0]

p = interact.Process()
#input got from the record functionality <== because seed is fixed so the games keep repeating
p.sendline("\n            \n\n           \n\n           \n\n           \n\n           \n\n           \n\n            \n\n           \n\n           \n\n            \n\n           \n\n          \n\n           \n\n           \n\n            \n\n            \n\naaa waaaaa d0wdddddaaaa dddd caaa aawaaaaa cawwwaa waaaaa waaaaa a aaaaa aaaaa dddd dddd ")
p.interactive()
