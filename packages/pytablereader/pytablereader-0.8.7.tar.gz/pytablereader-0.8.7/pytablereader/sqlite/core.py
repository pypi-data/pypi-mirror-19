# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals

from .._constant import (
    SourceType,
    TableNameTemplate as tnt
)
from .._validator import FileValidator
from ..interface import TableLoader
from .formatter import MarkdownTableFormatter


class SqliteTableFileLoader(TableLoader):
    """
    Markdown format file loader class.

    :param str file_path: Path to the loading Markdown file.

    .. py:attribute:: table_name

        Table name string. Defaults to ``%(filename)s_%(key)s``.
    """

    @property
    def format_name(self):
        return "sqlite"

    def __init__(self, file_path=None):
        super(SqliteTableFileLoader, self).__init__(file_path)

        self._validator = FileValidator(file_path)

    def load(self):
        """
        Extract tabular data as |TableData| incetances from a Markdown file.
        |load_source_desc_file|

        :return:
            Loaded table data iterator.
            |load_table_name_desc|

            ===================  ==============================================
            format specifier     value after the replacement
            ===================  ==============================================
            ``%(filename)s``     |filename_desc|
            ``%(key)s``          ``%(format_name)s%(format_id)s``
            ``%(format_name)s``  ``"markdown"``
            ``%(format_id)s``    |format_id_desc|
            ``%(global_id)s``    |global_id|
            ===================  ==============================================
        :rtype: |TableData| iterator
        :raises pytablereader.error.InvalidDataError:
            If the Markdown data is invalid or empty.
        """

        self._validate()

        with open(self.source, "r") as fp:
            formatter = MarkdownTableFormatter(fp.read())
        formatter.accept(self)

        return formatter.to_table_data()

    def _get_default_table_name_template(self):
        return "{:s}_{:s}".format(tnt.FILENAME, tnt.KEY)
