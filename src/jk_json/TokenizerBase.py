

import re
import collections






from .Token import *
from .ParserErrorException import *





_TokenizerActionTuple = collections.namedtuple("_TokenizerActionTuple", [ "actionID", "data" ])

#
# A tokenization action. Use the methods provided in `TokenizerAction` to provide actions.
#
class TokenizerAction(object):

	ERROR = 1
	ADVANCE = 2
	SWITCHMODE = 3
	EMITELEMENT = 4
	BEGINBUFFER = 5
	APPENDELEMENTTOBUFFER = 6
	EMITBUFFER = 7
	DROPBUFFER = 8
	APPENDTEXTTOBUFFER = 9

	#
	# Emit a tokenization error.
	#
	# @param	str errorCode			An error code the error message should be prefixed with. This code does not necessarily
	#									need to be unique: Multiple tokenization problems might emit the same error. (Nevertheless
	#									you should use the same error code for the same error class.)
	# @param	str errorMessage		A user friendly error message.
	# @param	str errorIdentifier		An error identifier. This ID should be unique in order to allow tracking of the
	#									error back to the tokenization rule. This is ment for debugging only.
	#
	@staticmethod
	def error(errorCode, errorMessage, errorIdentifier):
		return _TokenizerActionTuple(TokenizerAction.ERROR, errorMessage)
	#

	#
	# Advance a single character in the stream = ignore the current character.
	#
	@staticmethod
	def advance():
		return _TokenizerActionTuple(TokenizerAction.ADVANCE, None)
	#

	#
	# Switch to a differnt parsing mode.
	#
	@staticmethod
	def switchMode(mode):
		return _TokenizerActionTuple(TokenizerAction.SWITCHMODE, mode)
	#

	#
	# Emit a token. The buffer will remain untouched.
	#
	@staticmethod
	def emitElement(tokenType):
		return _TokenizerActionTuple(TokenizerAction.EMITELEMENT, tokenType)
	#

	#
	# Reset the buffer. The buffer will now be empty and new data can be written to it.
	#
	@staticmethod
	def beginBuffer():
		return _TokenizerActionTuple(TokenizerAction.BEGINBUFFER, None)
	#

	#
	# Append the current parsed item to the buffer. What exactly that is and how much data this element contains depends on the current parsing action.
	#
	@staticmethod
	def appendElementToBuffer(callbackFunction = None):
		return _TokenizerActionTuple(TokenizerAction.APPENDELEMENTTOBUFFER, callbackFunction)
	#

	#
	# Emit the buffer = create a token with the specified token type containing the current buffer's content.
	#
	@staticmethod
	def emitBuffer(tokenType):
		return _TokenizerActionTuple(TokenizerAction.EMITBUFFER, tokenType)
	#

	#
	# Reset the buffer. This is the same as "beginBuffer()".
	#
	@staticmethod
	def dropBuffer():
		return _TokenizerActionTuple(TokenizerAction.DROPBUFFER, None)
	#

	#
	# Append the specified text to the buffer.
	#
	@staticmethod
	def appendTextToBuffer(text):
		return _TokenizerActionTuple(TokenizerAction.APPENDTEXTTOBUFFER, text)
	#

#





_TokenizerPatternTuple = collections.namedtuple("_TokenizerPatternTuple", [ "patternID", "data", "dataLength" ])

#
# A tokenization pattern. Use the methods provided in `TokenizerPattern` to provide patterns.
#
class TokenizerPattern(object):

	EXACTCHAR = 1
	ANYCHAR = 2
	EXACTSTRING = 3
	REGEX = 4

	#
	# Is the character encountered equal to the specified character?
	#
	@staticmethod
	def exactChar(data):
		assert isinstance(data, str)
		assert len(data) == 1
		return _TokenizerPatternTuple(TokenizerPattern.EXACTCHAR, data, 1)
	#

	#
	# Are the characters encountered exactly the specified sequence?
	#
	@staticmethod
	def exactSequence(data):
		assert isinstance(data, str)
		assert len(data) > 0
		return _TokenizerPatternTuple(TokenizerPattern.EXACTSTRING, data, len(data))
	#

	#
	# Is the character encountered any of the specified characters?
	#
	@staticmethod
	def anyOfTheseChars(data):
		assert isinstance(data, str)
		assert len(data) > 0
		return _TokenizerPatternTuple(TokenizerPattern.ANYCHAR, data, -1)
	#

	#
	# Do the characters encountered match the specified regular expression?
	#
	@staticmethod
	def regEx(data):
		return _TokenizerPatternTuple(TokenizerPattern.REGEX, re.compile(data), -1)
	#

#




#
# This class represents a table that is part of the initialization data of a tokenizer.
#
class TokenizingTable(object):

	def __init__(self, tableID):
		self.tableID = tableID
		self.rows = []
		self.onOtherActions = None
		self.onEOSActions = None
	#

	def addPatternRow(self, pattern, actions):
		assert isinstance(pattern, _TokenizerPatternTuple)
		assert isinstance(actions, (tuple, list))
		for action in actions:
			assert isinstance(action, _TokenizerActionTuple)
		self.rows.append((pattern.patternID, pattern.data, pattern.dataLength, tuple(actions)))
	#

	def setOther(self, actions):
		assert isinstance(actions, (tuple, list))
		for action in actions:
			assert isinstance(action, _TokenizerActionTuple)
		self.onOtherActions = actions
	#

	def setEOS(self, actions):
		assert isinstance(actions, (tuple, list))
		for action in actions:
			assert isinstance(action, _TokenizerActionTuple)
		self.onEOSActions = actions
	#

#




#
# The base class or tokenizers.
#
class TokenizerBase(object):

	def __init__(self, tables):
		assert isinstance(tables, (tuple, list))
		for table in tables:
			assert isinstance(table, TokenizingTable)

		self.__tables = tuple(tables)
	#

	#
	# Create a set of empty tables.
	#
	# @param	int numberOfTables		The number of tables to create.
	# @return	tuple					A tuple containing exactly the number of tables specified.
	#
	def createTables(self, numberOfTables):
		assert isinstance(numberOfTables, int)
		assert numberOfTables > 1

		ret = []
		for n in range(0, numberOfTables):
			ret.append(TokenizingTable(n))
		return tuple(ret)
	#

	#
	# Tokenizes the specified string.
	#
	# The following token types are supported:
	# * "d" : Delimiter
	# * "i" : Integer
	# * "f" : Float
	# * "s" : String
	# * "w" : Word
	# * "eol" : New line
	# * "eos" : End of stream
	#
	# @param	str textData		The text data to tokenize.
	# @param	str sourceID		A file path or an URL that defines the origin of the source.
	# @return	iterator<Token>		Returns an iterator that provides tokens.
	#
	def tokenize(self, textData, sourceID = None, bDebuggingEnabled = False):
		i = 0
		maxi = len(textData)
		lineNo = 0
		charPos = 0
		bufferLineNo = 0
		bufferCharPos = 0

		if bDebuggingEnabled:
			print("Now tokenizing " + str(maxi) + " characters ...")

		buffer = ""
		mode = 0
		spanText = None
		nextLineNo = 0
		nextCharPos = 0

		while i < maxi:
			if bDebuggingEnabled:
				print("---- mode:" + str(mode) + " -- i:" + str(i))
			if (mode < 0) or (mode >= len(self.__tables)):
				raise Exception("Requested tokenization table does not exist: " + str(mode))
			currentTable = self.__tables[mode]

			selectedActions = None
			spanLength = None
			spanText = None
			iEnd = None

			# try to match

			for patternID, patternData, patternDataLength, actions in currentTable.rows:
				if patternID == TokenizerPattern.EXACTCHAR:
					if textData[i] == patternData:
						spanLength = 1
						iEnd = i + 1
						spanText = textData[i]
						selectedActions = actions
						break
				elif patternID == TokenizerPattern.ANYCHAR:
					if patternData.find(textData[i]) >= 0:
						spanLength = 1
						iEnd = i + 1
						spanText = textData[i]
						selectedActions = actions
						break
				elif patternID == TokenizerPattern.EXACTSTRING:
					iEnd = i + patternDataLength
					if (iEnd <= maxi) and (patternData == textData[i:iEnd]):
						spanLength = patternDataLength
						iEnd = i + patternDataLength
						spanText = patternData
						selectedActions = actions
						break
				elif patternID == TokenizerPattern.REGEX:
					pr = patternData.match(textData, i)
					if pr:
						iEnd = pr.end()
						spanText = textData[i:iEnd]
						spanLength = iEnd - i
						selectedActions = actions
						break
				else:
					raise Exception()

			# no match? => advance one character

			if selectedActions is None:
				spanLength = 1
				iEnd = i + 1
				spanText = textData[i]
				selectedActions = currentTable.onOtherActions

			# set correct line number and character position

			nextLineNo = lineNo
			nextCharPos = charPos
			for c in spanText:
				if c == "\n":
					nextLineNo += 1
					nextCharPos = 0
				else:
					nextCharPos += 1

			# perform parsing actions

			for actionID, actionData in selectedActions:
				if actionID == TokenizerAction.ERROR:
					raise ParserErrorException(SourceCodeLocation(sourceID, lineNo, charPos, lineNo, charPos), actionData, textData)
				elif actionID == TokenizerAction.ADVANCE:
					lineNo = nextLineNo
					charPos = nextCharPos
					i = iEnd
				elif actionID == TokenizerAction.SWITCHMODE:
					mode = actionData
				elif actionID == TokenizerAction.EMITELEMENT:
					yield Token(actionData, spanText, sourceID, lineNo, charPos, nextLineNo, nextCharPos)
				elif actionID == TokenizerAction.BEGINBUFFER:
					bufferLineNo = lineNo
					bufferCharPos = charPos
					buffer = ""
				elif actionID == TokenizerAction.APPENDELEMENTTOBUFFER:
					if actionData is not None:
						buffer += actionData(spanText)
					else:
						buffer += spanText
				elif actionID == TokenizerAction.EMITBUFFER:
					yield Token(actionData, buffer, sourceID, bufferLineNo, bufferCharPos, lineNo, charPos)
					buffer = ""
				elif actionID == TokenizerAction.DROPBUFFER:
					bufferLineNo = lineNo
					bufferCharPos = charPos
					buffer = ""
				elif actionID == TokenizerAction.APPENDTEXTTOBUFFER:
					buffer += actionData
				else:
					raise Exception()

		# EOS reached

		currentTable = self.__tables[mode]
		iEnd = len(textData)

		# perform final parsing actions

		# NOTE: the next lines are identical with the branching above
		for actionID, actionData in currentTable.onEOSActions:
			if actionID == TokenizerAction.ERROR:
				raise ParserErrorException(SourceCodeLocation(sourceID, lineNo, charPos, lineNo, charPos), actionData, textData)
			elif actionID == TokenizerAction.ADVANCE:
				lineNo = nextLineNo
				charPos = nextCharPos
				i = iEnd
			elif actionID == TokenizerAction.SWITCHMODE:
				mode = actionData
			elif actionID == TokenizerAction.EMITELEMENT:
				yield Token(actionData, spanText, sourceID, lineNo, charPos, nextLineNo, nextCharPos)
			elif actionID == TokenizerAction.BEGINBUFFER:
				bufferLineNo = lineNo
				bufferCharPos = charPos
				buffer = ""
			elif actionID == TokenizerAction.APPENDELEMENTTOBUFFER:
				if actionData is not None:
					buffer += actionData(spanText)
				else:
					buffer += spanText
			elif actionID == TokenizerAction.EMITBUFFER:
				yield Token(actionData, buffer, sourceID, bufferLineNo, bufferCharPos, lineNo, charPos)
				buffer = ""
			elif actionID == TokenizerAction.DROPBUFFER:
				bufferLineNo = lineNo
				bufferCharPos = charPos
				buffer = ""
			elif actionID == TokenizerAction.APPENDTEXTTOBUFFER:
				buffer += actionData
			else:
				raise Exception()

		if bDebuggingEnabled:
			print("Tokenizing completed.")

	#

#








