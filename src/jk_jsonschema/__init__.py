#!/usr/bin/env python3
# -*- coding: utf-8 -*-




from .SchemaParser import SchemaParser
from .SimpleSchemaGenerator import createSchemaGenerator, ObjectGenerator, ListGenerator,	\
			StringGenerator, FloatGenerator, IntegerGenerator, BooleanGenerator, AbstractGenerator



def parse(jsonDef, log = None):
	return SchemaParser.parse(jsonDef, log)
#

def loads(textToParse, log = None):
	import jk_json
	jsonDef = jk_json.loads(textToParse)
	return SchemaParser.parse(jsonDef, log)
#

def loadFromFile(filePath, log = None):
	with open(filePath, "r") as f:
		textToParse = f.read()
	import jk_json
	jsonDef = jk_json.loads(textToParse)
	return SchemaParser.parse(jsonDef, log)
#



#
# Deserialize a JSON string: Reconstruct a python data structure reading data from the specified JSON file.
#
# @param	str filePath		The path of the file to load.
# @param	bool bStrict		If ```True``` this parser sticks strictly to the JSON standard. If ```False``` C-style comments
#								are allowed and strings can be specified with single quotes and double quotes.
#								Furthermore NaN, positive and negative infinitiy is supported.
#
def loadJSONFromFileAndValidate(filePath, bStrict = False, bDebugging = False, validation = None):
	import jk_json
	from .schema_validator import Validator
	if validation:
		with open(filePath, "r", encoding="utf-8") as f:
			jsonData = jk_json.loads(f.read(), bStrict = bStrict, bDebugging = bDebugging)

		if isinstance(validation, dict):
			validator = SchemaParser.parse(validation, None)
		elif isinstance(validation, Validator):
			validator = validation
		else:
			raise Exception("Unexpected type for argument 'validation': " + repr(validation))

		if validator.validate(jsonData):
			return jsonData
		else:
			raise Exception("File " + repr(filePath) + " does not match the expected schema!")

	else:
		with open(filePath, "r", encoding="utf-8") as f:
			return jk_json.loads(f.read(), bStrict = bStrict, bDebugging = bDebugging)
#











