#!/usr/bin/env python3


import jk_json.tools


print(jk_json.tools.jsonIsEqual)




print(jk_json.tools.jsonIsEqual(
	3,
	3
	))


print(jk_json.tools.jsonIsEqual(
	"abc",
	"abc"
	))


print(jk_json.tools.jsonIsEqual(
	None,
	None
	))


print(jk_json.tools.jsonIsEqual(
	["a", "b"],
	["a", "b"]
	))


print(jk_json.tools.jsonIsEqual(
	{"a": "b", "c": 4},
	{"a": "b", "c": 4},
	))

print(jk_json.tools.jsonIsEqual(
	[],
	[],
	))

print(not jk_json.tools.jsonIsEqual(
	[],
	[ 1 ],
	))

print(not jk_json.tools.jsonIsEqual(
	[],
	[ {} ],
	))

print(not jk_json.tools.jsonIsEqual(
	[ [] ],
	[ {} ],
	))







