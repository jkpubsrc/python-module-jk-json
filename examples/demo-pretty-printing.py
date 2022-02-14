#!/usr/bin/env python3



import jk_json




FILE_NAME = "test-relaxed.json"

jData = jk_json.loadFromFile(FILE_NAME)

print("=" * 160)
jk_json.prettyPrint(jData)
print("=" * 160)


text = jk_json.prettyPrintToStr(jData)

jData2 = jk_json.loads(text)

print("Parsing again succeeded.")



