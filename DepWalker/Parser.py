from abc import ABC, abstractclassmethod
import re

class Parser(ABC):
    def __init__(self,name,regex):
        self.regex = regex
        self.name = name

    def parse(self,string):
        res = re.finditer(self.regex,string)

        return res

def multiline(start,end):
    return Parser("{0}([\\s\\S]*?){1}".format(start,end))

identifier = r"(?P<identifier>\w*)"
number = r"([\w.,]*)"
parameters = r"(?P<parameters>\(([\s\S]*?)\))"
comment = r"((!.*)\n)"

def Procedure():
    return Parser("Procedure",r"(?i)(?P<comment>{2}*)begin-procedure[\s]+{0}[\s]*{1}([\s\S]*?)end-procedure".format(identifier,parameters,comment))

def Define():
    return Parser("Define",r"(?m)#define[\s*](\w*)[\s*]([\w,.]*[\s]*|'[\s\S]*?')")

def Include():
    return Parser("Include",r"(?m)#include[\s*]'([\w.]*)?'")

def Comment():
    return Parser("Comment","(?P<comment>({}*))".format(comment))
    


fd = open('test.sqr','r')
s = fd.read()
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

