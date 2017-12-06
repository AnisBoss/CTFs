# G2foss-CTF_Writeup
Task crypto 25
```py
import math
a = ["3130343034","3131363634"]
print ''.join(map(lambda x: chr(int(math.sqrt(int(x.decode("hex"))))) ,a))
```

  - - - -

Task Misc 75 (Pharaon)
```py
import requests
import hashlib

url="http://52.213.51.195/pyramid/"
request = requests.Session()
a=request.get(url)
n=int(a.content.split("<strong><u>")[1].split("</u>")[0])
row = int(n**(0.5))+1
first_in_row= (row-1)**2 +1
diff = n - first_in_row - 1
first = (row-2)**2 +1
answer = first +diff

m = hashlib.md5()
m.update(str(answer))
cipher=m.hexdigest()


dataa={"response" : cipher,"essai" : ""}
b=request.post(url,data=dataa)

print b.content
```

  - - - -

Task Misc 75 (P!N9U!N_0F_VZKV6VN)
```py
from pwn import *
import sys

s = ssh(host='34.251.13.38',
user='OpenNin',
password='OpenNin')
sh = s.shell('/bin/sh')
print sh.recv(1800)
print sh.recvuntil("\n")
sh.sendline("call 197")
print sh.recv(980)
print sh.recv(800)
sh.sendline(sys.argv[1]) #argv[1]="36.83,10.14" ENIT location
print sh.recv(4069)
print sh.recv(4069)

#FLAG : p{!n9uN_5@WuR!_K|}!-k_A5%5
```
