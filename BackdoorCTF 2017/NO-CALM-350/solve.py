from z3 import *

s = Solver()

v6 = Int('v6')
v7 = Int('v7')
v8 = Int('v8')
v9 = Int('v9')
v10 = Int('v10')
v11 = Int('v11')
v12 = Int('v12')
v13 = Int('v13')
v14 = Int('v14')
v15 = Int('v15')
v16 = Int('v16')
v17 = Int('v17')
v18 = Int('v18')
v19 = Int('v19')
v20 = Int('v20')
v21 = Int('v21')
v22 = Int('v22')
v23 = Int('v23')
v24 = Int('v24')
v25 = Int('v25')
v26 = Int('v26')
v27 = Int('v27')
v28 = Int('v28')
v29 = Int('v29')
v30 = Int('v30')
v31 = Int('v31')
v32 = Int('v32')
v33 = Int('v33')
v34 = Int('v34')
v35 = Int('v35')


s.add(v6 >= 32,v6 <=126)

s.add(v7 >= 32,v7 <=126)

s.add(v8 >= 32,v8 <=126)

s.add(v9 >= 32,v9 <=126)

s.add(v10 >= 32,v10 <=126)

s.add(v11 >= 32,v11 <=126)

s.add(v12 >= 32,v12 <=126)

s.add(v13 >= 32,v13 <=126)

s.add(v14 >= 32,v14 <=126)

s.add(v15 >= 32,v15 <=126)

s.add(v16 >= 32,v16 <=126)

s.add(v17 >= 32,v17 <=126)

s.add(v18 >= 32,v18 <=126)

s.add(v19 >= 32,v19 <=126)

s.add(v20 >= 32,v20 <=126)

s.add(v21 >= 32,v21 <=126)

s.add(v22 >= 32,v22 <=126)

s.add(v23 >= 32,v23 <=126)

s.add(v24 >= 32,v24 <=126)

s.add(v25 >= 32,v25 <=126)

s.add(v26 >= 32,v26 <=126)

s.add(v27 >= 32,v27 <=126)

s.add(v28 >= 32,v28 <=126)

s.add(v29 >= 32,v29 <=126)

s.add(v30 >= 32,v30 <=126)

s.add(v31 >= 32,v31 <=126)

s.add(v32 >= 32,v32 <=126)

s.add(v33 >= 32,v33 <=126)

s.add(v34 >= 32,v34 <=126)
s.add(v35>=32, v35<=126)

s.add(v7 + v6 - v8 == 81)
s.add( v6 - v7 + v8 == 53)
s.add(v7 - v6 + v8 == 87)
s.add(v10 + v9 - v11 == 90)
s.add(v9 - v10 + v11 == 156)
s.add( v10 - v9 + v11 == 66)
s.add(v13 + v12 - v14 == 98 )
s.add(v12 - v13 + v14 == 140 )
s.add(v13 - v12 + v14 == 92)
s.add(v16 + v15 - v17 == 38 )
s.add(v15 - v16 + v17 == 170)
s.add(v16 - v15 + v17 == 60)
s.add(v19 + v18 - v20 == 29)
s.add(v18 - v19 + v20 == 161)
s.add(v19 - v18 + v20 == 69)
s.add(v22 + v21 - v23 == 163)
s.add(v21 - v22 + v23 == 27 )
s.add(v22 - v21 + v23 == 69)
s.add(v25 + v24 - v26 == 147)
s.add(v24 - v25 + v26 == 43)
s.add(v25 - v24 + v26 == 59)
s.add(v28 + v27 - v29 == 146)
s.add(v27 - v28 + v29 == 86 )
s.add(v28 - v27 + v29 == 44 )
s.add(v31 + v30 - v32 == 67)
s.add(v30 - v31 + v32 == 89)
s.add(v31 - v30 + v32 == 75)
s.add(v34 + v33 - v35 == 117)
s.add(v33 - v34 + v35 == 125)
s.add(v34 - v33 + v35 == 125)


if (s.check() == sat):
	print s.model() #reorder it then decimal->hex->string

#Ordered = [67,84,70,123,78,111,119,95,116,104,49,115,95,49,115,95,116,48,95,103,51,116,95,65,78,71,82,121,121,125]
#CTF{Now_th1s_1s_t0_g3t_ANGRyy}
