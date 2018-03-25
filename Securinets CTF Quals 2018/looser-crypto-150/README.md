## Description:
```
Can you help me recover the picture ?

Link : http://crypto.ctfsecurinets.com/0/flag.png.crypt
```
## Solution
The file has the png extension , so getting the header of a png and the encrypted header of the file given , <br>
we can figure out that the file is xored using the single byte \xee 
then running the following script reveals the original picture  

```python
def xor(data,key="\xee"):
        xored=""
        for i in data:
                xored+=chr(ord(i)^ord(key))
        return xored

content=""
with open("flag.png.crypt","r") as file :
        content=file.read()
        file.close()

plain=xor(content)

with open("flag.png","w") as file :
        file.write(plain)
        file.close()
```

# Flag{Hopefully_headers_are_constants}
