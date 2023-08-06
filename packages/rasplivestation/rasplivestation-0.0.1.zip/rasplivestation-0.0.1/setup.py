# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 14:56:46 2016

@author: croizerm
"""

from setuptools import setup,find_packages

import rasplivestation

setup(name='rasplivestation',version=rasplivestation.__version__,
packages=find_packages(),author='Krounet',author_email='krounet@gmail.com',
description="It's a usefull little package to launch a stream via the command-line utility Livestreamer : http://docs.livestreamer.io/index.html on a Raspberry Pi",
long_description=open('README.md').read(),include_package_data=True,
classifiers=["Programming Language :: Python",
"Development Status :: 1 - Planning",
"License :: OSI Approved",
"Natural Language :: French",
"Operating System :: OS Independent",
"Programming Language :: Python :: 2.7",
"Topic :: Multimedia"],
license="WTFPL")