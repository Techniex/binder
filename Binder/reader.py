# -*- coding: utf-8 -*-
"""
author            = Purnendu Kumar <purnendu@techniex.com>
copyright     = Copyright (C) 2020 Techniex <https://techniex.com>
license         = GPLv3
version         = 1.0
url                 = https://github.com/Techniex/binder
"""
import cv2
from . import fileutil
from . import param

class Reader(fileutil.FileUtil):
    """
    Description
    -----------
    Class contains methods to read text, image or binary(raw) file.

    Public Methods
    ---------------
    read_text(filepath, **kwargs)

    Private Methods
    ---------------
    __init__()
    """

    def read_text(self, filepath, **kwargs):
        """
        Description
        -----------
            reads the text based files and returns the output as dict.
            supported file types are: .txt, .c, .py, .m, .cpp, .h, .csv, .tab, etc.
            (any other plain text based file with utf encoding)

        Arguments
        ---------
            filepath(raw str): Path of text based file to be read.
            kwargs(optional key value pair)
                kwargs['skip_top'](positive int/str) :
                    number of lines to be skipped from top. default = 0
                    till the line where the str is in line is stripped from top.
                kwargs['skip_bottom'](positive int) :
                    number of lines to be skipped from bottom. default = 0
                    first line from bottom with occurance of specified str
                kwargs['comment_handler'](dict):
                    parameters required to operate on comments.
                        comment_handler['comment_method'](str): default = 'none'
                            options = 'none', 'skip', 'uncomment'
                        comment_handler['lcid'](str/tuple) :
                            line comment identifier. default = '#'
                        comment_handler['mlcid'](list) :
                            multiline comment identifier [start, stop] default = []
                        comment_handler['remove_inline_comment'](bool) : default = False
                        comment_handler['docstring_method'](str): default = 'none'
                            options = 'none', 'skip', 'read'
                        comment_handler['ldocid'](str/tuple) :
                            one line docstring identifier. default = "#!"
                        comment_handler['mldocid'](list) :
                            one line docstring identifier. default = ['"""' , '"""']
                        comment_handler['skip_white_lines'](bool): default = False
                        comment_handler['escape_char'](str): escape character, default = ''
                kwargs['filters'](str/list):
                    filter to choose/reject lines from selected section of file. default = []
                kwargs['data_format'](str):
                    output formatting. default = 'line'
                    options = 'line', 'list', 'dict', 'list', 'vlist', 'vdict'
                kwargs['delimeter'](str/list):
                    delimeter to sort header data. default = [',']

        Returns
        -------
        dict with keys: 'error'(int) , 'warning'(int)
        , 'data'(formatted data), 'docstring(dict)', 'data_format'(str).
        """

        if self.verbose:
            print("Function call: read_text(args)")

        #initialize return
        rdict = {'error':self.error, 'warning':self.warning}

        # Read file get all lines in list
        try:
            with open(filepath, 'r') as infile:
                original_lines = infile.read().splitlines()
        except IOError:
            self.error = 1
            rdict['error'] = self.error
            if self.verbose:
                print(param.errordisc[1].format(filepath))
            return rdict

        # Load default kwargs if not provided by user
        kwargs = self.__loadkwargs__(filepath, 'read_text', kwargs)

        # get data
        selected_lines = self.linestrip_top_bottom(original_lines, \
            kwargs['skip_top'], kwargs['skip_bottom'])

        #comment handler
        inline = kwargs['comment_handle']['remove_inline_comment']
        kwargs['comment_handle']['remove_inline_comment'] = False
        [stripped_lines, docstring] = self.comment_handler(selected_lines,\
             kwargs['comment_handle'])
        kwargs['comment_handle']['comment_method'] = 'none'
        kwargs['comment_handle']['docstring_method'] = 'none'
        kwargs['comment_handle']['skip_white_line'] = False
        kwargs['comment_handle']['remove_inline_comment'] = inline

        # filter data
        filtered_lines = self.str_filter(stripped_lines, kwargs['filters'])

        #format data
        [data_format, formatted_data] = self.line_format(filtered_lines,\
             kwargs['data_format'], kwargs['delimeter'], kwargs["comment_handle"])

        rdict['data'] = formatted_data
        rdict['docstring'] = docstring
        rdict['data_format'] = data_format
        if self.verbose:
            print("Success: File read successful\n%s"%filepath)
        return rdict

    # TODO : image read from binary
    def read_image(self, filepath):
        """
        Read image
        """
        return cv2.imread(filepath, -1)

    def read_raw(self, filepath):
        """
        Read Binary
        """
        with open(filepath, 'rb') as rawfile:
            xsap = bytearray(b'')
            for line in rawfile:
                xsap = xsap + line
        return xsap
