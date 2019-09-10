from  Parser import *
import math

WIDTH = 60


#parser = Procedure("begin-procedure",'end-procedure',ignore_case=True)
parser = Procedure("begin-procedure","end-procedure",True)
fd = open('test.sqr','r')
s = fd.read()
#parser = Procedure()
print("regex: "+parser.regex)
matches = parser.parse(s)

if matches == None:
    print('Empty')
print()
i = 0
for match in matches :
	for keyword in parser.groups :
		print("#" * (int)(WIDTH - math.floor(len(keyword) / 2)) + " " + keyword + " " + "#" * (int)(WIDTH - math.ceil(len(keyword) / 2)))
		print(match.group(keyword))

		