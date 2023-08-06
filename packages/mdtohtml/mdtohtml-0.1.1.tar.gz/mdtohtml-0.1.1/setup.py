import re
from setuptools import setup, find_packages

with open("README.rst", "rb") as f:
	long_descr = f.read().decode("utf-8")

setup(
	name = "mdtohtml",
	packages = ["mdtohtml"],
	install_requires=[
		'markdown',
	],
	entry_points = {
 			"console_scripts": ["mdtohtml=mdtohtml.mdtohtml:main"]
		},
	version = "0.1.1",
	description = "Duplicates folder and converts markdown files to html files",
	long_description = long_descr,
	author = "Oscar Vazquez",
	author_email = "oscar.vazquez2012@gmail.com",
	url = "https://github.com/oscarvazquez/mdtohtml",
	license='MIT',	
	classifiers=[
		'Development Status :: 3 - Alpha',

		# Indicate who your project is intended for
		'Intended Audience :: Developers',
		'Topic :: Software Development :: Build Tools',

		# Pick your license as you wish (should match "license" above)
		 'License :: OSI Approved :: MIT License',

		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 2.6',
		'Programming Language :: Python :: 2.7'
	]
)