given a welcome binary that don't have exec flag on it <br>
and a wrapper binary that has setuid (user that can read the flag.txt file )  <br>
The idea was to execute welcome binary using the linker "/lib/ld*.so" as ELF interpreter  <br>
so running the wrapper binary then just <br>
```
/lib64/ld-linux-x86-64.so.2 ./welcome
```

will print the flag <br>
## securinets{who_needs_exec_flag_when_you_have_linker_reloaded_last_time!!!?}

	
