# -*- coding: utf-8 -*-
"""
author            = Purnendu Kumar <purnendu@techniex.com>
copyright     = Copyright (C) 2020 Techniex <https://techniex.com>
license         = GPLv3
version         = 1.0
url                 = https://github.com/Techniex/binder
"""
import os
import struct
from . import param
# TODO : -1. Linting
class FileUtil():
    """
    Description
    -----------
    Class contains different function for file, string and binary operations.

    Class Public Methods
    --------------------
        comment_handler(lines, handle)
        parse_string(strdata)
        get_files(path, **kwargs)
        delete_files(path, force=False) # TODO: delete files
        parse_bin(bytearr, groupas, **kwargs)
        str_filter(lines, filterval)
        line_format(lines, form, dlm) # 
        write_format(data, dataformat) # TODO: write data from list, dict, vlist, vdict

    Class Private Methods
    ---------------------
        __init__()
        __loadkwargs__(file_path, method, kwargs)
        __validate_read_text__(filepath, updated_kwargs, kwargs)
        __validate_comment_handler__(extn, handle)
        __get_read_method__(filepath) # TODO - add validation
        __skip_white_line__(lines) # TODO : part of comment handling
        __skip_line_comment__(lines, lcid)
        __skip_inline_comment__(lines, lcid, echar)
        __uncomment_line__(lines, lcid)
        __read_line_comment__(lines, lcid)
        __uncomment_block__(lines, mlcid, echar)
        __skip_block_comment__(lines, mlcid, echar)
        __read_block_comment__(lines, mlcid, echar)        
        __to_list__(data)
    """
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.warning = 0
        self.error = 0

    #####################################################################
    # Kwargs Methods
    #####################################################################

    def __loadkwargs__(self, filepath, method, kwargs):
        """
        Description
        -----------
        Common method to call different kwarg validation mechanism.

        Arguments
        ---------
            filepath(raw str): filename with full path
            method(str): which method is being called
            kwargs: supplied with method

        Returns
        -------
        Validated and updated kwargs
        """
        updated_kwargs = param.keyval[method]
        if method == 'read_text':
            verified_kwargs = self.__validate_read_text__(filepath, updated_kwargs, kwargs)
        return verified_kwargs

    def __validate_read_text__(self, filepath, updated_kwargs, kwargs):
        # skip_top
        if 'skip_top' in kwargs:
            if isinstance(kwargs['skip_top'], (int, str)):
                updated_kwargs['skip_top'] = kwargs['skip_top']
        # skip_bottom
        if 'skip_bottom' in kwargs:
            if isinstance(kwargs['skip_bottom'], (int, str)):
                updated_kwargs['skip_bottom'] = kwargs['skip_bottom']
        # filters
        if 'filters' in kwargs:
            filters = self.__to_list__(kwargs['filters'])   
            if all(isinstance(fil, str) for fil in filters):
                updated_kwargs['filters'] = kwargs['filters']
        # data_format
        if 'data_format' in kwargs:
            if kwargs['data_format'] in param.supportedformat:
                updated_kwargs['data_format'] = kwargs['data_format']
        # delimeter
        if 'delimeter' in kwargs:
            if isinstance(kwargs['delimeter'], str):
                updated_kwargs['delimeter'] = kwargs['delimeter']
        # comment handler
        if 'comment_handler' in kwargs:
            filename = os.path.basename(filepath)
            extn = ''
            if len(filename.rsplit('.', 1)) == 2:
                extn = filename.rsplit('.', 1)[1]
            updated_kwargs['comment_handler'] =\
                self.__validate_comment_handler__(extn, kwargs['comment_handler'])
        for key in updated_kwargs:
            if key in kwargs:
                if key != 'comment_handler':
                    if updated_kwargs[key] != kwargs[key]:
                        self.warning += 1
                        if self.verbose:
                            print("Warning %d: Incorrect value for %s"%(self.warning, key))
            else:
                if self.verbose:
                    print("Info: Using default value for %s"%(key))
        return updated_kwargs

    #####################################################################
    # Comment Methods
    #####################################################################

    def comment_handler(self, lines, handle):
        initial_lines = self.__to_list__(lines)
        dsl = {}
        dsml = {}
        # comments
        if handle['comment_method'] == 'skip':
            line_comment_out = self.__skip_line_comment__(initial_lines, handle['lcid'])
            multi_line_comment_out = self.__skip_block_comment__(line_comment_out, handle['mlcid'], handle['escape_char'])
        elif handle['comment_method'] == 'uncomment':
            line_comment_out = self.__uncomment_line__(initial_lines, handle['lcid'])
            multi_line_comment_out = self.__uncomment_block__(line_comment_out, handle['mlcid'], handle['escape_char'])
        else:
            multi_line_comment_out = initial_lines
        # docstring
        if handle['docstring_method'] == 'skip':
            dsl_comment_out = self.__skip_line_comment__(multi_line_comment_out, handle['ldocid'])
            dsml_comment_out = self.__skip_block_comment__(dsl_comment_out, handle['mldocid'], handle['escape_char'])
        elif handle['docstring_method'] == 'read':
            dsl = self.__read_line_comment__(multi_line_comment_out, handle['ldocid'])
            dsml = self.__read_block_comment__(multi_line_comment_out, handle['mldocid'], handle['escape_char'])
            dsl_comment_out = self.__skip_line_comment__(multi_line_comment_out, handle['ldocid'])
            dsml_comment_out = self.__skip_block_comment__(dsl_comment_out, handle['mldocid'], handle['escape_char'])
        else:
            dsml_comment_out = multi_line_comment_out
        # skip white line
        if handle['skip_white_lines']:
            out = self.__skip_white_line__(dsml_comment_out, handle['lcid'])
        else:
            out = dsml_comment_out
        # remove inline comments
        if handle['remove_inline_comment']:
            out = self.__skip_inline_comment__(out, handle['lcid'], handle['escape_char'])
        docstring = {}
        docstring.update(dsl)
        docstring.update(dsml)
        return [out, docstring]

    def __validate_comment_handler__(self, extn, handle):
        """
        Description
        -----------
        Validate and update the handle parameters for comment

        Arguments
        ---------
            extn(str): file extension (lower case)
            handle(dict): parameters for comment handling

        Returns
        -------
        handle(dict) with updated or default values
        """
        default_handler = param.defaultcommenthandler
        default_handler['lcid'] = param.lcom_id[extn]
        default_handler['mlcid'] = param.mlcom_id[extn]
        default_handler['ldocid'] = param.ldoc_id[extn]
        default_handler['mldocid'] = param.mldoc_id[extn]
        if 'comment_method' in handle:
            if handle['comment_method'] in param.comment_method:
                default_handler['comment_method'] = handle['comment_method']
        if 'lcid' in handle:
            if isinstance(handle['lcid'], (str, tuple)):
                default_handler['lcid'] = handle['lcid']
        if 'mlcid' in handle:
            if isinstance(handle['mlcid'], list):
                if len(handle['mlcid']) == 2 and all(isinstance(val, str) \
                    for val in handle['mlcid']):
                    default_handler['mlcid'] = handle['mlcid']
        if 'remove_inline_comment' in handle:
            if isinstance(handle['remove_inline_comment'], bool):
                default_handler['remove_inline_comment'] = handle['remove_inline_comment']
        if 'docstring_method' in handle:
            if handle['docstring_method'] in param.docstring_method:
                default_handler['docstring_method'] = handle['docstring_method']
        if 'ldocid' in handle:
            if isinstance(handle['ldocid'], (str, tuple)):
                default_handler['ldocid'] = handle['ldocid']
        if 'mldocid' in handle:
            if isinstance(handle['mldocid'], list):
                if len(handle['mldocid']) == 2 and all(isinstance(val, str) \
                    for val in handle['mldocid']):
                    default_handler['mldocid'] = handle['mldocid']
        if 'skip_white_line' in handle:
            if isinstance(handle['skip_white_line'], bool):
                default_handler['skip_white_line'] = handle['skip_white_line']
        if 'escape_char' in handle:
            if isinstance(handle['escape_char'], str):
                default_handler['escape_char'] = handle['escape_char']

        for key in default_handler:
            if key in handle:
                if default_handler[key] != handle[key]:
                    self.warning += 1
                    if self.verbose:
                        print("Warning %d: Incorrect value for comment_handler['%s']"\
                            %(self.warning, key))
            else:
                if self.verbose:
                    print("Info : Restoring default value for comment_handler['%s']"\
                        %(self.warning, key))
        return default_handler

    def __skip_line_comment__(self, lines, lcid):
        """
        Description
        -----------
        Removes the line comments if they:
        are in whole line

        Arguments
        ---------
            lines(str/list): input data
            lcid(str/tuple): comment identifier/s

        Returns
        -------
        List of strings without line comments
        """
        out = self.__to_list__(lines)
        for line in out:
            pline = self.parse_string(line)
            if pline.startswith(lcid):
                line = ''
        return out

    def __skip_inline_comment__(self, lines, lcid, echar):
        """
        Description
        -----------
        Removes the line comments if they:
        are in whole line
        or are added with code as explanation in same line

        Arguments
        ---------
            lines(str/list): input data
            lcid(str/tuple): comment identifier/s
            echar(str): escape character

        Returns
        -------
        List of strings without line comments
        """
        out= self.__to_list__(lines)
        for line in out:
            linecs = [item for item in lcid if item in line and echar+item not in line]
            if len(linecs != 0):
                if len(linecs) > 1:
                    comidx = []
                    for linec in linecs:
                        comidx.append(line.index(linec))
                    comline = line[min(comidx)]
                else: comline = linecs[0]
                line = line.split(comline)[0]
        return out

    def __uncomment_line__(self, lines, lcid):
        """
        Description
        -----------
        Uncomment line comments which occupy whole line

        Arguments
        ---------
            lines(str/list): input data
            lcid(str/tuple): comment identifier/s

        Returns
        -------
        List of strings with comments uncommented.
        """
        out = self.__to_list__(lines)
        for line in out:
            pline = self.parse_string(line)
            if pline.startswith(lcid):
                comline = [item for item in lcid if item.startswith(pline)][0]
                line = line.replace(comline, '', 1)
        return out

    def __read_line_comment__(self, lines, lcid):
        """
        Description
        -----------
        Read Line comments as doc string
        Group continious line comments together

        Arguments
        ---------
            lines(str/list): input data
            lcid(str/tuple): comment identifier/s

        Returns
        -------
        grouped comments with previous line as key for dictionary
        """
        comment = {}
        out = self.__to_list__(lines)
        comkey = "First"
        comflag = False
        for count, line in enumerate(out):
            pline = self.parse_string(line)
            if pline.startswith(lcid):
                if count == 0:
                    comment[comkey] = []
                    comment[comkey].append(line)
                    comflag = True
                else:
                    if comflag:
                        comment[comkey].append(line)
                    else:
                        comkey = out[count-1]
                        comment[comkey] = []
                        comment[comkey].append(line)
                        comflag = True
            else:
                comflag = False
        return comment

    def __uncomment_block__(self, lines, mlcid, echar):
        """
        Description
        -----------
        Uncomment a block comment

        Arguments
        ---------
            lines(str/list) : input data
            mlcid(list) : mlcid[0] = start id, mlcid[1] = stop id
                e.g. ["/*", "*/"] for c file
            echar : escape character

        Returns
        -------
        list of strings with uncommented block comment
        """
        out = self.__to_list__(lines)
        for line in out:
            if (echar+mlcid[0] not in line) and (mlcid[0] in line):
                line.replace(mlcid[0], '')
            if (echar+mlcid[1] not in line) and (mlcid[1] in line):
                line.replace(mlcid[1], '')
        return out

    def __skip_block_comment__(self, lines, mlcid, echar):
        """
        Description
        -----------
        Skip a block comment

        Arguments
        ---------
            lines(str/list) : input data
            mlcid(list) : mlcid[0] = start id, mlcid[1] = stop id
                e.g. ["/*", "*/"] for c file
            echar : escape character

        Returns
        -------
        list of strings with uncommented block comment
        """
        out = self.__to_list__(lines)
        comflag = False
        for line in out:
            if (echar+mlcid[0] not in line) and (mlcid[0] in line):
                line = line.split(mlcid[0])[0]
                comflag = True
            if comflag:
                if (echar+mlcid[1] not in line) and (mlcid[1] in line):
                    lval = line.split(mlcid[1])[1:]
                    line = mlcid[1].join(lval)
                    comflag = False
                else:
                    line = ''
        return out

    def __read_block_comment__(self, lines, mlcid, echar):
        """
        Description
        -----------
        Read Line comments as doc string
        Group continious line comments together

        Arguments
        ---------
            lines(str/list): input data
            mlcid(list): mlcid[0] = start id, mlcid[1] = stop id
                e.g. ["/*", "*/"] for c file

        Returns
        -------
        grouped comments with previous line as key for dictionary
        """
        comment = {}
        out = self.__to_list__(lines)
        comkey = "First"
        comflag = False
        for count, line in enumerate(out):
            pline = self.parse_string(line)
            if not comflag:
                if pline.startswith(mlcid[0]):
                    if count == 0:
                        comment[comkey] = []
                        comment[comkey].append(line)
                        comflag = True
                    else:
                        comkey = out[count-1]
                        comment[comkey] = []
                        comment[comkey].append(line)
                        comflag = True
            else:
                comment[comkey].append(line)
                if pline.endswith(mlcid[0]):
                    comflag = False
        return comment

    def __skip_white_line__(self, lines, lcid):
        initial_lines = self.__to_list__(lines)
        listlines = self.__to_list__(lines)
        if isinstance(lcid, str):
            lcid = (lcid)
        for line in listlines:
            templine = line
            for member in lcid:
                templine = templine.replace(member, '')
            line = templine.strip()
        out = [initial_lines[listlines.index(nwl)] for nwl in listlines if nwl != '']
        return out

    #####################################################################
    # Filter and Formatting Methods
    #####################################################################

    def __to_list__(self, data):
        """
        Description
        -----------
        if input is list return as it is else convert to list and return

        Arguments
        ---------
        data(any): input data

        Returns
        -------
        list from input data
        """
        if self.verbose:
            print("Function Call: __to_list__(args)")
        if not type(data) == list:
            listdata = [data]
        else:
            listdata = data.copy()
        return listdata

    def linestrip_top_bottom(self, lines, *args):
        """
        Description
        -----------
        Skip top and bottom desitred lines and return remaining stripped lines.

        Arguments
        ---------
            lines(str/list): original data input
            arg[0](int/str): skip top keyword or num lines
            arg[1](int/str): skip from bottom keyword or num lines
            * if arguments not provided both are set to 0

        Returns
        -------
        Stripped lines(list)
        """
        lines = self.__to_list__(lines)
        if len(args) == 0:
            skip_top = 0
            skip_bottom = 0
        elif len(args) == 1:
            skip_top = args[0]
            skip_bottom = 0
        else:
            skip_top = args[0]
            skip_bottom = args[1]

        if isinstance(skip_top, str):
            search_top = [lines.index(val) for val in lines if skip_top in val]
            if search_top == []:
                self.warning += 1
                if self.verbose:
                    print("Warning %d: %s keyword not in file, neglected."\
                        %(self.warning, skip_top))
                top_stripped_lines = lines
            else:
                top_stripped_lines = lines[search_top[0]+1:]
        elif isinstance(skip_top, int):
            if skip_top > 0 and skip_top <= len(lines):
                top_stripped_lines = lines[skip_top:]
            else:
                self.warning += 1
                if self.verbose:
                    print("Warning %d: Num lines for top skipping out of bound, neglected."\
                        %(self.warning))
                top_stripped_lines = lines
        else:
            self.warning += 1
            if self.verbose:
                print("Warning %d: skip_top(arg[0]) should be either str or int, neglected."\
                    %(self.warning))
            top_stripped_lines = lines

        if isinstance(skip_bottom, str):
            search_bottom = [lines.index(val) for val in top_stripped_lines if skip_bottom in val]
            if search_bottom == []:
                self.warning += 1
                if self.verbose:
                    print("Warning %d: %s keyword not in file after top skipped, neglected."\
                        %(self.warning, skip_bottom))
                stripped_lines = top_stripped_lines
            else:
                top_stripped_lines = top_stripped_lines[:search_bottom[-1]]
        if isinstance(skip_bottom, int):
            if skip_bottom > 0 and skip_bottom <= len(top_stripped_lines):
                stripped_lines = top_stripped_lines[:len(top_stripped_lines) - skip_bottom]
            else:
                self.warning += 1
                if self.verbose:
                    print("Warning %d: Num lines for bottom skipping out of bound, neglected."\
                        %(self.warning))
                stripped_lines = top_stripped_lines
        else:
            self.warning += 1
            if self.verbose:
                print("Warning %d: skip_bottom(arg[1]) should be either str or int, neglected."\
                    %(self.warning))
            stripped_lines = top_stripped_lines
        
        return stripped_lines

    def str_filter(self, lines, filterval):
        """
        Description
        -----------
        Filters the supplied input lines with supplied set of filtervalues.
        And returns a list of strings satisfying filter criteria.

        Arguments
        ---------
        lines(str/list): Input string of list of strings to be filtered.
        filterval(str/list): filtering keywords
            Supported keyword styles:
                min keyword length = 1 char
                1. "keyword" : if present anywhere in string
                2. "*(keyword)*" : if present anywhere in string
                3. "*(keyowrd)" : if ends with keyword
                4. "(keyword)*" : if startswith keyword
                5. "#(keyword)#" : if not present anywhere in string
                6. "#(keyword)" : if not ends with keyword
                7. "(keyword)#" : if not starts with keyword
                by default all filterval arguments are "AND" to add an argument in "OR"
                use "-" before keyword style.
                e.g. "-*(keyword)*"

        Returns
        -------
        list of filtered strings

        """
        initial_lines =self.__to_list__(lines)
        out = initial_lines.copy()
        filterval = self.__to_list__(filterval)
        orval = []
        orflag = False
        for fval in filterval:
            if fval.startswith("-(") or fval.startswith("-*(") or fval.startswith("-#("):
                orflag = True
                old_out = out
                fval = fval.strip("-")
            fval_len = len(fval)
            if fval.startswith('*(') and fval.endswith(')*') and fval_len >= 5:
                out = [filtered_element for filtered_element in out \
                    if fval[2:fval_len-2] in filtered_element]
            elif fval.startswith('*(') and fval.endswith(')') and fval_len >= 4:
                out = [filtered_element for filtered_element in out \
                    if filtered_element.endswith(fval[2:fval_len-1])]
            elif fval.startswith('(') and fval.endswith(')*') and fval_len >= 4:
                out = [filtered_element for filtered_element in out \
                    if filtered_element.startswith(fval[1:fval_len-2])]
            elif fval.startswith('#(') and fval.endswith(')#') and fval_len >= 5:
                out = [filtered_element for filtered_element in out \
                    if fval[2:fval_len-2] not in filtered_element]
            elif fval.startswith('#(') and fval.endswith(')') and fval_len >= 4:
                out = [filtered_element for filtered_element in out \
                    if not filtered_element.endswith(fval[2:fval_len-1])]
            elif fval.startswith('(') and fval.endswith(')#') and fval_len >= 4:
                out = [filtered_element for filtered_element in out \
                    if not filtered_element.startswith(fval[1:fval_len-2])]
            else:
                out = [filtered_element for filtered_element in out if fval in filtered_element]
            if orflag:
                orval = orval + out.copy()
                out = old_out
                orflag = False
        filout = out + orval
        # organise in sequence as provided
        out = [val for val in initial_lines if val in filout]

        return out

    def line_format(self, lines, form, dlm, handle):
        """
        Description
        -----------
        Format the input string lines as specified

        Arguments
        ---------
            lines(str/list): input data
            form(str): output format
            dlm(str/list): delimeter [max length 2, min length 1]
            handle(dict): to remove inline comments

        Returns
        -------
        formatted data as list / list of list / dict
        """
        out = self.__to_list__(lines)
        if form in param.supportedformat:
            dlm = self.__to_list__(dlm)
            if form == 'dict':
                dout = {}
                for line in out:
                    splt = [self.parse_string(string) for string in line.strip().split(str(dlm[0]), 1)]
                    if len(splt) == 1:
                        dout[splt[0]] = ''
                    else:
                        dout[splt[0]] = splt[1]
                if len(dlm) == 2:
                    for key in dout.keys():
                        dout[key] = [self.parse_string(string) for string in dout[key].split[str(dlm[1])]]
                        # TODO : correct handle
                        dout[key] = self.comment_handler(dout[key], handle)
                out = dout
            elif form == 'list' or form == 'vlist' or form == 'vdict':
                out = [[self.parse_string(string) for string in l.strip().split(str(dlm[0]), 1)] for l in out]
                if form == 'vlist' or form == 'vdict' :
                    if len(list(set([len(line) for line in out]))) == 1:
                        out = [[out[lineitr][itr] for lineitr in range(0,len(out))] for itr in range(0,len(out[0]))]
                        if form == 'vdict':
                            dout = {}
                            for line in out:
                                dout[line[0]] = line[1:]
                            out = dout
                            form = 'vdict'
                        else:
                            form = 'vlist'
                    else:
                        form = 'list'
                        self.warning = self.warning + 1
                        print("Warning %d: size mismatch"%self.warning)
            else:
                form = 'line'
                pass
        else:
            form = 'line'
            self.warning = self.warning + 1
            print("Warning: Selected formatting is not supported. returning list of lines")
        return [form, out]

    def parse_string(self, strdata):
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
            print("Function Call: parse_string(args)")
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
            signedfloat = (outdata[1:].replace('.', '', 1).isdigit()) and decimal
            unsignedfloat = False
        else:
            signedfloat = False
            unsignedfloat = (outdata.replace('.', '', 1).isdigit()) and decimal

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

    def parse_bin(self, bytearr, groupas, **kwargs):
        """
        Description
        -----------
        Parse binary byte array as per key-value pair.

        Input Parameter
        ---------------
        bytearr: Byte array.
        groupas: output type: int8, uint8, int16, uint16, int32, uint32, int64, uint64,
            str, single, double.
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
            print("Function Call: parse_bin(args)")

        #check if parameters are available else set to default
        if 'skipcount' in kwargs.keys():
            bytearr = bytearr[kwargs['skipcount']:]

        if 'skipbyte' in kwargs.keys():
            bytearr = bytes([byt for byt in bytearr if byt not in self.__to_list__(kwargs['skipbyte'])])

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

        placeholder = placeholder + param.groupas[outtype]
        remainedbytes = len(bytearr) % param.bytecount[outtype]

        if remainedbytes != 0:
            print("Warning: Length mis-matched. ignoring last %d bytes"%remainedbytes)
            bytearr = bytearr[0:(0-remainedbytes)]

        listextract = [struct.unpack(placeholder, bytearr[x:x+param.bytecount[outtype]]) \
            for x in range(0, len(bytearr), param.bytecount[outtype])]

        if outtype == 'str':
            concatenatedstring = ''.join(listextract)
            if split:
                listfinal = concatenatedstring.split(kwargs['stringseparator'])
            else:
                return concatenatedstring

        return listfinal

    #####################################################################
    # File Methods
    #####################################################################

    def get_files(self, path, **kwargs):
        """
        Description
        -----------
        Provided the top folder and filter component.
        get_files function returns the list of all files in the directory.

        Arguments
        ---------------
        path(raw str): Path of top folder to be scanned for files.
        kwargs = dictionary with keys 'filters' and 'reccursive'
        Values can be both string of list of strings
            filters(str/list): filter keywords. check str_filter method for details about keyword.
            reccursive(bool): to look through subdirectories or not default value: False

        Returns
        -------
        List of files in directory as well as subdirectories matching filter constraint.

        """
        if self.verbose:
            print("Function Call: get_files(args)")

        # validate path
        if os.path.exists(path):
            files = [os.path.join(path, fileval) for fileval in os.listdir(path) \
                if os.path.isfile(os.path.join(path, fileval))]

            if "filters" in kwargs.keys():
                files = self.str_filter(files, kwargs['filters'])

            folders = [os.path.join(path, dirval) for dirval in os.listdir(path) \
                if os.path.isdir(os.path.join(path, dirval))]

            if "reccursive" not in kwargs.keys():
                kwargs["reccursive"] = True
            for folder in folders:
                if kwargs['reccursive']:
                    files = files + self.get_files(folder, **kwargs)
        else:
            self.error = 10
            print("Error %d: specified path doesn't exist.\n%s"%(self.error, path))
            files = []
        return files

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
            print("Function call: path_valid(args)")
        if flag.lower() == 'file':
            return os.path.isfile(path)
        elif flag.lower() == 'dir':
            return os.path.isdir(path)
        else:
            return False

    def delete_files(self, path, force=False):
        pass

    def __get_read_method__(self, filepath):
        #to-do: documentation
        if self.verbose: print("Function call: getReadMethod(args)")
        filepath = os.path.basename(filepath)
        ext = ''
        read = ''
        if len(filepath.rsplit('.', 1)) == 2:
            ext = filepath.rsplit('.', 1)[1]
        for key in param.method.keys():
            if ext in param.method[key]:
                read = key
                break
        if read == '':
            self.warning += 1
            if self.verbose: print("Warning[%d]: extension not fount in parameter list, reading as %s."%(self.warning, param.default))
            read = param.default
        return read
