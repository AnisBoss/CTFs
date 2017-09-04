import codecs
import sys
import random 
encrypted_hex = "7c153a474b6a2d3f7d3f7328703e6c2d243a083e2e773c45547748667c1511333f4f745e"
 
encrypted = codecs.decode(encrypted_hex, 'hex_codec')
 
msg_part = "TWCTF{"
key = []
 
# Recover first 6 characters
for i in range(0, 6):
    index = i + 1
 
    for j in range(0, 128):
        if chr((ord(msg_part[i]) + j + ord(encrypted[index - 1])) % 128) == encrypted[index]:
            key.append(chr(j))
 
for i in range(0, 7):
    key.append(None)
 
# Recover 4 characters in the end
ij = 0
for i in reversed(range(0, 4)):
    index = (len(encrypted) - 1) - (i + 9)
 
 
    for j in range(0, 128):
        if chr((j + ord(key[ij]) + ord(encrypted[index - 1])) % 128) == encrypted[index]:
            key[ij + 9] = chr(j)
 
    ij += 1
 
 
# Recover 3 characters
ij = 0
for i in reversed(range(0, 3)):
    index = (len(encrypted) - 1) - i
 
 
    for j in range(0, 128):
        if chr((j + ord(key[ij + 10]) + ord(encrypted[index - 1])) % 128) == encrypted[index]:
            key[ij + 6] = chr(j)
 
    ij += 1
 
print  "[+] Found the key : "+ ''.join(key)

clear="A"
key=''.join(key)
for i in range(0, len(encrypted)-1):
  clear+=chr((ord(encrypted[i+1])-ord(key[i % len(key)])-ord(encrypted[i]))%128)




print "[+] Found FLag : "+ clear
