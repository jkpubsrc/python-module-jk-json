#!/usr/bin/python3


import json
import os
import sys
import re

import jk_console
import jk_sysinfo
import jk_json
import jk_flexdata
import jk_logging
from jk_typing import *
import jk_argparsing









ap = jk_argparsing.ArgsParser("jsonPrettyPrint", "Format JSON data.")

ap.optionDataDefaults.set("help", False)
ap.optionDataDefaults.set("color", True)
ap.optionDataDefaults.set("stdin", False)
ap.optionDataDefaults.set("extractionPath", None)

ap.createOption('h', 'help', "Display this help text.").onOption = \
	lambda argOption, argOptionArguments, parsedArgs: \
		parsedArgs.optionData.set("help", True)
ap.createOption(None, 'no-color', "Dont' use colors in output.").onOption = \
	lambda argOption, argOptionArguments, parsedArgs: \
		parsedArgs.optionData.set("colors", False)
ap.createOption(None, 'stdin', "Read JSON data from stdin.").onOption = \
	lambda argOption, argOptionArguments, parsedArgs: \
		parsedArgs.optionData.set("stdin", True)
ap.createOption(None, 'extract', "Extract a specific part of the data object.").expectString("spath", 1).onOption = \
	lambda argOption, argOptionArguments, parsedArgs: \
		parsedArgs.optionData.set("extractionPath", jk_flexdata.FlexDataSelector(argOptionArguments[0]))

ap.createAuthor("Jürgen Knauth", "jk@binary-overflow.de")
ap.setLicense("Apache", YEAR = 2020, COPYRIGHTHOLDER = "Jürgen Knauth")

ap.createReturnCode(0, "Everything is okay.")
ap.createReturnCode(1, "An error occurred.")

#ap.createCommand("filePath", "The path of the JSON file to load") 





parsedArgs = ap.parse()
#parsedArgs.dump()

if parsedArgs.optionData["help"] or ((not parsedArgs.programArgs) and not parsedArgs.optionData["stdin"]):
	ap.showHelp()
	sys.exit(0)

"""
cmdName, cmdArgs = parsedArgs.parseNextCommand()
if cmdName is None:
	ap.showHelp()
	sys.exit(0)
"""

if parsedArgs.optionData["color"]:
	log = jk_logging.ConsoleLogger.create(logMsgFormatter = jk_logging.COLOR_LOG_MESSAGE_FORMATTER, printToStdErr = True)
else:
	log = jk_logging.ConsoleLogger.create(printToStdErr = True)

bSuccess = True

if parsedArgs.optionData["stdin"]:
	line = sys.stdin.readline()
	jsonData = json.loads(line)
else:
	for filePath in parsedArgs.programArgs:
		jsonData = jk_json.loadFromFile(filePath)

extractionPath = parsedArgs.optionData.get("extractionPath")
if extractionPath:
	assert isinstance(extractionPath, jk_flexdata.FlexDataSelector)
	_, result = extractionPath.getOne(jk_flexdata.FlexObject(jsonData))
	jsonData = result
	if isinstance(jsonData, jk_flexdata.FlexObject):
		jsonData = jsonData._toDict()

if isinstance(jsonData, str):
	retLine = "-" * 160
	ret2 = jsonData.encode("utf-8").decode('unicode_escape')
	print("\n".join([ retLine, ret2, retLine ]))
else:
	jk_json.prettyPrint(jsonData)

sys.exit(0 if bSuccess else 1)









