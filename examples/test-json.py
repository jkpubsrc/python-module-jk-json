#!/usr/bin/env python3



import os
import sys
import codecs
import timeit
import json
import cProfile

from jk_logging import *

import jk_json


#bStrict = True
#filePath = "test-strict.json"
bStrict = False
#filePath = "test-relaxed.json"
filePath = "test-performance-test.json"

bDebugging = False
#bDebugging = True

with codecs.open(filePath, "r", "utf-8") as f:
	jsonTextData = f.read()


#tokenizer = TokenizerStrict()
#tokenizer = TokenizerRelaxed()
#for token in tokenizer.tokenize(jsonTextData, bDebuggingEnabled = False):
#	print(token)


#parser = JsonParserStrict()
#parser = JsonParserRelaxed()
#value = parser.parse(tokenizer.tokenize(jsonTextData))
#print(value)


#print(jk_json.loads(jsonTextData, bStrict = bStrict, bDebugging = bDebugging))

def testMethod():
	#jk_json.loads(jsonTextData, bStrict = False, bDebugging = False)
	json.loads(jsonTextData)
#

result = timeit.timeit(
	testMethod,
	number=10000
	)
print(result)


jk_json.testPerformance(jsonTextData, "stats-tokenizing.prof", "stats-parsing.prof")
















