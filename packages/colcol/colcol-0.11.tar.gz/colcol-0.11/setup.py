#!/usr/bin/env python3


from setuptools import setup


import sys
if sys.version_info[0] == 2:
    sys.exit("Sorry, only Python 3 is supported by this package.")
    
    
setup(
	name='colcol',    # This is the name of your PyPI-package.
	description='A script to deal with color conversions, color transformations, and generating color scales.',       #package description
	version='0.11',                          # Update the version number for new releases
	scripts=['colcol.py'],                  # The name of your scipt, and also the command you'll be using for calling it
	author='Martin Engqvist',
	author_email='martin_engqvist@hotmail.com',
	license='GPL3',
	install_requires=[			#for dependancies
    ]
)


