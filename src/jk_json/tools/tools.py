#!/usr/bin/env python3
# -*- coding: utf-8 -*-




# ================================================================================================================================
# ================================================================================================================================
# ================================================================================================================================



TYPE_NULL = 0
TYPE_BOOL = 1
TYPE_INT = 2
TYPE_FLOAT = 3
TYPE_STR = 4
TYPE_ARRAY = 5
TYPE_OBJECT= 6

ALL_TYPES_LIST = [ TYPE_NULL, TYPE_BOOL, TYPE_INT, TYPE_FLOAT, TYPE_STR, TYPE_ARRAY, TYPE_OBJECT ]
ALL_TYPES_NAME_LIST = [ "null", "boolean", "integer", "float", "string", "array", "object" ]
ALL_TYPES_SET = frozenset(ALL_TYPES_LIST)



# ================================================================================================================================
# ================================================================================================================================
# ================================================================================================================================



def getTypeID(typeName:str):
	if typeName == "null":
		return TYPE_NULL
	if typeName == "boolean":
		return TYPE_BOOL
	if typeName == "integer":
		return TYPE_INT
	if typeName == "number":
		return TYPE_FLOAT
	if typeName == "string":
		return TYPE_STR
	if typeName == "array":
		return TYPE_ARRAY
	if typeName == "object":
		return TYPE_OBJECT
	raise Exception("Invalid type: " + str(typeName))
#

def getTypeIDs(typeNames:list):
	ret = []
	for typeName in typeNames:
		ret.append(getTypeID(typeName))
	return ret
#

def getTypeIDOfType(pythonType:type):
	if (pythonType is None) or (pythonType is type(None)):
		return TYPE_NULL
	if pythonType == bool:
		return TYPE_BOOL
	if pythonType == int:
		return TYPE_INT
	if pythonType == float:
		return TYPE_FLOAT
	if pythonType == str:
		return TYPE_STR
	if (pythonType == list) or (pythonType == tuple):
		return TYPE_ARRAY
	if pythonType == dict:
		return TYPE_OBJECT
	raise Exception("Invalid type: " + str(pythonType))
#

def getTypeIDOfTypeNonInt(pythonType:type):
	if (pythonType is None) or (pythonType is type(None)):
		return TYPE_NULL
	if pythonType == bool:
		return TYPE_BOOL
	if (pythonType == int) or (pythonType == float):
		return TYPE_FLOAT
	if pythonType == str:
		return TYPE_STR
	if (pythonType == list) or (pythonType == tuple):
		return TYPE_ARRAY
	if pythonType == dict:
		return TYPE_OBJECT
	raise Exception("Invalid type: " + str(pythonType))
#

def getTypeIDOfValue(value):
	if value is None:
		return TYPE_NULL
	if isinstance(value, bool):
		return TYPE_BOOL
	if isinstance(value, int):
		return TYPE_INT
	if isinstance(value, float):
		return TYPE_FLOAT
	if isinstance(value, str):
		return TYPE_STR
	if isinstance(value, (list, tuple)):
		return TYPE_ARRAY
	if isinstance(value, dict):
		return TYPE_OBJECT
	raise Exception("Invalid type: " + str(type(value)))
#

def getTypeIDOfValueNonInt(value):
	if value is None:
		return TYPE_NULL
	if isinstance(value, bool):
		return TYPE_BOOL
	if isinstance(value, (int, float)):
		return TYPE_FLOAT
	if isinstance(value, str):
		return TYPE_STR
	if isinstance(value, (list, tuple)):
		return TYPE_ARRAY
	if isinstance(value, dict):
		return TYPE_OBJECT
	raise Exception("Invalid type: " + str(type(value)))
#


# ================================================================================================================================
# ================================================================================================================================
# ================================================================================================================================



def _cmp_list(jsonListA, jsonListB):
	if len(jsonListA) != len(jsonListB):
		return False

	for va, vb in zip(jsonListA, jsonListB):
		ta = getTypeIDOfValue(va)
		tb = getTypeIDOfValue(vb)

		if ta != tb:
			return False

		if ta == TYPE_ARRAY:
			return _cmp_list(va, vb)
		elif ta == TYPE_OBJECT:
			return _cmp_obj(va, vb)
		else:
			return va == vb

	return True
#

def _cmp_list_nonInt(jsonListA, jsonListB):
	if len(jsonListA) != len(jsonListB):
		return False

	for va, vb in zip(jsonListA, jsonListB):
		ta = getTypeIDOfValueNonInt(va)
		tb = getTypeIDOfValueNonInt(vb)

		if ta != tb:
			return False

		if ta == TYPE_ARRAY:
			return _cmp_list_nonInt(va, vb)
		elif ta == TYPE_OBJECT:
			return _cmp_obj_nonInt(va, vb)
		else:
			return va == vb

	return True
#

def _cmp_obj(jsonObjA, jsonObjB):
	if len(jsonObjA) != len(jsonObjB):
		return False

	for propertyName in jsonObjA:
		if propertyName not in jsonObjB:
			return False

		va = jsonObjA[propertyName]
		vb = jsonObjB[propertyName]

		ta = getTypeIDOfValue(va)
		tb = getTypeIDOfValue(vb)
		if ta != tb:
			return False

		if ta == TYPE_ARRAY:
			return _cmp_list(va, vb)
		elif ta == TYPE_OBJECT:
			return _cmp_obj(va, vb)
		else:
			return va == vb

	return True
#

def _cmp_obj_nonInt(jsonObjA, jsonObjB):
	if len(jsonObjA) != len(jsonObjB):
		return False

	for propertyName in jsonObjA:
		if propertyName not in jsonObjB:
			return False

		va = jsonObjA[propertyName]
		vb = jsonObjB[propertyName]

		ta = getTypeIDOfValueNonInt(va)
		tb = getTypeIDOfValueNonInt(vb)
		if ta != tb:
			return False

		if ta == TYPE_ARRAY:
			return _cmp_list_nonInt(va, vb)
		elif ta == TYPE_OBJECT:
			return _cmp_obj_nonInt(va, vb)
		else:
			return va == vb

	return True
#

def jsonIsEqual(va, vb, dontDistinguishBetweenIntAndFloat = True):
	if dontDistinguishBetweenIntAndFloat:
		ta = getTypeIDOfValueNonInt(va)
		tb = getTypeIDOfValueNonInt(vb)
		# print(str(ta) + "\t" + repr(va))
		# print(str(tb) + "\t" + repr(vb))

		if ta != tb:
			return False

		if ta == TYPE_ARRAY:
			return _cmp_list_nonInt(va, vb)
		elif ta == TYPE_OBJECT:
			return _cmp_obj_nonInt(va, vb)
		else:
			return va == vb

	else:
		ta = getTypeIDOfValue(va)
		tb = getTypeIDOfValue(vb)
		# print(str(ta) + "\t" + repr(va))
		# print(str(tb) + "\t" + repr(vb))

		if ta != tb:
			return False

		if ta == TYPE_ARRAY:
			return _cmp_list(va, vb)
		elif ta == TYPE_OBJECT:
			return _cmp_obj(va, vb)
		else:
			return va == vb
#







