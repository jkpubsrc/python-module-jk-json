


import collections





Token = collections.namedtuple(
	"Token",
	[
		"type",
		"text",
		"sourceID",
		"lineNo",
		"charPos",
		"endLineNo",
		"endCharPos"
	]
)














