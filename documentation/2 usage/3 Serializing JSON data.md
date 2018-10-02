Serializing JSON data to string
===============================

Importing the module
--------------------

In order to serialize JSON data to a string you first need to import the `jk_json` module:

```python
import jk_json
```

Serializing JSON data to string
-------------------------------

For convenience there is a function that performs serializing so that this task is a one-liner:

```python
resultString = jk_json.dumps(myJsonObj)
```

The function `dumps()` supports two additional arguments:

* `indent` : A string value that is used for indentation. By default this is `None`. As a result the whole JSON data structure is serialized into a single line. Specify one or more character(s) here in order to get a more human readable output spanning over multiple lines.
* `sort_keys` : A boolean value to indicate if properties of objects (= keys of dictionaries) should be sorted before writing.

The result is a string.

This method behaves exactly as `dumps()` in the Python `json` package.

Serializing JSON data and write it to a file
--------------------------------------------

For convenience there is a function that performs serializing and writing so that this task is a one-liner:

```python
jk_json.saveToFile(myJsonObj, "myfile.json")
```

The function `saveToFile()` supports two additional arguments:

* `indent` : A string value that is used for indentation. By default this is `None`. As a result the whole JSON data structure is serialized into a single line. Specify one or more character(s) here in order to get a more human readable output spanning over multiple lines.
* `sort_keys` : A boolean value to indicate if properties of objects (= keys of dictionaries) should be sorted before writing.







