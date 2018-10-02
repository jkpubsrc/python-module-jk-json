Explanation

General
-------

Tokenization is performed by a simple state machine. This machine checks or pattern in the input stream, emits tokens based on these patterns and advances to the next pattern after that. In order to have a context dependent behaviour the machine can switch modes as necessary, processing different patterns as adequate in the current context.

Processing is done by looking at a character input stream provided. Either ...

* an defined character is matched,
* one character of a set of defined characters is matched,
* a regular expression is matched, or
* any character is matched.

The basic operation

Matching Operations
-------------------

| Command					| Code	|
|---------------------------|-------|
| exact string				| 1		|
| any character of string	| 2		|
| exact regex				| 3		|
| other						| -		|

Action Operations
-----------------

In order for easy design on each element eaten one or more of these actions can be performed:

| Command				| Code	| Description																						|
|-----------------------|-------|---------------------------------------------------------------------------------------------------|
| error str:xxx			| 1		| raise error message with text "xxx"																|
| advance				| 2		| the stream is advanced by the element matched														|
| mode int:xxx			| 3		| switch to table "xxx"																				|
| emitElement str:xxx	| 4		| emit a token; token type is "xxx", content is the current element matched							|
| appendElementToBuffer	| 5		| Append the current element to the buffer															|
| emitBuffer str:xxx	| 6		| emit a token; type is "xxx", content is the content of the buffer; afterwards: empty the buffer	|
| dropBuffer			| 7		| empty the buffer																					|







Concrete tokenizer implementation
=================================

States
------

* nrm
* instring
* instringmasked
* inlinecomment
* inblockcomment

Loops
-----

```
nrm

	loop:
		"\n"														->	emitElement "eol"; advance
		any:" \t"													->	emitElement "spc"; advance
		r"[+-]?0?\.[0-9]+([Ee][+-]?[1-9][0-9]+)?"					->	emitElement "f"; advance
		r"[+-]?[1-9][0-9]*(\.[0-9]+)?([Ee][+-]?[1-9][0-9]+)?"		->	emitElement "f"; advance
		r"[+-]?[1-9][0-9]*"											->	emitElement "i"; advance
		r"[+-]?0"													->	emitElement "i"; advance
		r"(//|#)"													->	emitElement "lcb"; advance; mode inlinecomment
		"/*"														->	emitElement "bcb"; advance; mode inblockcomment
		r"[a-zA-Z\._-][a-zA-Z0-9\._-]*"								->	emitElement "w"; advance
		"\""														->	advance; mode instring
		any:"_-+*~#'`!§$%&/()[]{}=?\\,.;:<>|"						->	emitElement "d"; advance
		other														->	error "Syntax error"
	eos:
		emit "eos"
```

```
inlinecomment

	loop:
		"\n"														->	emitBuffer "lcd"; mode nrm
		other														->	advance; appendElementToBuffer
	eos:
		emitBuffer "lcd"; mode nrm
```

```
inblockcomment

	loop:
		"*/"														->	emitBuffer "bc"; emitElement "bce"; advance; mode nrm
		other														->	advance; appendElementToBuffer
	eos:
		error "Syntax error"
```

```
instring

	loop:
		"\""														->	emitBuffer "str"; advance; mode nrm
		"\\"														->	advance; mode instringmasked
		other														->	advance; appendElementToBuffer
	eos:
		error "Syntax error"
```

```
instringmasked
	loop:
		"\\"														->	addToBuffer "\\"; advance; mode instring
		"n"															->	addToBuffer "\n"; advance; mode instring
		"t"															->	addToBuffer "\t"; advance; mode instring
		"r"															->	addToBuffer "\r"; advance; mode instring
		other														->	error "Syntax error"
	eos:
		error "Syntax error"
```







