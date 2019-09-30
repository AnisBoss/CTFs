# Web: Seek You El
We were given a website that contains a php application, looking at the php code, it will embed our given input which is a GET parameter "_" into an SQL query which looks like this :
```sql
Select user from bsides where username="admin" and pw="{$_GET['_']}";
```
This mean that we could login as admin if we provide the correct password for it.<br>
So as first step i feeded the web page with "?_=test" as a GET parameter, but suddenly i recieved <br> **Sorry NO !!!** message ; <== Good start xD <br>
It seems that the admin is blocking the character "\_" from being used at the URL ; 
after struggling for a while and thanks to my teammates @dali  and @kerro they feed me with this from [php documentation](https://www.php.net/manual/en/language.variables.external.php) : <br>

```
Note:
Dots and spaces in variable names are converted to underscores. For example <input name="a.b" /> becomes $_REQUEST["a_b"]. 
```

The idea is simple now we just use "?.=test" and we get as result 
```sql
Select user from bsides where username="admin" and pw="test";
```

we succesffuly bypassed the first check, doing a SQL injection using 
 
>' or '1'='1

didn't come up with a good result, so the author is waiting for an explicit password for the admin account and not the query itself. The page is responding either with the query or a blank page in case of error<br>
A basic idea is to use time based attack since we get the same result independently from the input given. <br>

among the SQL functions, we tried sleep() and benchmark() which were totally blocked and can't be used under this task ; <== the admin is so evil <br><BR>
**Time based SQL Injection** : <font color="red" > Failed !! </font><BR><br>
Looking again at  [mysql numeric functions list](https://dev.mysql.com/doc/refman/8.0/en/numeric-functions.html)  i noticed <u>exp(x)</u> function which stands for <i>Raising to the power of x</u><br>
Locally i tested the function with random numbers until i recieved a wonderful message 
> **ERROR 1690 (22003): DOUBLE value is out of range in 'exp(1000)'**.

So the function have boundaries when passed it triggers an error in this case the it just fail with that error when we go beyond 709 .<br>
The idea behind using exp() function is the construction  of a payload which extracts the first letter of the password (in our case pw) and calculate its ascii then add it to random number (which we control) and pass the whole result to exp() and check if it fail or not .<br>

**PoC||GTFO**

[http://35.232.184.83/index.php?.='or exp(ord(substr(pw,1,1))+1)>0 and user=0x61646d696e and '1'='1]()

the above payload just check if the ascii (same as ord) of the first character of password + 1 is under 709 or not ; we recived a page with our query. We conclude that : <br>
```
ascii(first_char(password))+1 < 70
```
After that we just play with the controller number until it gave us a blank page at exactly 653
with some quick **Mafs** we can find that the first char of password is **9** using <br>
> chr(709 - 653 + 1)

then just move on to the second character <br>
[http://35.232.184.83/index.php?.='or exp(ord(substr(pw,2,1))+1)>0 and user=0x61646d696e and '1'='1]()

and repeating the process until finish extracting the whole password which is :
>9f3b7c0e1a

then passing this password under the GET parameter gave us the flag \o/

>bsides_delhi{sequel_injections_are_really_great_i_guess_dont_you_think?}
<br>

---

I really want to thank the author for this challenge ; didn't knew about this trick before, i don't know what we can call it ; but i think it's more **error/boolean SQL injection Attack** .
i think there will be another function that has boundaries and can be used in this task .

