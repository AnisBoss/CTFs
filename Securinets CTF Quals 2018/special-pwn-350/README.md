# Description
History, Stephen said, is a nightmare from which I am trying to awake <br>

Link : ssh special@52.50.127.68 ; password: fd98201b8539e491a86f961c723951fe

# Solution
After connecting to the remote host , we are given custom  shell meterpreter with some hardcore filtering : <br>
* Only uppercase letters are accepted
* Numbers are filtered
* most special chars are filtered
* ? % ( ) . " ' ` = , &  ~ @ ] [ ! * / \ are all filtered 

after some test normally and considering the description that insists on the history , we check the output of $_ <br>
which normally output the argument of last command <br>

```
> $_
declare -x A="T"
declare -x AB="HI"
declare -x ABC="ISN"
declare -x ABCD="OTTH"
declare -x ABCDE="EFLAG"
declare -x ABCDEF="BUTMAY"
declare -x ABCDEFG="BEITCAN"
declare -x ABCDEFGH="HELPGETT"
declare -x ABCDEFGHI="INGFLAG:D"
declare -x OLDPWD
declare -x PWD="/home/special"
declare -x SHELL=""
declare -x SHLVL="1"
declare -x _="export"
> $PATH
bash: /usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin:.: No such file or directory

```
so we can read the string "THIS IS NOT THE FLAG BUT MAYBE IT CAN HELP GETTING FLAG :D" so it's already a hint <br>
the idea is to use shell expansion or bash substitution ${VAR:START:END} to substring the content of the variable VAR from START to END <br>
but we can't use numbers oO ! <br>
but we can generate length of string  with ${#VAR}

## \o/ Problem solved 

${PATH:${#AB}:${#A}}${PWD:${#A}:${#A}} <== executes sh 
then cat flag.txt
Flag{B4sh_subst1tut1on_is_gud!}

