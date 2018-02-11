Here we are given a pcap file which demonstrate ICMP exifiltration 
we can notice that the sender **192.168.42.218** send two bytes each time
Using tshark 
```bash
tshark -r challenge.pcapng -x 'icmp and  ip.src==192.168.42.218'|grep -i "*U........" |tr -s " "|cut -d " " -f 14 |sed 's/^.*\(.\{2\}\)$/\1/'|tr -d "\n"
>1f8b08006c4e7c5a0003edcf3d0ac2401005e01c65bb7432e3cc66ec6dbd43585ccc8a9b20d94910c4bb1bf0070bc1c620c27ecd2be6156f76d1350b3d69312300a82a3653a25878cd3bb6066949022c48620059080a03738e7a1892ba7e9a12d07beab41f24bced7dbadf3e31cffc13c16d0ffb1657e7d2627bdc50d27a1d3846ea1aaa13c4917c79f9f5c82ccbb2ecebae8be834d800080000
```
file.py
```python
content = "1f8b08006c4e7c5a0003edcf3d0ac2401005e01c65bb7432e3cc66ec6dbd43585ccc8a9b20d94910c4bb1bf0070bc1c620c27ecd2be6156f76d1350b3d69312300a82a3653a25878cd3bb6066949022c48620059080a03738e7a1892ba7e9a12d07beab41f24bced7dbadf3e31cffc13c16d0ffb1657e7d2627bdc50d27a1d3846ea1aaa13c4917c79f9f5c82ccbb2ecebae8be834d800080000".decode("hex")
file = open("output" , "w+")
file.write(content)
file.close()
```

```bash
anisboss@anisboss-PC:~/Nullcon-18$ file output 
output: gzip compressed data, last modified: Thu Feb  8 13:19:40 2018, from Unix
anisboss@anisboss-PC:~/Nullcon-18$ mv outout output.gz
anisboss@anisboss-PC:~/Nullcon-18$ gunzip output.gz 
anisboss@anisboss-PC:~/Nullcon-18$ ls
flag
anisboss@anisboss-PC:~/Nullcon-18$ file flag 
flag: POSIX tar archive
anisboss@anisboss-PC:~/Nullcon-18$ tar -xlf flag
anisboss@anisboss-PC:~/Nullcon-18$ ls
flag  flag.txt
anisboss@anisboss-PC:~/Nullcon-18$ cat flag.txt 
hackim18{'51mpL3st_Ch4ll3ng3_s0lv3d'}
```

