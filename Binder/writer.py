# -*- coding: utf-8 -*-
"""
author      = Purnendu Kumar <purnendu@techniex.com>
copyright   = Copyright (C) 2020 Techniex <https://techniex.com>
license     = GPLv3
version     = 1.0
url         = https://github.com/Techniex/binder
"""
from . import fileutil

class Writer(fileutil.FileUtil):
  def writeTxt(self, filepath, data, **kwargs):
    # TODO : write list, dict, line, vdict, vlist and append methods
    pass
  def writeRaw(self, filepath, data, **kwargs):
    pass
  def writeImg(self, filepath, data, **kwargs):
    pass