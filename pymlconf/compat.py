# -*- coding: utf-8 -*-
#@PydevCodeAnalysisIgnore
"""
Created on:    Nov 17, 2013
@author:        vahid
"""
import sys

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


# unittest compatibility
from unittest import TestCase

if sys.version_info[0] >= 3:
    TestCase.assertRegexpMatches = TestCase.assertRegex
    TestCase.assertNotRegexpMatches = TestCase.assertNotRegex

if hasattr(TestCase, 'assertIsInstance'):
    class _CompatTestCase: pass
else:
    from unittest.util import safe_repr
    class _CompatTestCase:
        def assertIsInstance(self, obj, cls, msg=None):
            if not isinstance(obj, cls):
                standardMsg = '%s is not an instance of %r' % (safe_repr(obj), cls)
                self.fail(self._formatMessage(msg, standardMsg))



def read_file(file_path, encoding):
    if sys.version_info[0] >= 3:
        with open(file_path, encoding=encoding) as stream:
            return stream.read()
    else:
        with open(file_path) as stream:
            return stream.read().decode(encoding)
