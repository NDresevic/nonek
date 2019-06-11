
### nonek ###

import random
import math


sol = 0
word = ''
words = []
fielPath = input()
n = int(input())
m = n
while (m > 0):	
	nWord = input()	
	words.append(nWord)	
	m = (m - 1)
content = open(fielPath, 'r').read()
i = 0
contLen = len(content)
while (i < contLen):	
	c = content[int(i)]	
	if ((int(c.isspace()) == 1) or (int(c in [',', '.', ':', '?', '!', ';']) == 1)):		
		j = 0		
		aSize = len(words)		
		while (j < aSize):			
			aElem = words[int(j)]			
			if aElem == word:				
				sol = (sol + 1)			
			j = (j + 1)		
		word = ''	
	if ((int(c.isspace()) == 0) and (int(c in [',', '.', ':', '?', '!', ';']) == 0)):		
		word = word + c	
	i = (i + 1)
print(sol)