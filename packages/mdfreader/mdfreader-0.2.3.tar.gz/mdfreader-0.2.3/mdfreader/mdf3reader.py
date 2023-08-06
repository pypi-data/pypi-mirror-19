# -*- coding: utf-8 -*-
""" Measured Data Format file reader module for version 3.x

Platform and python version
----------------------------------------
With Unix and Windows for python 2.6+ and 3.2+

:Author: `Aymeric Rateau <https://github.com/ratal/mdfreader>`__

Created on Sun Oct 10 12:57:28 2010

Dependencies
-------------------
- Python >2.6, >3.2 <http://www.python.org>
- Numpy >1.6 <http://numpy.scipy.org>
- Sympy to convert channels with formula

Attributes
--------------
PythonVersion : float
    Python version currently running, needed for compatibility of both python 2.6+ and 3.2+

mdf3reader module
--------------------------
"""
from __future__ import print_function

from numpy import average, right_shift, bitwise_and, diff, max, min, interp
from numpy import asarray, zeros, recarray, array, reshape, searchsorted
from numpy.core.records import fromfile
from math import log, exp
from sys import platform, version_info, stderr
from time import strftime, time
from struct import pack, Struct
from io import open  # for python 3 and 2 consistency
try:
    from .mdf import mdf_skeleton
    from .mdfinfo3 import info3
except:
    from mdf import mdf_skeleton
    from mdfinfo3 import info3
PythonVersion = version_info
PythonVersion = PythonVersion[0]

def linearConv(data, conv):  # 0 Parametric, Linear: Physical =Integer*P2 + P1
    """ apply linear conversion to data

    Parameters
    ----------------
    data : numpy 1D array
        raw data to be converted to physical value
    conv : mdfinfo3.info3 conversion block ('CCBlock') dict

    Returns
    -----------
    converted data to physical value
    """
    if conv['P2'] == 1.0 and conv['P1'] in (0.0, -0.0):
        return data  # keeps dtype probably more compact than float64
    else:
        return data * conv['P2'] + conv['P1']


def tabInterpConv(data, conv):  # 1 Tabular with interpolation
    """ apply Tabular interpolation conversion to data

    Parameters
    ----------------
    data : numpy 1D array
        raw data to be converted to physical value
    conv : mdfinfo3.info3 conversion block ('CCBlock') dict

    Returns
    -----------
    converted data to physical value
    """
    tmp = array([(key, val['int'], val['phys']) for (key, val) in conv.items()])
    return interp(data, tmp[:,1], tmp[:,2])

def tabConv(data, conv):  # 2 Tabular
    """ apply Tabular conversion to data

    Parameters
    ----------------
    data : numpy 1D array
        raw data to be converted to physical value
    conv : mdfinfo3.info3 conversion block ('CCBlock') dict

    Returns
    -----------
    converted data to physical value
    """
    tmp = array([(key, val['int'], val['phys']) for (key, val) in conv.items()])
    indexes = searchsorted(tmp[:, 1], data)
    return tmp[indexes, 2]


def polyConv(data, conv):  # 6 Polynomial
    """ apply polynomial conversion to data

    Parameters
    ----------------
    data : numpy 1D array
        raw data to be converted to physical value
    conv : mdfinfo3.info3 conversion block ('CCBlock') dict

    Returns
    -----------
    converted data to physical value
    """
    return (conv['P2'] - conv['P4'] * (data - conv['P5'] - conv['P6'])) / (conv['P3'] * (data - conv['P5'] - conv['P6']) - conv['P1'])


def expConv(data, conv):  # 7 Exponential
    """ apply exponential conversion to data

    Parameters
    ----------------
    data : numpy 1D array
        raw data to be converted to physical value
    conv : mdfinfo3.info3 conversion block ('CCBlock') dict

    Returns
    -----------
    converted data to physical value
    """
    if conv['P4'] == 0 and conv['P1'] != 0 and conv['P2'] != 0:
        return exp(((data - conv['P7']) * conv['P6'] - conv['P3']) / conv['P1']) / conv['P2']
    elif conv['P1'] == 0 and conv['P4'] != 0 and conv['P5'] != 0:
        return exp((conv['P3'] / (data - conv['P7']) - conv['P6']) / conv['P4']) / conv['P5']
    else:
        print('Non possible conversion parameters for channel ', file=stderr)


def logConv(data, conv):  # 8 Logarithmic
    """ apply logarithmic conversion to data

    Parameters
    ----------------
    data : numpy 1D array
        raw data to be converted to physical value
    conv : mdfinfo3.info3 conversion block ('CCBlock') dict

    Returns
    -----------
    converted data to physical value
    """
    if conv['P4'] == 0 and conv['P1'] != 0 and conv['P2'] != 0:
        return log(((data - conv['P7']) * conv['P6'] - conv['P3']) / conv['P1']) / conv['P2']
    elif conv['P1'] == 0 and conv['P4'] != 0 and conv['P5'] != 0:
        return log((conv['P3'] / (data - conv['P7']) - conv['P6']) / conv['P4']) / conv['P5']
    else:
        print('Non possible conversion parameters for channel ', file=stderr)


def rationalConv(data, conv):  # 9 rational
    """ apply rational conversion to data

    Parameters
    ----------------
    data : numpy 1D array
        raw data to be converted to physical value
    conv : mdfinfo3.info3 conversion block ('CCBlock') dict

    Returns
    -----------
    converted data to physical value
    """
    return(conv['P1'] * data * data + conv['P2'] * data + conv['P3']) / (conv['P4'] * data * data + conv['P5'] * data + conv['P6'])


def formulaConv(data, conv):  # 10 Text Formula
    """ apply formula conversion to data

    Parameters
    ----------------
    data : numpy 1D array
        raw data to be converted to physical value
    conv : mdfinfo3.info3 conversion block ('CCBlock') dict

    Returns
    -----------
    converted data to physical value

    Notes
    --------
    Requires sympy module
    """
    try:
        from sympy import lambdify, symbols
        X = symbols('X')  # variable is X
        formula = conv['textFormula']
        formula = formula[:formula.find('\x00')]  # remove trailing text after 0
        formula = formula.replace('pow(', 'power(')  # adapt ASAM-MCD2 syntax to sympy
        expr = lambdify(X, formula, modules='numpy', dummify=False)  # formula to function for evaluation
        return expr(data)
    except:
        print('Please install sympy to convert channel ', file=stderr)
        print('Failed to convert formulae ' + conv['textFormula'], file=stderr)


def textRangeTableConv(data, conv):  # 12 Text range table
    """ apply text range table conversion to data

    Parameters
    ----------------
    data : numpy 1D array
        raw data to be converted to physical value
    conv : mdfinfo3.info3 conversion block ('CCBlock') dict

    Returns
    -----------
    converted data to physical value
    """
    try:
        npair = len(conv)
        lower = [conv[pair]['lowerRange'] for pair in range(npair)]
        upper = [conv[pair]['upperRange'] for pair in range(npair)]
        text = [conv[pair]['Textrange'] for pair in range(npair)]
        temp = []
        for Lindex in range(len(data)):
            value = text[0]  # default value
            for pair in range(1, npair):
                if lower[pair] <= data[Lindex] <= upper[pair]:
                    value = text[pair]
                    break
            temp.append(value)
        try:
            temp = asarray(temp)  # try to convert to numpy
        except:
            pass
        return temp
    except:
        print('Failed to convert text to range table', file=stderr)


class recordChannel():

    """ recordChannel class gathers all about channel structure in a record

    Attributes
    --------------
    name : str
        Name of channel
    unit : str, default empty string
        channel unit
    desc : str
        channel description
    conversion : info class
        conversion dictionnary
    channelNumber : int
        channel number corresponding to mdfinfo3.info3 class
    signalDataType : int
        signal type according to specification
    bitCount : int
        number of bits used to store channel record
    nBytes : int
        number of bytes (1 byte = 8 bits) taken by channel record
    dataFormat : str
        numpy dtype as string
    CFormat : struct class instance
        struct instance to convert from C Format
    byteOffset : int
        position of channel record in complete record in bytes
    bitOffset : int
        bit position of channel value inside byte in case of channel having bit count below 8
    RecordFormat : list of str
        dtype format used for numpy.core.records functions ((name,name_title),str_stype)
    channelType : int
        channel type
    posBeg : int
        start position in number of bit of channel record in complete record
    posEnd : int
        end position in number of bit of channel record in complete record

    Methods
    ------------
    __init__(info, dataGroup, channelGroup, channelNumber, recordIDsize)
        constructor
    __str__()
        to print class attributes
    """

    def __init__(self, info, dataGroup, channelGroup, channelNumber, recordIDsize):
        """ recordChannel class constructor

        Parameters
        ------------
        info : mdfinfo3.info3 class
        dataGroup : int
            data group number in mdfinfo3.info3 class
        channelGroup : int
            channel group number in mdfinfo3.info3 class
        channelNumber : int
            channel number in mdfinfo3.info3 class
        recordIDsize : int
            size of record ID in Bytes
        """
        self.name = info['CNBlock'][dataGroup][channelGroup][channelNumber]['signalName']
        self.channelNumber = channelNumber
        self.signalDataType = info['CNBlock'][dataGroup][channelGroup][channelNumber]['signalDataType']
        self.bitCount = info['CNBlock'][dataGroup][channelGroup][channelNumber]['numberOfBits']
        ByteOrder = info['IDBlock']['ByteOrder']
        self.dataFormat = _arrayformat3(self.signalDataType, self.bitCount, ByteOrder[0])
        self.CFormat = Struct(_datatypeformat3(self.signalDataType, self.bitCount, ByteOrder[0]))
        self.nBytes = self.bitCount // 8 + 1
        if self.bitCount % 8 == 0:
            self.nBytes -= 1
        recordbitOffset = info['CNBlock'][dataGroup][channelGroup][channelNumber]['numberOfTheFirstBits']
        self.byteOffset = recordbitOffset // 8
        self.bitOffset = recordbitOffset % 8
        self.RecordFormat = ((self.name, self.name + '_title'), self.dataFormat)
        self.channelType = info['CNBlock'][dataGroup][channelGroup][channelNumber]['channelType']
        self.posBeg = recordIDsize + self.byteOffset
        self.posEnd = recordIDsize + self.byteOffset + self.nBytes
        if 'physicalUnit' in info['CCBlock'][dataGroup][channelGroup][channelNumber]:
            self.unit = info['CCBlock'][dataGroup][channelGroup][channelNumber]['physicalUnit']
        else:
            self.unit = ''
        if 'signalDescription' in info['CNBlock'][dataGroup][channelGroup][channelNumber]:
            self.desc = info['CNBlock'][dataGroup][channelGroup][channelNumber]['signalDescription']
        else:
            self.desc = ''
        self.conversion = info['CCBlock'][dataGroup][channelGroup][channelNumber]

    def __str__(self):
        output = str(self.channelNumber) + ' '
        output += self.name + ' '
        output += str(self.signalDataType) + ' '
        output += str(self.channelType) + ' '
        output += str(self.RecordFormat) + ' '
        output += str(self.bitOffset) + ' '
        output += str(self.byteOffset)
        output += 'unit ' + self.unit
        output += 'description ' + self.desc
        return output


class record(list):

    """ record class lists recordchannel classes, it is representing a channel group

    Attributes
    --------------
    recordLength : int
        length of record corresponding of channel group in Byte
    numberOfRecords : int
        number of records in data block
    recordID : int
        recordID corresponding to channel group
    recordIDsize : int
        size of recordID
    dataGroup : int:
        data group number
    channelGroup : int
        channel group number
    numpyDataRecordFormat : list
        list of numpy (dtype) for each channel
    dataRecordName : list
        list of channel names used for recarray attribute definition
    master : dict
        define name and number of master channel
    recordToChannelMatching : dict
        helps to identify nested bits in byte
    channelNames : list
        channel names to be stored, useful for low memory consumption but slow

    Methods
    ------------
    addChannel(info, channelNumber)
    loadInfo(info)
    readSortedRecord(fid, pointer, channelList=None)
    readUnsortedRecord(buf, channelList=None)
    """

    def __init__(self, dataGroup, channelGroup):
        self.recordLength = 0
        self.numberOfRecords = 0
        self.recordID = 0
        self.recordIDsize = 0
        self.dataGroup = dataGroup
        self.channelGroup = channelGroup
        self.numpyDataRecordFormat = []
        self.dataRecordName = []
        self.master = {}
        self.master['name'] = 'master_' + str(dataGroup)
        self.master['number'] = None
        self.recordToChannelMatching = {}
        self.channelNames = []

    def __repr__(self):
        output = 'Channels :\n'
        for chan in self.channelNames:
            output += chan + '\n'
        output += 'Datagroup number : ' + str(self.dataGroup) + '\n'
        if self.master['name'] is not None:
            output += 'Master channel : ' + self.master['name'] + '\n'
        output += 'Numpy records format : \n'
        for record in self.numpyDataRecordFormat:
            output += str(record) + '\n'
        return output

    def addChannel(self, info, channelNumber):
        """ add a channel in class

        Parameters
        ----------------
        info : mdfinfo3.info3 class
        channelNumber : int
            channel number in mdfinfo3.info3 class

        """
        self.append(recordChannel(info, self.dataGroup, self.channelGroup, channelNumber, self.recordIDsize))
        self.channelNames.append(self[-1].name)

    def loadInfo(self, info):
        """ gathers records related from info class

        Parameters
        ----------------
        info : mdfinfo3.info3 class

        """
        self.recordIDsize = info['DGBlock'][self.dataGroup]['numberOfRecordIDs']
        self.recordID = info['CGBlock'][self.dataGroup][self.channelGroup]['recordID']
        if not self.recordIDsize == 0:  # record ID existing
            self.dataRecordName.append('RecordID' + str(self.channelGroup))
            format = (self.dataRecordName[-1], self.dataRecordName[-1] + '_title')
            self.numpyDataRecordFormat.append((format, 'uint8'))
        self.recordLength = info['CGBlock'][self.dataGroup][self.channelGroup]['dataRecordSize']
        self.numberOfRecords = info['CGBlock'][self.dataGroup][self.channelGroup]['numberOfRecords']
        for channelNumber in list(info['CNBlock'][self.dataGroup][self.channelGroup].keys()):
            channel = recordChannel(info, self.dataGroup, self.channelGroup, channelNumber, self.recordIDsize)
            if self.master['number'] is None or channel.channelType == 1:  # master channel found
                self.master['name'] = channel.name
                self.master['number'] = channelNumber
            self.append(channel)
            self.channelNames.append(channel.name)
            if len(self) > 1 and channel.byteOffset == self[-2].byteOffset:  # several channels in one byte, ubit1 or ubit2
                self.recordToChannelMatching[channel.name] = self.recordToChannelMatching[self[-2].name]
            else:  # adding bytes
                self.recordToChannelMatching[channel.name] = channel.name
                self.numpyDataRecordFormat.append(channel.RecordFormat)
                self.dataRecordName.append(channel.name)
        if self.recordIDsize == 2:  # second record ID at end of record
            self.dataRecordName.append('RecordID' + str(self.channelGroup) + '_2')
            format = (self.dataRecordName[-1], self.dataRecordName[-1] + '_title')
            self.numpyDataRecordFormat.append((format, 'uint8'))

    def readSortedRecord(self, fid, pointer, channelList=None):
        """ reads record, only one channel group per datagroup

        Parameters
        ----------------
        fid : float
            file identifier
        pointer
            position in file of data block beginning
        channelList : list of str, optional
            list of channel to read

        Returns
        -----------
        rec : numpy recarray
            contains a matrix of raw data in a recarray (attributes corresponding to channel name)

        Notes
        --------
        If channelList is None, read data using numpy.core.records.fromfile that is rather quick.
        However, in case of large file, you can use channelList to load only interesting channels or
        only one channel on demand, but be aware it might be much slower.

        """
        fid.seek(pointer)
        if channelList is None:  # reads all, quickest but memory consuming
            return fromfile(fid, dtype=self.numpyDataRecordFormat, shape=self.numberOfRecords, names=self.dataRecordName)
        else:  # reads only some channels from a sorted data block
            # memory efficient but takes time
            if len(list(set(channelList) & set(self.channelNames))) > 0:  # are channelList in this dataGroup
                # check if master channel is in the list
                if not self.master['name'] in channelList:
                    channelList.append(self.master['name'])  # adds master channel
                rec = {}
                recChan = []
                numpyDataRecordFormat = []
                for channel in channelList:  # initialise data structure
                    rec[channel] = 0
                for channel in self:  # list of recordChannels from channelList
                    if channel.name in channelList:
                        recChan.append(channel)
                        numpyDataRecordFormat.append(channel.RecordFormat)
                rec = zeros((self.numberOfRecords, ), dtype=numpyDataRecordFormat)
                recordLength = self.recordIDsize + self.recordLength
                for r in range(self.numberOfRecords):  # for each record,
                    buf = fid.read(recordLength)
                    for channel in recChan:
                        rec[channel.name][r] = channel.CFormat.unpack(buf[channel.posBeg:channel.posEnd])[0]
                return rec.view(recarray)

    def readUnsortedRecord(self, buf, channelList=None):
        """ Not implemented yet, no reference files available to test it
        """
        pass


class DATA(dict):

    """ DATA class is organizing record classes itself made of recordchannel.
    This class inherits from dict. Keys are corresponding to channel group recordID
    A DATA class corresponds to a data block, a dict of record classes (one per channel group)
    Each record class contains a list of recordchannel class representing the structure of channel record.

    Attributes
    --------------
    fid : io.open
        file identifier
    pointerToData : int
        position of Data block in mdf file

    Methods
    ------------
    addRecord(record)
        Adds a new record in DATA class dict
    read(channelList, zip=None)
        Reads data block
    loadSorted(record, zip=None, nameList=None)
        Reads sorted data block from record definition
    load(nameList=None)
        Reads unsorted data block, not yet implemented
    """

    def __init__(self, fid, pointer):
        self.fid = fid
        self.pointerToData = pointer

    def addRecord(self, record):
        """Adds a new record in DATA class dict

        Parameters
        ----------------
        record class
            channel group definition listing record channel classes
        """
        self[record.recordID] = {}
        self[record.recordID]['record'] = record

    def read(self, channelList, zip=None):
        """Reads data block

        Parameters
        ----------------
        channelList : list of str, optional
            list of channel names
        zip : bool, optional
            flag to track if data block is compressed
        """
        if len(self) == 1:  # sorted dataGroup
            recordID = list(self.keys())[0]
            self[recordID]['data'] = self.loadSorted(self[recordID]['record'], zip=None, nameList=channelList)
        else:  # unsorted DataGroup
            self.load(nameList=channelList)

    def loadSorted(self, record, zip=None, nameList=None):  # reads sorted data
        """Reads sorted data block from record definition

        Parameters
        ----------------
        record class
            channel group definition listing record channel classes
        zip : bool, optional
            flag to track if data block is compressed
        channelList : list of str, optional
            list of channel names

        Returns
        -----------
        numpy recarray of data
        """
        return record.readSortedRecord(self.fid, self.pointerToData, nameList)

    def load(self, nameList=None):
        """ not yet implemented
        """
        return None


class mdf3(mdf_skeleton):

    """ mdf file version 3.0 to 3.3 class

    Attributes
    --------------
    fileName : str
        file name
    MDFVersionNumber : int
        mdf file version number
    masterChannelList : dict
        Represents data structure: a key per master channel with corresponding value containing a list of channels
        One key or master channel represents then a data group having same sampling interval.
    multiProc : bool
        Flag to request channel conversion multi processed for performance improvement.
        One thread per data group.
    convertAfterRead : bool
        flag to convert raw data to physical just after read
    filterChannelNames : bool
        flag to filter long channel names from its module names separated by '.'
    file_metadata : dict
        file metadata with minimum keys : author, organisation, project, subject, comment, time, date

    Methods
    ------------
    read3( fileName=None, info=None, multiProc=False, channelList=None, convertAfterRead=True)
        Reads mdf 3.x file data and stores it in dict
    _getChannelData3(channelName)
        Returns channel numpy array
    _convertChannel3(channelName)
        converts specific channel from raw to physical data according to CCBlock information
    _convertAllChannel3()
        Converts all channels from raw data to converted data according to CCBlock information
    write3(fileName=None)
        Writes simple mdf 3.3 file
    """

    def read3(self, fileName=None, info=None, multiProc=False, channelList=None, convertAfterRead=True, filterChannelNames=False):
        """ Reads mdf 3.x file data and stores it in dict

        Parameters
        ----------------
        fileName : str, optional
            file name

        info : mdfinfo3.info3 class
            info3 class containing all MDF Blocks

        multiProc : bool
            flag to activate multiprocessing of channel data conversion

        channelList : list of str, optional
            list of channel names to be read
            If you use channelList, reading might be much slower but it will save you memory. Can be used to read big files

        convertAfterRead : bool, optional
            flag to convert channel after read, True by default
            If you use convertAfterRead by setting it to false, all data from channels will be kept raw, no conversion applied.
            If many float are stored in file, you can gain from 3 to 4 times memory footprint
            To calculate value from channel, you can then use method .getChannelData()
        """
        self.multiProc = multiProc
        if platform == 'win32':
            self.multiProc = False  # no multiprocessing for windows platform

        if self.fileName is None and info is not None:
            self.fileName = info.fileName
        elif fileName is not None:
            self.fileName = fileName

        if channelList is None:
            allChannel = True
        else:
            allChannel = False

        # Read information block from file
        if info is None:
            info = info3(self.fileName, None, self.filterChannelNames)

        # reads metadata
        try:
            comment = info['HDBlock']['TXBlock']['Text']
        except:
            comment = ''
        # converts date to be compatible with ISO8601
        day, month, year = info['HDBlock']['Date'].split(':')
        ddate = year + '-' + month + '-' + day
        self.add_metadata(author=info['HDBlock']['Author'], \
                organisation=info['HDBlock']['Organization'], \
                project=info['HDBlock']['ProjectName'], \
                subject=info['HDBlock']['Subject'], comment=comment, \
                    date=ddate, time=info['HDBlock']['Time'])

        try:
            fid = open(self.fileName, 'rb')
        except IOError:
            raise Exception('Can not find file ' + self.fileName)


        # Read data from file
        for dataGroup in info['DGBlock'].keys():
            if info['DGBlock'][dataGroup]['numberOfChannelGroups'] > 0:  # data exists
                # Pointer to data block
                pointerToData = info['DGBlock'][dataGroup]['pointerToDataRecords']
                buf = DATA(fid, pointerToData)

                for channelGroup in range(info['DGBlock'][dataGroup]['numberOfChannelGroups']):
                    temp = record(dataGroup, channelGroup)  # create record class
                    temp.loadInfo(info)  # load all info related to record

                    if temp.numberOfRecords != 0:  # continue if there are at least some records
                        buf.addRecord(temp)

                buf.read(channelList) # reads datablock potentially containing several channel groups

                for recordID in buf.keys():
                    if 'record' in buf[recordID]:
                        master_channel = buf[recordID]['record'].master['name']
                        if master_channel in self.keys():
                            master_channel += '_' + str(dataGroup)

                        channels = (c for c in buf[recordID]['record']
                                    if allChannel or c.name in channelList)

                        for chan in channels: # for each recordchannel
                            recordName = buf[recordID]['record'].recordToChannelMatching[chan.name]  # in case record is used for several channels
                            temp = buf[recordID]['data'].__getattribute__(str(recordName) + '_title')

                            if len(temp) != 0:
                                # Process concatenated bits inside uint8
                                if not chan.bitCount // 8.0 == chan.bitCount / 8.0:  # if channel data do not use complete bytes
                                    mask = int(pow(2, chan.bitCount) - 1)  # masks isBitUint8
                                    if chan.signalDataType in (0, 1, 9, 10, 13, 14):  # integers
                                        temp = right_shift(temp, chan.bitOffset)
                                        temp = bitwise_and(temp, mask)
                                    else:  # should not happen
                                        print('bit count and offset not applied to correct data type', file=stderr)

                                self.add_channel(dataGroup, chan.name, temp, \
                                        master_channel, \
                                        master_type=1, \
                                        unit=chan.unit, \
                                        description=chan.desc, \
                                        conversion=chan.conversion, \
                                        info=None)
                del buf
        fid.close()  # close file
        if convertAfterRead:
            self._convertAllChannel3()

    def _getChannelData3(self, channelName):
        """Returns channel numpy array

        Parameters
        ----------------
        channelName : str
            channel name

        Returns:
        -----------
        numpy array
            converted, if not already done, data corresponding to channel name

        Notes
        ------
        This method is the safest to get channel data as numpy array from 'data' dict key might contain raw data
        """
        if channelName in self:
            return self._convert3(channelName)
        else:
            raise KeyError('Channel ' + channelName + ' not in mdf dictionary')
            return channelName

    def _convert3(self, channelName):
        """converts specific channel from raw to physical data according to CCBlock information

        Parameters
        ----------------
        channelName : str
            Name of channel

        Returns
        -----------
        numpy array
            returns numpy array converted to physical values according to conversion type
        """
        if 'conversion' in self[channelName]:  # there is conversion property
            conversion = self[channelName]['conversion']
            if conversion['type'] == 0:
                return linearConv(self[channelName]['data'], conversion['parameters'])
            elif conversion['type'] == 1:
                return tabInterpConv(self[channelName]['data'], conversion['parameters'])
            elif conversion['type'] == 2:
                return tabConv(self[channelName]['data'], conversion['parameters'])
            elif conversion['type'] == 6:
                return polyConv(self[channelName]['data'], conversion['parameters'])
            elif conversion['type'] == 7:
                return expConv(self[channelName]['data'], conversion['parameters'])
            elif conversion['type'] == 8:
                return logConv(self[channelName]['data'], conversion['parameters'])
            elif conversion['type'] == 9:
                return rationalConv(self[channelName]['data'], conversion['parameters'])
            elif conversion['type'] == 10:
                return formulaConv(self[channelName]['data'], conversion['parameters'])
            elif conversion['type'] == 12:
                return textRangeTableConv(self[channelName]['data'], conversion['parameters'])
            else:
                return self[channelName]['data']
        else:
            return self[channelName]['data']

    def _convertChannel3(self, channelName):
        """converts specific channel from raw to physical data according to CCBlock information

        Parameters
        ----------------
        channelName : str
            Name of channel
        """
        self.setChannelData(channelName, self._convert3(channelName))
        self.remove_channel_conversion(channelName)

    def _convertAllChannel3(self):
        """Converts all channels from raw data to converted data according to CCBlock information
        Converted data will take more memory.
        """
        for channel in self:
            self._convertChannel3(channel)

    def write3(self, fileName=None):
        """Writes simple mdf 3.3 file

        Parameters
        ----------------
        fileName : str, optional
            Name of file
            If file name is not input, written file name will be the one read with appended '_new' string before extension

        Notes
        --------
        All channels will be converted to physical data, so size might be bigger than original file
        """

        LINK = 'I'
        #CHAR = 'c'
        REAL = 'd'
        BOOL = 'h'
        #UINT8 = 'B'
        #BYTE =  'B'
        INT16 = 'h'
        UINT16 = 'H'
        UINT32 = 'I'
        #INT32 = 'i'
        UINT64 = 'Q'
        #INT64 = 'q'

        # put master channel in first position for each datagroup if not already the case
        for master in list(self.masterChannelList.keys()):
            masterList = sorted(self.masterChannelList[master])
            masterPosition = masterList.index(master)
            masterList.pop(masterPosition)  # remove  master channel
            masterList.insert(0, master)  # insert at first position master channel
            self.masterChannelList[master] = masterList

        pointers = {}  # records pointers of blocks when writing

        # writes characters
        def writeChar(f, value, size=None):
            if size is None:
                temp = value
            else:
                if len(value) > size:
                    temp = value[:size]
                else:
                    temp = value + '\0' * (size - len(value))
                temp += '\0'
            if self.MDFVersionNumber < 400:
                if PythonVersion >= 3:
                    temp = temp.encode('latin1', 'replace')
                f.write(pack('<' + str(len(temp)) + 's', temp))
            else:
                temp = temp.encode('latin1', 'replace')
                f.write(pack('<' + str(len(temp)) + 's', temp))

        # write pointer of block and come back to current stream position
        def writePointer(f, pointer, value):
            currentPosition = f.tell()
            f.seek(pointer)
            f.write(pack(LINK, value))
            f.seek(currentPosition)

        # Starts first to write ID and header
        fid = open(fileName, 'wb')  # buffering should automatically be set
        writeChar(fid, 'MDF     ')
        writeChar(fid, '3.30    ')
        writeChar(fid, 'MDFreadr')
        fid.write(pack(UINT16, 0))  # little endian
        fid.write(pack(UINT16, 0))  # floating format
        fid.write(pack(UINT16, 330))  # version 3.0
        fid.write(pack(UINT16, 28591))  # code page ISO2859-1 latin 1 western europe
        writeChar(fid, '\0' * 32)  # reserved

        # Header Block
        writeChar(fid, 'HD')
        fid.write(pack(UINT16, 208))  # block size
        pointers['HD'] = {}
        pointers['HD']['DG'] = fid.tell()
        fid.write(pack(LINK, 272))  # first Data block pointer
        pointers['HD']['TX'] = fid.tell()
        fid.write(pack(LINK, 0))  # pointer to TX Block file comment
        pointers['HD']['PR'] = fid.tell()
        fid.write(pack(LINK, 0))  # pointer to PR Block
        ndataGroup = len(self.masterChannelList)
        fid.write(pack(UINT16, ndataGroup))  # number of data groups
        writeChar(fid, strftime("%d:%m:%Y"))  # date
        writeChar(fid, strftime("%H:%M:%S"))  # time
        if self.file_metadata['author'] is not None:
            writeChar(fid, self.file_metadata['author'], size=31)  # Author
        else:
            writeChar(fid, ' ', size=31)  # Author
        if self.file_metadata['organisation'] is not None:
            writeChar(fid, self.file_metadata['organisation'], size=31)  # Organization
        else:
            writeChar(fid, ' ', size=31)
        if self.file_metadata['project'] is not None:
            writeChar(fid, self.file_metadata['project'], size=31)  # Project
        else:
            writeChar(fid, ' ', size=31)
        if self.file_metadata['subject'] is not None:
            writeChar(fid, self.file_metadata['subject'], size=31)  # Subject
        else:
            writeChar(fid, ' ', size=31)
        fid.write(pack(UINT64, int(time() * 1000000000)))  # Time Stamp
        fid.write(pack(INT16, 1))  # UTC time offset
        fid.write(pack(UINT16, 0))  # Time quality
        writeChar(fid, 'Local PC Reference Time         ')  # Timer identification

        # write DG block
        pointers['DG'] = {}
        pointers['CG'] = {}
        pointers['CN'] = {}

        for dataGroup in range(ndataGroup):
            # writes dataGroup Block
            pointers['DG'][dataGroup] = {}
            if 0 < dataGroup:  # not possible for first DG
                # previous datagroup pointer to this new datagroup
                writePointer(fid, pointers['DG'][dataGroup - 1]['nextDG'], fid.tell())
            else:
                # first datagroup pointer in header block
                writePointer(fid, pointers['HD']['DG'], fid.tell())
            writeChar(fid, 'DG')
            fid.write(pack(UINT16, 28))  # DG block size
            pointers['DG'][dataGroup]['nextDG'] = fid.tell()
            # pointer to next DataGroup, 0 by default until it is known when creating new datagroup
            fid.write(pack(LINK, 0))
            pointers['DG'][dataGroup]['CG'] = fid.tell()
            fid.write(pack(LINK, 0))  # pointer to channel group, 0 until CG created
            fid.write(pack(LINK, 0))  # pointer to trigger block, not used
            pointers['DG'][dataGroup]['data'] = fid.tell()
            fid.write(pack(LINK, 0))  # pointer to data block
            fid.write(pack(UINT16, 1))  # number of channel group, 1 because sorted data
            fid.write(pack(UINT16, 0))  # number of record IDs
            writeChar(fid, '\0' * 32)  # reserved

            # sorted data so only one channel group
            pointers['CG'][dataGroup] = {}
            # write first CG pointer in datagroup
            writePointer(fid, pointers['DG'][dataGroup]['CG'], fid.tell())
            writeChar(fid, 'CG')
            fid.write(pack(UINT16, 30))  # CG block size
            fid.write(pack(LINK, 0))  # pointer to next Channel Group but no other, one CG per DG
            pointers['CG'][dataGroup]['firstCN'] = fid.tell()
            fid.write(pack(LINK, 0))  # pointer to first channel block
            pointers['CG'][dataGroup]['TX'] = fid.tell()
            fid.write(pack(LINK, 0))  # pointer to TX block
            fid.write(pack(UINT16, 0))  # No record ID no need for sorted data
            masterChannel = list(self.masterChannelList.keys())[dataGroup]
            numChannels = len(self.masterChannelList[masterChannel])
            fid.write(pack(UINT16, numChannels))  # Number of channels
            pointers['CG'][dataGroup]['dataRecordSize'] = fid.tell()
            fid.write(pack(UINT16, 0))  # Size of data record
            masterData = self.getChannelData(masterChannel)
            nRecords = len(masterData)
            fid.write(pack(UINT32, nRecords))  # Number of records
            fid.write(pack(LINK, 0))  # pointer to sample reduction block, not used
            sampling = 0
            if masterData is not None and nRecords > 0 and masterData.dtype.kind not in ['S', 'U']:
                sampling = average(diff(masterData))

            # Channel blocks writing
            pointers['CN'][dataGroup] = {}
            dataList = ()
            dataTypeList = ''
            recordNumberOfBits = 0
            preceedingChannel = None
            bitOffset = 0
            writePointer(fid, pointers['CG'][dataGroup]['firstCN'], fid.tell())  # first channel bock pointer from CG
            for channel in self.masterChannelList[masterChannel]:
                pointers['CN'][dataGroup][channel] = {}
                pointers['CN'][dataGroup][channel]['beginCN'] = fid.tell()
                writeChar(fid, 'CN')
                fid.write(pack(UINT16, 228))  # CN block size
                pointers['CN'][dataGroup][channel]['nextCN'] = fid.tell()
                if preceedingChannel is not None:  # not possible for first CN
                    writePointer(fid, pointers['CN'][dataGroup][preceedingChannel]['nextCN'], pointers['CN'][dataGroup][channel]['beginCN'])  # pointer in previous cN
                preceedingChannel = channel
                fid.write(pack(LINK, 0))  # pointer to next channel block, 0 as not yet known
                pointers['CN'][dataGroup][channel]['CC'] = fid.tell()
                fid.write(pack(LINK, 0))  # pointer to conversion block
                fid.write(pack(LINK, 0))  # pointer to source depending block
                fid.write(pack(LINK, 0))  # pointer to dependency block
                pointers['CN'][dataGroup][channel]['TX'] = fid.tell()
                fid.write(pack(LINK, 0))  # pointer to comment TX, no comment
                # check if master channel
                if channel not in list(self.masterChannelList.keys()):
                    fid.write(pack(UINT16, 0))  # data channel
                else:
                    fid.write(pack(UINT16, 1))  # master channel
                # make channel name in 32 bytes
                writeChar(fid, channel, size=31)  # channel name
                # channel description
                desc = self.getChannelDesc(channel)
                writeChar(fid, desc, size=127)  # channel description
                fid.write(pack(UINT16, bitOffset))  # bit position
                data = self.getChannelData(channel)  # channel data
                temp = data
                if PythonVersion >= 3 and data.dtype.kind in ['S', 'U']:
                    temp = temp.encode('latin1', 'replace')
                dataList = dataList + (temp, )

                if data.dtype in ('float64', 'int64', 'uint64'):
                    numberOfBits = 64
                elif data.dtype in ('float32', 'int32', 'uint32'):
                    numberOfBits = 32
                elif data.dtype in ('uint16', 'int16'):
                    numberOfBits = 16
                elif data.dtype in ('uint8', 'int8'):
                    numberOfBits = 8
                else:
                    numberOfBits = 8  # if string, not considered
                recordNumberOfBits += numberOfBits
                fid.write(pack(UINT16, numberOfBits))  # Number of bits
                bitOffset += numberOfBits
                if data.dtype == 'float64':
                    dataType = 3
                elif data.dtype in ('uint8', 'uint16', 'uint32', 'uint64'):
                    dataType = 0
                elif data.dtype in ('int8', 'int16', 'int32', 'int64'):
                    dataType = 1
                elif data.dtype == 'float32':
                    dataType = 2
                elif data.dtype.kind in ['S', 'U']:
                    dataType = 7
                else:
                    raise Exception('Not recognized dtype')
                    return data.dtype
                if data.dtype.kind not in ['S', 'U']:
                    dataTypeList += data.dtype.char
                else:
                    dataTypeList += str(data.dtype.itemsize) + 's'
                fid.write(pack(UINT16, dataType))  # Signal data type
                if data.dtype.kind not in ['S', 'U']:
                    fid.write(pack(BOOL, 1))  # Value range valid
                    if len(data) > 0:
                        maximum = max(data)
                        minimum = min(data)
                    else:
                        maximum = 0
                        minimum = 0
                    fid.write(pack(REAL, minimum))  # Min value
                    fid.write(pack(REAL, maximum))  # Max value
                else:
                    fid.write(pack(BOOL, 0))  # No value range valid
                    fid.write(pack(REAL, 0))  # Min value
                    fid.write(pack(REAL, 0))  # Max value
                fid.write(pack(REAL, sampling))  # Sampling rate
                pointers['CN'][dataGroup][channel]['longChannelName'] = fid.tell()
                fid.write(pack(LINK, 0))  # pointer to long channel name
                fid.write(pack(LINK, 0))  # pointer to channel display name
                fid.write(pack(UINT16, 0))  # No Byte offset

                # TXblock for long channel name
                writePointer(fid, pointers['CN'][dataGroup][channel]['longChannelName'], fid.tell())
                writeChar(fid, 'TX')
                fid.write(pack(UINT16, len(channel) + 4 + 1))  # TX block size
                writeChar(fid, channel + '\0')  # channel name that can be long, should ends by 0 (NULL)

                # Conversion blocks writing
                writePointer(fid, pointers['CN'][dataGroup][channel]['CC'], fid.tell())
                writeChar(fid, 'CC')
                fid.write(pack(UINT16, 46))  # CC block size
                if data.dtype.kind not in ['S', 'U']:
                    fid.write(pack(BOOL, 1))  # Value range valid
                    fid.write(pack(REAL, minimum))  # Min value
                    fid.write(pack(REAL, maximum))  # Max value
                else:
                    fid.write(pack(BOOL, 0))  # No value range valid
                    fid.write(pack(REAL, 0))  # Min value
                    fid.write(pack(REAL, 0))  # Max value
                writeChar(fid, self.getChannelUnit(channel), size=19)  # channel description
                fid.write(pack(UINT16, 65535))  # conversion already done during reading
                fid.write(pack(UINT16, 0))  # additional size information, not necessary for 65535 conversion type ?
            # number of channels in CG
            currentPosition = fid.tell()
            fid.seek(pointers['CG'][dataGroup]['dataRecordSize'])
            fid.write(pack(UINT16, int(recordNumberOfBits / 8)))  # Size of data record
            fid.seek(currentPosition)

            # data writing
            # write data pointer in datagroup
            writePointer(fid, pointers['DG'][dataGroup]['data'], fid.tell())
            records = array(dataList, object).T
            records = reshape(records, (1, len(self.masterChannelList[masterChannel]) * nRecords), order='C')[0]  # flatten the matrix
            fid.write(pack('<' + dataTypeList * nRecords, *records))  # dumps data vector from numpy

        # print(pointers, file=stderr)
        fid.close()


def _datatypeformat3(signalDataType, numberOfBits, ByteOrder):
    """ function returning C format string from channel data type and number of bits

    Parameters
    ----------------
    signalDataType : int
        channel data type according to specification
    numberOfBits : int
        number of bits taken by channel data in a record

    Returns
    -----------
    dataType : str
        C format used by fread to read channel raw data
    """
    if signalDataType in (0, 9, 13):  # unsigned
        if numberOfBits <= 8:
            dataType = 'B'
        elif numberOfBits <= 16:
            dataType = 'H'
        elif numberOfBits <= 32:
            dataType = 'I'
        elif numberOfBits <= 64:
            dataType = 'Q'
        else:
            print(('Unsupported number of bits for unsigned int ' + str(signalDataType)), file=stderr)

    elif signalDataType in (1, 10, 14):  # signed int
        if numberOfBits <= 8:
            dataType = 'b'
        elif numberOfBits <= 16:
            dataType = 'h'
        elif numberOfBits <= 32:
            dataType = 'i'
        elif numberOfBits <= 64:
            dataType = 'q'
        else:
            print(('Unsupported number of bits for signed int ' + str(signalDataType)), file=stderr)

    elif signalDataType in (2, 3, 11, 12, 15, 16):  # floating point
        if numberOfBits == 32:
            dataType = 'f'
        elif numberOfBits == 64:
            dataType = 'd'
        else:
            print(('Unsupported number of bit for floating point ' + str(signalDataType)), file=stderr)

    elif signalDataType == 7:  # string
        dataType = str(numberOfBits // 8) + 's'
    elif signalDataType == 8:  # array of bytes
        dataType = str(numberOfBits // 8) + 's'
    else:
        print(('Unsupported Signal Data Type ' + str(signalDataType) + ' ', numberOfBits), file=stderr)

    # deal with byte order
    if signalDataType in (0, 1, 2, 3):
        if ByteOrder:
            dataType = '>' + dataType
        else:
            dataType = '<' + dataType
    elif signalDataType in (13, 14, 15, 16):  # low endian
        dataType = '<' + dataType
    elif signalDataType in (9, 10, 11, 12):  # big endian
        dataType = '>' + dataType

    return dataType


def _arrayformat3(signalDataType, numberOfBits, ByteOrder):
    """ function returning numpy style string from channel data type and number of bits
    Parameters
    ----------------
    signalDataType : int
        channel data type according to specification
    numberOfBits : int
        number of bits taken by channel data in a record

    Returns
    -----------
    dataType : str
        numpy dtype format used by numpy.core.records to read channel raw data
    """
    # Formats used by numpy

    if signalDataType in (0, 9, 13):  # unsigned
        if numberOfBits <= 8:
            dataType = 'u1'
        elif numberOfBits <= 16:
            dataType = 'u2'
        elif numberOfBits <= 32:
            dataType = 'u4'
        elif numberOfBits <= 64:
            dataType = 'u8'
        else:
            print('Unsupported number of bits for unsigned int ' + str(signalDataType) + ' nBits ', numberOfBits, file=stderr)

    elif signalDataType in (1, 10, 14):  # signed int
        if numberOfBits <= 8:
            dataType = 'i1'
        elif numberOfBits <= 16:
            dataType = 'i2'
        elif numberOfBits <= 32:
            dataType = 'i4'
        elif numberOfBits <= 64:
            dataType = 'i8'
        else:
            print('Unsupported number of bits for signed int ' + str(signalDataType) + ' nBits ', numberOfBits, file=stderr)

    elif signalDataType in (2, 3, 11, 12, 15, 16):  # floating point
        if numberOfBits == 32:
            dataType = 'f4'
        elif numberOfBits == 64:
            dataType = 'f8'
        else:
            print('Unsupported number of bit for floating point ' + str(signalDataType) + ' nBits ', numberOfBits, file=stderr)

    elif signalDataType == 7:  # string
        dataType = 'S' + str(numberOfBits // 8)  # not directly processed
    elif signalDataType == 8:  # array of bytes
        dataType = 'V' + str(numberOfBits // 8)  # not directly processed
    else:
        print('Unsupported Signal Data Type ' + str(signalDataType) + ' nBits ', numberOfBits, file=stderr)

    # deal with byte order
    if signalDataType in (0, 1, 2, 3):
        if ByteOrder:
            dataType = '>' + dataType
        else:
            dataType = '<' + dataType
    elif signalDataType in (13, 14, 15, 16):  # low endian
        dataType = '<' + dataType
    elif signalDataType in (9, 10, 11, 12):  # big endian
        dataType = '>' + dataType

    return dataType
