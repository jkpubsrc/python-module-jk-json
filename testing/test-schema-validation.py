#!/usr/bin/env python3



import jk_logging
import jk_json
import jk_jsonschema
import jk_testing



log = jk_logging.ConsoleLogger.create(logMsgFormatter=jk_logging.COLOR_LOG_MESSAGE_FORMATTER)
jk_logging.COLOR_LOG_MESSAGE_FORMATTER.setOutputMode(jk_logging.ColoredLogMessageFormatter.EnumOutputMode.FULL)



gen = jk_jsonschema.createObjectSchemaGenerator()
jsonSchema = gen.schema


schema = jk_jsonschema.SchemaParser.parse(gen.schema, log)





testData1 = {
	"abc": {
		"cde": "Hello, World!"
	}
}
testData2 = {
	"abc": {
		"cde": 123
	}
}
testData3 = {
	"abc": {
		"cdef": "Hello, World!"
	}
}

for testData in [ testData1, testData2, testData3 ]:
	print(schema.validate(testData))















