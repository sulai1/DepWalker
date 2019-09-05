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
	
def Identifier(name=None):
	if name == None:
		return Parser(r"(\w*)")
	else:
		groupname = Parser.group_name(name)
		return Parser(r"(?P<{}>\w*)".format(groupname), groups=[groupname])

def Keyword(keyword, ignore_case=False, hide=False):
	grpname = Parser.group_name(keyword)
	kw = ""
	# detect regex escape sequences
	for c in keyword :
		if Parser.ESCAPE.find(c) > 0:
			kw+=r"\{0}".format(c)
		else:
			kw+=c
	# detect valid name
	if len(grpname) == 0:
		grpname = Parser.error_grp()
	# hide group
	if hide :
		regex = "("
	else:
		regex = r"(?P<{0}>".format(grpname)
	# add respective case character
	if ignore_case :
		for c in kw :
			if c.islower() :
				regex += r"[{0}{1}]".format(c,c.upper())
			elif c.isupper :
				regex += r"[{0}{1}]".format(c,c.lower())
			else :
				regex+=r"[{0}]".format(c)
		regex+=")"
	else:
		regex += r"{0})".format(kw)
	if hide :
		return Parser(regex)
	else:
		return Parser(regex, groups=[grpname])

def Except(name,keyword,ignore_case=False,hide=False,hide_keyword=False):
	if hide:
		return Parser(r"([\s\S]*?)") + Keyword(keyword,ignore_case,hide_keyword)
	else:
		grpname = Parser.group_name(name)
		return Parser(r"(?P<{}>[\s\S]*?)".format(grpname),groups=[grpname]) + Keyword(keyword,ignore_case,hide_keyword)

def Multiline(name,start, end,  ignore_case=False, hide=False,hide_outer=True):
	s = Keyword(start, ignore_case=ignore_case,hide=hide_outer)
	c = Except(name,end, ignore_case=ignore_case,hide=hide,hide_keyword=hide_outer)
	return s + c

def Whitespaces():
	return Parser("\s*")

def Number():
	return Parser("((([0-9]*)?.)*)?[0-9]*(.([0-9]*)?)?")

def Procedure(start,end,ignore_case=False):
	return Keyword(start,ignore_case,hide=True) + Whitespaces() + Identifier("procedure") + Whitespaces() + Multiline("parameter","(",")",hide_outer=True) + Except("body",end,hide_keyword=True)

def Define():
	return Parser("Define",r"(?m)#define[\s*](?P<define>\w*)[\s*]([\w,.]*[\s]*|'[\s\S]*?')")

def Include():
	return Keyword("#include",hide=True) + Whitespaces() + Multiline("include","'","'",hide_outer=True)

def Comment():
	return Parser("Comment","(?P<comment>({}*))".format(Parserc.omment))
	
