import re
class parser(object):
	"""The Parser parses a code file for its components."""
	ERROR_GRP = "err"
	ESCAPE = '[\^$.|?*+(){}"'
	id = 0

	def __init__(self,regex,groups=[]):
		self.groups = groups
		self.regex = regex

	def parse(self,string):
		""" Parse the string and return the matches. The matches can be searched for the groups stored in the parser """
		res = re.finditer(self.regex,string)
		return res
	
	@staticmethod
	def dup_grp(name):
		parser.id += 1
		return "{0}{1}".format(name,parser.id) 
		
	@staticmethod
	def error_grp():
		parser.id += 1
		return "{0}{1}".format(parser.ERROR_GRP,parser.id) 
		
	@staticmethod
	def group_name(name):
		newname = ""
		for c in name :
			if c.isalnum() :
				newname+=c
			else :
				newname+=""
		return newname

	def __add__(self,other):
		g = self.groups[:]
		if len(other.groups) > 0:
			while  self.rename_dups(other):
				pass
			g.extend(other.groups)
		return parser(self.regex + other.regex,g)

	def rename_dups(self,other):
		b_dups = False
		if len(self.groups) > 0 and len(other.groups) > 0 :
			for gs in self.groups :
				for i in range(0, len(other.groups)) :
					if gs == other.groups[i] :
						other.regex = other.regex.replace(other.groups[i],other.groups[i] + "I")
						other.groups[i]+="I"
						b_dups = True
		return b_dups