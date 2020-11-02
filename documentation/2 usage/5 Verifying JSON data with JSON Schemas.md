Verifying JSON data with JSON Schemas
=====================================

Importing the module
--------------------

In order to verify a JSON object against a JSON schema you first need to import the `jk_jsonschema` module:

```python
import jk_jsonschema
```

Please have in mind that if parsing of JSON data is necessary you might want to import the module `jk_json` as well.

Parse a provided JSON schema
----------------------------

In order to be able to use a schema, you must provide a schema data structure and parse it using the function `parse()`:

```python
jsonSchemaData = {'type':'number','minimum':1}
jsonValidator = jk_jsonschema.parse(jsonSchemaData)
```

The function `parse()` supports one additional arguments:

* `log` : A log object from the Python module `jk_logging`. This is optional and primarily ment for debugging purposes. But if you choose to provide a logger here, you are required to use an instance of `jk_logging` as the parser will rely on some specific logging features only the module `jk_logging` provides.

The JSON validator then can be used later to validate a JSON object. (See below.)

Load a JSON schema from a string
--------------------------------

For convenience a function is provided that enables you to load a JSON schema directly from a JSON string using the function `loads()`:

```python
jsonText = "{'type':'number','minimum':1}"
jsonValidator = jk_jsonschema.loads(jsonText)
```

The function `loads()` supports one additional arguments:

* `log` : A log object from the Python module `jk_logging`. This is optional and primarily ment for debugging purposes. But if you choose to provide a logger here, you are required to use an instance of `jk_logging` as the parser will rely on some specific logging features only the module `jk_logging` provides.

The JSON validator then can be used later to validate a JSON object. (See below.)

Load a JSON schema from file
----------------------------

For convenience a function is provided that enables you to load a JSON schema directly from a JSON file using the function `loadFromFile()`:

```python
jsonValidator = jk_jsonschema.loadFromFile("myschema.json")
```

The function `loadFromFile()` supports one additional arguments:

* `log` : A log object from the Python module `jk_logging`. This is optional and primarily ment for debugging purposes. But if you choose to provide a logger here, you are required to use an instance of `jk_logging` as the parser will rely on some specific logging features only the module `jk_logging` provides.

The JSON validator then can be used later to validate a JSON object. (See below.)

Validating JSON data with a loaded JSON schema
----------------------------------------------

After you've created a schema object using one of the functions `jk_jsonschema.parse()`, `jk_jsonschema.loads()` or `jk_jsonschema.loadFromFile()` you can then verify an arbitrary JSON object if it matches this schema. For this you have three options:

* Using the method `validate(jsonData) -> bool`, which will return either `True` or `False` as the validation result.
* Using the method `validate2(jsonData) -> bool`, which will return a tuple of two values:
	* Either `True` or `False` as the validation result.
	* Either `None` or a list of tuples.
* Using the method `validateE(jsonData)`, which will return nothing but raise en Exception on error.
		
If there was an error you can use the tuples provided in the list returned by `validate2()` to get more details what exactly went wrong during validation. In this case the topmost entry might be the most expressive one regaring the validation error.

Such a tuple will have the following structure:
* First item: A path giving a hint where the schema violation occurred within the JSON document tested.
* Second item: A primitive value or `None` if inapplicable. If a value is provided here this was the value that caused the violation of schema rules.
* Third item: A string in English that provides a human readable error message. This is a message you might want to display to the end user.

The method `validateE()` will internally invoke `validate2()` to obtain error data. From this error data the error message within the exception raised is constructed of by `validateE()`.

Examples
--------

Example where everything loaded from files:

```python
import jk_json
import jk_jsonschema

jsonData = jk_json.loadFromFile("myjsonfile.json")

jsonValidator = jk_jsonschema.loadFromFile("myjsonschema.json")
jsonValidator.validateE(jsonData)
```

Example where everything is generated on the fly:

```python
import jk_json
import jk_jsonschema

jsonData = {
	"abc": "defghijk",
	"cde": 123
}

gen = jk_jsonschema.createObjectSchemaGenerator()
gen.strValue("abc")
gen.intValue("cde")
jsonSchemaData = gen.schema

jsonValidator = jk_jsonschema.parse(jsonSchemaData)
jsonValidator.validateE(jsonData)
```



