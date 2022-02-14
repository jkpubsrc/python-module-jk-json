

import typing
import re
import random

import jk_json
import jk_utils

from .re import compactVerboseRegEx



def _isType(x) -> bool:
	return type is type(x)
#


_compileSingleType = None









class AbstractGenerator(object):

	#
	# @param	list _xParentalRequiredList				The JSON list that holds the names of those properties that are required. This list is defined at the parent!
	#
	def __init__(self, _xParent, _xName:str, _xSchema:dict, _xParentalRequiredList:list):
		self._schema = _xSchema
		self._parent = _xParent
		self._name = _xName
		self._requiredList = _xParentalRequiredList
		self._definitionID = None					# if this is a definition, this variable holds the name of the definition
	#

	#
	# Returns `true` if this is a definition. `false` indicates this is a regular schema component.
	#
	def isDefinition(self) -> bool:
		return bool(self._definitionID)
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

	def __init__(self, _xParent, _xName:str, _xSchema:dict, _xParentalRequiredList:list):
		super().__init__(_xParent, _xName, _xSchema, _xParentalRequiredList)
	#

#



class IntegerGenerator(AbstractGenerator):

	def __init__(self, _xParent, _xName:str, _xSchema:dict, _xParentalRequiredList:list):
		super().__init__(_xParent, _xName, _xSchema, _xParentalRequiredList)
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

	def __init__(self, _xParent, _xName:str, _xSchema:dict, _xParentalRequiredList:list):
		super().__init__(_xParent, _xName, _xSchema, _xParentalRequiredList)
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

	def __init__(self, _xParent, _xName:str, _xSchema:dict, _xParentalRequiredList:list):
		super().__init__(_xParent, _xName, _xSchema, _xParentalRequiredList)
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

	def regexPatternVerbose(self, regexPattern:str):
		if regexPattern is None:
			if "enum" in self._schema:
				self._schema.remove("enum")
		else:
			regexPattern = compactVerboseRegEx(regexPattern)
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

	#
	# @param	AbtractGenerator[]			The generator or generators the list elements can be of
	#
	def __init__(self, _xParent, _xName:str, _xSchema:dict, _xParentalRequiredList:list, subGenList:list):
		super().__init__(_xParent, _xName, _xSchema, _xParentalRequiredList)

		assert isinstance(subGenList, (list, tuple))
		for subGen in subGenList:
			isinstance(subGen, AbstractGenerator)

		self.__subGenList = subGenList
	#

	@property
	def dataType(self) -> AbstractGenerator:
		if len(self.__subGenList) == 1:
			return self.__subGenList[0]
		else:
			raise Exception("There are multiple types defined!")
	#

	def minLength(self, minLength:int):
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

	def __init__(self, _xParent, _xName:str, _xSchema:dict, _xParentalRequiredList:list):
		super().__init__(_xParent, _xName, _xSchema, _xParentalRequiredList)
		if _xSchema is None:
			_xSchema = {
				"type": [ "object" ]
			}
		if not "properties" in _xSchema:
			_xSchema["properties"] = {}
		if not "required" in _xSchema:
			_xSchema["required"] = []
		self._schema = _xSchema
	#

	def objectValue(self, name:str, bRequired:bool = True):
		if bRequired:
			self._schema["required"].append(name)
		subSchema = {
			"type": [ "object" ]
		}
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

	#
	# A property should be of type "array".
	#
	# @param		str name							The name of the property.
	# @param		type|AbstractGenerator listType		The type of the property values. (All property values must be of exactly this single type specified here.)
	# @param		bool bRequired						This property is either optional or required.
	#
	def listValue(self, name:str, listType:typing.Union[type,AbstractGenerator], bRequired:bool = True) -> ListGenerator:
		if bRequired:
			self._schema["required"].append(name)

		# ----

		subTypeSchema, subGens = _compileListType(self, listType)

		# ----

		subSchema = {
			"type": [ "array" ],
			"items": subTypeSchema,
		}
		self._schema["properties"][name] = subSchema
		return ListGenerator(self, name, subSchema, self._schema["required"], subGens)
	#

#









_SUB_TYPE_CLASSES_BY_TYPE = {
	bool: (BooleanGenerator, "boolean"),
	int: (IntegerGenerator, "integer"),
	float: (FloatGenerator, "number"),
	str: (StringGenerator, "string"),
}

_SUB_TYPE_CLASSES_BY_STR = {
	"bool": (BooleanGenerator, "boolean"),
	"boolean": (BooleanGenerator, "boolean"),
	"int": (IntegerGenerator, "integer"),
	"integer": (IntegerGenerator, "integer"),
	"float": (FloatGenerator, "number"),
	"number": (FloatGenerator, "number"),
	"str": (StringGenerator, "string"),
	"string": (StringGenerator, "string"),
}




def _compileSingleType(parent, listType:typing.Union[type,str,"AbstractGenerator"]) -> tuple:
	if isinstance(listType, AbstractGenerator):
		if not listType.isDefinition:
			raise Exception("The specified list element type is not a definition!")

		subTypeSchema = dict(listType.schema)
		subGen = listType

	elif isinstance(listType, str):
		if listType in _SUB_TYPE_CLASSES_BY_STR:
			genClazz, jsType = _SUB_TYPE_CLASSES_BY_STR[listType]
			subTypeSchema = {
				"type": jsType
			}
			subGen = genClazz(parent, None, subTypeSchema, None)
		else:
			raise Exception("Invalid list element type specified: " + str(listType))

	elif _isType(listType):
		if listType in _SUB_TYPE_CLASSES_BY_TYPE:
			genClazz, jsType = _SUB_TYPE_CLASSES_BY_TYPE[listType]
			subTypeSchema = {
				"type": jsType
			}
			subGen = genClazz(parent, None, subTypeSchema, None)
		else:
			raise Exception("Invalid list element type specified: " + str(listType))

	else:
		raise Exception("Invalid list element type specified: " + str(listType))

	return subTypeSchema, subGen
#

def _compileListType(parent, listType:typing.Union[type,"AbstractGenerator"]) -> tuple:
	subTypeSchema, subGen = _compileSingleType(parent, listType)
	return subTypeSchema, [ subGen ]
#











class _Generator(object):

	def __init__(self):
		self.__schema = None
		self.__rng = random.Random()
		self.__defs = {}
	#

	def __generateID(self, existingIDs):
		CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

		while True:
			randID = "".join([ self.__rng.choice(CHARS) for i in range(0, 8) ])
			if randID not in existingIDs:
				return randID
	#

	def __str__(self):
		return jk_json.dumps(self.__schema)
	#

	def __repr__(self):
		return jk_json.dumps(self.__schema)
	#

	def objectValue(self) -> ObjectGenerator:
		if self.__schema is not None:
			raise Exception("This generator already provides a schema!")

		# ----

		ret = ObjectGenerator(None, None, None, None)
		self.__schema = ret._schema
		self.__schema["$schema"] = "http://json-schema.org/draft-04/schema#"
		return ret
	#

	#
	# A property should be of type "array".
	#
	# @param		str name							The name of the property.
	# @param		type|AbstractGenerator listType		The type of the property values. (All property values must be of exactly this single type specified here.)
	# @param		bool bRequired						This property is either optional or required.
	#
	def listValue(self, listType:typing.Union[type,AbstractGenerator], bRequired:bool = True) -> ListGenerator:
		if self.__schema is not None:
			raise Exception("This generator already provides a schema!")

		# ----

		subTypeSchema, subGens = _compileListType(self, listType)

		# ----

		subSchema = {
			"type": [ "array" ],
			"items": subTypeSchema,
		}
		ret = ListGenerator(self, None, subSchema, None, subGens)
		self.__schema = ret._schema
		self.__schema["$schema"] = "http://json-schema.org/draft-04/schema#"
		return ret
	#

	@property
	def schema(self):
		ret = dict(self.__schema)
		return ret
	#

	def __enter__(self):
		return self
	#

	def __exit__(self, etype, value, traceback):
		return False
	#

	#
	# Invoke this method to define an object schema that can be used as a component in other definitions later.
	#
	def defineObject(self, name:str = None) -> ObjectGenerator:
		if name is None:
			name = self.__generateID(list(self.__defs.keys()))
		else:
			assert isinstance(name, str)
			assert re.match("^[a-zA-Z]+$", name)
			assert name not in self.__defs

		ret = ObjectGenerator(None, None, None, None)
		ret._definitionID = name
		self.__defs[name] = ret
		return ret
	#

#











def createObjectSchemaGenerator() -> ObjectGenerator:
	return ObjectGenerator(None, None, None, None)
#

def createSchemaGenerator():
	return _Generator()
#






