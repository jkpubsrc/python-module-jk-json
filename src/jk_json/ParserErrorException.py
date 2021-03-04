


import typing

from .SourceCodeLocation import *




class ParserErrorException(Exception):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	def __init__(self, location:SourceCodeLocation, message, textData:str = None):
		assert isinstance(location, SourceCodeLocation)
		assert isinstance(message, str)
		if textData:
			lines = textData.split("\n")
			self.__textLine = lines[location.lineNo]
			assert isinstance(textData, str)
		else:
			self.__textLine = None

		super().__init__(str(location) + " :: " + message)

		self.__location = location
		self.__message = message
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def location(self) -> SourceCodeLocation:
		return self.__location
	#

	@property
	def textLine(self) -> typing.Union[str,None]:
		return self.__textLine
	#

	@property
	def message(self) -> str:
		return self.__message
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

#







