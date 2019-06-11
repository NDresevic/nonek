
### nonek ###

import random
import math

def myMin(a, b):		
	m = a	
	if (b < a):		
		m = b
	return m

a = int(input())
b = 5
m = myMin(a, b)

print('Min is: ')
print(m)
if (m < 2):	
	print('Min is less than 2.')