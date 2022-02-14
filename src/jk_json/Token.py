#!/usr/bin/env python3
# -*- coding: utf-8 -*-




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














