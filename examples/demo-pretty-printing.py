#!/usr/bin/env python3



import jk_json




FILE_NAME = "test-relaxed.json"

jData = jk_json.loadFromFile(FILE_NAME)

print("=" * 160)
jk_json.prettyPrint(jData, comment=[
	"-" * 80,
	"Pretty printed version of the data in file \"{}\"".format(FILE_NAME),
	"-" * 80,
])
print("=" * 160)


text = jk_json.prettyPrintToStr(jData, comment=[
	"-" * 80,
	"Pretty printed version of the data in file \"{}\"".format(FILE_NAME),
	"-" * 80,
])

jData2 = jk_json.loads(text)

print("Parsing again succeeded.")



