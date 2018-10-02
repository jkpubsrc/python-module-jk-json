#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from .TokenStream import *
from .ParserErrorException import *





class ParsingContext(object):

	def __init__(self, debuggingEnabled = True):
		assert isinstance(debuggingEnabled, bool)

		self.bDebugging = debuggingEnabled
		self.indent = -1
		self.__prefix = " " * 100
	#

	def _debugBegin(self, functionName, token):
		if self.indent > len(self.__prefix*2):
			self.__prefix += "  "
		print(self.__prefix[:self.indent*2] + functionName + " ... " + str(token))
	#

	def _debugEnd(self, functionName, bSuccess):
		if self.indent > len(self.__prefix*2):
			self.__prefix += "  "
		if bSuccess:
			print(self.__prefix[:self.indent*2] + functionName + " succeeded.")
		else:
			print(self.__prefix[:self.indent*2] + functionName + " failed.")
	#

#



def debugDecorator(func):

	def func_wrapper(self, ctx, ts):
		if ctx.bDebugging:
			ctx.indent += 1
			ctx._debugBegin(func.__name__, ts.peek())

		x = func(self, ctx, ts)

		if ctx.bDebugging:
			ctx._debugEnd(func.__name__, x[0])
			ctx.indent -= 1

		return x
	#

	return func_wrapper
#



class ParserBase(object):

	#
	# Parse the tokens. Construct an abstract syntax tree from the tokens provided by the tokenizer.
	#
	# @param	Tokenizer tokenizer		The tokenizer that provides the tokens.
	#
	def parse(self, tokenizer, bDebugging = False):
		raise Exception("Overwrite this method")
	#

#


