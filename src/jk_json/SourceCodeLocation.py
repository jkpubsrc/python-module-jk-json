



import typing

from .Token import *






class SourceCodeLocation(object):

	################################################################################################################################
	## Constants
	################################################################################################################################

	################################################################################################################################
	## Constructor
	################################################################################################################################

	def __init__(self, sourceID:typing.Union[str,None], lineNo:int, charPos:int, endLineNo:int, endCharPos:int):
		self.sourceID = sourceID
		self.lineNo = lineNo
		self.charPos = charPos
		self.endLineNo = endLineNo
		self.endCharPos = endCharPos
	#

	################################################################################################################################
	## Properties
	################################################################################################################################

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def __str__(self):
		if self.sourceID != None:
			return self.sourceID + "(" + str(self.lineNo + 1) + ":" + str(self.charPos + 1) + ")"
		else:
			return "(" + str(self.lineNo + 1) + ":" + str(self.charPos + 1) + ")"
	#

	def __repr__(self):
		if self.sourceID != None:
			return self.sourceID + "(" + str(self.lineNo + 1) + ":" + str(self.charPos + 1) + ")"
		else:
			return "(" + str(self.lineNo + 1) + ":" + str(self.charPos + 1) + ")"
	#

	def spanTo(self, sourceCodeLocation):
		assert isinstance(sourceCodeLocation, SourceCodeLocation)

		return SourceCodeLocation(self.sourceID, self.lineNo, self.charPos, sourceCodeLocation.endLineNo, sourceCodeLocation.endCharPos)
	#

	################################################################################################################################
	## Static Methods
	################################################################################################################################

	@staticmethod
	def fromTokens(tokenA, tokenB):
		assert isinstance(tokenA, Token)
		assert isinstance(tokenB, Token)

		return SourceCodeLocation(tokenA.sourceID, tokenA.lineNo, tokenA.charPos, tokenB.endLineNo, tokenB.endCharPos)
	#

	@staticmethod
	def fromToken(token):
		assert isinstance(token, Token)

		return SourceCodeLocation(token.sourceID, token.lineNo, token.charPos, token.endLineNo, token.endCharPos)
	#

#







