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

class FileUtil():
    """
    Description
    -----------
    Class contains different function for file, string and binary operations.

    Class Public Methods
    --------------------
        parse_string(strdata)
        get_files(path, **kwargs)
        delete_files(path, force=False) # to-do
        parse_bin(bytearr, groupas, **kwargs)
        comment_handler(lines, handle) # to-do - escape condition
        str_filter(lines, filterval)
        line_format(self, lines, form, dlm) # to-do -add vdict and vlist

    Class Private Methods
    ---------------------
        __init__()
        __loadkwargs__(filepath, method, kwargs) # to-do - add kwargs validation
        __to_list__(data)
        __get_read_method__(filepath) # to-do - add validation
        __skip_white_line__(lines) # to-do : remove
        __skip_line_comment__(lines, lcid)
        __skip_inline_comment__(lines, lcid, echar) # to-do : add escape condition
        __uncomment_line__(lines, lcid)
        __read_line_comment__(lines, lcid)
        __uncomment_block__(lines, mlcid, echar) # to-do : add escape condition
        __skip_block_comment__(lines, mlcid, echar) # to-do : add escape condition
        __read_block_comment__(lines, mlcid, echar) # to-do : add escape condition
    """
    def __init__(self):
        self.verbose = False
        self.error = 0
        self.warning = 0

    def __loadkwargs__(self, filepath, method, kwargs):
        #to-do: documentation
        if 'commentidentifier' not in kwargs.keys():
            ci = self.__getCommentIdentifier__(filepath)
            if ci != '':
                if self.verbose:
                    print("Info: Auto selceting %s as comment identifier based on filetype."%(ci))
                kwargs['commentidentifier'] = ci
        kwargupdate = {}
        for kwarg in param.keyval[method.lower()].keys():
            if kwarg in kwargs.keys():
                kwargupdate[kwarg] = kwargs[kwarg]
            else:
                if self.verbose:
                    print("Info: %s parameter is not available in function call, restoring to default value %s"\
                        %(kwarg, str(param.keyval[method.lower()][kwarg])))
                kwargupdate[kwarg] = param.keyval[method.lower()][kwarg]
        return kwargupdate

    def to_list(self, data):
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
            print("Function Call: to_list(args)")
        if not type(data) == list:
            listdata = [data]
        else:
            listdata = data.copy()
        return listdata

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
            bytearr = bytes([byt for byt in bytearr if byt not in self.to_list(kwargs['skipbyte'])])

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
    # to-do : remove
    def path_valid(self, path, flag):
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
    # to-do : remove
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
        if len(filepath.rsplit('.', 1)) == 2:
            ext = filepath.rsplit('.', 1)[1]
        if ext.lower() in param.ci.keys():
            return param.ci[ext.lower()]
        else:
            return ''

    def skip_white_line(self, lines):
        return [l for l in self.to_list(lines) if l.strip() != '']

    def comment_handler(self, lines, handle):
        initial_lines = self.to_list(lines)
        comment = []

        if handle['line_comment_method'] == param.comment_method[0]:
            out = self.skip_line_comment(initial_lines, handle['lcid'])
        elif handle['line_comment_method'] == param.comment_method[1]:
            out = self.uncomment_line(initial_lines, handle['lcid'])
        else:
            comment = self.read_line_comment(initial_lines, handle['lcid'])
            out = self.skip_line_comment(initial_lines, handle['lcid'])

        if handle['block_comment_method'] == param.comment_method[0]:
            out = self.skip_block_comment(out, handle['mlcid'], handle['echar'])
        elif handle['block_comment_method'] == param.comment_method[1]:
            out = self.uncomment_block(out, handle['mlcid'], handle['echar'])
        else:
            comment = self.uncomment_block(out, handle['mlcid'], handle['echar'])
            out = self.skip_block_comment(out, handle['mlcid'], handle['echar'])

        return [out, comment]

    def skip_line_comment(self, lines, lcid):
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
        out = self.to_list(lines)
        for line in out:
            pline = self.parse_string(line)
            if pline.startswith(lcid):
                line = ''
        return out
    # to do : Add escape condition
    def skip_inline_comment(self, lines, lcid, echar):
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
        out= self.to_list(lines)
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

    def uncomment_line(self, lines, lcid):
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
        out = self.to_list(lines)
        for line in out:
            pline = self.parse_string(line)
            if pline.startswith(lcid):
                comline = [item for item in lcid if item.startswith(pline)][0]
                line = line.replace(comline, '', 1)
        return out

    def read_line_comment(self, lines, lcid):
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
        out = self.to_list(lines)
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
    # todo : Add escape condition
    def uncomment_block(self, lines, mlcid, echar):
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
        out = self.to_list(lines)
        for line in out:
            if (echar+mlcid[0] not in line) and (mlcid[0] in line):
                line.replace(mlcid[0], '')
            if (echar+mlcid[1] not in line) and (mlcid[1] in line):
                line.replace(mlcid[1], '')
        return out
    # todo : Add escape condition
    def skip_block_comment(self, lines, mlcid, echar):
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
        out = self.to_list(lines)
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
    # todo : Add escape condition
    def read_block_comment(self, lines, mlcid, echar):
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
        out = self.to_list(lines)
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
        initial_lines =self.to_list(lines)
        out = initial_lines.copy()
        filterval = self.to_list(filterval)
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
        out = self.to_list(lines)
        if form in param.supportedformat:
            dlm = self.to_list(dlm)
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
                        # to - do : correct handle
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
