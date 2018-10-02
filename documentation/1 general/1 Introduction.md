Introduction
============

This is a JSON library which performs loading and parsing of JSON strings or files quite similar to Python's built in JSON parser.

The JSON data format
--------------------

JSON is a data format. It is used to represent data and store it in (text) files. While it has it's origins in the JavaScript world, it nowadays is used in a wide range of applications far beyond the JavaScript realm.

To give you an idea here is an example. This is JSON:

```JavaScript
{
	'someKey': 12.345678,
	'anotherDictionary': {
		'anotherKey': 'This is a string',
		'evenAnotherKey': [
			'and',
			'some',
			'list',
			'items',
			123,
			true
		]
	} 
}
```

If you want to read this kind of data from a file and use it within a computer program you need a parser to analyse the text and transform it to elementary data values. This implementation `jk_json` exactly does that.

More information about JSON can be found here:

* https://tools.ietf.org/html/rfc7159
* https://www.json.org/

Why this JSON Parser Implementation
-----------------------------------

Python already provides a default JSON parser implementation in the `json` module. Why another implementation if there already is one? For several reasons:

* If parsing fails it is often quite obscure where the actual error in the JSON file originates from. The default JSON parser provided by Python often does not give human readable information about the error situation. This JSON parser does.
* For JSON configuration files it is sometimes quite useful to have comments within these files. For example if you provide configuration data to software using the JSON file format having comments might really be convenient. But this exceeds the JSON standard and therefore Python's default JSON parser does not accept comments in JSON files though. This parser does.

Regarding comments there is another JSON parser out in the wild named `jsoncomment`. The author of these lines used it for quite some time. Unfortunately this parser is a hack, using regular expressions in strings before normal JSON parsing is performed. And to the knowledge of the author this parser is abandoned. Especially as `jsoncomment` is a hack and not a real parser and sometimes doesn't parse correctly, the author of these lines once upon a time decided to build a new and better one from scratch take a correct and much more sophisticated approach. This parser `jk_json` is the result.

Recommendation of Use
---------------------

So if you want to make use of these features this JSON parser is the right one to use. But there is a drawback: As this parser is written completely in Python it is slower than Python's built-in JSON parser: The native Python parser is about twice as fast as this implementation. So if you require an absolute maximum of performance in parsing JSON - f.e. if you need to load millions of large JSON files to process large amount of data - you might want to use the built-in parser instead. But if an absolute maximum of speed is not your focus - you still can load tens of thousands of JSON files in a single second with this parser - and find the features offered by this parser quite appealing you might want to give it a try.

State of Development
--------------------

The current state of development: Release. Only the schema parser ist Beta.

For details please have a look to section `Current State of Development`.

License
-------

This parser is provided under the Apache License 2.0. It therefor is compatible with private and commercial use.

As it took quite a lot of time and effort for this parser to achieve this level of quality and speed you might want to consider spending a small amount of money to the author of this software. Thank you.










