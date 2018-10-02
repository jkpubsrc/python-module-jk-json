#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import re
from typing import List, Union

import jk_logging
from jk_testing import Assert
from jk_json.tools import *

from ._SchemaAST import _SchemaAST




# ================================================================================================================================
# ================================================================================================================================
# ================================================================================================================================



class ValidatorStackTrace(list):

	def __init__(self, errPath:str, errValue, errMsg:str):
		assert isinstance(errPath, str)
		assert isinstance(errMsg, str)
		self.append((errPath, errValue, errMsg))
	#

	def appendError(self, errPath:str, errValue, errMsg:str):
		assert isinstance(errPath, str)
		assert isinstance(errMsg, str)
		self.append((errPath, errValue, errMsg))
		return self
	#

#



# ================================================================================================================================
# ================================================================================================================================
# ================================================================================================================================



class ValidationContext(object):

	def __init__(self):
		self.allProperties = None
	#

	def derive(self):
		return ValidationContext()
	#

#



class ValidationContext2(object):

	def __init__(self, path:str = "/"):
		self.allProperties = None
		self.__path = path
	#

	@property
	def path(self):
		if self.__path == "/":
			return "/"
		else:
			return self.__path[:-1]
	#

	def deriveOnIndex(self, index:int):
		p = self.__path + str(index) + "/"
		return ValidationContext2(p)
	#

	def deriveOnPropertyName(self, propertyName:str):
		p = self.__path + propertyName + "/"
		return ValidationContext2(p)
	#

#



class AbstractElementaryValidator(object):

	def validate(self, ctx:ValidationContext, jsonData):
		raise NotImplementedError()
	#

	def validate2(self, ctx:ValidationContext2, jsonData):
		raise NotImplementedError()
	#

	def dump(self, prefix = "", writeFunction = print):
		raise NotImplementedError()
	#

#



# ================================================================================================================================
# ================================================================================================================================
# ================================================================================================================================



class _TypeSpecificValidator(AbstractElementaryValidator):

	def __init__(self, typeID):
		self.__typeID = typeID
		self._validators = []
		self._default = True
	#

	def validate(self, ctx:ValidationContext, jsonData):
		for v in self._validators:
			if not v.validate(ctx, jsonData):
				return False
		return self._default
	#

	def validate2(self, ctx:ValidationContext2, jsonData):
		for v in self._validators:
			retSuccess, retStackTrace = v.validate2(ctx, jsonData)
			if not retSuccess:
				return False, retStackTrace.appendError(ctx.path, None, "failed for type: " + ALL_TYPES_NAME_LIST[self.__typeID])

		if self._default:
			return True, None
		else:
			return False, ValidatorStackTrace(ctx.path, None, "default is: to fail (a)")
	#

	def dump(self, prefix = "", writeFunction = print):
		writeFunction(prefix + "TypeSpecificValidator[" + ALL_TYPES_NAME_LIST[self.__typeID] + "]:")
		prefix += "\t"
		for v in self._validators:
			v.dump(prefix, writeFunction)
		writeFunction(prefix + "default: " + str(self._default).lower())
	#

#



class _Validator(AbstractElementaryValidator):

	def __init__(self):
		self._validators = {}
		for typeID in ALL_TYPES_SET:
			self._validators[typeID] = _TypeSpecificValidator(typeID)
		self._any = []
		self._default = True
	#

	def validate(self, ctx:ValidationContext, jsonData):
		t = getTypeIDOfValue(jsonData)
		if not self._validators[t].validate(ctx, jsonData):
			return False
		for v in self._any:
			if not v.validate(ctx, jsonData):
				return False
		return self._default
	#

	def validate2(self, ctx:ValidationContext2, jsonData):
		t = getTypeIDOfValue(jsonData)

		retSuccess, retStackTrace = self._validators[t].validate2(ctx, jsonData)
		if not retSuccess:
			return False, retStackTrace.appendError(ctx.path, None, "failed in category for type: " + ALL_TYPES_NAME_LIST[t])

		for v in self._any:
			retSuccess, retStackTrace = v.validate2(ctx, jsonData)
			if not retSuccess:
				return False, retStackTrace.appendError(ctx.path, None, "failed in category for all types")

		if self._default:
			return True, None
		else:
			return False, ValidatorStackTrace(ctx.path, None, "default is: to fail (b)")
	#

	def dump(self, prefix = "", writeFunction = print):
		writeFunction(prefix + "Validator:")
		prefix += "\t"
		for v in self._validators.values():
			v.dump(prefix, writeFunction)
		writeFunction(prefix + "any:")
		prefix2 = prefix + "\t"
		for a in self._any:
			a.dump(prefix2, writeFunction)
		writeFunction(prefix + "default: " + str(self._default).lower())
	#

#



# ================================================================================================================================
# ================================================================================================================================
# ================================================================================================================================



class Validator(object):

	def __init__(self, validator:_Validator):
		self.__validator = validator
	#

	#
	# Validate the specified JSON data.
	#
	# @return	bool bValidationResult		Returns `True` or `False`.
	#
	def validate(self, jsonData):
		return self.__validator.validate(ValidationContext(), jsonData)
	#

	#
	# Validate the specified JSON data.
	#
	# @return	bool bValidationResult				Returns `True` or `False`.
	# @return	ValidatorStackTrace stackTrace		If validation failed returns a stack trace object. Otherwise `None` is returned.
	#
	def validate2(self, jsonData):
		return self.__validator.validate2(ValidationContext2(), jsonData)
	#

	#
	# Validate the specified JSON data. An exception is thrown on error.
	#
	def validateE(self, jsonData):
		bResult, errStackTrace = self.__validator.validate2(ValidationContext2(), jsonData)
		if not bResult:
			v = errStackTrace[0][1]
			if v is None:
				msg = errStackTrace[0][2]
				if msg[0].islower():
					msg = msg[0].upper() + msg[1:]
			else:
				msg = errStackTrace[0][2]
				#msg = str(v) + " " + msg
			raise Exception("JSON VALIDATION ERROR! " + msg)
	#

	def dump(self, writeFunction = print):
		self.__validator.dump("", writeFunction)
	#

#



# ================================================================================================================================
# ================================================================================================================================
# ================================================================================================================================



class _validate_any_anyOfTheseValues(AbstractElementaryValidator):

	def __init__(self, log, allowedValues:list):
		Assert.isInstance(allowedValues, list, log=log)

		self.__allowedValues = allowedValues
	#

	def validate(self, ctx:ValidationContext, jsonData):
		for v in self.__allowedValues:
			if jsonIsEqual(jsonData, v):
				return True
		return False
	#

	def validate2(self, ctx:ValidationContext2, jsonData):
		for v in self.__allowedValues:
			if jsonIsEqual(jsonData, v):
				return True, None
		return False, ValidatorStackTrace(ctx.path, jsonData, "not found in: " + repr(self.__allowedValues))
	#

	def dump(self, prefix = "", writeFunction = print):
		writeFunction(prefix + self.__class__.__name__ + ": " + repr(self.__allowedValues))
	#

#

class _validate_any_exactValue(AbstractElementaryValidator):

	def __init__(self, log, referenceValue):
		self.__referenceValue = referenceValue
	#

	def validate(self, ctx:ValidationContext, jsonData):
		return jsonIsEqual(jsonData, self.__referenceValue)
	#

	def validate2(self, ctx:ValidationContext2, jsonData):
		if jsonIsEqual(jsonData, self.__referenceValue):
			return True, None
		else:
			return False, ValidatorStackTrace(ctx.path, jsonData, "not equal to: " + repr(self.__referenceValue))
	#

	def dump(self, prefix = "", writeFunction = print):
		writeFunction(prefix + self.__class__.__name__ + ": " + repr(self.__referenceValue))
	#

#

# Check the value is a multiple of the argument value.
# int|float
class _validate_number_multipleValueOf(AbstractElementaryValidator):

	def __init__(self, log, referenceValue:Union[int,float]):
		Assert.isInstance(referenceValue, (int, float), log=log)

		self.__referenceValue = referenceValue
	#

	def validate(self, ctx:ValidationContext, jsonData):
		return (jsonData % self.__referenceValue) == 0
	#

	def validate2(self, ctx:ValidationContext2, jsonData):
		r = jsonData % self.__referenceValue
		if r == 0:
			return True, None
		else:
			return False, ValidatorStackTrace(ctx.path, jsonData, "not divisible by " + repr(self.__referenceValue) + ": "	\
				+ repr(jsonData) + " % " + repr(self.__referenceValue) + " == " + repr(r))
	#

	def dump(self, prefix = "", writeFunction = print):
		writeFunction(prefix + self.__class__.__name__ + ": " + repr(self.__referenceValue))
	#

#

# Check the value against an upper bound.
# int|float
class _validate_number_maximum(AbstractElementaryValidator):

	def __init__(self, log, referenceValue:Union[int,float]):
		Assert.isInstance(referenceValue, (int, float), log=log)

		self.__referenceValue = referenceValue
	#

	def validate(self, ctx:ValidationContext, jsonData):
		return jsonData <= self.__referenceValue
	#

	def validate2(self, ctx:ValidationContext2, jsonData):
		if jsonData <= self.__referenceValue:
			return True, None
		else:
			return False, ValidatorStackTrace(ctx.path, jsonData, "larger than: " + repr(self.__referenceValue))
	#

	def dump(self, prefix = "", writeFunction = print):
		writeFunction(prefix + self.__class__.__name__ + ": " + repr(self.__referenceValue))
	#

#

# Check the value against an lower bound.
# int|float
class _validate_number_minimum(AbstractElementaryValidator):

	def __init__(self, log, referenceValue:Union[int,float]):
		Assert.isInstance(referenceValue, (int, float), log=log)

		self.__referenceValue = referenceValue
	#

	def validate(self, ctx:ValidationContext, jsonData):
		return jsonData >= self.__referenceValue
	#

	def validate2(self, ctx:ValidationContext2, jsonData):
		if jsonData >= self.__referenceValue:
			return True, None
		else:
			return False, ValidatorStackTrace(ctx.path, jsonData, "smaller than: " + repr(self.__referenceValue))
	#

	def dump(self, prefix = "", writeFunction = print):
		writeFunction(prefix + self.__class__.__name__ + ": " + repr(self.__referenceValue))
	#

#

# Check the value against an upper bound.
# int|float
class _validate_number_exclusiveMaximum(AbstractElementaryValidator):

	def __init__(self, log, referenceValue:Union[int,float]):
		Assert.isInstance(referenceValue, (int, float), log=log)

		self.__referenceValue = referenceValue
	#

	def validate(self, ctx:ValidationContext, jsonData):
		return jsonData < self.__referenceValue
	#

	def validate2(self, ctx:ValidationContext2, jsonData):
		if jsonData < self.__referenceValue:
			return True, None
		else:
			return False, ValidatorStackTrace(ctx.path, jsonData, "larger than or equal to: " + repr(self.__referenceValue))
	#

	def dump(self, prefix = "", writeFunction = print):
		writeFunction(prefix + self.__class__.__name__ + ": " + repr(self.__referenceValue))
	#

#

# Check the value against an lower bound.
# int|float
class _validate_number_exclusiveMinimum(AbstractElementaryValidator):

	def __init__(self, log, referenceValue:Union[int,float]):
		Assert.isInstance(referenceValue, (int, float), log=log)

		self.__referenceValue = referenceValue
	#

	def validate(self, ctx:ValidationContext, jsonData):
		return jsonData > self.__referenceValue
	#

	def validate2(self, ctx:ValidationContext2, jsonData):
		if jsonData > self.__referenceValue:
			return True, None
		else:
			return False, ValidatorStackTrace(ctx.path, jsonData, "smaller than or equal to: " + repr(self.__referenceValue))
	#

	def dump(self, prefix = "", writeFunction = print):
		writeFunction(prefix + self.__class__.__name__ + ": " + repr(self.__referenceValue))
	#

#

# Check the size of the python value against a lower bound.
# int
class _validate_item_minLength(AbstractElementaryValidator):

	def __init__(self, log, referenceValue:int):
		Assert.isInstance(referenceValue, int, log=log)

		self.__referenceValue = referenceValue
	#

	def validate(self, ctx:ValidationContext, jsonData):
		return len(jsonData) >= self.__referenceValue
	#

	def validate2(self, ctx:ValidationContext2, jsonData):
		if len(jsonData) >= self.__referenceValue:
			return True, None
		else:
			return False, ValidatorStackTrace(ctx.path, jsonData, "length/size is " + str(len(jsonData)) + " and therefore smaller than: " + str(self.__referenceValue))
	#

	def dump(self, prefix = "", writeFunction = print):
		writeFunction(prefix + self.__class__.__name__ + ": " + repr(self.__referenceValue))
	#

#

# Check the size of the python value against an upper bound.
# int
class _validate_item_maxLength(AbstractElementaryValidator):

	def __init__(self, log, referenceValue:int):
		Assert.isInstance(referenceValue, int, log=log)

		self.__referenceValue = referenceValue
	#

	def validate(self, ctx:ValidationContext, jsonData):
		return len(jsonData) <= self.__referenceValue
	#

	def validate2(self, ctx:ValidationContext2, jsonData):
		if len(jsonData) <= self.__referenceValue:
			return True, None
		else:
			return False, ValidatorStackTrace(ctx.path, jsonData, "length/size is " + str(len(jsonData)) + " and therefore greater than: " + str(self.__referenceValue))
	#

	def dump(self, prefix = "", writeFunction = print):
		writeFunction(prefix + self.__class__.__name__ + ": " + repr(self.__referenceValue))
	#

#

class _validate_item_mustBeNoneOrEmpty(AbstractElementaryValidator):

	def __init__(self, log):
		pass
	#

	def validate(self, ctx:ValidationContext, jsonData):
		return (jsonData is None) or (len(jsonData) == 0)
	#

	def validate2(self, ctx:ValidationContext2, jsonData):
		if (jsonData is None) or (len(jsonData) == 0):
			return True, None
		else:
			return False, ValidatorStackTrace(ctx.path, jsonData, "there is data")
	#

	def dump(self, prefix = "", writeFunction = print):
		writeFunction(prefix + self.__class__.__name__)
	#

#

class _validate_item_mustNotBeNoneNorEmpty(AbstractElementaryValidator):

	def __init__(self, log):
		pass
	#

	def validate(self, ctx:ValidationContext, jsonData):
		return (jsonData != None) and (len(jsonData) > 0)
	#

	def validate2(self, ctx:ValidationContext2, jsonData):
		if (jsonData != None) and (len(jsonData) > 0):
			return True, None
		else:
			return False, ValidatorStackTrace(ctx.path, jsonData, "there is no data")
	#

	def dump(self, prefix = "", writeFunction = print):
		writeFunction(prefix + self.__class__.__name__)
	#

#

class _validate_item_mustNotBeNone(AbstractElementaryValidator):

	def __init__(self, log):
		pass
	#

	def validate(self, ctx:ValidationContext, jsonData):
		return jsonData != None
	#

	def validate2(self, ctx:ValidationContext2, jsonData):
		if jsonData != None:
			return True, None
		else:
			return False, ValidatorStackTrace(ctx.path, jsonData, "there is no data")
	#

	def dump(self, prefix = "", writeFunction = print):
		writeFunction(prefix + self.__class__.__name__)
	#

#

# Check the string against the argument pattern.
# string_pattern
class _validate_string_pattern(AbstractElementaryValidator):

	def __init__(self, log, referencePatternStr:str):
		Assert.isInstance(referencePatternStr, str, log=log)

		self.__referencePatternStr = referencePatternStr
		self.__referencePattern = re.compile(referencePatternStr)
	#

	def validate(self, ctx:ValidationContext, jsonData):
		return self.__referencePattern.search(jsonData) != None
	#

	def validate2(self, ctx:ValidationContext2, jsonData):
		if self.__referencePattern.search(jsonData) != None:
			return True, None
		else:
			return False, ValidatorStackTrace(ctx.path, jsonData, "does not match pattern: " + repr(self.__referencePatternStr))
	#

	def dump(self, prefix = "", writeFunction = print):
		writeFunction(prefix + self.__class__.__name__ + ": " + repr(self.__referencePatternStr))
	#

#

# Check if all array elements match against the specified validator.
# AbstractElementaryValidator
class _validate_array_checkIfAllItemsMatchValidator(AbstractElementaryValidator):

	def __init__(self, log, validator:AbstractElementaryValidator):
		Assert.isInstance(validator, AbstractElementaryValidator, log=log)

		self.__validator = validator
	#

	def validate(self, ctx:ValidationContext, jsonData):
		for item in jsonData:
			ctx2 = ctx.derive()
			if not self.__validator.validate(ctx2, item):
				return False
		return True
	#

	def validate2(self, ctx:ValidationContext2, jsonData):
		i = 0
		for item in jsonData:
			ctx2 = ctx.deriveOnIndex(i)
			retSuccess, retStackTrace = self.__validator.validate2(ctx2, item)
			if not retSuccess:
				return False, retStackTrace.appendError(ctx.path, None, "an item does not validate")
			i += 1
		return True, None
	#

	def dump(self, prefix = "", writeFunction = print):
		writeFunction(prefix + self.__class__.__name__ + ":")
		writeFunction(prefix + "\tvalidator:")
		self.__validator.dump(prefix + "\t\t", writeFunction)
	#

#

# Check if at least one array elements matches against the specified validator.
# AbstractElementaryValidator
class _validate_array_checkIfAnyItemMatchesValidator(AbstractElementaryValidator):

	def __init__(self, log, validator:AbstractElementaryValidator):
		Assert.isInstance(validator, AbstractElementaryValidator, log=log)

		self.__validator = validator
	#

	def validate(self, ctx:ValidationContext, jsonData):
		for item in jsonData:
			ctx2 = ctx.derive()
			if self.__validator.validate(ctx2, item):
				return True
		return False
	#

	def validate2(self, ctx:ValidationContext2, jsonData):
		i = 0
		for item in jsonData:
			ctx2 = ctx.deriveOnIndex(i)
			retSuccess, retStackTrace = self.__validator.validate2(ctx2, item)
			if retSuccess:
				return True, None
			i += 1
		return False, retStackTrace.appendError(ctx.path, None, "no item validates")
	#

	def dump(self, prefix = "", writeFunction = print):
		writeFunction(prefix + self.__class__.__name__ + ":")
		writeFunction(prefix + "\tvalidator:")
		self.__validator.dump(prefix + "\t\t", writeFunction)
	#

#

# Check if all array elements match against the specified list of validators.
# AbstractElementaryValidator[]
class _validate_array_checkAllItemsMatchListOfValidators(AbstractElementaryValidator):

	def __init__(self, log, validators:List[AbstractElementaryValidator]):
		Assert.isInstance(validators, list, log=log)
		for validator in validators:
			Assert.isInstance(validator, AbstractElementaryValidator, log=log)

		self.__validators = validators
		self.__count = len(validators)
	#

	def validate(self, ctx:ValidationContext, jsonData):
		#if len(jsonData) != self.__count:
		#	return False

		for jsonItem, validator in zip(jsonData, self.__validators):
			ctx2 = ctx.derive()
			if not validator.validate(ctx2, jsonItem):
				return False
		return True
	#

	def validate2(self, ctx:ValidationContext2, jsonData):
		#if len(jsonData) != self.__count:
		#	return False, ValidatorStackTrace(ctx.path, jsonData, str(self.__count) + " items expected, " + str(len(jsonData)) + " found")

		i = 0
		for jsonItem, validator in zip(jsonData, self.__validators):
			ctx2 = ctx.deriveOnIndex(i)
			retSuccess, retStackTrace = validator.validate2(ctx2, jsonItem)
			if not retSuccess:
				return False, retStackTrace.appendError(ctx.path, None, "validator at index " + str(i) + " failed.")
			i += 1
		return True, None
	#

	def dump(self, prefix = "", writeFunction = print):
		writeFunction(prefix + self.__class__.__name__ + ":")
		writeFunction(prefix + "\tvalidators:")
		for v in self.__validators:
			v.dump(prefix + "\t\t", writeFunction)
	#

#

# Check if all array elements match against the specified list of validators.
# AbstractElementaryValidator[], AbstractElementaryValidator
class _validate_array_checkAllItemsMatchListOfValidatorsWithExtraValidator(AbstractElementaryValidator):

	def __init__(self, log, validators:List[AbstractElementaryValidator], extraValidator:AbstractElementaryValidator):
		Assert.isInstance(validators, list, log=log)
		for validator in validators:
			Assert.isInstance(validator, AbstractElementaryValidator, log=log)
		Assert.isInstance(extraValidator, AbstractElementaryValidator, log=log)

		self.__validators = validators
		self.__extraValidator = extraValidator
		self.__count = len(validators)
	#

	def validate(self, ctx:ValidationContext, jsonData):
		if len(jsonData) < self.__count:
			return False
		extraJsonData = jsonData[self.__count:]
		jsonData = jsonData[0:self.__count]

		for jsonItem, validator in zip(jsonData, self.__validators):
			ctx2 = ctx.derive()
			if not validator.validate(ctx2, jsonItem):
				return False

		for jsonItem in extraJsonData:
			ctx2 = ctx.derive()
			if not self.__extraValidator.validate(ctx2, jsonItem):
				return False

		return True
	#

	def validate2(self, ctx:ValidationContext2, jsonData):
		#if len(jsonData) < self.__count:
		#	return False, ValidatorStackTrace(ctx.path, jsonData, "at least " + str(self.__count) + " items expected, " + str(len(jsonData)) + " found")

		extraJsonData = jsonData[self.__count:]
		jsonData = jsonData[0:self.__count]

		i = 0
		for jsonItem, validator in zip(jsonData, self.__validators):
			ctx2 = ctx.deriveOnIndex(i)
			retSuccess, retStackTrace = validator.validate2(ctx2, jsonItem)
			if not retSuccess:
				return False, retStackTrace.appendError(ctx.path, None, "validator failed at index " + str(i))
			i += 1

		for jsonItem in extraJsonData:
			ctx2 = ctx.deriveOnIndex(i)
			retSuccess, retStackTrace = self.__extraValidator.validate2(ctx2, jsonItem)
			if not retSuccess:
				return False, retStackTrace.appendError(ctx.path, None, "extra validator failed at index " + str(i))
			i += 1

		return True, None
	#

	def dump(self, prefix = "", writeFunction = print):
		writeFunction(prefix + self.__class__.__name__ + ":")
		writeFunction(prefix + "\tvalidators:")
		for v in self.__validators:
			v.dump(prefix + "\t\t", writeFunction)
		writeFunction(prefix + "\textraValidator:")
		self.__extraValidator.dump(prefix + "\t\t", writeFunction)
	#

#

# Check if all array elements match against the specified list of validators.
# AbstractElementaryValidator[], AbstractElementaryValidator[]
class _validate_array_checkAllItemsMatchListOfValidatorsWithExtraListOfValidators(AbstractElementaryValidator):

	def __init__(self, log, validators:List[AbstractElementaryValidator], extraValidators:List[AbstractElementaryValidator]):
		Assert.isInstance(validators, list, log=log)
		for validator in validators:
			Assert.isInstance(validator, AbstractElementaryValidator, log=log)
		Assert.isInstance(extraValidators, list, log=log)
		for validator in extraValidators:
			Assert.isInstance(validator, AbstractElementaryValidator, log=log)

		self.__validators = validators
		self.__extraValidators = extraValidators
		self.__count = len(validators)
		self.__extraCount = len(self.__extraValidators)
	#

	def validate(self, ctx:ValidationContext, jsonData):
		if len(jsonData) < self.__count:
			return False
		extraJsonData = jsonData[self.__count:]
		jsonData = jsonData[0:self.__count]

		if len(extraJsonData) < self.__extraCount:
			return False

		for jsonItem, validator in zip(jsonData, self.__validators):
			ctx2 = ctx.derive()
			if not validator.validate(ctx2, jsonItem):
				return False

		for jsonItem, validator in zip(extraJsonData, self.__extraValidators):
			ctx2 = ctx.derive()
			if not validator.validate(ctx2, jsonItem):
				return False

		return True
	#

	def validate2(self, ctx:ValidationContext2, jsonData):
		#if len(jsonData) < self.__count:
		#	return False, ValidatorStackTrace(ctx.path, jsonData, "at least " + str(self.__count) + " items expected, " + str(len(jsonData)) + " found")

		extraJsonData = jsonData[self.__count:]
		jsonData = jsonData[0:self.__count]

		i = 0
		for jsonItem, validator in zip(jsonData, self.__validators):
			ctx2 = ctx.deriveOnIndex(i)
			retSuccess, retStackTrace = validator.validate2(ctx2, jsonItem)
			if not retSuccess:
				return False, retStackTrace.appendError(ctx.path, None, "validator failed at index " + str(i))
			i += 1

		for jsonItem, validator in zip(extraJsonData, self.__extraValidators):
			ctx2 = ctx.deriveOnIndex(i)
			retSuccess, retStackTrace = validator.validate2(ctx2, jsonItem)
			if not retSuccess:
				return False, retStackTrace.appendError(ctx.path, None, "extra validator failed at index " + str(i))
			i += 1

		return True, None
	#

	def dump(self, prefix = "", writeFunction = print):
		writeFunction(prefix + self.__class__.__name__ + ":")
		writeFunction(prefix + "\tvalidators:")
		for v in self.__validators:
			v.dump(prefix + "\t\t", writeFunction)
		writeFunction(prefix + "\textraValidators:")
		for v in self.__extraValidators:
			v.dump(prefix + "\t\t", writeFunction)
	#

#

# Check if no array element is equal to another array element.
class _validate_array_itemsMustBeUnique(AbstractElementaryValidator):

	def __init__(self, log):
		pass
	#

	def validate(self, ctx:ValidationContext, jsonData):
		n = len(jsonData)
		if n < 2:
			return True
		for i in range(0, n - 1):
			v1 = jsonData[i]
			t1 = getTypeIDOfValue(v1)
			for j in range(i + 1, n):
				v2 = jsonData[j]
				t2 = getTypeIDOfValue(v2)
				if t1 != t2:
					continue
				if jsonIsEqual(v1, v2):
					return False
		return True
	#

	def validate2(self, ctx:ValidationContext2, jsonData):
		n = len(jsonData)
		if n < 2:
			return True, None
		for i in range(0, n - 1):
			v1 = jsonData[i]
			t1 = getTypeIDOfValue(v1)
			for j in range(i + 1, n):
				v2 = jsonData[j]
				t2 = getTypeIDOfValue(v2)
				if t1 != t2:
					continue
				if jsonIsEqual(v1, v2):
					return False, ValidatorStackTrace(ctx.path, jsonData, "item at " + int(i) + " and " + int(j) + " are equal")
		return True, None
	#

	def dump(self, prefix = "", writeFunction = print):
		writeFunction(prefix + self.__class__.__name__)
	#

#

# Check if at least one array element matches the reference.
# (any)
class _validate_array_mustContainExactValue(AbstractElementaryValidator):

	def __init__(self, log, referenceValue):
		self.__referenceValue = referenceValue
	#

	def validate(self, ctx:ValidationContext, jsonData):
		for v in jsonData:
			if jsonIsEqual(v, self.__referenceValue):
				return True
		return False
	#

	def validate2(self, ctx:ValidationContext2, jsonData):
		for v in jsonData:
			if jsonIsEqual(v, self.__referenceValue):
				return True, None
		return False, ValidatorStackTrace(ctx.path, jsonData, "no such item: " + repr(self.__referenceValue))
	#

	def dump(self, prefix = "", writeFunction = print):
		writeFunction(prefix + self.__class__.__name__ + ": " + repr(self.__referenceValue))
	#

#

# AbstractElementaryValidator
class _validate_not(AbstractElementaryValidator):

	def __init__(self, log, validator:AbstractElementaryValidator):
		Assert.isInstance(validator, AbstractElementaryValidator, log=log)

		self.__validator = validator
	#

	def validate(self, ctx:ValidationContext, jsonData):
		return not self.__validator.validate(ctx, jsonData)
	#

	def validate2(self, ctx:ValidationContext2, jsonData):
		if not self.__validator.validate(ctx, jsonData):
			return True, None
		else:
			return False, ValidatorStackTrace(ctx.path, jsonData, "validator validated successfully")
	#

	def dump(self, prefix = "", writeFunction = print):
		writeFunction(prefix + self.__class__.__name__ + ":")
		writeFunction(prefix + "\tvalidator:")
		self.__validator.dump(prefix + "\t\t", writeFunction)
	#

#

# AbstractElementaryValidator, AbstractElementaryValidator, AbstractElementaryValidator
class _validate_if(AbstractElementaryValidator):

	def __init__(self, log, validatorIf:AbstractElementaryValidator, validatorThen:AbstractElementaryValidator, validatorElse:AbstractElementaryValidator):
		Assert.isInstance(validatorIf, AbstractElementaryValidator, log=log)
		if validatorThen:
			Assert.isInstance(validatorThen, AbstractElementaryValidator, log=log)
		if validatorElse:
			Assert.isInstance(validatorElse, AbstractElementaryValidator, log=log)

		self.__validatorIf = validatorIf
		self.__validatorThen = validatorThen
		self.__validatorElse = validatorElse
	#

	def validate(self, ctx:ValidationContext, jsonData):
		if self.__validatorIf.validate(ctx, jsonData):
			if self.__validatorThen:
				return self.__validatorThen.validate(ctx, jsonData)
			else:
				return True
		else:
			if self.__validatorElse:
				return self.__validatorElse.validate(ctx, jsonData)
			else:
				return True
	#

	def validate2(self, ctx:ValidationContext2, jsonData):
		if self.__validatorIf.validate(ctx, jsonData):
			if self.__validatorThen:
				retSuccess, retStackTrace = self.__validatorThen.validate(ctx, jsonData)
				if retSuccess:
					return True, None
				else:
					return False, retStackTrace.appendError(ctx.path, None, "then-validator failed.")
			else:
				return True
		else:
			if self.__validatorElse:
				retSuccess, retStackTrace = self.__validatorElse.validate(ctx, jsonData)
				if retSuccess:
					return True, None
				else:
					return False, retStackTrace.appendError(ctx.path, None, "else-validator failed.")
			else:
				return True
	#

	def dump(self, prefix = "", writeFunction = print):
		writeFunction(prefix + self.__class__.__name__ + ":")
		writeFunction(prefix + "\tvalidatorIF:")
		self.__validatorIf.dump(prefix + "\t\t", writeFunction)
		if self.__validatorThen:
			writeFunction(prefix + "\tvalidatorTHEN:")
			self.__validatorThen.dump(prefix + "\t\t", writeFunction)
		if self.__validatorElse:
			writeFunction(prefix + "\tvalidatorELSE:")
			self.__validatorElse.dump(prefix + "\t\t", writeFunction)
	#

#

# Check if all validators evaluate to true
# AbstractElementaryValidator[]
class _validate_allOf(AbstractElementaryValidator):

	def __init__(self, log, validators:List[AbstractElementaryValidator]):
		Assert.isInstance(validators, list, log=log)
		for validator in validators:
			Assert.isInstance(validator, AbstractElementaryValidator, log=log)

		self.__validators = validators
	#

	def validate(self, ctx:ValidationContext, jsonData):
		for v in self.__validators:
			if not v.validate(ctx, jsonData):
				return False
		return True
	#

	def validate2(self, ctx:ValidationContext2, jsonData):
		for v in self.__validators:
			retSuccess, retStackTrace = v.validate2(ctx, jsonData)
			if not retSuccess:
				return False, retStackTrace.appendError(ctx.path, None, "validator failed")
		return True, None
	#

	def dump(self, prefix = "", writeFunction = print):
		writeFunction(prefix + self.__class__.__name__ + ":")
		writeFunction(prefix + "\tvalidators:")
		for v in self.__validators:
			v.dump(prefix + "\t\t", writeFunction)
	#

#

# Check if at least one validator evaluates to true
# AbstractElementValidator[]
class _validate_anyOf(AbstractElementaryValidator):

	def __init__(self, log, validators:List[AbstractElementaryValidator]):
		Assert.isInstance(validators, list, log=log)
		for validator in validators:
			Assert.isInstance(validator, AbstractElementaryValidator, log=log)

		self.__validators = validators
	#

	def validate(self, ctx:ValidationContext, jsonData):
		for v in self.__validators:
			if v.validate(ctx, jsonData):
				return True
		return False
	#

	def validate2(self, ctx:ValidationContext2, jsonData):
		for v in self.__validators:
			retSuccess, retStackTrace = v.validate2(ctx, jsonData)
			if retSuccess:
				return True, None
		return False, retStackTrace.appendError(ctx.path, None, "no validator succeeded")
	#

	def dump(self, prefix = "", writeFunction = print):
		writeFunction(prefix + self.__class__.__name__ + ":")
		writeFunction(prefix + "\tvalidators:")
		for v in self.__validators:
			v.dump(prefix + "\t\t", writeFunction)
	#

#

# Check if exactly one validator evaluates to true
# AbstractElementValidator[]
class _validate_oneOf(AbstractElementaryValidator):

	def __init__(self, log, validators:List[AbstractElementaryValidator]):
		Assert.isInstance(validators, list, log=log)
		for validator in validators:
			Assert.isInstance(validator, AbstractElementaryValidator, log=log)

		self.__validators = validators
	#

	def validate(self, ctx:ValidationContext, jsonData):
		n = 0
		for v in self.__validators:
			if v.validate(ctx, jsonData):
				if n == 0:
					n += 1
				else:
					return False
		return n == 1
	#

	def validate2(self, ctx:ValidationContext2, jsonData):
		n = 0
		for v in self.__validators:
			if v.validate(ctx, jsonData):
				if n == 0:
					n += 1
				else:
					return False, ValidatorStackTrace(ctx.path, jsonData, "another validator already succeeded")
		if n == 1:
			return True, None
		else:
			return False, ValidatorStackTrace(ctx.path, jsonData, "no validator succeeded")
	#

	def dump(self, prefix = "", writeFunction = print):
		writeFunction(prefix + self.__class__.__name__ + ":")
		writeFunction(prefix + "\tvalidators:")
		for v in self.__validators:
			v.dump(prefix + "\t\t", writeFunction)
	#

#

# Check if all property names match against the specified validator.
# AbstractElementaryValidator
class _validate_object_allPropertyNamesMatchValidator(AbstractElementaryValidator):

	def __init__(self, log, validator:AbstractElementaryValidator):
		Assert.isInstance(validator, AbstractElementaryValidator, log=log)

		self.__validator = validator
	#

	def validate(self, ctx:ValidationContext, jsonData):
		for propertyName in jsonData.keys():
			if not self.__validator.validate(ctx, propertyName):
				return False
		return True
	#

	def validate2(self, ctx:ValidationContext2, jsonData):
		for propertyName in jsonData.keys():
			retSuccess, retStackTrace = self.__validator.validate2(ctx, propertyName)
			if not retSuccess:
				return False, retStackTrace.appendError(ctx.path, propertyName, "property name failed to validate")
		return True, None
	#

	def dump(self, prefix = "", writeFunction = print):
		writeFunction(prefix + self.__class__.__name__ + ":")
		writeFunction(prefix + "\tvalidator:")
		self.__validator.dump(prefix + "\t\t", writeFunction)
	#

#

class _validate_object_otherPropertyMustExist(AbstractElementaryValidator):

	def __init__(self, log, propertyNameToExpectedPropertyNamesMap:dict):
		Assert.isInstance(propertyNameToExpectedPropertyNamesMap, dict, log=log)
		for key, value in propertyNameToExpectedPropertyNamesMap.items():
			Assert.isInstance(key, str, log=log)
			Assert.isInstance(value, list, log=log)
			for item in value:
				Assert.isInstance(item, str, log=log)

		self.__propertyNameToExpectedPropertyNamesMap = propertyNameToExpectedPropertyNamesMap
	#

	def validate(self, ctx:ValidationContext, jsonData):
		for propertyName, expectedOtherProperties in self.__propertyNameToExpectedPropertyNamesMap.items():
			if propertyName in jsonData:
				for p in expectedOtherProperties:
					if not p in jsonData:
						return False
		return True
	#

	def validate2(self, ctx:ValidationContext2, jsonData):
		for propertyName, expectedOtherProperties in self.__propertyNameToExpectedPropertyNamesMap.items():
			if propertyName in jsonData:
				for p in expectedOtherProperties:
					if not p in jsonData:
						return False, ValidatorStackTrace(ctx.path, jsonData, repr(propertyName) + " exists, so expecting " + repr(expectedOtherProperties)
							+ " from where " + repr(p) + " did not exist")
		return True, None
	#

	def dump(self, prefix = "", writeFunction = print):
		writeFunction(prefix + self.__class__.__name__ + ":")
		writeFunction(prefix + "\tpropertyNameToExpectedPropertyNamesMap:")
		for propertyName, expectedOtherProperties in self.__propertyNameToExpectedPropertyNamesMap.items():
			writeFunction(prefix + "\t\t" + repr(propertyName) + ": " + repr(expectedOtherProperties))
	#

#

class _validate_object_objectMustMatchSchema(AbstractElementaryValidator):

	def __init__(self, log, propertyNameToSchemaMap:dict):
		Assert.isInstance(propertyNameToSchemaMap, dict, log=log)
		for key, value in propertyNameToSchemaMap.items():
			Assert.isInstance(key, str, log=log)
			Assert.isInstance(value, AbstractElementaryValidator, log=log)

		self.__propertyNameToSchemaMap = propertyNameToSchemaMap
	#

	def validate(self, ctx:ValidationContext, jsonData):
		for propertyName, validator in self.__propertyNameToSchemaMap.items():
			if propertyName in jsonData:
				return validator.validate(ctx, jsonData)
		return True
	#

	def validate2(self, ctx:ValidationContext2, jsonData):
		for propertyName, validator in self.__propertyNameToSchemaMap.items():
			if propertyName in jsonData:
				retSuccess, retStackTrace = validator.validate2(ctx, jsonData)
				if not retSuccess:
					return False, retStackTrace.appendError(ctx.path, None, repr(propertyName) + " exists, so expecting property related schema to match object but that failed")
		return True, None
	#

	def dump(self, prefix = "", writeFunction = print):
		writeFunction(prefix + self.__class__.__name__ + ":")
		writeFunction(prefix + "\tpropertyNameToSchemaMap:")
		for propertyName, validator in self.__propertyNameToSchemaMap.items():
			writeFunction(prefix + "\t\t" + repr(propertyName) + ":")
			validator.dump(prefix + "\t\t\t", writeFunction)
	#

#

# dict<str,_SchemaAST>
# modifies: ctx.allProperties
class _validate_object_propertiesMustMatchSchema(AbstractElementaryValidator):

	def __init__(self, log, propertyNameToSchemaMap:dict):
		Assert.isInstance(propertyNameToSchemaMap, dict, log=log)
		for key, value in propertyNameToSchemaMap.items():
			Assert.isInstance(key, str, log=log)
			Assert.isInstance(value, AbstractElementaryValidator, log=log)

		self.__propertyNameToSchemaMap = propertyNameToSchemaMap
	#

	def validate(self, ctx:ValidationContext, jsonData):
		for propertyName, validator in self.__propertyNameToSchemaMap.items():
			ctx2 = ctx.derive()
			if propertyName in jsonData:
				ctx.allProperties.remove(propertyName)
				v = jsonData[propertyName]
				if not validator.validate(ctx2, v):
					return False
			else:
				return True
		return True
	#

	def validate2(self, ctx:ValidationContext2, jsonData):
		for propertyName, validator in self.__propertyNameToSchemaMap.items():
			if propertyName in jsonData:
				ctx.allProperties.remove(propertyName)
				ctx2 = ctx.deriveOnPropertyName(propertyName)
				v = jsonData[propertyName]
				retSuccess, retStackTrace = validator.validate2(ctx2, v)
				if not retSuccess:
					return False, retStackTrace.appendError(ctx.path, None, repr(propertyName) + " exists, so expecting property related schema to match property value but that failed")
		return True, None
	#

	def dump(self, prefix = "", writeFunction = print):
		writeFunction(prefix + self.__class__.__name__ + ":")
		writeFunction(prefix + "\tpropertyNameToSchemaMap:")
		for propertyName, validator in self.__propertyNameToSchemaMap.items():
			writeFunction(prefix + "\t\t" + repr(propertyName) + ":")
			validator.dump(prefix + "\t\t\t", writeFunction)
	#

#

# list<(regexstr,_SchemaAST)>
# modifies: ctx.allProperties
class _validate_object_regexPropertiesMustMatchSchema(AbstractElementaryValidator):

	def __init__(self, log, propertyNamePatternAndValidatorList:list):
		Assert.isInstance(propertyNamePatternAndValidatorList, list, log=log)
		for propertyNamePattern, validator in propertyNamePatternAndValidatorList:
			Assert.isInstance(propertyNamePattern, str, log=log)
			Assert.isInstance(validator, AbstractElementaryValidator, log=log)

		self.__recordList =	\
			[ (p, re.compile(p), v) for (p, v) in propertyNamePatternAndValidatorList ]
	#

	def validate(self, ctx:ValidationContext, jsonData):
		for propertyName in jsonData:
			for propertyNamePattern, rePattern, validator in self.__recordList:
				if rePattern.search(propertyName):
					ctx.allProperties.remove(propertyName)
					ctx2 = ctx.derive()
					v = jsonData[propertyName]
					retSuccess = validator.validate(ctx2, v)
					if not retSuccess:
						return False
		return True
	#

	def validate2(self, ctx:ValidationContext2, jsonData):
		for propertyName in jsonData:
			for propertyNamePattern, rePattern, validator in self.__recordList:
				if rePattern.search(propertyName):
					ctx.allProperties.remove(propertyName)
					ctx2 = ctx.deriveOnPropertyName(propertyName)
					v = jsonData[propertyName]
					retSuccess, retStackTrace = validator.validate2(ctx2, v)
					if not retSuccess:
						return False, retStackTrace.appendError(ctx.path, None, repr(propertyName) + " matches " + propertyNamePattern + " but validation of property value failed")
		return True, None
	#

	def dump(self, prefix = "", writeFunction = print):
		writeFunction(prefix + self.__class__.__name__ + ":")
		writeFunction(prefix + "\trecordList:")
		for propertyNamePattern, rePattern, validator in self.__recordList:
			writeFunction(prefix + "\t\t" + repr(propertyNamePattern) + ":")
			validator.dump(prefix + "\t\t\t", writeFunction)
	#

#

# Check that certain properties exist
# str[]
class _validate_object_mustHaveProperties(AbstractElementaryValidator):

	def __init__(self, log, propertyNames:list):
		Assert.isInstance(propertyNames, list, log=log)
		for key in propertyNames:
			Assert.isInstance(key, str, log=log)

		self.__propertyNames = propertyNames
	#

	def validate(self, ctx:ValidationContext, jsonData):
		for propertyName in self.__propertyNames:
			if propertyName not in jsonData:
				return False
		return True
	#

	def validate2(self, ctx:ValidationContext2, jsonData):
		for propertyName in self.__propertyNames:
			if propertyName not in jsonData:
				return False, ValidatorStackTrace(ctx.path, jsonData, repr(propertyName) + " does not exist")
		return True, None
	#

	def dump(self, prefix = "", writeFunction = print):
		writeFunction(prefix + self.__class__.__name__ + ":")
		writeFunction(prefix + "\tpropertyNames: " + repr(self.__propertyNames))
	#

#

# modifies: ctx.allProperties
class _validate_object_collectAllPropertyNames(AbstractElementaryValidator):

	def __init__(self, log):
		pass
	#

	def validate(self, ctx:ValidationContext, jsonData):
		ctx.allProperties = set(jsonData.keys())
		return True
	#

	def validate2(self, ctx:ValidationContext2, jsonData):
		ctx.allProperties = set(jsonData.keys())
		return True, None
	#

	def dump(self, prefix = "", writeFunction = print):
		writeFunction(prefix + self.__class__.__name__ + ":")
	#

#

# Check if all additional properties match against the specified validator.
# AbstractElementaryValidator
class _validate_object_additionalPropertiesMatchValidator(AbstractElementaryValidator):

	def __init__(self, log, validator:AbstractElementaryValidator):
		Assert.isInstance(validator, AbstractElementaryValidator, log=log)

		self.__validator = validator
	#

	def validate(self, ctx:ValidationContext, jsonData):
		if ctx.allProperties is None:
			raise Exception()

		for propertyName in ctx.allProperties:
			ctx2 = ctx.derive()
			if not self.__validator.validate(ctx2, jsonData[propertyName]):
				return False
		return True
	#

	def validate2(self, ctx:ValidationContext2, jsonData):
		if ctx.allProperties is None:
			raise Exception()

		for propertyName in ctx.allProperties:
			ctx2 = ctx.deriveOnPropertyName(propertyName)
			retSuccess, retStackTrace = self.__validator.validate2(ctx2, jsonData[propertyName])
			if not retSuccess:
				return False, retStackTrace.appendError(ctx.path, jsonData, "property failed to validate")
		return True, None
	#

	def dump(self, prefix = "", writeFunction = print):
		writeFunction(prefix + self.__class__.__name__ + ":")
		writeFunction(prefix + "\tvalidator:")
		self.__validator.dump(prefix + "\t\t", writeFunction)
	#

#





# TODO: check argument types as well, not only the number of arguments

ANY_VALIDATORS = {
	("any_allowedValues", _validate_any_anyOfTheseValues, 1),
}

NUMBER_VALIDATORS = (
	("number_minimum", _validate_number_minimum, 1),
	("number_exclusiveMinimum", _validate_number_exclusiveMinimum, 1),
	("number_maximum", _validate_number_maximum, 1),
	("number_exclusiveMaximum", _validate_number_exclusiveMaximum, 1),
	("number_multipleValueOf", _validate_number_multipleValueOf, 1),
)

STRING_VALIDATORS = (
	("string_minLength", _validate_item_minLength, 1),
	("string_maxLength", _validate_item_maxLength, 1),
	("string_pattern", _validate_string_pattern, 1),
)

ARRAY_VALIDATORS = (
	("array_minItems", _validate_item_minLength, 1),
	("array_maxItems", _validate_item_maxLength, 1),
	("array_mustContainExactValue", _validate_array_mustContainExactValue, 1),
	("array_itemsMustBeUnique", _validate_array_itemsMustBeUnique, 0),
)

OPS_VALIDATORS = {
	("op_not", _validate_not, 1),
	("op_anyOf", _validate_anyOf, 1),
	("op_allOf", _validate_allOf, 1),
	("op_oneOf", _validate_oneOf, 1),
}

EXCLUSIVE_OPS = [
	"op_if", "op_not", "op_anyOf", "op_oneOf", "op_allOf"
]

OBJECT_VALIDATORS = (
	("object_requiredProperties", _validate_object_mustHaveProperties, 1),
	("object_minProperties", _validate_item_minLength, 1),
	("object_maxProperties", _validate_item_maxLength, 1),
	("object_propertyDependencyObjectMustMatchSchema", _validate_object_objectMustMatchSchema, 1),
	("object_propertyDependencyOtherPropertyMustExist", _validate_object_otherPropertyMustExist, 1),
	("object_propertyNames", _validate_object_allPropertyNamesMatchValidator, 1),
	("object_properties", _validate_object_propertiesMustMatchSchema, 1),							# must be placed before object_additionalProperties
	("object_patternProperties", _validate_object_regexPropertiesMustMatchSchema, 1),				# must be placed before object_additionalProperties
	("object_additionalProperties", _validate_object_additionalPropertiesMatchValidator, 1),		# must be placed after object_properties and after object_patternProperties
)






def compileAstList(astList:list, log:jk_logging.AbstractLogger):
	Assert.isInstance(log, jk_logging.AbstractLogger, log=log)

	if astList is None:
		return None
	Assert.isInstance(astList, list)
	return [ compileAst(x, log) for x in astList ]
#



def tryCompile(something, log:jk_logging.AbstractLogger):
	if something is None:
		return None
	elif isinstance(something, _SchemaAST):
		return compileAst(something, log)
	elif isinstance(something, (tuple, list)):
		return [ tryCompile(item, log) for item in something ]
	elif isinstance(something, dict):
		return { key: tryCompile(value, log) for (key, value) in something.items() }
	else:
		return something
#



def __compileAccordingToDefinitions(ast:_SchemaAST, typeIDorTypeIDs:Union[None,int,List[int]], listOfValidatorDefs:list, ret:_Validator, log:jk_logging.AbstractLogger):
	for (astVarName, validatorClass, nArgs) in listOfValidatorDefs:
		bAppendValidator = False

		if nArgs == 0:
			a = getattr(ast, astVarName, None)
			if a != None:
				v = validatorClass(log)
				bAppendValidator = True
		elif nArgs == 1:
			a = getattr(ast, astVarName, None)
			if a != None:
				a = tryCompile(a, log)
				v = validatorClass(log, a)
				bAppendValidator = True
		else:
			a = getattr(ast, astVarName, None)
			if a != None:
				a = tryCompile(a, log)
				v = validatorClass(log, *a)
				bAppendValidator = True

		if bAppendValidator:
			if typeIDorTypeIDs is None:
				ret._any.append(v)
			elif isinstance(typeIDorTypeIDs, (tuple, list)):
				for typeID in typeIDorTypeIDs:
					ret._validators[typeID]._validators.append(v)
			else:
				ret._validators[typeIDorTypeIDs]._validators.append(v)
#



def compileAst(ast:_SchemaAST, log:jk_logging.AbstractLogger):
	Assert.isInstance(log, jk_logging.AbstractLogger, log=log)

	if ast is None:
		return None
	Assert.isInstance(ast, _SchemaAST, log=log)

	ret = _Validator()

	# -------- boolean --------

	if ast.always != None:
		# this overrides everything
		ret._default = ast.always
		return ret

	# -------- ops --------

	lastOpVarName = None
	for astOpVarName in EXCLUSIVE_OPS:
		a = getattr(ast, astOpVarName, None)
		if a != None:
			if lastOpVarName:
				raise Exception("Can't compile " + astOpVarName + " as " + lastOpVarName + " has already been defined!")
			lastOpVarName = astOpVarName

	if ast.op_if:
		ret._any.append(_validate_if(log,
			compileAst(ast.op_if, log),
			compileAst(ast.op_then, log),
			compileAst(ast.op_else, log)))

	__compileAccordingToDefinitions(ast, None, OPS_VALIDATORS, ret, log)

	# -------- any --------

	__compileAccordingToDefinitions(ast, None, ANY_VALIDATORS, ret, log)

	if ast.any_mustBeExactValue:
		ret._any.append(_validate_any_exactValue(log, ast.any_mustBeExactValue[0]))

	# -------- number --------

	__compileAccordingToDefinitions(ast, (TYPE_INT, TYPE_FLOAT), NUMBER_VALIDATORS, ret, log)

	# -------- string --------

	__compileAccordingToDefinitions(ast, TYPE_STR, STRING_VALIDATORS, ret, log)

	# -------- array --------

	__compileAccordingToDefinitions(ast, TYPE_ARRAY, ARRAY_VALIDATORS, ret, log)

	if ast.array_itemsMustBeNone:
		ret._validators[TYPE_ARRAY]._validators.append(_validate_item_mustBeNoneOrEmpty(log))
	elif ast.array_itemsMustNotBeNone:
		ret._validators[TYPE_ARRAY]._validators.append(_validate_item_mustNotBeNone(log))
	elif ast.array_items != None:
		if isinstance(ast.array_items, _SchemaAST):
			ret._validators[TYPE_ARRAY]._validators.append(_validate_array_checkIfAllItemsMatchValidator(log,
				compileAst(ast.array_items, log)))
		else:
			# assert isinstance(ast.array_items, list)
			Assert.isInstance(ast.array_items, list, log=log)
			if ast.array_additionalItems != None:
				if isinstance(ast.array_additionalItems, bool):
					if not ast.array_additionalItems:
						ret._validators[TYPE_ARRAY]._validators.append(_validate_array_checkAllItemsMatchListOfValidatorsWithExtraValidator(log,
							compileAstList(ast.array_items, log),
							[]))
				elif isinstance(ast.array_additionalItems, _SchemaAST):
					ret._validators[TYPE_ARRAY]._validators.append(_validate_array_checkAllItemsMatchListOfValidatorsWithExtraValidator(log,
						compileAstList(ast.array_items, log),
						compileAst(ast.array_additionalItems, log)))
				else:
					# assert isinstance(ast.array_additionalItems, list)
					Assert.isInstance(ast.array_additionalItems, list, log=log)
					ret._validators[TYPE_ARRAY]._validators.append(_validate_array_checkAllItemsMatchListOfValidatorsWithExtraListOfValidators(log,
						compileAstList(ast.array_items, log),
						compileAstList(ast.array_additionalItems, log)))
			else:
				ret._validators[TYPE_ARRAY]._validators.append(_validate_array_checkAllItemsMatchListOfValidators(log,
					compileAstList(ast.array_items, log)))

	# -------- objects --------

	if ast.object_properties or ast.object_patternProperties:
		ret._validators[TYPE_OBJECT]._validators.append(_validate_object_collectAllPropertyNames(log))

	__compileAccordingToDefinitions(ast, TYPE_OBJECT, OBJECT_VALIDATORS, ret, log)

	# -------- types --------

	if ast.any_allowedTypes:
		# only let the specified types pass.
		typeIDs = set(ast.any_allowedTypes)
		extraTypeIDs = ALL_TYPES_SET.difference(typeIDs)
		for typeID in extraTypeIDs:
			v = ret._validators[typeID]
			v._validators.clear()
			v._default = False

	# --------

	return ret
#









