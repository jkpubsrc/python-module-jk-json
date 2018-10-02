#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import re
from typing import List






class AbtractValidator(object):

	def validate(self, jsonData):
		raise NotImplementedError()
	#

#












# Check if properties that are named in the specification match the associated schema.
# dict<str,_SchemaAST>
def object_properties(jsonData, arg):
	for propertyName in jsonData:
		if propertyName in arg:
			schema = arg[propertyName]
			value = jsonData[propertyName]
			if not schema.validate(value):
				return False
	return True
#



# Check if properties that are matched by any specification match the associated schema.
# list<(regex,_SchemaAST)>
def object_patternProperties(jsonData, arg):
	for propertyName in jsonData:
		for pattern, schema in arg:
			if pattern.fullmatch(propertyName) != None:
				value = jsonData[propertyName]
				if not schema.validate(value):
					return False
	return True
#



# Check if a property is registered the current object also validates against the associated schema
# dict<str,_SchemaAST>
def object_onPropertyObjectMustMatchSchema(jsonData, arg):
	for propertyName in jsonData:
		schema = arg.get(propertyName)
		if schema:
			if not schema.validate(jsonData):
				return False
	return True
#



# Check if a property is registered specific other properties exist
# dict<str,str[]>
def object_onPropertyOtherPropertyMustExist(jsonData, arg):
	for propertyName in jsonData:
		otherPropertyNames = arg.get(propertyName)
		if otherPropertyNames:
			for otherPropertyName in otherPropertyNames:
				if not otherPropertyName in jsonData:
					return False
	return True
#



# Check if all property names match the specified schema
# _SchemaAST
def object_propertyNames(jsonData, arg):
	for propertyName in jsonData:
		if not arg.validate(propertyName):
			return False
	return True
#



class ValidatorStd(AbtractValidator):

	def __init__(self, validationFunction, validationParameter):
		self.__validationFunction = validationFunction
		self.__validationParameter = validationParameter
	#

	def validate(self, jsonData):
		return self.__validationFunction(jsonData, self.__validationParameter)
	#

#



class ValidatorPropertyName(AbtractValidator):

	def __init__(self, propertyName:str, validator:AbtractValidator):
		self.__propertyName = validationFunction
		self.__propertyName = validationParameter
	#

	def validate(self, jsonData):
	for propertyName in jsonData:
		if not arg.validate(propertyName):
			return False
	return True
	#

#












