# -*- coding: utf-8 -*-
"""
author      = Purnendu Kumar <purnendu@techniex.com>
copyright   = Copyright (C) 2020 Techniex <https://techniex.com>
license     = GPLv3
version     = 1.0
url         = https://github.com/Techniex/binder
"""

import sys
sys.path.insert(1, "..")

import Binder

f = Binder.fUtil()
#r = Binder.Reader();
#w = Binder.Writer();

def test_toList():
  # check with string
  assert f.toList('test') == ['test']
  # check with int
  assert f.toList(15) == [15]
  # check with list
  assert f.toList([10, 'test']) == [10, 'test']

def test_getFiles():
  pass

def test_parseString():
  # check with string and whitespaces
  assert f.parseString("  yes  ") == "yes"
  # check with integer
  assert f.parseString("100") == 100
  assert f.parseString("-20") == -20
  assert f.parseString("+10") == 10
  # check with float
  assert f.parseString("1.20") == 1.20
  assert f.parseString("-1.20") == -1.20
  assert f.parseString("0.1.20") == "0.1.20"

def test_parseBin():
  pass

def test_pathValid():
  pass

def test_getFileType():
  pass