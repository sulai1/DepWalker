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
		g = self.groups
		while  self.rename_dups(other):
			pass
		g.extend(other.groups)
		return Parser(self.regex + other.regex,g)

	def rename_dups(self,other):
		b_dups = False
		for gs in self.groups :
			for i in range(0, len(other.groups)) :
				if gs == other.groups[i] :
					other.regex = other.regex.replace(other.groups[i],other.groups[i] + "I")
					other.groups[i]+="I"
					b_dups = True
		return b_dups

def Identifier(ignore_case=False):
	return Parser(r"(?P<identifier>\w*)", groups=["identifier"])

def Keyword(keyword, ignore_case=False):
	grpname = Parser.group_name(keyword)
	kw=""
	for c in keyword :
		if Parser.ESCAPE.find(c)>0:
			kw+=r"\{0}".format(c)
	if len(grpname) == 0:
		grpname = Parser.error_grp()
	if ignore_case :
		regex = r"(?P<{0}>".format(grpname)
		for c in kw :
			if Parser.ESCAPE.find(c)>0:
				regex+=r"[\{0}]".format(c)
			elif c.islower() :
				regex += r"[{0}{1}]".format(c,c.upper())
			elif c.isupper :
				regex += r"[{0}{1}]".format(c,c.lower())
			else :
				regex+=r"[{0}]".format(c)
		regex+=")"
	else:
		regex = r"(?P<{0}>{1})".format(grpname,kw)
	return Parser(regex, groups=[grpname])

def Except(string,ignore_case=False):
	return Parser(r"(?P<content>[\s\S]*?)",groups=[Parser.group_name("content")]) + Keyword(string,ignore_case)

def Multiline(start, end, ignore_case=False):
	s = Keyword(start, ignore_case)
	c = Except(end, ignore_case)
	return s + c

def Whitespaces():
	return Parser("\s*")



def Procedure(start,end,ignore_case=False):
	return Keyword(start,ignore_case) + Whitespaces() + Identifier() + Whitespaces() + Multiline("(",")") + Except(end)
	#return
	#Parser("Procedure",r"(?i)(?P<comment>{2}*)begin-procedure[\s]+{0}[\s]*{1}([\s\S]*?)end-procedure".format(Parser.IDENTIFIEER,Parser.PARAMETERS,Parser.COMMENT,['identifier','parameters','comment']))
def Define():
	return Parser("Define",r"(?m)#define[\s*](?P<define>\w*)[\s*]([\w,.]*[\s]*|'[\s\S]*?')")

def Include():
	return Parser("Include",r"(?m)#include[\s*]'([\w.]*)?'")

def Comment():
	return Parser("Comment","(?P<comment>({}*))".format(Parserc.omment))
	
