#!/usr/bin/python3


import json
import os
import sys
import re

import jk_exceptionhelper
import jk_console
import jk_json
import jk_flexdata
import jk_logging
from jk_typing import *
import jk_argparsing









ap = jk_argparsing.ArgsParser("jkjson", "Simple JSON processor.")

ap.optionDataDefaults.set("help", False)
ap.optionDataDefaults.set("stdin", False)
ap.optionDataDefaults.set("extractionPath", None)

ap.createOption('h', 'help', "Display this help text.").onOption = \
	lambda argOption, argOptionArguments, parsedArgs: \
		parsedArgs.optionData.set("help", True)

ap.createAuthor("Jürgen Knauth", "jk@binary-overflow.de")
ap.setLicense("Apache", YEAR = 2020, COPYRIGHTHOLDER = "Jürgen Knauth")

ap.createReturnCode(0, "Everything is okay.")
ap.createReturnCode(1, "An error occurred.")

ap.createCommand("load", "Load data from a JSON file.").expectFile("<fileName>", mustExist=True, toAbsolutePath=True) 
ap.createCommand("stdin", "Load data from STDIN.")
ap.createCommand("save", "Write data to a JSON file.").expectFile("<fileName>", toAbsolutePath=True) 
ap.createCommand("savePretty", "Write data to a JSON file.").expectFile("<fileName>", toAbsolutePath=True) 
ap.createCommand("prettyPrint", "Write the JSON data to STDOUT.")
ap.createCommand("linePrint", "Write the JSON data to STDOUT.")
ap.createCommand("print", "Canonincal print to STDOUT.")
ap.createCommand("extract", "Extract a specific part of the JSON data.").expectString("<extractionPath>", 1)





parsedArgs = ap.parse()
#parsedArgs.dump()

if parsedArgs.optionData["help"] or (len(parsedArgs.programArgs) == 0):
	ap.showHelp()
	sys.exit(0)






bSuccess = False
jsonData = None

try:

	while True:
		cmdName, cmdArgs = parsedArgs.parseNextCommand()
		if cmdName is None:
			bSuccess = True
			break

		if cmdName == "stdin":
			line = sys.stdin.readline()
			jsonData = json.loads(line)
			continue

		if cmdName == "load":
			jsonData = jk_json.loadFromFile(cmdArgs[0])
			continue

		if cmdName == "save":
			if jsonData is None:
				raise Exception("No data loaded!")
			jk_json.saveToFile(jsonData, cmdArgs[0])
			continue

		if cmdName == "savePretty":
			if jsonData is None:
				raise Exception("No data loaded!")
			jk_json.saveToFilePretty(jsonData, cmdArgs[0])
			continue

		if cmdName == "prettyPrint":
			if jsonData is None:
				raise Exception("No data loaded!")
			jk_json.prettyPrint(jsonData)
			continue

		if cmdName == "linePrint":
			if jsonData is None:
				raise Exception("No data loaded!")
			print(jk_json.dumps(jsonData))
			continue

		if cmdName == "print":
			if jsonData is None:
				raise Exception("No data loaded!")
			if isinstance(jsonData, (str,int,float,bool)):
				print(jsonData)
			else:
				jk_json.prettyPrint(jsonData)
			continue

		if cmdName == "extract":
			if jsonData is None:
				raise Exception("No data loaded!")
			extractionPath = jk_flexdata.FlexDataSelector(cmdArgs[0])
			_, result = extractionPath.getOne(jk_flexdata.FlexObject(jsonData))
			if isinstance(result, jk_flexdata.FlexObject):
				jsonData = result._toDict()
			else:
				jsonData = result
			continue

		raise Exception(repr((cmdName, cmdArgs)))

except Exception as ee:
	jk_exceptionhelper.analyseException(ee).dump()




sys.exit(0 if bSuccess else 1)









