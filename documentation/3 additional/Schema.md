JSON Schema Validation
======================

Current draft: https://tools.ietf.org/html/draft-handrews-json-schema-validation-01

Test cases: https://github.com/json-schema-org/JSON-Schema-Test-Suite/

Status
------

334 test cases are processed successfully.

Comments to Test Cases Failing
------------------------------

* uniode processing is different in very specific aspects so that some test cases relying on these Unicode aspects fail; this is a Python specific problem related to Python's interpretation of Unicode in strings
* mathmatical calculations in Python might result in floating point inaccuracies so that "multipleOf" sometimes can't be validated correctly on small floating point numbers
* "default" is not supported
* "definitions" is not supported
* "ref" is not supported

JSON-Validators according to specification
==========================================

According to the JSON schema specification there are the following validators:

* **type** *str|str[]* : The value to verify must be of one of the specified type identifiers. Valid type identifiers are: "null", "boolean", "object", "array", "number", "integer", "string"
* **enum** *any[]* : The value to verify must be equal to one of these values.
* **const** *any* : The value to verify must be of this type.

* **multipleOf** *float|int* : If the value to verify is a numeric value it must be a multiple of the reference number.
* **minimum** *float|int* : If the value to verify is a numeric value it must be greater than or equal to the reference number.
* **maximum** *float|int* : If the value to verify is a numeric value it must be smaller than or equal to the reference number.
* **exclusiveMinimum** *float|int* : If the value to verify is a numeric value it must be greater than the reference number.
* **exclusiveMaximum** *float|int* : If the value to verify is a numeric value it must be smaller than the reference number.

* **minLength** *int* : If the value to verify is a string its length must not be smaller than the reference number.
* **maxLength** *int* : If the value to verify is a string its length must not be greater than the reference number.
* **pattern** *regexstr* : If the value to verify is a string it must conform to the specified regular expression.

* **items** *schema* : If the value to verify is an array all of its items must conform to the reference schema.
* **items** *schema[]* : If the value to verify is an array all of its items must conform to the reference schemata. That implies that the array length exactly matches the number of schemata specified. If the array is larger than the number of reference schemata "additionalItems" must be applied. If no "additionalItems" is specified this is an error.
* **additionalItems** *schema* : "items schema[]" must be applied first. The rest of the array items must match against the reference schema.
* **additionalItems** *schema[]* : "items schema[]" must be applied first. The rest of the array items must match against the reference schemata. That implies that the remaining array length must exactly match the number of reference schemata specified.
* **minItems** *int* : If the value to verify is an array its length must not be lower than the reference number.
* **maxItems** *int* : If the value to verify is an array its length must not be greater than the reference number.
* **uniqueItems** *bool* : If the value to verify is an array all items within the array must be unique.
* **contains** *schema* : If the value to verify is an array at least one item within the array must validate against the specified schema.

* **minProperties** *int* : If the value to verify is an object its size must not be lower than the reference number.
* **maxProperties** *int* : If the value to verify is an object its size must not be greater than the reference number.
* **required** *str[]* : If the value to verify is an object it must have all of the properties specified.
* **properties** *dict<str,schema>* : If the value to verify is an object and there is a property of a corresponding name with the key in the reference dictionary that property's value must validate against the specified schema.
* **patternProperties** *dict<regexstr,schema>* : If the value to verify is an object and there is a property with a name in that dictionary matching one of the regular expressions in the reference dictionary that property's value must validate against the specified schema.
* **additionalProperties** *schema* : If the value to verify is an object and a property did neither match any keys in "properties" nor any key in "patternProperties" the values of these properties then must validate successfully against the referenced schema here in "additionalProperties".
* **dependencies** *dict<str,schema|str[]>* : If the value to verify is an object and has properties found in this reference dictionary the rules defined as values of this reference dictionary apply to the current object to verify. If the values is a string list the list items name properties that must exist in the object to verify. If the value is an object this value must be schema to evaluate the current object against.
* **propertyNames** *schema* : If the value to verify is an object every property name in that dictionary must evaluate against the specified schema.

* **if** *schema*
* **then** *schema*
* **else** *schema*
* **allOf** *schema[]* : The value to verify must evaluate successfully against all of the reference schemata.
* **anyOf** *schema[]* : The value to verify must evaluate successfully against at least one of the reference schemata.
* **oneOf** *schema[]* : The value to verify must evaluate successfully against exactly one of the reference schemata.
* **not** *schema*

Formal semantic pseudo-code definition of the JSON-Validators
=============================================================

According to the JSON schema specification there are the following validators:

* **type** *str|str[]* : The value to verify must be of one of the specified type identifiers. Valid type identifiers are: "null", "boolean", "object", "array", "number", "integer", "string"
	* if <testvalue> is of type <reftypeidentifier>
		* => false
* **enum** *any[]* : The value to verify must be equal to one of these values.
	* if <testvalue> not in <refarray>
		* => false
* **const** *any* : The value to verify must be of this value.
	* if <testvalue> == <refvalue>
		* => true
	* else
		* => false

* **multipleOf** *float|int* : If the value to verify is a numeric value it must be a multiple of the reference number.
	* if <testvalue> is of type "float" or "float"
		* if <testvalue> modulo <refvalue> != 0
			* => false
* **minimum** *float|int* : If the value to verify is a numeric value it must be greater than or equal to the reference number.
	* if <testvalue> is of type "float" or "float"
		* if <testvalue> < <refvalue>
			* => false
* **maximum** *float|int* : If the value to verify is a numeric value it must be smaller than or equal to the reference number.
	* if <testvalue> is of type "float" or "float"
		* if <testvalue> > <refvalue>
			* => false
* **exclusiveMinimum** *float|int* : If the value to verify is a numeric value it must be greater than the reference number.
	* if <testvalue> is of type "float" or "float"
		* if <testvalue> <= <refvalue>
			* => false
* **exclusiveMaximum** *float|int* : If the value to verify is a numeric value it must be smaller than the reference number.
	* if <testvalue> is of type "float" or "float"
		* if <testvalue> >= <refvalue>
			* => false

* **minLength** *int* : If the value to verify is a string its length must not be smaller than the reference number.
	* if <testvalue> is of type "string"
		* if length(<testvalue>) < <refvalue>
			* => false
* **maxLength** *int* : If the value to verify is a string its length must not be greater than the reference number.
	* if <testvalue> is of type "string"
		* if length(<testvalue>) > <refvalue>
			* => false
* **pattern** *regexstr* : If the value to verify is a string it must conform to the specified regular expression.
	* if <testvalue> is of type "string"
		* if not <refregex>.match(<testvalue>)
			* => false

* **items** *schema* : If the value to verify is an array all of its items must conform to the reference schema.
	* if <testvalue> is of type "array"
		* for <testitem> in <testvalue>:
			* if <testitem> does not validate against <refschema>
				* => false
* **items** *schema[]* : If the value to verify is an array all of its items must conform to the reference schemata. That implies that the array length exactly matches the number of schemata specified. If the array is larger than the number of reference schemata "additionalItems" must be applied. If no "additionalItems" is specified this is an error.
	* if <testvalue> is of type "array"
		* if <items>:
			* if length(<testvalue>) < length(<refschemata>)
				=> false
			* if length(<testvalue>) > length(<refschemata>)
				* n = length(<refschemata>)
				* <additionalTestItems> = <testvalue>.subarray(n)
				* <testvalue> = <testvalue>.subarray(0, n)
			* for <testitem>, <testschema> in zip(<testvalue>, <refschemata>)
				* if <testitem> does not validate against <testschema>
					* => false
* **additionalItems** *schema* : "items schema[]" must be applied first. The rest of the array items must match against the reference schema.
	* if <additionalTestItems>
		* for <testitem> in zip(<additionalTestItems>)
			* if <testitem> does not validate against <refschema>
				* => false
* **additionalItems** *schema[]* : "items schema[]" must be applied first. The rest of the array items must match against the reference schemata. That implies that the remaining array length must exactly match the number of reference schemata specified.
	* if <additionalTestItems>
		* for <testitem>, <testschema> in zip(<additionalTestItems>, <refschemata>)
			* if <testitem> does not validate against <testschema>
				* => false
* **minItems** *int* : If the value to verify is an array its length must not be lower than the reference number.
	* if <testvalue> is of type "array"
		* if length(<testvalue>) < <refvalue>
			* => false
* **maxItems** *int* : If the value to verify is an array its length must not be greater than the reference number.
	* if <testvalue> is of type "array"
		* if length(<testvalue>) > <refvalue>
			* => false
* **uniqueItems** *bool* : If the value to verify is an array all items within the array must be unique.
	* if <testvalue> is of type "array"
		* if <refvalue> is true
			* for <a,b> in allPairs(<testvalue>)
				* if <a> == <b>
					* => false
* **contains** *schema* : If the value to verify is an array at least one item within the array must validate against the specified schema.
	* if <testvalue> is of type "array"
		* for <testitem> in <testvalue>
			* if <testitem> does not validate against <refschema>
				* => false

* **minProperties** *int* : If the value to verify is an object its size must not be lower than the reference number.
	* if <testvalue> is of type "object"
		* if length(<testvalue>) < <refvalue>
			* => false
* **maxProperties** *int* : If the value to verify is an object its size must not be greater than the reference number.
	* if <testvalue> is of type "object"
		* if length(<testvalue>) > <refvalue>
			* => false
* **required** *str[]* : If the value to verify is an object it must have all of the properties specified.
	* if <testvalue> is of type "object"
		* for <propertyname> in <testvalue>
			* if <propertyname> not in <reflist>
				* => false
* **properties** *dict<str,schema>* : If the value to verify is an object and there is a property of a corresponding name with the key in the reference dictionary that property's value must validate against the specified schema.
	* if <testvalue> is of type "object"
		* if <propertyname> in <refdict>
			* <refdata> = <refdict>.get(<propertyname>)
			* if <refdata> is of type "string":
				* if <refdata> not in <testvalue>
					* => false
			* else
				* if <refdata> does not validate against <testvalue>
					* => false
* **patternProperties** *dict<regexstr,schema>* : If the value to verify is an object and there is a property with a name in that dictionary matching one of the regular expressions in the reference dictionary that property's value must validate against the specified schema.
	* if <testvalue> is of type "object"
		* <tempAdditionalProperties> = <testvalue>.allPropertyNames()
		* if <patternProperties>
			* for <propertyname>, <propertyvalue> in <testvalue>.items()
				* if <refregexkey>.match(<propertyname>)
					* <tempAdditionalProperties>.remove(<propertyname>)
					* if <refschema> does not validate against <propertyvalue>
						* => false
		* else
			* <tempAdditionalProperties> = <testvalue>.keys()
* **additionalProperties** *schema* : If the value to verify is an object and a property did neither match any keys in "properties" nor any key in "patternProperties" the values of these properties then must validate successfully against the referenced schema here in "additionalProperties".
	* if <testvalue> is of type "object"
		* for <propertyName> in <tempAdditionalProperties>
			* if <propertyName> in <testvalue>
				* if <refschema> does not validate against <testvalue>.get(<propertyName>)
					* => false
* **dependencies** *dict<str,schema|str[]>* : If the value to verify is an object and has properties found in this reference dictionary the rules defined as values of this reference dictionary apply to the current object to verify. If the values is a string list the list items name properties that must exist in the object to verify. If the value is an object this value must be schema to evaluate the current object against.
* **propertyNames** *schema* : If the value to verify is an object every property name in that dictionary must evaluate against the specified schema.
	* if <testvalue> is of type "object"
		* for <propertyName> in <testvalue>
			* if <refschema> does not validate against <propertyName>
				* => false

* **if** *schema*
	* if <currentschema> has <thenschema> or has <elseschema>
		* if <refschema> validates against <testvalue>
			* validate <thenschema> against <testvalue>
		* else
			* validate <elseschema> against <testvalue>
* **then** *schema*
* **else** *schema*
* **allOf** *schema[]* : The value to verify must evaluate successfully against all of the reference schemata.
	* for <refschema> in <refschemata>
		* if <refschema> does not validate against <testvalue>
			* => false
* **anyOf** *schema[]* : The value to verify must evaluate successfully against at least one of the reference schemata.
	* for <refschema> in <refschemata>
		* if <refschema> validates against <testvalue>
			* => true
	* => false
* **oneOf** *schema[]* : The value to verify must evaluate successfully against exactly one of the reference schemata.
	* <b> = false
	* for <refschema> in <refschemata>
		* if <refschema> validates against <testvalue>
			* if <b>
				* => false
			* else
				* <b> = true
	* if <b>
		* => true
	* else
		* => false
* **not** *schema*
	* if <refschema> validates against <testvalue>
		* => false
	* else
		* => true








































