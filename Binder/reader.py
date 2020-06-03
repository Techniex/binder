# -*- coding: utf-8 -*-
"""
author      = Purnendu Kumar <purnendu@techniex.com>
copyright   = Copyright (C) 2020 Techniex <https://techniex.com>
license     = GPLv3
version     = 1.0
url         = https://github.com/Techniex/binder
"""
import os
from . import param
from . import fileutil
import cv2

class Reader(fileutil.fUtil):
  def __init__(self):
    super().__init__()
    
  def readTxt(self, filepath, **kwargs):
    """
    Description
    -----------
      reads the text based files and returns the output as dict. Keys of dict depends on parameters passed.
      default keys are: filename and lines as list of lines
      supported file types are: .txt, .c, .py, .m, .cpp, .h, .csv, .tab, etc.(any other plain text based file with utf encoding)
      
    Input Parameter
    ---------------
    filepath: Path of text based file to be read.
    kwargs = dictionary with keys     
      skiplines: integer to identify how many lines to skip and it won't be included in header or data, default = 0
      headerlines: number of lines in header. if the keyword is not defined program doesn't look for header in file.
      skipwhitelines: if True, skips all white lines or lines only with comment identifier are skipped, default True

      commentidentifier: character to be identified as starting of comment. e.g. "#" for configfiles
      headercommenthandler: 'skipcomment'/ 'uncomment'
      datacommenthandler: 'skipcomment'/ 'uncomment'
      removeinlinecomment: True/False

      headerfilter: select lines only if starts with keyword
      datafilter: select lines only if starts with keyword

      headerdelimeter: to seperate key and value pair in header. if not defined, headers are returned as lines.
      headerformat:

      datadelimeter:
      dataformat:

    Input Parameter Type
    --------------------
    filepath: string --> required
    kwargs['skiplines']: int --> optional
    kwargs['commentidentifier']: str --> optional
    kwargs['skipwhitelines']: bool --> optional
    kwargs['header']: bool --> optional
    kwargs['headerlines']: int --> optional
    kwargs['headerdict']: bool --> optional
    kwargs['headerdelimeter']: str --> optional
    kwargs['commentskip']: bool --> optional
    kwargs['startswithfilter']: str/list --> optional
    kwargs['startswithexclude']: str/list --> optional
    kwargs['linefilter']: str/list --> optional
    kwargs['lineexclude']: str/list --> optional
    kwargs['columns']: bool --> optional
    kwargs['delimeter']: str --> optional
    
    Returns
    -------
    dictionary with default keywords 'filename', 'filetype', 'lines', remaining keys depends on file and selection of arguments.
    
    Return Type
    -----------
    dict
  
    To Do
    -----
    1. Create Documentation
    2. Implement the function in c for faster operations.
    
    """
    if self.verbose:
      print("Function call: readTxt(args)")

    #initialize return
    rdict = {'Error':self.error, 'Warning':self.warning}

    # Load default kwargs if not provided by user
    kwargs = self.__loadkwargs__(filepath, 'text', kwargs)

    # Read file get all lines in list
    with open(filepath , 'r') as infile:
      origlines = infile.read().splitlines()
    
    #skiplines
    origlines = origlines[kwargs['skiplines']:]
    
    # separate header, data, footer
    outfile = {}
    outfile['header'] = origlines[0: kwargs['headerlines']]
    outfile['data'] = origlines[kwargs['headerlines']:len(origlines)-kwargs['footerlines']]
    outfile['footer'] = origlines[kwargs['footerlines']:]

    # skip white lines
    if kwargs['skipwhitelines']:
      for key in outfile.keys():
        outfile[key] = self.skip_white_line(outfile[key])
    
    #comment handler
    if kwargs['comment_maipulation']:
      for key in outfile.keys():
        outfile[key] = self.comment_handler(outfile[key],kwargs[key+'_comment_handle'])[0]

    #Handle docstring
    docstring = {}
    if kwargs['read_docstring']:
      for key in outfile.keys():
        outval = self.comment_handler(outfile[key],kwargs[key+'_docstring_handle'])[0]
        outfile[key] = outval[0]
        docstring[key] = outval[1]

    # filter data
    for key in outfile.keys():
      outfile[key] = self.str_filter(outfile[key], kwargs[key+'_header_filter'])
          
    #format data
    for key in outfile.keys():
      outfile[key] = self.lineFormat(outfile[key], kwargs[key+'_format'], kwargs[key+'_delimeter'])

    rdict.update(outfile)
    rdict.update(docstring)
    return rdict
         
  def readImg(self, filepath, **kwargs):
    return cv2.imread(filepath, -1)

  def readRaw(self, filepath, **kwargs):
    with open(filepath , 'rb') as rawfile:
      xs= bytearray(b'')
      for line in rawfile:
        xs = xs + line
    return xs
