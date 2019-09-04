import re

class Parser(object):
	""" The Parser parses a code file for its components."""
	
	def __init__(self,regex,groups=[]):
		self.groups = groups
		self.regex = regex

	def parse(self,string):
		""" Parse the string and return the matches. The matches can be searched for the groups stored in the parser """
		res = re.finditer(self.regex,string)
		return res
	
	@staticmethod
	def group_name(name):
		newname=""
		for c in name :
			if c.isalnum() :
				newname+=c
			else :
				newname+=""
		return newname

	def __add__(self,other):
		g = self.groups;
		g.extend(other.groups)
		return Parser(self.regex+other.regex,g);
	
class Identifier(Parser):
	def __init__(self,identifier,ignore_case=False):
		return super(Identifier, self).__init__(r"(?P<{0}>\w*)".format(identifier), groups=["identifier"])

class Keyword(Parser):
	def __init__(self, keyword, ignore_case=False) :
		newname = Parser.group_name(keyword)
		if ignore_case :
			regex=r"(?P<{0}>".format(newname)
			for c in keyword :
				if c.islower() :
					regex += r"[{0}{1}]".format(c,c.upper())
				elif c.isupper :
					regex += r"[{0}{1}]".format(c,c.lower())
				else :
					regex+=r"[{0}]".format(c)
			regex+=")"
		else:
			regex=r"(?P<{0}>{0})".format(newname)
		print("name "+newname)
		return super(Keyword,self).__init__(regex, groups=[newname])

class Except(Parser):
	def __init__(self, string):
		return super(Except,self).__init__(r"(?P<{0}>[\s\S]*?)({0})".format(string),groups=[Parser.group_name(string)])

class Multiline(Parser):
	def __init__(self, start, end, name="multiline", ignore_case=False):
		s = Keyword(start, ignore_case)
		e = Keyword(end, ignore_case)
		g  = s.groups
		g.extend(e.groups)
		g.append("content")
		return super(Identifier, self).__init__( r"{0}(?P<content>[\s\S]*?){1}".format(s.regex,e.regex), groups=g)

def Procedure():
	return Parser("Procedure",r"(?i)(?P<comment>{2}*)begin-procedure[\s]+{0}[\s]*{1}([\s\S]*?)end-procedure".format(Parser.IDENTIFIEER,Parser.PARAMETERS,Parser.COMMENT,['identifier','parameters','comment']))

def Define():
	return Parser("Define",r"(?m)#define[\s*](?P<define>\w*)[\s*]([\w,.]*[\s]*|'[\s\S]*?')")

def Include():
	return Parser("Include",r"(?m)#include[\s*]'([\w.]*)?'")

def Comment():
	return Parser("Comment","(?P<comment>({}*))".format(Parserc.omment))
	
