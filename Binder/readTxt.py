# -*- coding: utf-8 -*-
"""
author      = Purnendu Kumar <purnendu@techniex.com>
copyright   = Copyright (C) 2020 Techniex <https://techniex.com>
license     = GPLv3
version     = 1.0
url         = https://github.com/Techniex/binder
"""

def readTxt(filepath, **kwargs):
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
    skipwhitelines: if True, skips all white lines or lines only with comment identifier are skipped, default True
    
    header: to identify if it is required to read header separately or not, default = False
    headerlines: number of lines in header. if the keyword is not defined but files first line contains this, still it works.
    headerdict: to identify if header is needed to be read as key valye pair else all header lines will be in a separate list, default = False
    headerdelimeter: to seperate key and value pair in header. if nt defined, headers are returned as lines.
    
    commentidentifier: character to be identified as starting of comment.
    commentskip: skip comments in data section? if header is False then this works for top comment block also.
    
    startswithfilter: select lines only if it starts with a keyword.
    startswithexclude: select lines only if keyword is not in of line else discard.
    linefilter: select lines only if keyword is in the line.
    lineexclude: select lines only if keyword is not in line else discard.
    
    columns: if data has columns in case of data is separated with delimeter, checked just after header.
    delimeter: data returned as list of list separated by delimeter.
  
  Input Parameter Type
  --------------------
  filepath: string --> required
  kwargs['skiplines']: bool --> optional
  kwargs['skipwhitelines']: bool --> optional
  kwargs['header']: bool --> optional
  kwargs['headerlines']: int --> optional
  kwargs['headerdict']: bool --> optional
  kwargs['headerdelimeter']: str --> optional
  kwargs['commentidentifier']: str --> optional
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
  #check input arguments