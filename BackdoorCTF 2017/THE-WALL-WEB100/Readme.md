<b><u>First Step</u></b> <br>
Get the "Lord Commander"  password because he is the only user that have role = 'admin'  using the <b>bruter.py </b><br>

<b><u>Second Step</u></b><br>
Bypass the vuln <b>"if($password == $users['password']){" </b>because it's not a strict equality 
so after some researchs we found that : <br>
<i>md5('240610708') == '0e462097431906509019562988736854' </i><br><br>
then php will compare the two hashes as numbers and our input will bypass the verification <br>

<b><u>Third Step </u></b><br>

Login and get the flag \o/ 

