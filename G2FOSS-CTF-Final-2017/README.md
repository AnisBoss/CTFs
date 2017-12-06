# G2foss-CTF_Writeup
Task JS 25
```py
chaine="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
content=""
k=15;a=23;i=23;l=15;b=11;o=21;g=22;m=11;h=22;c=8;n=8;d=9;e=18;j=12;p=8;f=22;
for y in range(26):
        content=chaine[a]+chaine[b]+chaine[c]+chaine[d]+chaine[e]+chaine[f]+chaine[g]+chaine[h]+chaine[i]+chaine[j]+chaine[k]+chaine[l]+chaine[m]+chaine[n]+chaine[o]+chaine[p]
        a+=1;b+=1;c+=1;d+=1;e+=1;f+=1;g+=1;h+=1;i+=1;j+=1;k+=1;l+=1;m+=1;n+=1;o+=1;p+=1;
        print "counter  : "+str(y) + " "+content
        if a==26:a=0
        if b==26:b=0
        if c==26:c=0
        if d==26:d=0
        if e==26:e=0
        if f==26:f=0
        if g==26:g=0
        if h==26:h=0
        if i==26:i=0
        if j==26:j=0
        if k==26:k=0
        if l==26:l=0
        if m==26:m=0
        if n==26:n=0
        if o==26:o=0
        if p==26:p=0

```

  - - - -

Task Steg  75 

java -jar StegSolve.jar ;) 
#flag : God_FO2S_US
