#!/usr/bin/env python3
# -*- coding: utf-8 -*-



import jk_logging

from jk_json.tools import *

from ._SchemaAST import _SchemaAST, ALWAYS_FALSE, ALWAYS_TRUE
from .schema_validator import Validator, compileAst



def _walk(v):
	if isinstance(v, (tuple, list)):
		for x in v:
			yield x
	else:
		yield v
#

def _getN(dictionary, key, expectedTypeOrTypes):
	if key in dictionary:
		v = dictionary[key]
		if isinstance(expectedTypeOrTypes, (tuple, list)):
			if type(v) in expectedTypeOrTypes:
				return v
			else:
				raise Exception("Value of unexpected type " + str(type(v)) + " at key " + key)
		else:
			if type(v) == expectedTypeOrTypes:
				return v
			else:
				raise Exception("Value of unexpected type " + str(type(v)) + " at key " + key)
	else:
		return None
#

def _getE(dictionary, key, expectedTypeOrTypes):
	if key in dictionary:
		v = dictionary[key]
		if isinstance(expectedTypeOrTypes, (tuple, list)):
			if type(v) in expectedTypeOrTypes:
				return v
			else:
				raise Exception("Value of unexpected type " + str(type(v)) + " at key " + key)
		else:
			if type(v) == expectedTypeOrTypes:
				return v
			else:
				raise Exception("Value of unexpected type " + str(type(v)) + " at key " + key)
	else:
		raise Exception("Value expected at key " + key)
#










class SchemaContext(object):

	def __init__(self):
		self.definitions = {}
	#

#



class SchemaParser(object):

	TYPESTR_TO_TYPEID_MAP = {
		"null": TYPE_NULL,
		"number": TYPE_FLOAT,
		"integer": TYPE_INT,
		"boolean": TYPE_BOOL,
		"string": TYPE_STR,
		"array": TYPE_ARRAY,
		"object": TYPE_OBJECT,
	}

	@staticmethod
	def parse(jsonDef, log = None):
		if log is None:
			log = jk_logging.NullLogger.create()
		ctx = SchemaContext()
		log.debug("Building AST ...")
		ast = SchemaParser.__parse(ctx, jsonDef)
		log.debug("Compiling AST ...")
		return Validator(compileAst(ast, log))
	#

	#
	# Perform the parsing.
	#
	# @return		_SchemaAST		An AST object.
	#
	@staticmethod
	def __parse(ctx, jsonDef):

		if jsonDef is None:
			return None

		if jsonDef == True:
			return ALWAYS_TRUE

		if jsonDef == False:
			return ALWAYS_FALSE

		if not isinstance(jsonDef, dict):
			raise Exception()

		if "definitions" in jsonDef:
			definitions = _getE(jsonDef, "definitions", dict)
			newDefs = {}
			for defName, defSchema in definitions.items():
				p = SchemaParser.__parse(ctx, defSchema)
				if p:
					newDefs[defName] = p
			if newDefs:
				ctx.definitions.update(newDefs)

		any_allowedTypes = None
		if "type" in jsonDef:
			any_allowedTypes = []
			for t in _walk(jsonDef["type"]):
				if t in SchemaParser.TYPESTR_TO_TYPEID_MAP:
					typeID = SchemaParser.TYPESTR_TO_TYPEID_MAP[t]
					any_allowedTypes.append(typeID)
					if typeID == TYPE_FLOAT:
						any_allowedTypes.append(TYPE_INT)
				else:
					raise Exception("Invalid type specified: " + repr(t))
			if len(any_allowedTypes) == 0:
				any_allowedTypes = None

		any_allowedValues = _getN(jsonDef, "enum", (tuple, list))

		any_mustBeExactValue = None
		if "const" in jsonDef:
			any_mustBeExactValue = ( jsonDef["const"], )

		number_multipleValueOf = _getN(jsonDef, "multipleOf", (int, float))

		number_maximum = _getN(jsonDef, "maximum", (int, float))

		number_exclusiveMaximum = _getN(jsonDef, "exclusiveMaximum", (int, float))

		number_minimum = _getN(jsonDef, "minimum", (int, float))

		number_exclusiveMinimum = _getN(jsonDef, "exclusiveMinimum", (int, float))

		string_minLength = _getN(jsonDef, "minLength", int)

		string_maxLength = _getN(jsonDef, "maxLength", int)

		string_pattern = None
		if "pattern" in jsonDef:
			string_pattern = _getE(jsonDef, "pattern", str)

		array_itemsMustNotBeNone = False
		array_itemsMustBeNone = False
		array_items = None
		if "items" in jsonDef:
			x = jsonDef["items"]
			if isinstance(x, dict):
				s = SchemaParser.__parse(ctx, x)
				if s.isNotEmpty():
					array_items = s
			elif isinstance(x, list):
				array_items = []
				for x in _walk(jsonDef["items"]):
					s = SchemaParser.__parse(ctx, x)
					array_items.append(s)
				#if len(array_items) == 0:
				#	array_items = None
			elif isinstance(x, bool):
				if x:
					array_itemsMustNotBeNone = True
				else:
					array_itemsMustBeNone = True
			else:
				raise Exception("Invalid value specified for 'items'")

		array_additionalItems = None
		if "additionalItems" in jsonDef:
			array_additionalItems = SchemaParser.__parse(ctx, jsonDef["additionalItems"])

		array_maxItems = _getN(jsonDef, "maxItems", int)

		array_minItems = _getN(jsonDef, "minItems", int)

		array_itemsMustBeUnique = None
		if "uniqueItems" in jsonDef:
			array_itemsMustBeUnique = _getE(jsonDef, "uniqueItems", bool)

		array_mustContainExactValue = SchemaParser.__parse(ctx, _getN(jsonDef, "contains", (dict, bool)))

		object_properties = None
		if "properties" in jsonDef:
			object_properties = {}
			for propertyName in jsonDef["properties"]:
				p = SchemaParser.__parse(ctx, jsonDef["properties"][propertyName])
				if p:
					object_properties[propertyName] = p
			if len(object_properties) == 0:
				object_properties = None

		object_patternProperties = None
		if "patternProperties" in jsonDef:
			object_patternProperties = []
			for propertyPattern in jsonDef["patternProperties"]:
				p = SchemaParser.__parse(ctx, jsonDef["patternProperties"][propertyPattern])
				if p:
					object_patternProperties.append((propertyPattern, p))
			if len(object_patternProperties) == 0:
				object_patternProperties = None

		object_maxProperties = jsonDef.get("maxProperties", None)

		object_minProperties = jsonDef.get("minProperties", None)

		object_additionalProperties = None
		if "additionalProperties" in jsonDef:
			object_additionalProperties = SchemaParser.__parse(ctx, jsonDef["additionalProperties"])

		object_requiredProperties = jsonDef.get("required", None)

		object_propertyDependencyObjectMustMatchSchema = None
		object_propertyDependencyOtherPropertyMustExist = None
		if "dependencies" in jsonDef:
			object_propertyDependencyObjectMustMatchSchema = {}
			object_propertyDependencyOtherPropertyMustExist = {}
			for propertyName in jsonDef["dependencies"]:
				v = jsonDef["dependencies"][propertyName]
				if isinstance(v, (tuple, list)):
					object_propertyDependencyOtherPropertyMustExist[propertyName] = v
				elif isinstance(v, (dict, bool)):
					p = SchemaParser.__parse(ctx, v)
					if p != None:
						object_propertyDependencyObjectMustMatchSchema[propertyName] = p
				else:
					raise Exception("Not supported!")
			if len(object_propertyDependencyObjectMustMatchSchema) == 0:
				object_propertyDependencyObjectMustMatchSchema = None
			if len(object_propertyDependencyOtherPropertyMustExist) == 0:
				object_propertyDependencyOtherPropertyMustExist = None

		object_propertyNames = None
		if "propertyNames" in jsonDef:
			object_propertyNames = SchemaParser.__parse(ctx, jsonDef["propertyNames"])

		op_if = None
		op_then = None
		op_else = None
		xIf = _getN(jsonDef, "if", dict)
		if xIf is None:
			xThen = None
			xElse = None
		else:
			xThen = _getN(jsonDef, "then", dict)
			xElse = _getN(jsonDef, "else", dict)
			if (xThen != None) or (xElse != None):
				op_if = SchemaParser.__parse(ctx, xIf)
				if xThen:
					op_then = SchemaParser.__parse(ctx, xThen)
				if xElse:
					op_else = SchemaParser.__parse(ctx, xElse)

		op_not = None
		if "not" in jsonDef:
			op_not = SchemaParser.__parse(ctx, _getE(jsonDef, "not", (dict, bool)))

		op_allOf = None
		if "allOf" in jsonDef:
			subSchemas = _getE(jsonDef, "allOf", list)
			if len(subSchemas) == 0:
				raise Exception("'allOf' has empty schema list!")
			op_allOf = []
			for x in subSchemas:
				p = SchemaParser.__parse(ctx, x)
				if p:
					op_allOf.append(p)
			#if len(op_allOf) == 0:
			#	raise Exception("'allOf' results in empty schema list!")

		op_anyOf = None
		if "anyOf" in jsonDef:
			subSchemas = _getE(jsonDef, "anyOf", list)
			if len(subSchemas) == 0:
				raise Exception("'anyOf' has empty schema list!")
			op_anyOf = []
			for x in subSchemas:
				p = SchemaParser.__parse(ctx, x)
				if p:
					op_anyOf.append(p)
			#if len(op_anyOf) == 0:
			#	raise Exception("'anyOf' results in empty schema list!")

		op_oneOf = None
		if "oneOf" in jsonDef:
			subSchemas = _getE(jsonDef, "oneOf", list)
			if len(subSchemas) == 0:
				raise Exception("'oneOf' has empty schema list!")
			op_oneOf = []
			for x in subSchemas:
				p = SchemaParser.__parse(ctx, x)
				if p:
					op_oneOf.append(p)
			#if len(op_oneOf) == 0:
			#	raise Exception("'oneOf' results in empty schema list!")

		return _SchemaAST(
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
			string_pattern,										# regexstr
			array_items,										# _SchemaAST[]
			array_additionalItems,								# _SchemaAST
			array_maxItems,										# int
			array_minItems,										# int
			array_itemsMustBeUnique,							# bool
			array_mustContainExactValue,						# _SchemaAST
			array_itemsMustNotBeNone,							# bool
			array_itemsMustBeNone,								# bool
			object_minProperties,								# int
			object_maxProperties,								# int
			object_properties,									# dict<str,_SchemaAST>
			object_patternProperties,							# list<(regexstr,_SchemaAST)>
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
			op_oneOf											# list<_SchemaAST>
		)
	#

#












