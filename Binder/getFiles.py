# -*- coding: utf-8 -*-
"""
author      = Purnendu Kumar <purnendu@techniex.com>
copyright   = Copyright (C) 2020 Techniex <https://techniex.com>
license     = GPLv3
version     = 1.0
url         = https://github.com/Techniex/binder
"""
import os

def getFiles(path, **kwargs):
  """
  Description
  -----------
  Provided the top folder and filter component, getFiles function returns the list of all files in the directory as well as subdirectories.
  
  Input Parameter
  ---------------
  path: Path of top folder to be scanned for files.
  kwargs = dictionary with keys 'ext', 'keyword','exclude','reccursive' and 'excludedir'
  Values can be both string of list of strings
    ext: list of extensions to be checked in files [ext1, ext2] or just one string ext1.
    keyword: list of keywords to be checked in files [filter1, filter2] or just one keyword.
    exclude: keyword or list of keywords to exclude.
    reccursive: to look through subdirectories or not default value: False
    excludedir: directory or list of directories to be excluded
  
  Input Parameter Type
  --------------------
  filepath: string --> required
  kwargs['ext']: list/str --> optional
  kwargs['keyword']: list/str --> optional
  kwargs['exclude']: list/str --> optional
  kwargs['reccursive']: bool --> optional
  kwargs['excludedir']: list/str --> optional
  
  Returns
  -------
  List of files in directory as well as subdirectories matching filter constraint.
  
  Return Type
  -----------
  list

  """
  #check if parameters are available else set to default
  if not 'ext' in kwargs.keys():
    #no filtering based on extension
    extflag = False;
  else:
    extflag = True;
      
  if not 'keyword' in kwargs.keys():
    #no filtering based keyword string
    filflag = False;
  else:
    filflag = True;
      
  if not 'exclude' in kwargs.keys():
    #no exclusion based on keyword
    excflag = False;
  else:
    excflag = True;
      
  if not 'reccursive' in kwargs.keys():
    subdir = False;
  else:
    subdir = kwargs['reccursive'];
      
  if not 'excludedir' in kwargs.keys():
    #no exclusion based on directory
    excdflag = False;
  else:
    excdflag = True;
        
  #get files in directory
  inpfiles = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))];
    
  #check for excluded keyword
  allfiles =[];
  for file in inpfiles:
    if excflag:
      if type(kwargs['exclude']) == str:
        if not kwargs['exclude'] in file:
          allfiles.append(file);
      else:
        if type(kwargs['exclude']) == list:
          ekflag = False;
          for exk in kwargs['exclude']:
            if exk in file:
              ekflag = True;
              break;
          if not ekflag:
            allfiles.append(file);
    else:
      allfiles.append(file);
      
  #check for extensions
  if extflag:
    exlfiles = [];
    for f in allfiles:
      if type(kwargs['ext']) == str:
        if f.rsplit('.',1)[-1] == kwargs['ext']:
          exlfiles.append(f);
      else:
        if type(kwargs['ext']) == list:
          for ext in kwargs['ext']:
            if f.rsplit('.',1)[-1] == ext:
              exlfiles.append(f);
              break;
  else:
    exlfiles = allfiles;

  #check for filter
  if filflag:
    filfiles = [];
    for f in exlfiles:
      if type(kwargs['keyword']) == str:
        if kwargs['keyword'] in f.rsplit('.',1)[0]:
          filfiles.append(f);
      else:
        if type(kwargs['keyword']) == list:
          for fil in kwargs['keyword']:
            if fil in f.rsplit('.',1)[0]:
              filfiles.append(f);
              break;
  else:
      filfiles = exlfiles;
 
  # Joint path for final output
  files = [];
  for file in filfiles:
    files.append(os.path.join(path, file))
    
  # Recurrsively getting files from subdirectories
  if subdir:
    folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))];
    exf = [];
    for folder in folders:
      if excdflag:
        if type(kwargs['excludedir']) == str:
          if not kwargs['excludedir'] in folder:
            exf.append(folder);
        else:
          if type(kwargs['excludedir']) == list:
            edflag = False;
            for exd in kwargs['excludedir']:
              if exd in folder:
                edflag = True;
                break;
            if not edflag:
              exf.append(folder);
      else:
        exf.append(folder);   
           
    for filder in exf:
      files = files + getFiles(os.path.join(path,folder), **kwargs);    
      
  return files