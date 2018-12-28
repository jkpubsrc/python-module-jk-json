from setuptools import setup


def readme():
	with open("README.rst") as f:
		return f.read()


setup(name="jk_json",
	version="0.2018.12.28",
	description="This python module provides parser and validator for JSON files and data structures. "
		+ "The JSON parser is designed as a drop-in replacement for the built in python JSON parser as this parser here supports using comments in JSON files "
		+ "(which in some use cases is very a very handy feature).",
	author="Jürgen Knauth",
	author_email="pubsrc@binary-overflow.de",
	license="Apache 2.0",
	url="https://github.com/jkpubsrc/python-module-jk-json",
	download_url="https://github.com/jkpubsrc/python-module-jk-json/tarball/0.2018.12.28",
	keywords=[
		"json",
		"parsing",
		"schema",
		],
	packages=[
		"jk_json",
		"jk_json.tools",
		"jk_jsonschema",
		],
	install_requires=[
	],
	include_package_data=True,
	classifiers=[
		"Development Status :: 4 - Beta",
		#"Development Status :: 5 - Production/Stable",
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: Apache Software License",
	],
	long_description=readme(),
	zip_safe=False)

