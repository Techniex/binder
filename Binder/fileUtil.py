# -*- coding: utf-8 -*-
"""
author      = Purnendu Kumar <purnendu@techniex.com>
copyright   = Copyright (C) 2020 Techniex <https://techniex.com>
license     = GPLv3
version     = 1.0
url         = https://github.com/Techniex/binder
"""

from . import param
import os
import struct

class fUtil():
  def __init__(self):
    self.verbose = False
    self.error = 0
    self.warning = 0

  def __loadKwargs__(self, filepath, method, kwargs):
    #to-do: documentation
    if 'commentidentifier' not in kwargs.keys():
      ci = self.__getCommentIdentifier__(filepath)
      if ci != '':
        if self.verbose: print("Info: Auto selceting %s as comment identifier based on filetype."%(ci))
        kwargs['commentidentifier'] = ci
    kwargupdate ={}
    for kwarg in param.keyval[method.lower()].keys():
      if kwarg in kwargs.keys():
        kwargupdate[kwarg] = kwargs[kwarg]
      else:
        if self.verbose: print("Info: %s parameter is not available in function call, restoring to default value %s"%(kwarg, str(param.keyval[method.lower()][kwarg])))
        kwargupdate[kwarg] = param.keyval[method.lower()][kwarg]
    return kwargupdate

  def toList(self, data):
    """
    Description
    -----------
    if input is list return as it is else convert to list and return

    Input Parameters
    ----------------
    data: input data

    Input Parameter Type
    --------------------
    data: any

    Returns
    -------
    list from input params

    Return Type
    -----------
    list

    """
    if self.verbose:
      print("Function Call: toList(args)")
    if not type(data) == list:
      listdata = [data]
    else:
      listdata = data.copy()
    return listdata

  def getFiles(self, path, **kwargs):
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
    if self.verbose:
      print("Function Call: getFiles(args)")
    #check if parameters are available else set to default
    if not 'ext' in kwargs.keys():
      #no filtering based on extension
      extflag = False
    else:
      extflag = True
        
    if not 'keyword' in kwargs.keys():
      #no filtering based keyword string
      filflag = False
    else:
      filflag = True
        
    if not 'exclude' in kwargs.keys():
      #no exclusion based on keyword
      excflag = False
    else:
      excflag = True
        
    if not 'reccursive' in kwargs.keys():
      subdir = False
    else:
      subdir = kwargs['reccursive']
        
    if not 'excludedir' in kwargs.keys():
      #no exclusion based on directory
      excdflag = False
    else:
      excdflag = True
          
    #get files in directory
    inpfiles = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
      
    #check for excluded keyword
    allfiles =[]
    for file in inpfiles:
      if excflag:
        excludedkeyword = self.toList(kwargs['exclude'])
        ekflag = False
        for exk in excludedkeyword:
          if exk in file:
            ekflag = True
            break
        if not ekflag:
          allfiles.append(file)
      else:
        allfiles.append(file)
        
    #check for extensions
    if extflag:
      exlfiles = []
      for f in allfiles:
        extensions = self.toList(kwargs['ext'])
        for ext in extensions:
          if f.rsplit('.',1)[-1] == ext:
            exlfiles.append(f)
            break
    else:
      exlfiles = allfiles
  
    #check for filter
    if filflag:
      filfiles = []
      for f in exlfiles:
        filterkeyword = self.toList(kwargs['keyword'])
        for fil in filterkeyword:
          if fil in f.rsplit('.',1)[0]:
            filfiles.append(f)
            break
    else:
        filfiles = exlfiles
   
    # Joint path for final output
    files = []
    for file in filfiles:
      files.append(os.path.join(path, file))
      
    # Recurrsively getting files from subdirectories
    if subdir:
      folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
      exf = []
      for folder in folders:
        if excdflag:
          excludeddir = self.toList(kwargs['excludedir'])
          edflag = False
          for exd in excludeddir:
            if exd in folder:
              edflag = True
              break
          if not edflag:
            exf.append(folder)
        else:
          exf.append(folder)
             
      for folder in exf:
        files = files + self.getFiles(os.path.join(path,folder), **kwargs)
        
    return files
  
  def parseString(self, strdata):
    """
    Description
    -----------
    Convert a string to integer or float if possible else return string

    Input Parameters
    ----------------
    strdata: input string

    Input Parameter Type
    --------------------
    data: str

    Returns
    -------
    parsed string

    Return Type
    -----------
    int/float/string

    """
    if self.verbose:
      print("Function Call: parseString(args)")
    # remove leading and trailing white space
    outdata = strdata.strip()
    
    # Check if number is signed
    sign = (strdata[0] == '-') or (strdata[0] == '+')
      
    # check if all digit with or without sign
    if sign:
      signedint = outdata[1:].isdigit()
      unsignedint = False
    else:
      signedint = False
      unsignedint = outdata.isdigit()
    
    #check if only one decimal
    decimal = outdata.count('.') == 1
    
    # check if all digit with or without sign look for decimal
    if sign:
      signedfloat = (outdata[1:].replace('.','',1).isdigit()) and decimal
      unsignedfloat = False
    else:
      signedfloat =False
      unsignedfloat = (outdata.replace('.','',1).isdigit()) and decimal
      
    # Convert if convertable to int
    if unsignedint or signedint:
      outdata = int(outdata)
      if self.verbose: print("Return Type: integer")
    else:
    # Convert if convertable to float
      if signedfloat or unsignedfloat:
        outdata = float(outdata)
        if self.verbose: print("Return Type: floating point number")
      else:        
        if self.verbose: print("Return Type: string")
    # if not converted return string  
    return outdata
  
  def parseBin(self, bytearr, groupas, **kwargs):
    """
    Description
    -----------
    Parse binary byte array as per key-value pair.
    
    Input Parameter
    ---------------
    bytearr: Byte array.
    groupas: output type: int8, uint8, int16, uint16, int32, uint32, int64, uint64, str, single, usingle, double, udouble.
    kwargs = dictionary with keys 'skipcount', 'skipbyte', 'endiness' and 'stringseparator'
    Values can be both string of list of strings
      skipcount: number of bytes to be excluded from beginning.
      skipbyte: specific byte values to be skipped.
      endiness: byte order: little, big, native.
      stringseparator: value based on which strings are separated.
    
    Input Parameter Type
    --------------------
    bytearr: byte --> required
    groupas: string --> required
    kwargs['skipcount']: int --> optional
    kwargs['skipbyte']: byte/list --> optional
    kwargs['endiness']: string --> optional
    kwargs['stringseparator']: str/list --> optional
    
    Returns
    -------
    string or list of values as per key value pair
    
    Return Type
    -----------
    str/list
  
    """
    if self.verbose:
      print("Function Call: parseBin(args)")
    
    #check if parameters are available else set to default
    if 'skipcount' in kwargs.keys():
      bytearr = bytearr[kwargs['skipcount']:]
        
    if 'skipbyte' in kwargs.keys():
      bytearr = bytes([byt for byt in bytearr if byt not in self.toList(kwargs['skipbyte'])])

    if 'endiness' in kwargs.keys():
      if kwargs['endiness'].lower() in param.endiness.keys():
        placeholder = param.endiness[kwargs['endiness'].lower()]
      else:
        print('Warning: Invalid endiness - Switching to native.')
        placeholder = param.endiness['native']
    else:
      placeholder = param.endiness['native']
        
    if groupas == 'str' and 'stringseparator' in kwargs.keys():
      split = True
    else:
      split = False

    if groupas.lower() in param.groupas.keys():
      outtype = groupas.lower()
    else:
      print('Warning: Invalid argument -- switching to int8')
      outtype = 'int8'
    
    placeholder = placeholder + param.groupas[outtype ]
    remainedbytes = len(bytearr) % param.bytecount[outtype]
    
    if remainedbytes != 0:
      print("Warning: Length mis-matched. ignoring last %d bytes"%remainedbytes)
      bytearr = bytearr[0:(0-remainedbytes)]

    listextract = [struct.unpack(placeholder, bytearr[x:x+param.bytecount[outtype]]) for x in range (0, len(bytearr), param.bytecount[outtype])]

    if outtype == 'str':
      concatenatedstring = ''.join(listextract)
      if split:
        listfinal = concatenatedstring.split(kwargs['stringseparator'])
      else:
        return concatenatedstring

    return listfinal
  
  def pathValid(self, path, flag):
    """
    Description
    -----------
    returns the status if the file or directory exist.
    
    Input Parameter
    ---------------
    path : complete path for file or directory.
    flag : indicate if path provided is file or directory: 'file'/'dir'
    
    Input Parameter Type
    --------------------
    path : str --> required
    flag: str --> required
    
    Return
    ------
    Status if path exist
    
    Return Type
    -----------
    bool
    """
    if self.verbose:
      print("Function call: pathValid(args)")
    if flag.lower() == 'file':
      return os.path.isfile(path)
    elif flag.lower() == 'dir':
      return os.path.isdir(path)
    else:
      return False

  def __getReadMethod__(self, filepath):
    #to-do: documentation
    if self.verbose: print("Function call: getReadMethod(args)")
    filepath = os.path.basename(filepath)
    ext = ''
    read = ''
    if (len(filepath.rsplit('.', 1)) == 2):
      ext = filepath.rsplit('.', 1)[1]
    for key in param.method.keys():
      if ext in param.method[key]:
        read = key
        break 
    if read == '':
      self.warning += 1
      if self.verbose: print("Warning[%d]: extension not fount in parameter list, reading as %s."%(self.warning,param.default))
      read = param.default
    return read

  def __getCommentIdentifier__(self, filepath):
    """
    Description
    -----------
    returns the comment identifier besed on extension.
    
    Input Parameter
    ---------------
    filepath : complete filename with extension.
    
    Input Parameter Type
    --------------------
    ext : str --> required
    
    Return
    ------
    comment identifier
    
    Return Type
    -----------
    str
    """
    if self.verbose: print("Function call: getCommentIdentifier(args)")
    filepath = os.path.basename(filepath)
    ext = ''
    if (len(filepath.rsplit('.', 1)) == 2):
      ext = filepath.rsplit('.', 1)[1]
    if ext.lower() in param.ci.keys():
      return param.ci[ext.lower()]
    else:
      return ''
  
  def skipWhiteLine(self, lines):
    return [l for l in self.toList(lines) if l.strip() != '']

  def __commentHandler__(self, lines, linecomment, handle):
    #to-do: handle if more than one comment identifier is present
    #todo: Handle bulk comments
    #todo: Handle inline comments
    if handle in param.commenthandlermethod and linecomment !='':
      if handle == 'skipcomment':
        return [l for l in self.toList(lines) if not l.strip().startswith(linecomment)]
      else:
        out = []
        for l in self.toList(lines):
          if l.strip().startswith(linecomment):
            out.append(l.replace(linecomment, '', 1))
          else:
            out.append(l)
        return out
    else:
      self.warning += 1
      if self.verbose: print("Warning[%d]: Indicated comment handling method or comment identifier is not defined. Treating all comments as normal lines"%self.warning)
      return self.toList(lines)

  def lineFilter(self, lines, filterval):
    out =self.toList(lines)
    filterval = str(filterval)
    if filterval != '':
      fl = len(filterval)
      if filterval.startswith('*') and filterval.endswith('*'):
        if len(filterval) >= 3: out = [l for l in out if filterval[1:-1] in l]
      elif filterval.startswith('*'):
        out = [l for l in out if l.endswith(filterval[1:fl])]
      elif filterval.endswith('*'):
        out = [l for l in out if l.startswith(filterval[0:-1])]
      elif filterval.startswith('#') and filterval.endswith('#'):
        if len(filterval) >= 3: out = [l for l in out if filterval[1:-1] not in l]
      elif filterval.startswith('#'):
        out = [l for l in out if not l.endswith(filterval[1:fl])]
      elif filterval.endswith('#'):
        out = [l for l in out if not l.startswith(filterval[0:-1])]
      else:
        out = [l for l in out if filterval in l]
    return out

  def lineFormat(self, lines, form, dlm):
    out = self.toList(lines)
    if form in param.supportedformat:
      dlm = self.toList(dlm)
      if form == 'dict':
        d = {}
        for l in out:
          sp = [self.parseString(string) for string in l.strip().split(str(dlm[0]), 1)]
          if len(sp) == 1:
            d[sp[0]] = ''
          else:
            d[sp[0]] = sp[1]
        if len(dlm) == 2:
          for key in d.keys():
            d[key] = [self.parseString(string) for string in d[key].split[str(dlm[1])]]
        out = d
      elif form == 'list':
        out = [[self.parseString(string) for string in l.strip().split(str(dlm[0]), 1)] for l in out]
      else:
        pass
    else:
      self.warning = self.warning + 1
      print("Warning: Selected formatting is not supported. returning list of lines")
    return out