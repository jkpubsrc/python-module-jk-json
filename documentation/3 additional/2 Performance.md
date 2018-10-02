Performance
===========

Prerequisites
-------------

Test data is recorded using ```cProfile```.

Evaluation of tests can be performed with this tool: https://jiffyclub.github.io/snakeviz/

Testing
-------

For testing the following JSON file has been used:

```JavaScript

{
	"bla": 123,
	"blubb": [
		2345,
		-678,
		3.1415927,
		-2e-10,
		"abc",
		"def\n\u0040",
		null,
		true,
		false,
		[],
		{},
		123,
		[
			"The quick brown fox jumps over the lazy dog.",
			"THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG."
		]
	]
}

```

Results
-------

The following performance results have been achieved single threaded with Python 3.6 on a Intel(R) Core(TM) i5-6440HQ CPU @ 2.60GHz:

| Parser name				| Parsing duration in seconds for 20.000 files			|
|---------------------------|-------------------------------------------------------|
| Builtin `json`			| 0.08207602298352867									|
| Module `jk_json`			| 1.0654626390023623									|

Discussion
----------

Parsing JSON data with this tool is much slower than the builtin python JSON parser. It is about 12.9 times slower than the native implementation.

The tokenization process itself is quite fast, about 10 times as fast as the actual parsing attempt. The python implementation is quite efficient. Only slight improvements might be expected in optimizing some regular expressions.

But the parsing process is quite slow as this parser attempts to perform numerous different approaches to find the correct parse tree. It is a recursive descent parser. Different grammar based implementations would be required in order to improve on that.

Performance can be increased slightly if the debugging-decorators in the code are removed from the parsing methods by an additional ```0.3``` for the performance factor. As this is only a minor increase we can well live with some debugging support at the moment.

Nevertheless you will be able to parse round about ten thousand small real world JSON files per second. In regular situations ```jk_json``` should perform well enough.

Future Work
-----------

Taking everything into account the most important future task would be to implement a table driven parser based on the JSON grammar. Unfortunately this is beyond what I, the (current) author of this module, is willing to do. Parsing works well and with acceptable speed. Though I would be quite happy to improve performance here I personally don't have any use case where such an improvement would really make a difference. It would take a considerable amount of time to build a table driven parser. Time which I won't spend for now on that topic as long as I'm a "one-man-show" with this and other open source libraries and modules. I think this time is better spent on other tasks and other open source projects.

Nevertheless if you'd like to pick up on that task yourself and build a more efficient parser, please contact to me. I'll assist you in any way I can so that you can get the work done. I'll be very happy to work together with others on that topic!
























