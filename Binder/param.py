# -*- coding: utf-8 -*-
"""
author      = Purnendu Kumar <purnendu@techniex.com>
copyright   = Copyright (C) 2020 Techniex <https://techniex.com>
license     = GPLv3
version     = 1.0
url         = https://github.com/Techniex/binder
"""

# dictionary of file extentions
ci = {'c':'//',
         'cpp':'//',
         'csv': '',
         'h':'//',
         'm':'%',
         'py':'#',
         'tab': '',
         'txt':''}

#category
method = {'text' : ['c', 'cpp', 'csv', 'h', 'm', 'py', 'tab', 'txt'],
          'image' : ['png', 'jpg', 'jpeg', 'bmp'],
          'raw' : ['raw','bin','dat', 'ip']}

# default_comment_handler
defaultcommenthandler = {'comment_method':'none', 'lcid':'#', 'mlcid': [],
                        'docstring_method':'none', 'ldocid':'#!', 'mldocid':['"""', '"""'],
                        'remove_inline_comment':False, 'skip_white_lines':False, 'escape_char':'/'}

# default kwarg values
keyval = {'read_text':{'skip_top':0, 'skip_bottom':0, 'filters':[], 'data_format':'line', 'delimeter':',',
                'comment_handler':defaultcommenthandler},
          'image':{},
          'raw':{}}


# default read method
default = 'text'

#endiness
endiness = {'little':'<', 'big':'>', 'native':'', 'l':'<', 'b':'>', 'n':''}

#bytegroupin
groupas = {'int8':'b', 'uint8':'B', 'int16':'h', 'uint16':'H', 'int32':'i', 'uint32':'I', 'int64':'l', 'uint64':'L', 'str':'c', 'single':'f', 'double':'d'}

#bytecount
bytecount = {'int8':1, 'uint8':1, 'int16':2, 'uint16':2, 'int32':4, 'uint32':4, 'int64':8, 'uint64':8, 'str':1, 'single':4, 'double':8}

#supported formats
supportedformat = ['dict', 'line', 'list', 'vdict', 'vlist']

#commentmethod
comment_method = ['skip' , 'uncomment', 'none']
docstring_method = ['skip', 'read', 'none']

#error description
errordisc = {0: 'File operation complete : {file}:',
            -1: 'Error: File[{file}] not found.',
            1: 'IO error, unable to read.\n{file}',
            2: 'Error: Number of skipped lines are more than total number of lines in file[{file}].',
            3: 'Error: Wrong parameter [{para}] values. Conditions: {cd}'}