import re



class Parser(object):
	""" The Parser parses a code file for its components."""
	ERROR_GRP = "err"
	ESCAPE = "[\^$.|?*+(){}"
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
		Parser.id += 1
		return "{0}{1}".format(name,Parser.id) 
		
	@staticmethod
	def error_grp():
		Parser.id += 1
		return "{0}{1}".format(Parser.ERROR_GRP,Parser.id) 
		
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
		return Parser(self.regex + other.regex,g)

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
	
def Identifier():
		return Parser(r"\w*")

def Keyword(keyword, ignore_case=False):
	kw = ""
	# detect regex escape sequences
	for c in keyword :
		if Parser.ESCAPE.find(c) > 0:
			kw+=r"\{0}".format(c)
		else:
			kw+=c
	regex=""
	# add respective case character
	if ignore_case :
		for c in kw :
			if c.islower() :
				regex += r"[{0}{1}]".format(c,c.upper())
			elif c.isupper :
				regex += r"[{0}{1}]".format(c,c.lower())
			else :
				regex+=r"[{0}]".format(c)
	else:
		regex += kw
	return Parser(regex)

def Except():
	return Parser(r"([\s\S]*?)")

def Whitespaces():
	return Parser(r"[\s]*")

def Number():
	return Parser("((([0-9]*)?.)*)?[0-9]*(.([0-9]*)?)?")

def Procedure(start,end,ignore_case=False):
	return Group(Comment(),name="comment",flag="*") + Keyword(start,ignore_case) + Whitespaces() + Group(Identifier(),name="procedure") + Whitespaces() + Keyword("(") + Group(Except(),name="parameter") + Keyword(")") + Group(Except(),name="body") + Keyword(end) 

def Define():
	return Parser("Define",r"(?m)#define[\s*](?P<define>\w*)[\s*]([\w,.]*[\s]*|'[\s\S]*?')")

def Include():
	return Keyword("#include") + Whitespaces() + Keyword("'") + Group(Except(),name="include") + Keyword("'")

def Comment():
	return Keyword("!") + Except() + Keyword(r"\n")

def Group(parser,name="", flag=""):
	"""The flag is either of the following:
			an integer number indicating the number of the expected matches
			'*' indicating any match
			'+' indicating one ore more matches
			'?' indicating that it may occurre once or not"""
	g = parser.groups[:]
	regex = "("
	if len(name) > 0:
		g.append(Parser.group_name(name))
		regex += "?P<{}>".format(name)
	regex+=parser.regex + ")"
	if isinstance(flag,(int,long)):
		regex+= "{" + flag + "}"
	else:
		regex+=flag
	return Parser(regex,g)