#!/usr/bin/env python3
# -*- coding: utf-8 -*-



import os

import jk_json
import jk_jsonschema
import jk_logging
import jk_console



jk_logging.COLOR_LOG_MESSAGE_FORMATTER.setOutputMode(jk_logging.COLOR_LOG_MESSAGE_FORMATTER.EnumOutputMode.FULL)
LOGGER = jk_logging.ConsoleLogger.create(logMsgFormatter=jk_logging.COLOR_LOG_MESSAGE_FORMATTER)

#BASE_DIR = os.path.abspath("JSON-Schema-Test-Suite/tests/draft7")
#BASE_DIR = os.path.abspath("tests")
BASE_DIR = os.path.abspath("tests/SUCCEEDED")
if os.path.isdir(BASE_DIR):
	LOGGER.info("Using base directory for test cases: " + BASE_DIR)
else:
	raise Exception("No such directory: " + BASE_DIR)






def runTests(schema, jTests, log):
	nSucceeded = 0
	nFailed = 0
	for jtest in jTests:
		description = jtest["description"]
		jsonData = jtest["data"]
		bValid = jtest["valid"]

		blog = jk_logging.BufferLogger.create()
		bForward = False

		log2 = blog.descend("TEST: " + description)
		try:
			log2.notice("JSON data:")
			for line in jk_json.dumps(jsonData, indent="\t").split("\n"):
				log2.notice("\t" + line)
			bResult, stackTrace = schema.validate2(jsonData)
			s = "Result calculated: " + str(bResult).upper() + " --- Result expected: " + str(bValid).upper()
			if bResult == bValid:
				log2.success(s)
				nSucceeded += 1
			else:
				log2.error(s)
				if stackTrace:
					for s in stackTrace:
						log2.error(str(s))
				nFailed += 1
				bForward = True
		except Exception as ee:
			log2.error(ee)
			bForward = True

		if bForward:
			blog.forwardTo(log)
	return nSucceeded, nFailed
#








nFilesSucceeded = 0
nFilesFailed = 0
nTestsSucceeded = 0
nTestsFailed = 0

for entryName in os.listdir(BASE_DIR):
	fullPath = os.path.join(BASE_DIR, entryName)
	if not os.path.isfile(fullPath):
		continue

	LOGGER.notice("################################################################################################################################")
	LOGGER.notice("################################################################################################################################")
	log = LOGGER.descend("TEST-FILE: " + entryName)
	try:
		jsonData = jk_json.loadFromFile(fullPath, bStrict=False)
		bHadError = False
		for jpart in jsonData:
			jschema = jpart["schema"]
			jtests = jpart["tests"]
			description = jpart["description"]

			blog = jk_logging.BufferLogger.create()
			bForward = False

			log2 = blog.descend("TEST-GROUP: " + description)
			try:
				log2.notice("Schema:")
				for line in jk_json.dumps(jschema, indent="\t").split("\n"):
					log2.notice("\t" + line)
				schema = jk_jsonschema.SchemaParser.parse(jschema, log2)
				schema.dump(writeFunction=log2.notice)
				nSucceeded, nFailed = runTests(schema, jtests, log2)
				if nFailed > 0:
					bHadError = True
					bForward = True
				nTestsSucceeded += nSucceeded
				nTestsFailed += nFailed
			except Exception as ee:
				nTestsFailed += 1
				log2.error(ee)
				bHadError = False
				bForward = True

			if bForward:
				blog.forwardTo(log)

		if bHadError:
			nFilesFailed += 1
		else:
			nFilesSucceeded += 1

	except Exception as ee:
		nFilesFailed += 1
		log.error(ee)


def printValue(text, outlength, value, mode):
	if mode > 0:
		s = jk_console.Console.ForeGround.STD_GREEN
	elif mode < 0:
		s = jk_console.Console.ForeGround.STD_RED
	else:
		s = jk_console.Console.ForeGround.STD_DARKGRAY
	while len(text) < outlength:
		text = " " + text
	s += text
	s += ": "
	s += str(value)
	s += jk_console.Console.RESET
	print(s)
#


print()
print("#### S T A T S ####")
print()
printValue("tests succeeded", 20, nTestsSucceeded, int(nTestsSucceeded > 0))
printValue("tests failed", 20, nTestsFailed, - int(nTestsFailed > 0))
printValue("files succeeded", 20, nFilesSucceeded, int(nFilesSucceeded > 0))
printValue("files failed", 20, nFilesFailed, - int(nFilesFailed > 0))



