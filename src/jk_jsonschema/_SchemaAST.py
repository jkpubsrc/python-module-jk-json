#!/usr/bin/env python3
# -*- coding: utf-8 -*-








class _SchemaAST(object):

	def __init__(self,
		any_allowedTypes,									# list<int>
		any_allowedValues,									# list<*>
		any_mustBeExactValue,								# 1tuple<*>
		number_multipleValueOf,								# int|float
		number_maximum,										# int|float
		number_exclusiveMaximum,							# int|float
		number_minimum,										# int|float
		number_exclusiveMinimum,							# int|float
		string_minLength,									# int
		string_maxLength,									# int
		string_pattern,										# regex
		array_items,										# _SchemaAST|_SchemaAST[]
		array_additionalItems,								# _SchemaAST|_SchemaAST[]
		array_maxItems,										# int
		array_minItems,										# int
		array_itemsMustBeUnique,							# bool
		array_mustContainExactValue,						# _SchemaAST
		array_itemsMustNotBeNone,							# bool
		array_itemsMustBeNone,								# bool
		object_minProperties,								# int
		object_maxProperties,								# int
		object_properties,									# dict<str,_SchemaAST>
		object_patternProperties,							# list<(str,_SchemaAST)>
		object_propertyDependencyObjectMustMatchSchema,		# dict<str,_SchemaAST>
		object_propertyDependencyOtherPropertyMustExist,	# dict<str,str[]>
		object_propertyNames,								# _SchemaAST
		object_requiredProperties,							# str[]
		object_additionalProperties,						# _SchemaAST
		op_if,												# _SchemaAST
		op_then,											# _SchemaAST
		op_else,											# _SchemaAST
		op_not,												# _SchemaAST
		op_allOf,											# list<_SchemaAST>
		op_anyOf,											# list<_SchemaAST>
		op_oneOf,											# list<_SchemaAST>
		always = None										# bool
	):
		self.any_allowedTypes = any_allowedTypes
		self.any_allowedValues = any_allowedValues
		self.any_mustBeExactValue = any_mustBeExactValue
		self.number_multipleValueOf = number_multipleValueOf
		self.number_maximum = number_maximum
		self.number_exclusiveMaximum = number_exclusiveMaximum
		self.number_minimum = number_minimum
		self.number_exclusiveMinimum = number_exclusiveMinimum
		self.string_minLength = string_minLength
		self.string_maxLength = string_maxLength
		self.string_pattern = string_pattern
		self.array_items = array_items
		self.array_additionalItems = array_additionalItems
		self.array_maxItems = array_maxItems
		self.array_minItems = array_minItems
		self.array_itemsMustBeUnique = array_itemsMustBeUnique
		self.array_mustContainExactValue = array_mustContainExactValue
		self.array_itemsMustNotBeNone = array_itemsMustNotBeNone
		self.array_itemsMustBeNone = array_itemsMustBeNone
		self.object_minProperties = object_minProperties
		self.object_maxProperties = object_maxProperties
		self.object_properties = object_properties
		self.object_patternProperties = object_patternProperties
		self.object_propertyDependencyObjectMustMatchSchema = object_propertyDependencyObjectMustMatchSchema
		self.object_propertyDependencyOtherPropertyMustExist = object_propertyDependencyOtherPropertyMustExist
		self.object_propertyNames = object_propertyNames
		self.object_requiredProperties = object_requiredProperties
		self.object_additionalProperties = object_additionalProperties
		self.op_if = op_if
		self.op_then = op_then
		self.op_else = op_else
		self.op_not = op_not
		self.op_allOf = op_allOf
		self.op_anyOf = op_anyOf
		self.op_oneOf = op_oneOf
		self.always = always
	#

	def __makeNullIfEmptyListOrDict(self, item):
		if item is None:
			return None

		if len(item) == 0:
			return None
		else:
			return item
	#

	def __normalize_makeNullIfEmptyListOrDict(self, item):
		if item is None:
			return None

		if isinstance(item, list):
			for f in item:
				f.normalize()
		elif isinstance(item, dict):
			newItem = {}
			for k, f in item.items():
				if f != None:
					f.normalize()
					newItem[k] = f
			item = newItem

		if len(item) == 0:
			return None
		else:
			return item
	#

	def __normalize_makeNullIfEmptyAST(self, ast):
		if ast is None:
			return None

		ast.normalize()
		if ast.isNotEmpty():
			return ast
		else:
			return None
	#

	def normalize(self):
		self.any_allowedTypes = self.__makeNullIfEmptyListOrDict(self.any_allowedTypes)
		self.any_allowedValues = self.__makeNullIfEmptyListOrDict(self.any_allowedValues)

		newList = []
		for regex, schema in self.object_patternProperties:
			schema = self.__normalize_makeNullIfEmptyAST(schema)
			if schema != None:
				newList.append((regex, schema))
		if len(newList) == 0:
			newList = None
		self.object_patternProperties = newList

		self.array_items = self.__normalize_makeNullIfEmptyListOrDict(self.array_items)
		self.object_properties = self.__normalize_makeNullIfEmptyListOrDict(self.object_properties)
		self.object_propertyDependencyObjectMustMatchSchema = self.__normalize_makeNullIfEmptyListOrDict(self.object_propertyDependencyObjectMustMatchSchema)
		self.op_allOf = self.__normalize_makeNullIfEmptyListOrDict(self.op_allOf)
		self.op_anyOf = self.__normalize_makeNullIfEmptyListOrDict(self.op_anyOf)
		self.op_oneOf = self.__normalize_makeNullIfEmptyListOrDict(self.op_oneOf)

		newDict = {}
		for key, stringList in self.object_propertyDependencyOtherPropertyMustExist.items():
			if len(stringList) > 0:
				newDict[key] = stringList
		if len(newDict) == 0:
			newDict = None
		self.object_propertyDependencyOtherPropertyMustExist[key] = newDict

		self.array_additionalItems = self.__normalize_makeNullIfEmptyAST(self.array_additionalItems)
		self.array_mustContainExactValue = self.__normalize_makeNullIfEmptyAST(self.array_mustContainExactValue)
		self.object_propertyNames = self.__normalize_makeNullIfEmptyAST(self.object_propertyNames)
		self.op_if = self.__normalize_makeNullIfEmptyAST(self.op_if)
		self.op_then = self.__normalize_makeNullIfEmptyAST(self.op_then)
		self.op_else = self.__normalize_makeNullIfEmptyAST(self.op_else)
		self.op_not = self.__normalize_makeNullIfEmptyAST(self.op_not)
	#

	def isNotEmpty(self):
		return									\
				self.hasAnyTypeConstraint()		\
				or self.hasStringConstraint() 	\
				or self.hasArrayConstraint()	\
				or self.hasObjectConstraint()	\
				or self.hasNumberConstraint()	\
				or self.hasOpConstraint()
	#

	def isEmpty(self):
		return not								\
			(									\
				self.hasAnyTypeConstraint()		\
				or self.hasStringConstraint()	 \
				or self.hasArrayConstraint()	\
				or self.hasObjectConstraint()	\
				or self.hasNumberConstraint()	\
				or self.hasOpConstraint()		\
			)
	#

	def hasAnyTypeConstraint(self):
		return (self.any_allowedTypes != None)			\
		 	or (self.any_allowedValues != None)			\
		 	or (self.any_mustBeExactValue != None)		\
		 	or (self.always != None)
	#

	def hasStringConstraint(self):
		return (self.string_minLength != None)			\
		 	or (self.string_maxLength != None)			\
		 	or (self.string_pattern != None)
	#

	def hasArrayConstraint(self):
		return (self.array_items != None)				\
		 	or (self.array_additionalItems != None)		\
		 	or (self.array_maxItems != None)			\
		 	or (self.array_minItems != None)			\
		 	or (self.array_itemsMustBeUnique != None)	\
		 	or (self.array_mustContainExactValue != None)
	#

	def hasObjectConstraint(self):
		return (self.object_minProperties != None)					\
			or (self.object_maxProperties != None)					\
			or (self.object_properties != None)						\
		 	or (self.object_patternProperties != None)				\
		 	or (self.object_propertyDependencyOtherPropertyMustExist != None)	\
		 	or (self.object_propertyDependencyOtherPropertyMustExist != None)	\
		 	or (self.object_propertyNames != None)					\
			or (self.object_requiredProperties != None)
	#

	def hasOpConstraint(self):
		return (self.op_if != None)						\
		 	or (self.op_not != None)					\
		 	or (self.op_allOf != None)					\
		 	or (self.op_anyOf != None)					\
		 	or (self.op_oneOf != None)
	#

	def hasNumberConstraint(self):
		return (self.number_multipleValueOf != None)	\
		 	or (self.number_maximum != None)			\
		 	or (self.number_exclusiveMaximum != None)	\
		 	or (self.number_minimum != None)			\
		 	or (self.number_exclusiveMinimum != None)	\
	#

#





ALWAYS_TRUE = _SchemaAST(
	None, None, None, None, None, None, None, None, None, None,
	None, None, None, None, None, None, None, None, None, None,
	None, None, None, None, None, None, None, None, None, None,
	None, None, None, None, None,
	True)

ALWAYS_FALSE = _SchemaAST(
	None, None, None, None, None, None, None, None, None, None,
	None, None, None, None, None, None, None, None, None, None,
	None, None, None, None, None, None, None, None, None, None,
	None, None, None, None, None,
	False)


















