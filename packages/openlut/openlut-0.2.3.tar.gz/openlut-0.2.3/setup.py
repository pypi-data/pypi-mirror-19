#!/usr/bin/env python3

import sys, os
import os.path as path

from setuptools import setup
from setuptools import Extension
from setuptools import find_packages

#pybind11, a dependency, can report its own includes!
import pybind11

#Make sure we're using gcc.
os.environ["CC"] = "g++"
os.environ["CXX"] = "g++"

cpp_args = ['-fopenmp', '-std=gnu++14', '-O3']
link_args = ['-fopenmp']

olOpt = Extension(	'openlut.lib.olOpt',
					sources = ['openlut/lib/olOpt.cpp'],
					include_dirs=[pybind11.get_include()], #Include pybind11.
					language = 'c++',
					extra_compile_args = cpp_args,
					extra_link_args = cpp_args
		)

setup(	name = 'openlut',
		version = '0.2.3',
		description = 'OpenLUT is a practical color management library.',
		author = 'Sofus Rose',
		author_email = 'sofus@sofusrose.com',
		url = 'https://www.github.com/so-rose/openlut',
		
		packages = find_packages(exclude=['src']),
		
		ext_modules = [olOpt],

		license = 'MIT Licence',
		
		keywords = ['color', 'image', 'images', 'processing'],
		
		install_requires = ['numpy', 'wand', 'scipy', 'pygame','PyOpenGL', 'setuptools', 'pybind11'],
		
		classifiers = [
			'Development Status :: 3 - Alpha',
			
			'License :: OSI Approved :: MIT License',
			
			'Programming Language :: Python :: 3'
		]
)
