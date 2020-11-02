#!/usr/bin/python3

import jk_json
import jk_jsonschema

jsonData = {
	"abc": "defghijk",
	"cde": 123
}

gen = jk_jsonschema.createObjectSchemaGenerator()
gen.strValue("abc")
gen.intValue("cde")
jsonSchemaData = gen.schema

jsonValidator = jk_jsonschema.parse(jsonSchemaData)
jsonValidator.validateE(jsonData)







