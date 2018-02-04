from z3 import *

s = Solver()
#declare BitVec variables
for i in range(1,27):
	globals()['a%i'%i]=BitVec('a%i'%i,32)

#func1
s.add(a1 * 2 * (a1 ^ a2) - a2 == 10858)
s.add(a1>85,a1<=95)
s.add(a2>96,a2<=111)

#func2
s.add(a2 % a3 == 7)
s.add(a2>90)

#func3
s.add(a3 / a4 +(a4 ^ a3) == 21)
s.add(a3 <=99 )
s.add(a4<=119)

#func4
s.add(a5==95)

#func5
s.add((a6 + a5)^(a5 ^ a6 ^ a5 ) == 225)
s.add(a5>90)
s.add(a6 <=89)

#func6
s.add(a6<=a7)
s.add(a7<=a8)
s.add(a6>85)
s.add(a7>110)
s.add(a8>115)
s.add((a7+a8) ^ (a6 + a7) == 44)
s.add((a7 + a8)%a6 + a7  == 161)

#func7
s.add(a8>=a9)
s.add(a9>=a10)
s.add(a8<=119)
s.add(a9>90)
s.add(a10<=89)
s.add((a8 + a10) ^ (a9 + a10)==122)
s.add((a8 + a10)%a9 + a10 == 101)

#func8
s.add(a10<=a11)
s.add(a11<=a12)
s.add(a12<=114)
s.add((a10 + a11)/a12 * a11 == 97)
s.add((a12 ^ (a10-a11))*a11 == -10088)

#func9
s.add(a12==a13)
s.add(a13>=a14)
s.add(a14<=99)
s.add(a14+a12*(a14-a13)-a12==-1443)

#func10
s.add(a14>=a15)
s.add(a15>=a16)
s.add(a15 * (a14+ a16 +1)- a16==15514)
s.add(a15>90)
s.add(a15<=99)

#func11
s.add(a17>=a16)
s.add(a16>=a18)
s.add(a17>100)
s.add(a17<=104)
s.add(a16 + (a17 ^ (a17- a18))-a18 == 70)
s.add((a17 + a18) / a16 + a16 == 68)

#func12
s.add(a18>=a19)
s.add(a19>=a20)
s.add(a19<=59)
s.add(a20<=44)
s.add(a18+(a19 ^ (a20 + a19))-a20 == 111)
s.add((a19 ^ (a19 - a20))+a19 == 101)

#func13
s.add(a20<=a21)
s.add(a21<=a22)
s.add(a20>40)
s.add(a21>90)
s.add(a22<=109)
s.add(a22+(a21 ^ (a22+ a20))-a20 == 269)
s.add((a22 ^ (a21 - a20)) + a21 == 185)

#func14
s.add(a22>=a24)
s.add(a23>=a24)
s.add(a23<=99)
s.add(a24>90)
s.add(a22 + (a23 ^ (a23+ a22))-a24==185)

#func15
s.add(a25>=a26)
s.add(a25>=a24)
s.add(a26>95)
s.add(a25<=109)
s.add(((a25-a24)*a25^a26)-a24==1214)
s.add(((a26-a25)*a26^a24)+a25==-1034)

if (s.check() == sat):
        values =s.model()
	flag=""
	for i in range(1,27):
	    obj = globals()['a%i' % i]
	    char = values[obj].as_long()
	    flag += chr(char)
	print flag

#Flag = What_You_Wanna_Be?:)_lc_la <==Change "c" with "a" ==> (la_la)  , Dunno why ! 
