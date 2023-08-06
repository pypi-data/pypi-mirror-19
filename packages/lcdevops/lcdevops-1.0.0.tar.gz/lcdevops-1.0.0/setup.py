#!/usr/bin/env python
# -*- coding: utf-8 -*-

## 
from distutils.core import setup 

setup(
	name='lcdevops',
	author='Colin',
	author_email='colin50631@gmail.com',
	version='1.0.0',
#	packages=['_opslogs','_opsdate'],
	py_modules=['_opslogs','_opsdate'],
	url='https://github.com/opscolin/devops.git',
	license='MIT',
	description='devops package',
	long_description='customize common api for devops by python',
	platforms='Linux,unix',
	keywords='devops, opsdate, opslogs'
)
