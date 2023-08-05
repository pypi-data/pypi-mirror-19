#!/usr/bin/env python3

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#LICENSE:
#
#wsvg is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation; either version 3 of the License, or
#(at your option) any later version.
#
#wsvg is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU Library General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software Foundation,
#Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from setuptools import setup


import sys
if sys.version_info[0] == 2:
    sys.exit("Sorry, only Python 3 is supported by this package.")
    
    
setup(
	name='wsvg',    # This is the name of your PyPI-package.
	description='A lightweight wrapper around the SVG format to script SVG files.',       #package description
	version='0.1.1',                          # Update the version number for new releases
	author='Martin Engqvist',
	author_email='martin_engqvist@hotmail.com',
	url='https://github.com/mengqvist/wsvg',
	license='GPLv3+',
	install_requires=['colcol'],
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



