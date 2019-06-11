
### nonek ###

import random
import math


s = input()
n = int(input())
word = ''
output = ''
i = 0
lenS = len(s)
while (i < lenS):	
	c = s[int(i)]	
	if ((int(c.isspace()) == 1) or (int(c in [',', '.', ':', '?', '!', ';']) == 1)):		
		lenW = len(word)		
		if (lenW > n):			
			upper = word.upper()			
			output = output + upper		
		if (lenW <= n):			
			output = output + word		
		word = ''	
	word = word + c	
	i = (i + 1)
print(output)