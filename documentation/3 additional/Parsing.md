Parsing
=======

Tokenizing
----------

The tokenizer follows a very simple architecture:

* It is state driven.
* Transitions are defined between states.
* Whenever the tokenizing automaton can follow a transition parsinig actions can be performed.

A variety of states may be defined for the tokenizer, each represented by a single - so called - tokenizing table. Such a table contains conditions. If any of the conditions match the current position in the input stream the tokenizer automaton performs the parsing actions. If no condition is matched the automaton executes default parsing actions. If EOS is encountered special default parsing actions can be executed.

Parsing actions include:
- clear the internal buffer
- append the matched element to the buffer
- emit a new token (based on the current buffer)
- switch to another tokenizing table (an such to another tokenizing state with - typically - quite different rules)
- advance in the stream ignoring the current element matched

So effectively the tokenizer will try to match the next characters in the stream, perform some parsing actions as putting data into the buffer, emitting the buffer, emitting the data encountered, advance through the stream and switch to different states. All these activities can be performed in any combination as defined by the user.

The advantage of this approach is a human readable tokenizer and a tokenizer that can be built on regular expressions in a modular way. By following this approach the tokenizer can easily be written and adapted.

Of course this comes with a drawback: The tokenizer will not be the fastest tokenizer possible.

Parsing
-------

For parsing a very simple grammar ist used. The parser is then implemented as a recursive descend hand made parser.

In order to simplify debugging of the parser each parsing rule is decorated with a debuging decorator that logs start and end of each method call. This log is printed to STDOUT in a hierarchical fashion so that you can study the parser's behaviour if needed.



