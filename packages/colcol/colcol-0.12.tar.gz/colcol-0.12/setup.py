#!/usr/bin/env python3


from setuptools import setup


import sys
if sys.version_info[0] == 2:
    sys.exit("Sorry, only Python 3 is supported by this package.")
    
    
setup(
	name='colcol',    # This is the name of your PyPI-package.
	description='A script to deal with color conversions, color transformations, and generating color scales.',       #package description
	version='0.12',                          # Update the version number for new releases
#	scripts=['colcol.py'],                  # The name of your scipt, and also the command you'll be using for calling it
	author='Martin Engqvist',
	author_email='martin_engqvist@hotmail.com',
	url='https://github.com/mengqvist/colcol',
	license='GPLv3+',
	classifiers=[
	# How mature is this project? Common values are
	#   3 - Alpha
	#   4 - Beta
	#   5 - Production/Stable
	'Development Status :: 3 - Alpha',

	# Indicate who your project is intended for
	'Intended Audience :: Science/Research',
	'Topic :: Scientific/Engineering :: Visualization',

	# Pick your license as you wish (should match "license" above)
	'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',

	# Specify the Python versions you support here. In particular, ensure
	# that you indicate whether you support Python 2, Python 3 or both.
	'Programming Language :: Python :: 3 :: Only',
	'Programming Language :: Python :: 3',
	'Programming Language :: Python :: 3.2',
	'Programming Language :: Python :: 3.3',
	'Programming Language :: Python :: 3.4',
	'Programming Language :: Python :: 3.5',
	'Programming Language :: Python :: 3.6']    
)


