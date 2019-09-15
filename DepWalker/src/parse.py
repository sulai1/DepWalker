from parser import parser as p

class parse(object):
					

	def __init__(self\
		,extension=['sqr','inc']\
		,single_comment="!"\
		,string_delimiter="'"\
		,decimal_separator="."\
		,define="#define"\
		,include="#include"\
		,begin_procedure="begin-procedure"\
		,end_procedure="end-procedure"\
		,ignore_case=True):
		self.extension = extension
		self.single_comment = single_comment
		self.string_delimiter = string_delimiter 
		self.decimal_separator = decimal_separator
		self.define = define
		self.include = include
		self.begin_procedure = begin_procedure
		self.end_procedure = end_procedure
		self.ignore_case = ignore_case


	def Identifier(self):
		return p(r"\w*")

	def Keyword(self,keyword, ignore_case=False):
		kw = ""
		# detect regex escape sequences
		for c in keyword :
			if p.ESCAPE.find(c) > 0:
				kw+=r"\{0}".format(c)
			else:
				kw+=c
		regex = ""
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
		return p(regex)
		  
					   
	def Group(self,parser,name="", flag=""):
		g = parser.groups[:]
		regex = "("
		if len(name) > 0:
			g.append(parser.group_name(name))
			regex += "?P<{}>".format(name)
		regex+=parser.regex + ")"
		if isinstance(flag,(int,long)):
			regex+= "{" + flag + "}"
		else:
			regex+=flag
		return p(regex,g)

	def Or(self):
		return p("|")
				   
	def Until(self):
		return p(r"[\s\S]*?")

	def Except(self,parser):
		return p(r"(?:") + parser + p(")")
									
	def Whitespaces(self):
		return p(r"[\s]*")
	
	def EmptyLines(self):
		return  p(r"(?:\n*)")

	def Newline(self):
		return p(r"\n")
	
	def Number(self):
		return p("[0-9+]{0}*[0-9*]".format(self.decimal_separator))
											
	def String(self):
		return p(self.string_delimiter) + self.Until() + p(self.string_delimiter)
															 
	def Parameter(self):
		return self.Keyword("(") + self.Group(self.Until(),name="parameter") + self.Keyword(")")
																			  
	def Procedure(self):
		return self.Group(self.Comment(),name="comment") + self.Keyword(self.begin_procedure) + self.Whitespaces() + self.Group(self.Identifier(),name="procedure") + self.Whitespaces() + self.Parameter() + self.Group(self.Until(),name="body") + self.Keyword(self.end_procedure) 
																							   
	def Define(self):
		return self.Keyword(self.define) + self.Whitespaces() + self.Group(self.Identifier(),name="identifier") + self.Whitespaces() + self.Group(self.Number() + self.Or() + self.String(),name="value",flag="?")
																												
	def Include(self):
		return self.Keyword(self.include) + self.Whitespaces() + self.Keyword("'") + self.Group(self.Until(),name="include") + self.Keyword("'")
																																 
	def Comment(self):
		return p(r"((!.*\n)*)")

