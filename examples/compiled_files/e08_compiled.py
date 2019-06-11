
### nonek ###

import random
import math


s = input()
n = len(s)
m = (n - 1)
i = (m // 2)
j = (n // 2)
while (j < n):	
	t = i	
	spaces = ''	
	while (t > 0):		
		spaces = spaces + ' '		
		t = (t - 1)	
	end = (j + 1)	
	subs = s[i:end]	
	spaces = spaces + subs	
	print(spaces)	
	i = (i - 1)	
	j = (j + 1)