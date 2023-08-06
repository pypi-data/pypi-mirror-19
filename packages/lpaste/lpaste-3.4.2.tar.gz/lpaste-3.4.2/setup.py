#!/usr/bin/env python

# Project skeleton maintained at https://github.com/jaraco/skeleton

import io

import setuptools

with io.open('README.rst', encoding='utf-8') as readme:
	long_description = readme.read()

name = 'lpaste'
description = 'Library Paste command-line client'

params = dict(
	name=name,
	use_scm_version=True,
	author="Chris Mulligan",
	author_email="chmullig@gmail.com",
	mainainer="Jason R. Coombs",
	maintainer_email="jaraco@jaraco.com",
	description=description or name,
	long_description=long_description,
	url="https://github.com/jaraco/" + name,
	packages=setuptools.find_packages(),
	include_package_data=True,
	namespace_packages=name.split('.')[:-1],
	install_requires=[
		'requests',
		'keyring>=0.6',
		'six>=1.4',
	],
	extras_require={
		'clipboard': 'jaraco.clipboard',
	},
	setup_requires=[
		'setuptools_scm>=1.15.0',
	],
	classifiers=[
		"Development Status :: 5 - Production/Stable",
		"Intended Audience :: Developers",
		"License :: OSI Approved :: MIT License",
		"Programming Language :: Python :: 2.7",
		"Programming Language :: Python :: 3",
	],
	entry_points={
		'console_scripts': [
			'lpaste=lpaste.lpaste:main',
		],
	},
)
if __name__ == '__main__':
	setuptools.setup(**params)
