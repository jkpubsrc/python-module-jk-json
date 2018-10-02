#!/usr/bin/env python3
# -*- coding: utf-8 -*-



from .SourceCodeLocation import *




class ParserErrorException(Exception):

	def __init__(self, location, message):
		assert isinstance(location, SourceCodeLocation)

		super().__init__(str(location) + " :: " + message)

		self.__location = location
		self.__message = message
	#

	@property
	def location(self):
		return self.__location
	#

	@property
	def message(self):
		return self.__message
	#

#







