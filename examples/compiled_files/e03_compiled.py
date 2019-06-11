
### nonek ###

import random
import math


a = int(input())
b = int(input())
c = int(input())
d = int(input())
max = a
if (((b > a) and (b > c)) and (b > d)):	
	max = b
if (((c > a) and (c > b)) and (c > d)):	
	max = c
if (((d > a) and (d > b)) and (d > c)):	
	max = d
print(max)