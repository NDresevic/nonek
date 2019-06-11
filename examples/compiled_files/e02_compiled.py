
### nonek ###

import random
import math


n = int(input())
sum = 0
while (n > 0):	
	sum = (sum + (n % 10))	
	n = (n // 10)
if (sum > 10):	
	print('veci')
if (sum <= 10):	
	print('manji')