

import math

from .TokenStream import *
from .ParserErrorException import *
from .ParserBase import *
from .JsonParserStrict import *



class JsonParserRelaxed(JsonParserStrict):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	def __init__(self):
		pass
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	@debugDecorator
	def _tryEat_JVALUE_LIST(self, ctx:ParsingContext, ts:TokenStream):
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
				return (True, retData)
			retData.append(parsedData)
	#

	@debugDecorator
	def _tryEat_JPROPERTY_LIST(self, ctx:ParsingContext, ts:TokenStream):
		# loc = ts.location

		retData = {}
		bSuccess, parsedData = self._tryEat_JPROPERTY(ctx, ts)
		if not bSuccess:
			return (False, None)

		retData[parsedData[0]] = parsedData[1]

		while True:
			t1 = ts.peek()
			if (t1.type != "d") or (t1.text != ","):
				return (True, retData)
			ts.skip()

			bSuccess, parsedData = self._tryEat_JPROPERTY(ctx, ts)
			if not bSuccess:
				return (True, retData)

			if parsedData[0] in retData:
				if not ctx.allowDuplicatePropertyNames:
					raise ParserErrorException(ts.location, "Syntax error: Duplicate property key detected: " + repr(parsedData[0]))
			retData[parsedData[0]] = parsedData[1]
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

#






