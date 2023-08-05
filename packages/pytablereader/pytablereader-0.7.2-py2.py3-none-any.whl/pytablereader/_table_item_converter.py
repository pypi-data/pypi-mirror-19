# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import

import dataproperty as dp
from mbstrdecoder import MultiByteStrDecoder


class TableItemModifier(object):

    def __init__(self):
        self.__is_strict_int = False
        self.__is_strict_float = False
        self.__strip_str = '"'

    def modify_item(self, item):
        try:
            data = item.strip(self.__strip_str)
        except AttributeError:
            return None

        inttype = dp.IntegerType(data, is_strict=self.__is_strict_int)
        if inttype.is_convertible_type():
            return inttype.convert()

        floattype = dp.FloatType(data, is_strict=self.__is_strict_float)
        if floattype.is_convertible_type():
            return floattype.convert()

        return MultiByteStrDecoder(data).unicode_str
