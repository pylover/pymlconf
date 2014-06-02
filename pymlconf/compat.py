# -*- coding: utf-8 -*-
#@PydevCodeAnalysisIgnore
"""
Created on:    Nov 17, 2013
@author:        vahid
"""

# noinspection PyBroadException
try:
    # Python 2.7+
    from collections import OrderedDict
except:
    # Python 2.6-
    # noinspection PyPackageRequirements,PyUnresolvedReferences
    from ordereddict import OrderedDict


# For compatibility with python3
# TODO: When support for python 2.x is dropped,
# get rid of the import as well as substitute all basestring with str
try:
    # noinspection PyUnboundLocalVariable
    basestring = basestring
except NameError:
    basestring = str


def isiterable(o):
    if isinstance(o,(basestring, type)):
        return False
    elif hasattr(o, '__iter__'):
        return True
    else:
        return False 
    
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO