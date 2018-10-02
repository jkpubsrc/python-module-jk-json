Loading and parsing of JSON strings
===================================

Importing the module
--------------------

In order to parse JSON data provided as a string you first need to import the `jk_json` module:

```python
import jk_json
```

Parsing a JSON strings
----------------------

For convenience there is a function that performs parsing so that this task is a one-liner:

```python
jsonData = jk_json.loads("{'someKey':123,'anotherKey':true}")
```

The function `loads()` supports two additional arguments:

* `bStrict` : A boolean value to force parsing in strict mode. This is not the default: The default value of `true` enables parsing in a specific more relaxed mode, where comments within the file, Infinitiy and NaN is supported.
* `bDebugging` : A boolean value to enable writing of debug information during parsing. This is required for development and you will likely not want to modify the default value, which is `False`.

The result is a data structure - according to the contents of the JSON file - of one of the following types:

* `None`
* `bool`
* `int`
* `float`
* `str`
* `list`
* `dict`

This method behaves similar to `loads()` in the Python `json` package.

Loading and parsing a JSON file
-------------------------------

For convenience there is a function that performs loading and parsing so that this task is a one-liner:

```python
jsonData = jk_json.loadFromFile("myfile.json")
```

The function `loadFromFile()` supports two additional arguments:

* `bStrict` : A boolean value to force parsing in strict mode. This is not the default: The default value of `true` enables parsing in a specific more relaxed mode, where comments within the file, Infinitiy and NaN is supported.
* `bDebugging` : A boolean value to enable writing of debug information during parsing. This is required for development and you will likely not want to modify the default value, which is `False`.

The result is a data structure - according to the contents of the JSON file - of one of the following types:

* `None`
* `bool`
* `int`
* `float`
* `str`
* `list`
* `dict`







