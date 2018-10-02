#!/usr/bin/env python3
# -*- coding: utf-8 -*-



import jk_json



class AbstractGenerator(object):

	def __init__(self, _xParent, _xName:str, _xSchema:dict, _xRequired:list):
		self._schema = _xSchema
		self._parent = _xParent
		self._name = _xName
		self._requiredList = _xRequired
	#

	def required(self):
		if self._requiredList:
			if self._name not in self._requiredList:
				self._requiredList.append(self._name)
			return self
		else:
			raise Exception("This is not a value key that could be set to optional/required.")
	#

	def notRequired(self):
		if self._requiredList:
			if self._name in self._requiredList:
				self._requiredList.remove(self._name)
			return self
		else:
			raise Exception("This is not a value key that could be set to optional/required.")
	#

	def __str__(self):
		return jk_json.dumps(self._schema)
	#

	def __repr__(self):
		return jk_json.dumps(self._schema)
	#

	@property
	def schema(self):
		return self._schema
	#

	def __enter__(self):
		return self
	#

	def __exit__(self, etype, value, traceback):
		return False
	#

#



class BooleanGenerator(AbstractGenerator):

	def __init__(self, _xParent, _xName:str, _xSchema:dict, _xRequired:list):
		super().__init__(_xParent, _xName, _xSchema, _xRequired)
	#

#



class IntegerGenerator(AbstractGenerator):

	def __init__(self, _xParent, _xName:str, _xSchema:dict, _xRequired:list):
		super().__init__(_xParent, _xName, _xSchema, _xRequired)
	#

	def minimum(self, minimum:int):
		if minimum is None:
			if "minimum" in self._schema:
				self._schema.remove("minimum")
		else:
			self._schema["minimum"] = minimum
		return self
	#

	def exclusiveMinimum(self, minimum:int):
		if minimum is None:
			if "exclusiveMinimum" in self._schema:
				self._schema.remove("exclusiveMinimum")
		else:
			self._schema["exclusiveMinimum"] = minimum
		return self
	#

	def maximum(self, maximum:int):
		if maximum is None:
			if "maximum" in self._schema:
				self._schema.remove("maximum")
		else:
			self._schema["maximum"] = maximum
		return self
	#

	def exclusiveMaximum(self, maximum:int):
		if maximum is None:
			if "exclusiveMaximum" in self._schema:
				self._schema.remove("exclusiveMaximum")
		else:
			self._schema["exclusiveMaximum"] = maximum
		return self
	#

	def allowedValues(self, allowedValues:list):
		if allowedValues is None:
			if "enum" in self._schema:
				self._schema.remove("enum")
		else:
			self._schema["enum"] = allowedValues
		return self
	#

#



class FloatGenerator(AbstractGenerator):

	def __init__(self, _xParent, _xName:str, _xSchema:dict, _xRequired:list):
		super().__init__(_xParent, _xName, _xSchema, _xRequired)
	#

	def minimum(self, minimum:float):
		if minimum is None:
			if "minimum" in self._schema:
				self._schema.remove("minimum")
		else:
			self._schema["minimum"] = minimum
		return self
	#

	def exclusiveMinimum(self, minimum:float):
		if minimum is None:
			if "exclusiveMinimum" in self._schema:
				self._schema.remove("exclusiveMinimum")
		else:
			self._schema["exclusiveMinimum"] = minimum
		return self
	#

	def maximum(self, maximum:float):
		if maximum is None:
			if "maximum" in self._schema:
				self._schema.remove("maximum")
		else:
			self._schema["maximum"] = maximum
		return self
	#

	def exclusiveMaximum(self, maximum:float):
		if maximum is None:
			if "exclusiveMaximum" in self._schema:
				self._schema.remove("exclusiveMaximum")
		else:
			self._schema["exclusiveMaximum"] = maximum
		return self
	#

	def allowedValues(self, allowedValues:list):
		if allowedValues is None:
			if "enum" in self._schema:
				self._schema.remove("enum")
		else:
			self._schema["enum"] = allowedValues
		return self
	#

#



class StringGenerator(AbstractGenerator):

	def __init__(self, _xParent, _xName:str, _xSchema:dict, _xRequired:list):
		super().__init__(_xParent, _xName, _xSchema, _xRequired)
	#

	def minLength(self, minLength:int):
		if minLength is None:
			if "minLength" in self._schema:
				self._schema.remove("minLength")
		else:
			self._schema["minLength"] = minLength
		return self
	#

	def maxLength(self, maxLength:int):
		if maxLength is None:
			if "maxLength" in self._schema:
				self._schema.remove("maxLength")
		else:
			self._schema["maxLength"] = maxLength
		return self
	#

	def regexPattern(self, regexPattern:str):
		if regexPattern is None:
			if "enum" in self._schema:
				self._schema.remove("enum")
		else:
			if len(regexPattern) != len(regexPattern.strip()):
				raise Exception("Invalid pattern!")
			self._schema["pattern"] = regexPattern
		return self
	#

	def allowedValues(self, allowedValues:list):
		if allowedValues is None:
			if "enum" in self._schema:
				self._schema.remove("enum")
		else:
			self._schema["enum"] = allowedValues
		return self
	#

#



class ListGenerator(AbstractGenerator):

	def __init__(self, _xParent, _xName:str, _xSchema:dict, _xRequired:list, subTypeGenMap:AbstractGenerator):
		super().__init__(_xParent, _xName, _xSchema, _xRequired)
		self.__subTypeGenMap = subTypeGenMap
	#

	@property
	def dataType(self) -> AbstractGenerator:
		return self.__subTypeGenMap
	#

	def minLengths(self, minLength:int):
		if minLength is None:
			if "minItems" in self._schema:
				self._schema.remove("minItems")
		else:
			self._schema["minItems"] = minLength
		return self
	#

	def maxLength(self, maxLength:int):
		if maxLength is None:
			if "maxItems" in self._schema:
				self._schema.remove("maxItems")
		else:
			self._schema["maxItems"] = maxLength
		return self
	#

	def allowedValues(self, allowedValues:list):
		# TODO: The intention is to restrict the allowed values to certain values. Does this implementation here conform to the JSON schema specification?
		if allowedValues is None:
			if "enum" in self._schema:
				self._schema.remove("enum")
		else:
			self._schema["enum"] = allowedValues
		return self
	#

#



class ObjectGenerator(AbstractGenerator):

	def __init__(self, _xParent, _xName:str, _xSchema:dict, _xRequired:list):
		super().__init__(_xParent, _xName, _xSchema, _xRequired)
		if _xSchema is None:
			_xSchema = {}
		if not "properties" in _xSchema:
			_xSchema["properties"] = {}
		if not "required" in _xSchema:
			_xSchema["required"] = []
		self._schema = _xSchema
		self.__parent = _xParent
	#

	def subCategory(self, name:str, bRequired:bool = True):
		if bRequired:
			self._schema["required"].append(name)
		subSchema = {}
		self._schema["properties"][name] = subSchema
		return ObjectGenerator(self, None, subSchema, None)
	#

	def intValue(self, name:str, bRequired:bool = True) -> IntegerGenerator:
		if bRequired:
			self._schema["required"].append(name)
		subSchema = {
			"type": [ "integer" ]
		}
		self._schema["properties"][name] = subSchema
		return IntegerGenerator(self, name, subSchema, self._schema["required"])
	#

	def floatValue(self, name:str, bRequired:bool = True) -> FloatGenerator:
		if bRequired:
			self._schema["required"].append(name)
		subSchema = {
			"type": [ "number" ]
		}
		self._schema["properties"][name] = subSchema
		return FloatGenerator(self, name, subSchema, self._schema["required"])
	#

	def boolValue(self, name:str, bRequired:bool = True) -> BooleanGenerator:
		if bRequired:
			self._schema["required"].append(name)
		subSchema = {
			"type": [ "boolean" ]
		}
		self._schema["properties"][name] = subSchema
		return BooleanGenerator(self, name, subSchema, self._schema["required"])
	#

	def strValue(self, name:str, bRequired:bool = True) -> StringGenerator:
		if bRequired:
			self._schema["required"].append(name)
		subSchema = {
			"type": [ "string" ]
		}
		self._schema["properties"][name] = subSchema
		return StringGenerator(self, name, subSchema, self._schema["required"])
	#

	def listValue(self, name:str, listType:type, bRequired:bool = True) -> ListGenerator:
		if bRequired:
			self._schema["required"].append(name)

		typeID = jk_json.tools.getTypeIDOfType(listType)
		subTypeSchema = {
			"type": [ jk_json.tools.ALL_TYPES_NAME_LIST[typeID] ]
		}
		subTypeGenMap = {
			jk_json.tools.TYPE_BOOL: BooleanGenerator,
			jk_json.tools.TYPE_INT: IntegerGenerator,
			jk_json.tools.TYPE_FLOAT: FloatGenerator,
			jk_json.tools.TYPE_STR: StringGenerator,
			jk_json.tools.TYPE_OBJECT: ObjectGenerator,
		}
		if typeID in subTypeGenMap:
			subtypeGen = subTypeGenMap[typeID](self, None, subTypeSchema, None)
		else:
			raise Exception("This generator does not support types other than 'boolean', 'integer', 'float' (= 'number'), 'string' and 'object'")

		subSchema = {
			"type": [ "array" ],
			"items": subTypeSchema,
		}
		self._schema["properties"][name] = subSchema
		return ListGenerator(self, name, subSchema, self._schema["required"], subTypeGenMap)
	#

#









def createSchemaGenerator():
	return ObjectGenerator(None, None, None, None)
#







