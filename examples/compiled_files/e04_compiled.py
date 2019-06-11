
### nonek ###

import random
import math


x = int(input())
sum = 0
cnt = 0
while (x != 0):	
	sum = (sum + x)	
	cnt = (cnt + 1)	
	x = int(input())
res = (sum / cnt)
print(res)