Building Schemas with the Simple Schema Generator
=================================================

Importing the modules
---------------------

In order to generate a schema with the simple schema genereator you first need to import the `jk_jsonschema` module:

```python
import jk_jsonschema
```

Create a Schema Generator 
-------------------------

In order to produce schemas you need to instantiate a schema generator first. This is done with the following Python code:

```python
gen = jk_jsonschema.createObjectSchemaGenerator()
```

Note: This function will provide an object for schema generation. As possibly maybe sometimes there might be different implementations in the future, all generation of objects is performed by this method. Please always use this factory method as it will be adapted to future implementations if necessary.

Define the Expectations
------------------------

After having generated a schema generator you can use it to define your schemas.

This default schema generator assumes you want to produce a schema matching an object with certain keys and values. This generator is - by default - of type `ObjectGenerator`.

### ObjectGenerator

The object generator provides the following methods:

* `objectValue(name:str, bRequired:bool) -> ObjectGenerator`
	* Expect the current object matched later by the schema to have a key with name `name`.
	* Depending on `bRequired` this key later on is required or optional.
	* The value of this key should again be an **object**.
* `intValue(name:str, bRequired:bool) -> IntegerGenerator`
	* Expect the current object matched later by the schema to have a key with name `name`.
	* Depending on `bRequired` this key later on is required or optional.
	* The value of this key should be an **integer value**.
* `floatValue(name:str, bRequired:bool) -> FloatGenerator`
	* Expect the current object matched later by the schema to have a key with name `name`.
	* Depending on `bRequired` this key later on is required or optional.
	* The value of this key should be a **float or an integer value**.
* `boolValue(name:str, bRequired:bool) -> BooleanGenerator`
	* Expect the current object matched later by the schema to have a key with name `name`.
	* Depending on `bRequired` this key later on is required or optional.
	* The value of this key should be a **boolean value**.
* `strValue(name:str, bRequired:bool) -> StringGenerator`
	* Expect the current object matched later by the schema to have a key with name `name`.
	* Depending on `bRequired` this key later on is required or optional.
	* The value of this key should be a **string value**.
* `listValue(name:str, listType:type, bRequired:bool) -> ListGenerator`
	* Expect the current object matched later by the schema to have a key with name `name`.
	* Depending on `bRequired` this key later on is required or optional.
	* The value of this key should be a **list**.
	* The argument `listType` expects a Python type object to be specified. This must be one of the following types:
		* `bool`
		* `int`
		* `float`
		* `str`
		* `dict`

All methods return a new generator object.

For convenience the object generator can be used in a `with` context. Example:

```python
with gen.objectValue("abc") as c:
	c.strValue("cde")
```

The code above has the following meaning:
* An object is expected. (Objects are always expected by default).
* Then this object must have an `abc` key (=> `objectValue()`, no `bRequired=False` is specified).
* For this key another object is expected (=> `objectValue()`).
* This value object at this key must itself have a key named `cde` (=> `strValue()`).
* At this key a value of type *string* (=> `strValue()`) must be provided.

### BooleanGenerator

The boolean generator provides the following methods:

* `required() -> self`
	* Change the expectation: If invoked the current component of the data structure verified later **is required**. This is equivalent to providing `True` in `bRequired` during a method call to receive this generator.
* `notRequired() -> self`
	* Change the expectation: If invoked the current component of the data structure verified later **is not required**. This is equivalent to providing `False` in `bRequired` during a method call to receive this generator.

### IntegerGenerator

The integer generator provides the following methods:

* `required() -> self`
	* Change the expectation: If invoked the current component of the data structure verified later **is required**. This is equivalent to providing `True` in `bRequired` during a method call to receive this generator.
* `notRequired() -> self`
	* Change the expectation: If invoked the current component of the data structure verified later **is not required**. This is equivalent to providing `False` in `bRequired` during a method call to receive this generator.
* `minimum(minimum:int) -> self`
	* Expect the current integer value later to be **greater or equal to** the value specified.
	* The method will return the genator object you invoked this method on for your convenience so that you can immediately invoke other methods if required.
* `exclusiveMinimum(minimum:int) -> self`
	* Expect the current integer value later to be **greater than** the value specified.
	* The method will return the genator object you invoked this method on for your convenience so that you can immediately invoke other methods if required.
* `maximum(maximum:int) -> self`
	* Expect the current integer value later to be **smaller or equal to** the value specified.
	* The method will return the genator object you invoked this method on for your convenience so that you can immediately invoke other methods if required.
* `exclusiveMaximum(maximum:int) -> self`
	* Expect the current integer value later to be **smaller than** the value specified.
	* The method will return the genator object you invoked this method on for your convenience so that you can immediately invoke other methods if required.
* `allowedValues(allowedValues:list[int]) -> self`
	* Expect the current integer value later to be one of the speficied values.
	* The method will return the genator object you invoked this method on for your convenience so that you can immediately invoke other methods if required.

Example:

```python
gen.intValue("abc").minimum(123).maximum(234)
```

The code above has the following meaning:
* An object is expected. (Objects are always expected by default).
* Then this object must have an `abc` key (=> `intValue()`, no `bRequired=False` is specified).
* For this key an integer value is expected (=> `intValue()`).
* This value must be greater or equal to `123` (=> `minimum()`) and lower or equal to `234` (=> `maximum()`)

### FloatGenerator

The float generator provides the following methods:

* `required() -> self`
	* Change the expectation: If invoked the current component of the data structure verified later **is required**. This is equivalent to providing `True` in `bRequired` during a method call to receive this generator.
* `notRequired() -> self`
	* Change the expectation: If invoked the current component of the data structure verified later **is not required**. This is equivalent to providing `False` in `bRequired` during a method call to receive this generator.
* `minimum(minimum:int) -> self`
	* Expect the current float or integer value later to be **greater or equal to** the value specified.
	* The method will return the genator object you invoked this method on for your convenience so that you can immediately invoke other methods if required.
* `exclusiveMinimum(minimum:int) -> self`
	* Expect the current float or integer value later to be **greater than** the value specified.
	* The method will return the genator object you invoked this method on for your convenience so that you can immediately invoke other methods if required.
* `maximum(maximum:int) -> self`
	* Expect the current float or integer value later to be **smaller or equal to** the value specified.
	* The method will return the genator object you invoked this method on for your convenience so that you can immediately invoke other methods if required.
* `exclusiveMaximum(maximum:int) -> self`
	* Expect the current float or integer value later to be **smaller than** the value specified.
	* The method will return the genator object you invoked this method on for your convenience so that you can immediately invoke other methods if required.
* `allowedValues(allowedValues:list[float]) -> self`
	* Expect the current float or integer value later to be one of the speficied values.
	* The method will return the genator object you invoked this method on for your convenience so that you can immediately invoke other methods if required.

Example:

```python
gen.floatValue("abc").minimum(12.3).maximum(23.4)
```

The code above has the following meaning:
* An object is expected. (Objects are always expected by default).
* Then this object must have an `abc` key (=> `floatValue()`, no `bRequired=False` is specified).
* For this key an integer or float value is expected (=> `floatValue()`).
* This value must be greater or equal to `12.3` (=> `minimum()`) and lower or equal to `23.4` (=> `maximum()`)

### StringGenerator

The string generator provides the following methods:

* `required() -> self`
	* Change the expectation: If invoked the current component of the data structure verified later **is required**. This is equivalent to providing `True` in `bRequired` during a method call to receive this generator.
* `notRequired() -> self`
	* Change the expectation: If invoked the current component of the data structure verified later **is not required**. This is equivalent to providing `False` in `bRequired` during a method call to receive this generator.
* `minLength(minLength:int) -> self`
	* Expect the current string value later to be **greater or equal in length** to the value specified here.
	* The method will return the genator object you invoked this method on for your convenience so that you can immediately invoke other methods if required.
* `maxLength(maxLength:int) -> self`
	* Expect the current string value later to be **lower or equal in length** to the value specified here.
	* The method will return the genator object you invoked this method on for your convenience so that you can immediately invoke other methods if required.
* `regexPattern(regexPattern:str) -> self`
	* Expect the current string value to match this regular expression pattern specified.
	* The method will return the genator object you invoked this method on for your convenience so that you can immediately invoke other methods if required.
* `allowedValues(allowedValues:list[str]) -> self`
	* Expect the current string value later to be one of the speficied values.
	* The method will return the genator object you invoked this method on for your convenience so that you can immediately invoke other methods if required.

Example:

```python
gen.strValue("abc").minLength(2).maxLength(4)
```

The code above has the following meaning:
* An object is expected. (Objects are always expected by default).
* Then this object must have an `abc` key (=> `strValue()`, no `bRequired=False` is specified).
* For this key a string value is expected (=> `strValue()`).
* This value must be have a length greater or equal to `2` (=> `minLength()`) and lower or equal to `4` (=> `maxLength()`)

### ListGenerator

The list generator provides the following methods:

* `required() -> self`
	* Change the expectation: If invoked the current component of the data structure verified later **is required**. This is equivalent to providing `True` in `bRequired` during a method call to receive this generator.
* `notRequired() -> self`
	* Change the expectation: If invoked the current component of the data structure verified later **is not required**. This is equivalent to providing `False` in `bRequired` during a method call to receive this generator.
* `minLength(minLength:int) -> self`
	* Expect the list matched later to be **greater or equal in length** to the value specified here.
	* The method will return the genator object you invoked this method on for your convenience so that you can immediately invoke other methods if required.
* `maxLength(maxLength:int) -> self`
	* Expect the list match later to be **lower or equal in length** to the value specified here.
	* The method will return the genator object you invoked this method on for your convenience so that you can immediately invoke other methods if required.
* `allowedValues(allowedValues:list[*]) -> self`
	* Expect the list items to be of the speficied values.
	* The method will return the genator object you invoked this method on for your convenience so that you can immediately invoke other methods if required.

The list generator provides the following properties:

* `dataType -> AbstractGenerator`
	* The `dataType` property provides a generator object. It's type depends on your type argument provided during creation of this list generator. It can be used to modify expectations about the list items.

Example:

```python
gen.listValue("abc", int).minLength(2).dataType.minimum(123)
```

The code above has the following meaning:
* An object is expected. (Objects are always expected by default).
* Then this object must have an `abc` key (=> `listValue()`, no `bRequired=False` is specified).
* For this key a list is expected (=> `listValue()`). Each list item must be of type `int` (=> `listValue()`)
* This list must be have a length greater or equal to `2` (=> `minLength()`).
* Each integer list value must be greater or equal to `123` (=> `minimum()`)

### Complex Example

```python
with gen.objectValue("abc") as c:
	c.strValue("cde")
```

Produce the JSON Schema
-----------------------

Now finally after having defined all expectations of the objects we want to match we can produce a schema for matching JSON objects against this schema later:

```python
theSchema = gen.schema
```

`schema` is a property provided by the generator. It returns a JSON object which in this example is stored in a variable named `theSchema`.

TODO
See "Verifying JSON data with JSON Schemas" for details about how to perform a verification.











