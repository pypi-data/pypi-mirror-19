#!/usr/bin/env python

# Project skeleton maintained at https://github.com/jaraco/skeleton

import io
import sys

import setuptools

with io.open('README.rst', encoding='utf-8') as readme:
	long_description = readme.read()

needs_wheel = {'release', 'bdist_wheel', 'dists'}.intersection(sys.argv)
wheel = ['wheel'] if needs_wheel else []

name = 'jaraco.mongodb'
description = 'Routines and classes supporting MongoDB environments'

setup_params = dict(
	name=name,
	use_scm_version=True,
	author="Jason R. Coombs",
	author_email="jaraco@jaraco.com",
	description=description or name,
	long_description=long_description,
	url="https://github.com/jaraco/" + name,
	packages=setuptools.find_packages(),
	include_package_data=True,
	namespace_packages=name.split('.')[:-1],
	install_requires=[
		'pymongo',
		'six',
		'python-dateutil',
		'jaraco.services',
		'portend',
		'jaraco.itertools>=1.8',
		'jaraco.functools',
		'jaraco.ui',
		'jaraco.context',
		'more_itertools',
		'jaraco.logging',
		'jaraco.timing',
		'pytimeparse',
	],
	extras_require={
	},
	setup_requires=[
		'setuptools_scm>=1.15.0',
	] + wheel,
	classifiers=[
		"Development Status :: 5 - Production/Stable",
		"Intended Audience :: Developers",
		"License :: OSI Approved :: MIT License",
		"Programming Language :: Python :: 2.7",
		"Programming Language :: Python :: 3.3",
		"Programming Language :: Python :: 3.4",
		"Programming Language :: Python :: 3.5",
		"Framework :: Pytest",
	],
	entry_points={
		'pytest11': [
			'MongoDB = jaraco.mongodb.fixtures',
		],
		'pmxbot_handlers': [
			'create in MongoDB shard = jaraco.mongodb.pmxbot',
		],
	},
)
if __name__ == '__main__':
	setuptools.setup(**setup_params)
