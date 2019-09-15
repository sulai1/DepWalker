from parse import parse
from parser import parser as p
class document(object):
	"""description of class"""
	def __init__(self,path,parse):
		
		fd = open(path,'r')
		s = fd.read()
		#parser = Procedure()
		self.gather(parse.Procedure(),s)
		self.gather(parse.Include(),s)
		self.gather(parse.Define(),s)
	
	def gather(self,parser, string):
		print("regex: " + parser.regex)
		matches = parser.parse(string)
		i = 0
		for match in matches:
			if len(match.groups()) > 0:
				i+=1
			print("{}".format(i) + "#" * 40)
			for group in parser.groups:
				g = match.group(group)
				if g != None:
					print(group + ":")
					print(g)