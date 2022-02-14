

__version__ = "0.2022.2.14"



import json as __json
import gzip
import bz2
import typing

import chardet

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
def loads(textToParse:str, bStrict:bool = False, bDebugging:bool = False):
	assert isinstance(textToParse, str)
	assert isinstance(bStrict, bool)
	assert isinstance(bDebugging, bool)

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
	rawData = fp.read()
	return loads(rawData, bStrict = bStrict, bDebugging = bDebugging)
#



#
# Deserialize a JSON string: Reconstruct a python data structure reading data from the specified JSON file.
#
# @param	str filePath		The path of the file to load.
# @param	bool bStrict		If ```True``` this parser sticks strictly to the JSON standard. If ```False``` C-style comments
#								are allowed and strings can be specified with single quotes and double quotes.
#								Furthermore NaN, positive and negative infinitiy is supported.
#
def loadFromFile(filePath:str, bStrict:bool = False, bDebugging:bool = False, encoding:str = None, autoDetectEncoding:bool = True, errPrintFunc = None):
	assert isinstance(filePath, str)
	assert isinstance(bStrict, bool)
	assert isinstance(bDebugging, bool)

	if filePath.endswith(".bz2"):
		with bz2.open(filePath, "rb") as f:
			rawData = f.read()
	elif filePath.endswith(".gz"):
		with gzip.open(filePath, "rb") as f:
			rawData = f.read()
	else:
		with open(filePath, "rb") as f:
			rawData = f.read()

	textData = None

	if encoding is None:
		if autoDetectEncoding:
			try:
				if rawData.startswith(b"\xef\xbb\xbf"):		# utf-8 byte order mark
					rawData = rawData[3:]

				textData = rawData.decode("utf-8")

			except:
				encoding = chardet.detect(rawData)["encoding"]
				if encoding is None:
					encoding = "utf-8"

		else:
			encoding = "utf-8"

	if textData is None:
		textData = rawData.decode(encoding)

	if errPrintFunc and callable(errPrintFunc):
		try:
			return loads(textData, bStrict = bStrict, bDebugging = bDebugging)
		except ParserErrorException as ee:
			s = filePath if len(filePath) < 40 else ("..." + filePath[-40:])
			prefix = "{}:{} ".format(s, ee.location.lineNo + 1)
			errPrintFunc(prefix + ee.textLine.replace("\t", " "))
			errPrintFunc(" " * (len(prefix) + ee.location.charPos + 1) + "ᐃ")
			errPrintFunc(" " * (len(prefix) + ee.location.charPos + 1 - 6) + "╌╌╍╍━━┛")
			raise
	else:
		return loads(textData, bStrict = bStrict, bDebugging = bDebugging)
#



#
# Serialize the specified object or value to a JSON formatted JSON string.
#
# @param		mixed jsonObj		The object to serialize
# @param		str indent			The indentation to use
# @param		bool sort_keys		It ```True``` sort the properties
#
def dumps(
		jsonObj:typing.Union[str,int,float,bool,tuple,list,dict],
		indent:str = None,
		sort_keys:bool = False,
		linePrefix:str = None,
		cls = None,
		comment:typing.Union[typing.List[str],typing.Tuple[str],str] = None,
	):

	assert isinstance(jsonObj, (str,int,float,bool,tuple,list,dict,None))

	if indent is not None:
		assert isinstance(indent, str)

	if sort_keys is not None:
		assert isinstance(sort_keys, bool)

	if linePrefix is not None:
		assert isinstance(linePrefix, str)

	if comment:
		if isinstance(comment, str):
			comment = [ str ]
		elif isinstance(comment, list):
			for x in comment:
				if not isinstance(x, str):
					raise Exception("fileComment has data of invalid type!")
		elif isinstance(comment, tuple):
			for x in comment:
				if not isinstance(x, str):
					raise Exception("fileComment has data of invalid type!")
			comment = list(comment)
		else:
			raise Exception("fileComment has data of invalid type!")

	# ----

	# for now we rely on the default json serializer/deserializer
	if indent is None:
		return __json.dumps(jsonObj, indent=None, separators=(',', ':'), sort_keys=sort_keys, cls=cls)
	else:
		if linePrefix is None:
			if comment:
				sRet = "/*\n" + "\n".join(comment) + "\n*/\n"
			else:
				sRet = ""

			sRet += __json.dumps(jsonObj, indent=indent, sort_keys=sort_keys, cls=cls)
			return sRet

		else:
			if comment:
				lines = [ "/*" ] + comment + [ "*/" ]
			else:
				lines = []

			lines += __json.dumps(jsonObj, indent=indent, sort_keys=sort_keys, cls=cls).split("\n")

			ret = linePrefix + ("\n" + linePrefix).join(lines) + "\n"
			return ret
#



def dump(
		jsonObj:typing.Union[str,int,float,bool,tuple,list,dict],
		f,
		indent:str = None,
		sort_keys:bool = False,
		linePrefix:str = None,
		cls = None,
		comment:typing.Union[typing.List[str],typing.Tuple[str],str] = None,
	):

	assert isinstance(jsonObj, (str,int,float,bool,tuple,list,dict,None))

	if indent is not None:
		assert isinstance(indent, str)

	if sort_keys is not None:
		assert isinstance(sort_keys, bool)

	if linePrefix is not None:
		assert isinstance(linePrefix, str)

	if comment:
		if isinstance(comment, str):
			comment = [ str ]
		elif isinstance(comment, list):
			for x in comment:
				if not isinstance(x, str):
					raise Exception("fileComment has data of invalid type!")
		elif isinstance(comment, tuple):
			for x in comment:
				if not isinstance(x, str):
					raise Exception("fileComment has data of invalid type!")
			comment = list(comment)
		else:
			raise Exception("fileComment has data of invalid type!")

	# ----

	# for now we rely on the default json serializer/deserializer
	if indent is None:
		return __json.dump(jsonObj, f, indent=None, separators=(',', ':'), sort_keys=sort_keys, cls=cls)
	else:
		if linePrefix is None:
			if comment:
				sRet = "/*\n" + "\n".join(comment) + "\n*/\n"
			else:
				sRet = ""

			sRet += __json.dump(jsonObj, f, indent=indent, sort_keys=sort_keys, cls=cls)
			return sRet

		else:
			if comment:
				lines = [ "/*" ] + comment + [ "*/" ]
			else:
				lines = []

			lines += __json.dump(jsonObj, f, indent=indent, sort_keys=sort_keys, cls=cls).split("\n")

			ret = linePrefix + lines.join("\n" + linePrefix) + "\n"
			return ret
#



def saveToFile(
		jsonObj:typing.Union[str,int,float,bool,tuple,list,dict],
		filePath:str,
		indent:str = None,
		sort_keys:bool = False,
		linePrefix:str = None,
	):

	assert isinstance(filePath, str)

	# ----

	with open(filePath, "w", encoding="utf-8", newline="\n") as f:
		dump(jsonObj, f, indent=indent, sort_keys=sort_keys, linePrefix=linePrefix)
		#__json.dump(jsonObj, f, indent=indent, sort_keys=sort_keys)
#



def saveToFilePretty(
		jsonObj:typing.Union[str,int,float,bool,tuple,list,dict],
		filePath:str,
		linePrefix:str = None,
		comment:typing.Union[typing.List[str],typing.Tuple[str],str] = None,
	):

	assert isinstance(filePath, str)
	if comment:
		if isinstance(comment, str):
			comment = [ str ]
		elif isinstance(comment, (tuple,list)):
			for x in comment:
				if not isinstance(x, str):
					raise Exception("fileComment has data of invalid type!")
		else:
			raise Exception("fileComment has data of invalid type!")

	# ----

	with open(filePath, "w", encoding="utf-8", newline="\n") as f:
		dump(jsonObj, f, indent="\t", sort_keys=True, linePrefix=linePrefix, cls=ObjectEncoder, comment=comment)
		#__json.dump(jsonObj, f, indent=indent, sort_keys=sort_keys)
#



def prettyPrint(
		jsonObj:typing.Union[str,int,float,bool,tuple,list,dict],
		linePrefix:str = None,
		comment:typing.Union[typing.List[str],typing.Tuple[str],str] = None,
	):

	print(dumps(jsonObj, indent="\t", sort_keys=True, linePrefix=linePrefix, cls=ObjectEncoder, comment=comment))
#



def prettyPrintToStr(
		jsonObj:typing.Union[str,int,float,bool,tuple,list,dict],
		linePrefix:str = None,
		comment:typing.Union[typing.List[str],typing.Tuple[str],str] = None,
	) -> str:

	return dumps(jsonObj, indent="\t", sort_keys=True, linePrefix=linePrefix, cls=ObjectEncoder, comment=comment)
#



#