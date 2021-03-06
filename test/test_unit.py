# -*- coding: utf-8 -*-
"""
author      = Purnendu Kumar <purnendu@techniex.com>
copyright   = Copyright (C) 2020 Techniex <https://techniex.com>
license     = GPLv3
version     = 1.0
url         = https://github.com/Techniex/binder
"""

import sys
import os
sys.path.insert(1, "..")

import Binder

f = Binder.fUtil()
f.verbose = True
#r = Binder.Reader();
#w = Binder.Writer();

def test_to_list():
  # check with string
  assert f.to_list('test') == ['test']
  # check with int
  assert f.to_list(15) == [15]
  # check with list
  assert f.to_list([10, 'test']) == [10, 'test']

def test_get_files():
  res1 = ['fileio.py', 'fileutil.py', 'param.py', 'reader.py',\
    'writer.py', '__init__.py', '__main__.py']
  exp1 = [os.path.basename(filename) \
    for filename in f.get_files(r"..",filters=["*(Binder)*", "*(py)"])]
  assert exp1==res1

def test_parse_string():
  # check with string and whitespaces
  assert f.parse_string("  yes  ") == "yes"
  # check with integer
  assert f.parse_string("100") == 100
  assert f.parse_string("-20") == -20
  assert f.parse_string("+10") == 10
  # check with float
  assert f.parse_string("1.20") == 1.20
  assert f.parse_string("-1.20") == -1.20
  assert f.parse_string("0.1.20") == "0.1.20"

def test_parseBin():
  #todo
  pass

def test_pathValid():
  #todo
  pass

def test_getFileType():
  #todo
  pass

def test_str_filter():
  with open(r"./testdir/filtertext.txt", 'r') as flread:
    lines = flread.read().splitlines()
  fil1 = "#"
  exmp1 = ["*#", "#*"]
  fil2 = ["(this)#", "#(keyword)#", "#(keyword)", "*(okay)*"]
  exmp2 = ["okay!"]
  fil3 = ["(this)#", "#(keyword)#", "#(keyword)", "(good)*"]
  exmp3 = ["good again"]
  fil4 = ["(this)#", "#(keyword)#", "#(keyword)", "*(.)"]
  exmp4 = ["line is fine to read."]
  fil5 = ["(this)#", "#(keyword)#", "#(keyword)", "-*(okay)*", "(good)*"]
  exmp5 = ["okay!", "good again"]
  assert f.str_filter(lines, fil1) == exmp1
  assert f.str_filter(lines, fil2) == exmp2
  assert f.str_filter(lines, fil3) == exmp3
  assert f.str_filter(lines, fil4) == exmp4
  assert f.str_filter(lines, fil5) == exmp5