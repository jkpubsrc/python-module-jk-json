#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import math

from .TokenStream import *
from .ParserErrorException import *
from .ParserBase import *




class JsonParserStrict(ParserBase):

	def __init__(self):
		pass
	#

	#
	# Parse the tokens. Construct an abstract syntax tree from the tokens provided by the tokenizer.
	#
	# @param	Tokenizer tokenizer		The tokenizer that provides the tokens.
	#
	def parse(self, tokenizer, bDebugging = False):
		if isinstance(tokenizer, TokenStream):
			ts = tokenizer
		else:
			ts = TokenStream(tokenizer)

		ctx = ParsingContext(bDebugging)
		bSuccess, data = self._tryEat_S(ctx, ts)
		if bSuccess:
			return data
		else:
			raise Exception()
	#

	@debugDecorator
	def _tryEat_S(self, ctx, ts):
		# loc = ts.location

		n = ts.skipAll("eol", None)

		bSuccess, parsedData = self._tryEat_JANYVALUE(ctx, ts)
		if not bSuccess:
			raise ParserErrorException(ts.location, "Syntax error: Expecting valid JSON value element")

		n = ts.skipAll("eol", None)

		#if not ts.isEOS:
		#	raise ParserErrorException(ts.location, "Syntax error")

		return (True, parsedData)
	#

	@debugDecorator
	def _tryEat_JANYVALUE(self, ctx, ts):
		# loc = ts.location

		t1 = ts.peek()
		if t1.type == "w":
			if t1.text == "null":
				ts.skip()
				return (True, None)
			if t1.text == "true":
				ts.skip()
				return (True, True)
			if t1.text == "false":
				ts.skip()
				return (True, False)
			if t1.text == "Infinity":
				ts.skip()
				return (True, math.inf)
			if t1.text == "NaN":
				ts.skip()
				return (True, math.nan)
			raise ParserErrorException(ts.location, "Syntax error: Expecting valid JSON value element")
		if t1.type == "s":
			ts.skip()
			return (True, t1.text)
		if t1.type == "i":
			ts.skip()
			return (True, int(t1.text))
		if t1.type == "f":
			ts.skip()
			return (True, float(t1.text))

		bSuccess, parsedData = self._tryEat_JARRAY(ctx, ts)
		if bSuccess:
			return (True, parsedData)

		bSuccess, parsedData = self._tryEat_JOBJECT(ctx, ts)
		if bSuccess:
			return (True, parsedData)

		if (t1.type == "d") and (t1.text == "-"):
			m = ts.mark()
			ts.skip()
			t2 = ts.peek()
			if (t2.type == "w") and (t2.text == "Infinity"):
				ts.skip()
				return (True, float("-inf"))
			m.resetToMark()

		return (False, None)
	#

	@debugDecorator
	def _tryEat_JARRAY(self, ctx, ts):
		# loc = ts.location

		t1 = ts.peek()
		if (t1.type != "d") or (t1.text != "["):
			return (False, None)
		ts.skip()

		bSuccess, parsedData = self._tryEat_JVALUE_LIST(ctx, ts)
		if not bSuccess:
			parsedData = []

		t1 = ts.peek()
		if (t1.type != "d") or (t1.text != "]"):
			raise ParserErrorException(ts.location, "Syntax error: Expecting JSON array elements or ']'")
		ts.skip()

		return (True, parsedData)
	#

	@debugDecorator
	def _tryEat_JVALUE_LIST(self, ctx, ts):
		# loc = ts.location

		retData = []
		bSuccess, parsedData = self._tryEat_JANYVALUE(ctx, ts)
		if not bSuccess:
			return (False, None)
		retData.append(parsedData)

		while True:
			t1 = ts.peek()
			if (t1.type != "d") or (t1.text != ","):
				return (True, retData)
			ts.skip()

			bSuccess, parsedData = self._tryEat_JANYVALUE(ctx, ts)
			if not bSuccess:
				raise ParserErrorException(ts.location, "Syntax error: Expecting valid JSON value element")
			retData.append(parsedData)
	#

	@debugDecorator
	def _tryEat_JOBJECT(self, ctx, ts):
		# loc = ts.location

		t1 = ts.peek()
		if (t1.type != "d") or (t1.text != "{"):
			return (False, None)
		ts.skip()

		bSuccess, parsedData = self._tryEat_JPROPERTY_LIST(ctx, ts)
		if not bSuccess:
			parsedData = {}

		t1 = ts.peek()
		if (t1.type != "d") or (t1.text != "}"):
			raise ParserErrorException(ts.location, "Syntax error: Expecting JSON property or '}'")
		ts.skip()

		return (True, parsedData)
	#

	@debugDecorator
	def _tryEat_JPROPERTY_LIST(self, ctx, ts):
		# loc = ts.location

		retData = {}
		bSuccess, parsedData = self._tryEat_JPROPERTY(ctx, ts)
		if not bSuccess:
			return (False, None)

		if parsedData[0] in retData:
			raise ParserErrorException(ts.location, "Syntax error: Duplicate property name detected: " + repr(parsedData[0]))
		retData[parsedData[0]] = parsedData[1]

		while True:
			t1 = ts.peek()
			if (t1.type != "d") or (t1.text != ","):
				return (True, retData)
			ts.skip()

			bSuccess, parsedData = self._tryEat_JPROPERTY(ctx, ts)
			if not bSuccess:
				raise ParserErrorException(ts.location, "Syntax error: Expecting JSON property")

			if parsedData[0] in retData:
				raise ParserErrorException(ts.location, "Syntax error: Duplicate property key detected: " + repr(parsedData[0]))
			retData[parsedData[0]] = parsedData[1]
	#

	@debugDecorator
	def _tryEat_JPROPERTY(self, ctx, ts):
		# loc = ts.location

		t1 = ts.peek()
		if t1.type != "s":
			return (False, None)
		ts.skip()

		t2 = ts.peek()
		if (t2.type != "d") or (t2.text != ":"):
			raise ParserErrorException(ts.location, "Syntax error: Expecting ':' followed by a property value!")
		ts.skip()

		bSuccess, parsedData = self._tryEat_JANYVALUE(ctx, ts)
		if bSuccess:
			return (True, (t1.text, parsedData))

		raise ParserErrorException(ts.location, "Syntax error: Expecting a valid JSON value!")
	#

#






