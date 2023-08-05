# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
import abc
import hashlib
import re

import dataproperty
import pathvalidate as pv
import six

from .error import InvalidTableNameError
from .error import InvalidHeaderNameError
from .data import TableData

"""
def validate_table_name(name):
    :param str name: Table name to validate.
    :raises InvalidTableNameError: |raises_validate_table_name|

    try:
        pathvalidate.validate_sqlite_table_name(name)
    except pathvalidate.InvalidReservedNameError as e:
        raise InvalidTableNameError(e)
    except pathvalidate.NullNameError:
        raise InvalidTableNameError("table name is empty")
    except pathvalidate.InvalidCharError as e:
        raise InvalidTableNameError(e)
"""


@six.add_metaclass(abc.ABCMeta)
class TableDataSanitizerInterface(object):
    """
    Interface class to validate and sanitize data of |TableData|.
    """

    @abc.abstractmethod
    def validate(self):  # pragma: no cover
        pass

    @abc.abstractmethod
    def sanitize(self):  # pragma: no cover
        pass


class TableDataSanitizer(TableDataSanitizerInterface):

    def __init__(self, tabledata):
        self._tabledata = tabledata

    def validate(self):
        self._validate_table_name()
        self.__validate_header_list()

    def sanitize(self):
        preprocessed_table_name = self._preprocess_table_name()

        try:
            self.validate_table_name(preprocessed_table_name)
            new_table_name = preprocessed_table_name
        except InvalidTableNameError:
            new_table_name = self._sanitize_table_name(
                preprocessed_table_name)
            self.validate_table_name(new_table_name)

        new_header_list = self.__sanitize_header_list()

        return TableData(
            new_table_name, new_header_list, self._tabledata.record_list)

    def __validate_header_list(self):
        for header in self.header_list:
            self._validate_header(header)

    def __sanitize_header_list(self):
        new_header_list = []

        for header in enumerate(self.header_list):
            header = self._preprocess_header(header)

            try:
                self.validate_header(header)
                new_header = header
            except InvalidHeaderNameError:
                new_header = self._sanitize_header(header)
                self.validate_header(new_header)

            new_header_list.append(new_header)

        return new_header_list

    def _preprocess_table_name(self):
        """
        Always calld before table name validation.
        You must return preprocessed table name.
        """

        return self._tabledata.table_name

    @abc.abstractmethod
    def _validate_table_name(self, table_name):
        """
        Must raise :py:class:`~.InvalidHeaderNameError`
        when you consider the table name is invalid.

        :param str header: Table name to validate.
        :raises pytablereader.InvalidTableNameError:
            If the table name is invalid.
            |raises_validate_table_name|
        """

    @abc.abstractmethod
    def _sanitize_table_name(self, table_name):
        """
        must return a sanitized table name.
        sanitized table name should valid with _validate_table_name method.

        :param str header: Table name to sanitize.
        :return: Sanitized table name.
        :rtype: str
        """

    def _preprocess_header(self, header):
        """
        Always calld before a header validation.
        You must return preprocessed header.
        """

        return header

    @abc.abstractmethod
    def _validate_header(self, header):
        """
        No operation.

        This method called for each table header.
        Override this method in subclass if you want to detect
        invalid table header element.
        Raise
        :py:class:`~.InvalidHeaderNameError`
        if an element is invalid.

        :param str header: Table header name.
        :raises pytablereader.InvalidHeaderNameError:
            If the ``header`` is invalid.
        """

    @abc.abstractmethod
    def _sanitize_header(self, header):
        """
        This method called when :py:meth:`._validate_header` method raise
        :py:class:`~.InvalidHeaderNameError`.
        Override this method in subclass if you want to rename invalid
        table header element.

        :param int i: Table header index.
        :return: Renamed header name.
        :rtype: str
        """


class NullTableDataSanitizer(TableDataSanitizer):

    def _validate_table_name(self):
        pass

    def _sanitize_table_name(self):
        return self._tabledata.table_name

    def _validate_header_name(self):
        pass

    def _sanitize_header_name(self, header):
        return header


class SQLiteTableDataSanitizer(TableDataSanitizer):

    def _preprocess_table_name(self):
        return re.sub("['\"]", "", self._tabledata.table_name)

    def _validate_table_name(self, table_name):
        try:
            pv.validate_sqlite_table_name(table_name)
        except (pv.InvalidReservedNameError, pv.InvalidCharError) as e:
            raise InvalidTableNameError(e)
        except pv.NullNameError:
            raise

    def _sanitize_table_name(self, table_name):
        return "rename_{:s}".format(table_name)

    def _validate_header(self, header):
        try:
            pathvalidate.validate_sqlite_attr_name(header)
        except pathvalidate.ValidReservedNameError:
            pass
        except pathvalidate.InvalidReservedNameError:
            raise InvalidHeaderNameError()

    def _sanitize_header(self, header):
        return "rename_{:s}".format(self.header_list[i])
