#!/usr/bin/env python3

from setuptools import setup
from setuptools import Extension

olOpt = Extension(	'olOpt',
					sources = ['openlut/lib/olOpt.cpp'],
					extra_compile_args = ['-fopenmp', '-std=gnu++14']
		)

setup(	name = 'openlut',
		version = '0.1.0',
		description = 'OpenLUT is a practical color management library.',
		author = 'Sofus Rose',
		author_email = 'sofus@sofusrose.com',
		url = 'https://www.github.com/so-rose/openlut',
		
		ext_modules = [olOpt],

		license = 'MIT Licence',
		
		keywords = 'color image images processing',
		
		install_requires = ['numpy', 'wand', 'scipy', 'pygame','PyOpenGL'],
		
		classifiers = [
			'Development Status :: 3 - Alpha',
			
			'License :: OSI Approved :: MIT License',
			
			'Programming Language :: Python :: 3.5'
		]
)
