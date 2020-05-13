# -*- coding: utf-8 -*-
"""
author      = Purnendu Kumar <purnendu@techniex.com>
copyright   = Copyright (C) 2020 Techniex <https://techniex.com>
license     = GPLv3
version     = 1.0
url         = https://github.com/Techniex/binder
"""
from . import reader
from . import writer
from . import param

def writefile(filepath, data, **kwargs):
  # to-do: documentation
  w = writer.Writer()
  #to-do: implement

def readfile(filepath, **kwargs):
  # to-do: documentation
  r = reader.Reader()

  # Switch to debug mode if specified
  if 'verbose' in kwargs.keys():
    r.verbose = kwargs['verbose']

  # Check if path is valid
  if not r.pathValid(filepath, 'file'):
    r.error = -1
    print(param.errordisc[r.error].format(filepath))
    return {}
  # to-do: Add support for config file.

  # decide method to read file
  if 'readas' in kwargs.keys():
    if kwargs['readas'].lower() in param.method.keys():
      ra = kwargs['readas'].lower()
    else:
      r.warning += 1
      if r.verbose: print("Warning[%d]: reading method specified is not supported, reading as %s."%(r.warning, param.default))
      ra = param.default
  else:
    ra = r.Reader__getReadMethod__(filepath)

  # read file
  if ra == 'text':
    rdict = r.readTxt(filepath, **kwargs)
  elif ra == 'image':
    rdict = r._readImg(filepath, **kwargs)
  else:
    rdict = r._readRaw(filepath,**kwargs)

  # remove empty keys
  for key in rdict.keys():
    if rdict[key] ==[] or rdict[key] == {}:
      del rdict[key]

  return rdict