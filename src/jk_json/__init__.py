#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import json as __json

from .ObjectEncoder import ObjectEncoder

from .Token import Token
from .TokenStream import TokenStream
from .TokenizerBase import TokenizerBase
from .SourceCodeLocation import SourceCodeLocation
from .ParserErrorException import ParserErrorException

from .TokenizerRelaxed import TokenizerRelaxed
from .TokenizerStrict import TokenizerStrict
from .JsonParserRelaxed import JsonParserRelaxed
from .JsonParserStrict import JsonParserStrict




__parserRelaxed = JsonParserRelaxed()
__tokenizerRelaxed = TokenizerRelaxed()

__parserStrict = JsonParserStrict()
__tokenizerStrict = TokenizerStrict()



#
# Deserialize a JSON string: Reconstruct a python data structure from the specified JSON string.
#
# @param	str textToParse		The JSON to parse in binary or string representation. If binary data is specified a simple UTF-8 decoding is performed
#								to get to a string which is then parsed.
# @param	bool bStrict		If ```True``` this parser sticks strictly to the JSON standard. If ```False``` C-style comments
#								are allowed and strings can be specified with single quotes and double quotes.
#								Furthermore NaN, positive and negative infinitiy is supported.
#
def loads(textToParse, bStrict = False, bDebugging = False):
	if isinstance(textToParse, (bytes, bytearray)):
		textToParse = textToParse.decode("utf-8")
	elif not isinstance(textToParse, str):
		raise Exception("Can't decode JSON data from a non-string or non-binary value!")

	if bStrict:
		tokenizer = __tokenizerStrict
		parser = __parserStrict
	else:
		tokenizer = __tokenizerRelaxed
		parser = __parserRelaxed

	return parser.parse(tokenizer.tokenize(textToParse), bDebugging)
#



#
# Deserialize a JSON string: Reconstruct a python data structure reading data from the specified JSON file.
#
# @param	File fp				A file like object. All data contained in that file is read.
# @param	bool bStrict		If ```True``` this parser sticks strictly to the JSON standard. If ```False``` C-style comments
#								are allowed and strings can be specified with single quotes and double quotes.
#								Furthermore NaN, positive and negative infinitiy is supported.
#
def load(fp, bStrict = False, bDebugging = False):
	return loads(fp.read(), bStrict = bStrict, bDebugging = bDebugging)
#



#
# Deserialize a JSON string: Reconstruct a python data structure reading data from the specified JSON file.
#
# @param	str filePath		The path of the file to load.
# @param	bool bStrict		If ```True``` this parser sticks strictly to the JSON standard. If ```False``` C-style comments
#								are allowed and strings can be specified with single quotes and double quotes.
#								Furthermore NaN, positive and negative infinitiy is supported.
#
def loadFromFile(filePath, bStrict = False, bDebugging = False):
	with open(filePath, "r", encoding="utf-8") as f:
		return loads(f.read(), bStrict = bStrict, bDebugging = bDebugging)
#



#
# Serialize the specified object or value to a JSON formatted JSON string.
#
# @param		mixed jsonObj		The object to serialize
# @param		str indent			The indentation to use
# @param		bool sort_keys		It ```True``` sort the properties
#
def dumps(jsonObj, indent=None, sort_keys=False, linePrefix=None, cls=None):
	# for now we rely on the default json serializer/deserializer
	if indent is None:
		return __json.dumps(jsonObj, indent=None, separators=(',', ':'), sort_keys=sort_keys, cls=cls)
	else:
		if linePrefix is None:
			return __json.dumps(jsonObj, indent=indent, sort_keys=sort_keys, cls=cls)
		else:
			lines = __json.dumps(jsonObj, indent=indent, sort_keys=sort_keys, cls=cls).split("\n")
			ret = linePrefix + ("\n" + linePrefix).join(lines) + "\n"
			return ret
#



def dump(jsonObj, f, indent=None, sort_keys=False, linePrefix=None, cls=None):
	# for now we rely on the default json serializer/deserializer
	if indent is None:
		return __json.dump(jsonObj, f, indent=None, separators=(',', ':'), sort_keys=sort_keys, cls=cls)
	else:
		if linePrefix is None:
			return __json.dump(jsonObj, f, indent=indent, sort_keys=sort_keys, cls=cls)
		else:
			lines = __json.dump(jsonObj, f, indent=indent, sort_keys=sort_keys, cls=cls).split("\n")
			ret = linePrefix + lines.join("\n" + linePrefix) + "\n"
			return ret
#



def saveToFile(jsonObj, filePath, indent=None, sort_keys=False, linePrefix=None):
	with open(filePath, "w", encoding="utf-8") as f:
		dump(jsonObj, f, indent=indent, sort_keys=sort_keys, linePrefix=linePrefix)
		#__json.dump(jsonObj, f, indent=indent, sort_keys=sort_keys)
#



def saveToFilePretty(jsonObj, filePath, linePrefix=None):
	with open(filePath, "w", encoding="utf-8") as f:
		dump(jsonObj, f, indent="\t", sort_keys=True, linePrefix=linePrefix, cls=ObjectEncoder)
		#__json.dump(jsonObj, f, indent=indent, sort_keys=sort_keys)
#



def prettyPrint(jsonObj):
	print(dumps(jsonObj, indent="\t", sort_keys=True, cls=ObjectEncoder))
#



