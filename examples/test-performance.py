#!/usr/bin/env python3
# -*- coding: utf-8 -*-



import json
import codecs
import cProfile
import timeit

import jk_json




REPEATS = 20000



__parserRelaxed = jk_json.JsonParserRelaxed()
__tokenizerRelaxed = jk_json.TokenizerRelaxed()


filePath = "test-performance-test.json"
with codecs.open(filePath, "r", "utf-8") as f:
	jsonTextData = f.read()

tokens = jk_json.TokenStream(__tokenizerRelaxed.tokenize(jsonTextData))

def doTestT1():
	for i in range(0, REPEATS):
		__tokenizerRelaxed.tokenize(jsonTextData)
#

def doTestT2():
	__tokenizerRelaxed.tokenize(jsonTextData)
#

def doTestP1():
	for i in range(0, REPEATS):
		tokens.reset()
		__parserRelaxed.parse(tokens)
#

def doTestP2():
	tokens.reset()
	__parserRelaxed.parse(tokens)
#

cProfile.run("doTestT1()", 'stats-tokenizing.prof')
cProfile.run("doTestP1()", 'stats-parsing.prof')

resultT = timeit.timeit(
	doTestT2,
	number=REPEATS
	)
print("Module:  Avg millis spent in " + str(REPEATS) + "              tokenizings: " + str(resultT * 1000) + " ms")

resultP = timeit.timeit(
	doTestP2,
	number=REPEATS
	)
print("Module:  Avg millis spent in " + str(REPEATS) + "                 parsings: " + str(resultP * 1000) + " ms")
print("Module:  Avg millis spent in " + str(REPEATS) + " tokenizings and parsings: " + str((resultT + resultP) * 1000) + " ms")

def doTestBuiltIn():
	json.loads(jsonTextData)

result = timeit.timeit(
	doTestBuiltIn,
	number=REPEATS
	)
print("Builtin: Avg millis spent in " + str(REPEATS) + " tokenizings and parsings: " + str(result * 1000) + " ms")

print("Builtin implementation is " + str((resultP + resultT) / result) + " times faster.")


