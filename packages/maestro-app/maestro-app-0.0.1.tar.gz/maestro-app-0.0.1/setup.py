#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
import maestro

with open('README.md') as readme_file:
	readme = readme_file.read()

requirements = [
	'pyqt5'
]

test_requirements = [
]

setup(
	name='maestro-app',
	version=maestro.__version__,
	description=maestro.__description__,
	long_description=readme,
	author=maestro.__author__,
	author_email=maestro.__email__,
	url='https://github.com/urosjarc/maestro',
	packages=[
		'maestro',
	],
	package_dir={'maestro': 'maestro'},
	entry_points={
		'console_scripts': [
			'maestro=maestro.gui:main'
		]
	},
	include_package_data=False,
	install_requires=requirements,
	license="MIT license",
	zip_safe=True,
	keywords='maestro',
	classifiers=[
		'Development Status :: 2 - Pre-Alpha',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Natural Language :: English',
		"Programming Language :: Python :: 2",
		'Programming Language :: Python :: 2.6',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.3',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
	],
	test_suite='tests',
	tests_require=test_requirements
)
