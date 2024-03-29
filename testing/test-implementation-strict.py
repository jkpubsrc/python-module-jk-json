#!/usr/bin/env python3




import math
import os
import sys
import codecs
import timeit
import json
import cProfile

from jk_logging import *

import jk_json



bDebugging = False
#bDebugging = True

with codecs.open("test-strict.json", "r", "utf-8") as f:
	jsonTextData = f.read()

#for t in jk_json.TokenizerStrict().tokenize(jsonTextData):
#	print(t)

jsonData = jk_json.loads(jsonTextData, bStrict=True, bDebugging=bDebugging)

#print(jk_json.dumps(jsonData, indent="\t"))

assert "bla" in jsonData
assert isinstance(jsonData["bla"], int)
assert jsonData["bla"] == 123

assert "blubb" in jsonData
assert isinstance(jsonData["blubb"], list)
assert isinstance(jsonData["blubb"][0], int)
assert jsonData["blubb"][0] == 2345
assert isinstance(jsonData["blubb"][1], int)
assert jsonData["blubb"][1] == -678
assert isinstance(jsonData["blubb"][2], float)
assert jsonData["blubb"][2] == 3.1415927
assert isinstance(jsonData["blubb"][3], float)
assert jsonData["blubb"][3] == -.2e-10
assert isinstance(jsonData["blubb"][4], str)
assert jsonData["blubb"][4] == "abc"
assert isinstance(jsonData["blubb"][5], str)
assert jsonData["blubb"][5] == "def\n\u0040"
assert jsonData["blubb"][6] == None
assert jsonData["blubb"][7] == True
assert jsonData["blubb"][8] == False
assert isinstance(jsonData["blubb"][9], list)
assert len(jsonData["blubb"][9]) == 0
assert isinstance(jsonData["blubb"][10], dict)
assert len(jsonData["blubb"][10]) == 0
assert isinstance(jsonData["blubb"][11], int)
assert jsonData["blubb"][11] == 123
assert isinstance(jsonData["blubb"][12], list)
assert len(jsonData["blubb"][12]) == 2
assert isinstance(jsonData["blubb"][12][0], str)
assert jsonData["blubb"][12][0] == "The quick brown fox jumps over the lazy dog."
assert isinstance(jsonData["blubb"][12][1], str)
assert jsonData["blubb"][12][1] == "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG."


print("SUCCESS")












