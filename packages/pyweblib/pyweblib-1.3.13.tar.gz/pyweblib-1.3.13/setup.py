#! /usr/bin/env python
"""
setup.py - Setup package with the help Python's DistUtils

$Id: setup.py,v 1.8 2015/01/10 16:34:28 michael Exp $
"""

import sys,os
from distutils.core import setup

##################################################################
# Weird Hack to grab release version from local dir
##################################################################

sys.path.insert(0,os.getcwd())

import pyweblib

setup(
  #-- Package description
  name = 'pyweblib',
  license = pyweblib.__license__,
  version = pyweblib.__version__,
  description = 'Yet another web programming framework for Python',
  long_description = """Yet another web programming framework for Python

Sub-modules:
pyweblib.forms        class library for handling <FORM> input
pyweblib.session      server-side web session handling
pyweblib.helper       misc. stuff useful in CGI-BINs
pyweblib.sslenv       retrieves SSL-related env vars
pyweblib.httphelper   very basic HTTP functions
""",
  author = 'Michael Stroeder', 
  author_email = 'michael@stroeder.com',
  maintainer = 'Michael Stroeder', 
  maintainer_email = 'michael@stroeder.com',
  url = 'http://www.stroeder.com/pylib/PyWebLib/',
  packages = ['pyweblib'],
#  keywords = ['web programming','CGI-BIN','session handling','form handling']
)
