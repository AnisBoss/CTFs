Unlike other challenges this was a format string vulnarability, the goal was 
1 : Overwrite perror function with main to gain infinite loop format string  <br>
2 : Leak a libc address  <br>
3 : Identify Libc version
3 : Overwrite printf with system <br>
4 : Feed printf(now system) with /bin/sh <br>

[Simpe writeup ](https://ptr-yudai.hatenablog.com/entry/2019/03/25/152043#Pwn-998pts-Simple)

