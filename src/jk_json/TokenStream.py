


from .Token import *
from .TokenizerBase import *
from .SourceCodeLocation import *






class TokenStreamMark(object):

	def __init__(self, tokenStream):
		self.__pos = tokenStream.position
		self.__tokenStream = tokenStream
	#

	def resetToMark(self):
		self.__tokenStream._setPosition(self.__pos)
	#

#





class TokenStream(object):

	def __init__(self, tokens):
		self.__tokens = list(tokens)
		assert len(self.__tokens) > 0
		self.__pos = 0
		self.__maxpos = len(self.__tokens) - 1
		self.__eosToken = self.__tokens[self.__maxpos]
		assert self.__eosToken.type == "eos"
	#

	def reset(self):
		self.__pos = 0
	#

	@property
	def isEOS(self):
		return self.__pos == self.__maxpos
	#

	@property
	def position(self):
		return self.__pos
	#

	def mark(self):
		return TokenStreamMark(self)
	#

	def multiPeek(self, nCount):
		if nCount <= 0:
			raise Exception("Invalid nCount!")
		if self.__pos + nCount > self.__maxpos:
			ret = []
			for i in range(0, nCount):
				j = self.__pos + i
				if j < self.__maxpos:
					ret.append(self.__tokens[j])
				else:
					ret.append(self.__eosToken)
			return ret
		else:
			return self.__tokens[self.__pos:self.__pos + nCount]
	#

	@property
	def location(self):
		t = self.__tokens[self.__pos]
		return SourceCodeLocation.fromToken(t)

	def peek(self):
		return self.__tokens[self.__pos]
	#

	def skip(self, n = 1):
		if n < 0:
			raise Exception("Invalid n: " + str(n))
		if self.__pos + n > self.__maxpos:
			raise Exception("Skipping too far!")
		self.__pos += n
	#

	def skipAll(self, tokenType, tokenText):
		assert isinstance(tokenType, str)

		n = 0
		while self.__pos < self.__maxpos:
			t = self.__tokens[self.__pos]
			if t.type == "eos":
				return n
			if t.type != tokenType:
				return n
			if tokenText != None:
				if t.text != tokenText:
					return n
			n += 1
			self.__pos += 1

		return n
	#

	def _setPosition(self, pos:int):
		if (pos < 0) or (pos > self.__maxpos):
			raise Exception("Invalid position: " + str(pos))
		self.__pos = pos
	#

	def read(self):
		t = self.__tokens[self.__pos]
		if self.__pos < self.__maxpos:
			self.__pos += 1
		return t
	#

#







