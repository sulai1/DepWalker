class Document():
	""" description of class """
	def __init__(self,file):
		fd = open('test.sqr','r')
		self.content = fd.read()

