#Author Anis_Boss
#!/bin/bash


handler()
{
echo "Hemm, nice one but you can't escape "
}

trap handler  1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21

echo "
================================
	     Y O U
||     ||<(.)>||<(.)>||     ||
||    _||     ||     ||_    ||
||   (__D     ||     C__)   ||
||   (__D     ||     C__)   ||
||   (__D     ||     C__)   ||
||   (__D     ||     C__)   ||
||     ||     ||     ||     ||
================================"
while :
do
read -r -p ">> "  x
output=$(echo $x|tr -d [:alpha:]234567890\\@+=\]\[\~\&\;.\!\?,:\*^\`\/\>éèçù\|\%_à)
evaluated=(printf "%s" $output)
eval $(eval ${evaluated[@]})
done
