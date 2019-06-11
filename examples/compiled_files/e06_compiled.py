
### nonek ###

import random
import math


a = []
output = ''
x = int(input())
while (x > 0):	
	sqrt = math.sqrt(x)	
	if float.is_integer(sqrt):		
		a.append(x)	
	x = int(input())
n = len(a)
if (n > 0):	
	elem = a[int('0')]	
	output = str(elem)	
	index = 1	
	while (index < n):		
		output = output + ','		
		elem = a[int(index)]		
		strElem = str(elem)		
		output = output + strElem		
		index = (index + 1)
print(output)