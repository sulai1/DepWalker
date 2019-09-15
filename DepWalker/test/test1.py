import unittest
from src.parse import *

procedure_full = "!comment\n{name(x,y,z)\nbody\n}"
procedure_min = "{name()}"

test_name='test'

class Test_test1(unittest.TestCase):

	def parser_no_match(self,parser,string):  
		iter = parser.parse(string)
		self.assertIsNotNone(iter)
		try:
			match = iter.next()
		except StopIteration:
			self.assertTrue(True)
		else:
			self.assertTrue(False)


	def parser_success(self,parser,string,resultArray):  
		""" test first match. Every group should contain the corresponding value from the resultArray.
			The iterator must contain at least one match or the test fails """
		iter = parser.parse(string)
		self.assertIsNotNone(iter)

		match = iter.next()				 
		groups = match.groups()

		i = 0
		for group in parser.groups:				  
			g = match.group(group)
			self.assertEquals(g,resultArray[i])
			i+=1

	def test_procedure(self):
		parser = Procedure("{","}")
		self.parser_success(parser,procedure_min,["","name","",""])		
		self.parser_success(parser,procedure_full,["!comment\n","name","x,y,z","\nbody\n"])


	def test_comment(self):
		parser = Group(Comment(),name="comment")		 
		self.parser_success(parser,procedure_full,["!comment\n"])
		self.parser_no_match(parser,procedure_min)
	
	def test_Parameter(self):
		parser = Parameter()
		self.parser_success(parser,procedure_full,["x,y,z"])
		self.parser_success(parser,procedure_min,[""])

	def test_number(self):
		parser = Group(Number(),name=test_name);												  
		self.parser_success(parser,"123",["123"])										  
		self.parser_success(parser,"123.124",["123.124"])						  
		self.parser_success(parser,"sda123.124asd",["123.124"])		
		
		self.parser_no_match(parser,"sdasd")
																
	def test_include(self):
		parser = Include()																		  
		self.parser_success(parser,"#include 'test.inc'",['test.inc'])									  
		self.parser_no_match(parser,"'test.inc'")						  
		self.parser_no_match(parser,"#includ 'test.inc'")	
		
	def test_define(self):
		parser = Define()																		  
		self.parser_success(parser,"#define test 'test.inc'",['test',"'test.inc'"])			  				
		self.parser_success(parser,"#define test 123",['test','123'])									
		self.parser_success(parser,"#define test 123.123",['test','123.123'])									  
		self.parser_no_match(parser,"'test.inc'")						  
		self.parser_no_match(parser,"#def 'test.inc'")			  
		self.parser_no_match(parser,"123")	

	
if __name__ == '__main__':
	unittest.main()
