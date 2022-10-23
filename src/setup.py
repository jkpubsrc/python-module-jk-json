################################################################################
################################################################################
###
###  This file is automatically generated. Do not change this file! Changes
###  will get overwritten! Change the source file for "setup.py" instead.
###  This is either 'packageinfo.json' or 'packageinfo.jsonc'
###
################################################################################
################################################################################


from setuptools import setup

def readme():
	with open("README.md", "r", encoding="UTF-8-sig") as f:
		return f.read()

setup(
	author = "Jürgen Knauth",
	author_email = "pubsrc@binary-overflow.de",
	classifiers = [
		"Development Status :: 5 - Production/Stable",
		"License :: OSI Approved :: Apache Software License",
		"Programming Language :: Python :: 3",
	],
	description = "This python module provides parser and validator for JSON files and data structures. The JSON parser is designed as a drop-in replacement for the built in python JSON parser as this parser here supports using comments in JSON files (which in some use cases is very a very handy feature).",
	include_package_data = True,
	install_requires = [
		"chardet",
	],
	keywords = [
		"json",
		"parsing",
		"schema",
	],
	license = "Apache2",
	name = "jk_json",
	package_data = {
		"": [
			"data/*",
			"data/html_default/*",
			"data/html_default/files/*",
			"data/html_default/files/images/*",
			"data/html_default/templates/*",
		],
	},
	packages = [
		"jk_json",
		"jk_json.tools",
		"jk_jsonschema",
	],
	scripts = [
		"bin/jsonPrettyPrint.py",
		"bin/jkjson.py",
	],
	version = '0.2022.10.23',
	zip_safe = False,
	long_description = readme(),
	long_description_content_type = "text/markdown",
)
