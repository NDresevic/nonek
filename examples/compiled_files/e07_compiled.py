
### nonek ###

import random
import math


output = ''
curr = ''
prev = ''
s = input()
index = 0
n = len(s)
while (index < n):	
	curr = s[int(index)]	
	if prev != '':		
		if ((int(prev.isdigit()) == 1) and (int(curr.isalpha()) == 1)):			
			output = output + '#'		
		if ((int(prev.isalpha()) == 1) and (int(curr.isdigit()) == 1)):			
			output = output + '*'	
	output = output + curr	
	prev = curr	
	index = (index + 1)
print(output)