JSON Grammar
============



Strict JSON
-----------


```
S			=		JANYVALUE

JOBJECT		=		"{"		JPROPERTY_LIST?		"}"

JARRAY		=		"["		JVALUE_LIST?		"]"

JPROPERTY	=		<string>		":"		JANYVALUE

JANYVALUE	=		"null"
			|		"true"
			|		"false"
			|		"-Infinity"
			|		"Infinity"
			|		"NaN"
			|		<string>
			|		<float>
			|		<integer>
			|		JARRAY
			|		JOBJECT

JVALUE_LIST	=	JANYVALUE	[	","		JANYVALUE	]*

JPROPERTY_LIST	=	JPROPERTY	[	","		JPROPERTY	]*
```





Relaxed JSON
------------


```
S			=		JANYVALUE

JOBJECT		=		"{"		JPROPERTY_LIST?		"}"

JARRAY		=		"["		JVALUE_LIST?		"]"

JPROPERTY	=		<string>		":"		JANYVALUE

JANYVALUE	=		"null"
			|		"true"
			|		"false"
			|		"-Infinity"
			|		"Infinity"
			|		"NaN"
			|		<string>
			|		<float>
			|		<integer>
			|		JARRAY
			|		JOBJECT

JVALUE_LIST	=	JANYVALUE	[	","		JANYVALUE	]*		","?

JPROPERTY_LIST	=	JPROPERTY	[	","		JPROPERTY	]*		","?
```

In relaxed mode ...

* ... single or double quotes can be used
* ... comments are allowed at any time




















