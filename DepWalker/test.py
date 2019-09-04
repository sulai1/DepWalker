import Parser

class DepWalker():
	""" find """


parser = Comment()
#parser = Procedure()
matches = parser.parse(s)

if matches == None:
    print('Empty')
    
i = 0
if parser.name == "Procedure":
    for match in matches:
        print(match.group('comment'))
        print('procedure : {} {}'.format(match.group('identifier'),match.group('parameters')))
        print('##############################################')
        i = i + 1
        
if parser.name == "Comment":
    for match in matches:
        print(match.group('comment'))
        print('##############################################')
        i = i + 1

print(i)

