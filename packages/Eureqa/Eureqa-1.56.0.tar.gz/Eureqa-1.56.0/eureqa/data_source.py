# Copyright (c) 2016, Nutonian Inc
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#   * Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the Nutonian Inc nor the
#     names of its contributors may be used to endorse or promote products
#     derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL NUTONIAN INC BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from search import Search
from variable_details import VariableDetails
from utils import *
from utils.jsonrest import _JsonREST

from session import Http404Exception

import base64
import json
import urllib

import warnings

class DataSource(_JsonREST):
    """Acts as an interface to a data source on the server.

    DataSources can be created by calling :py:meth:`~eureqa.eureqa.Eureqa.create_data_source`
    or an existing one can be retreived with :py:meth:`~eureqa.eureqa.Eureqa.get_data_source`

    :var str `~eureqa.data_source.DataSource.name`: The data source name.
    :var str `~eureqa.data_source.DataSource.series_id_column_name`: The name of the column that splits data into series based on its values.
    :var str `~eureqa.data_source.DataSource.series_order_column_name`: The name of the column that defines the order of the data. This indicates the data is timeseries data and will sort the rows based on this column.
    :var int `~eureqa.data_source.DataSource.number_columns`: The number of columns (variables) in the data source.
    :var int `~eureqa.data_source.DataSource.number_rows`: The number of rows in the data source.
    :var int `~eureqa.data_source.DataSource.number_series`: The number of series (chunks of rows) in the data source.
    """

    EXISTING_ROW_ORDER = "<row>"

    def __init__(self, eureqa, datasource_name=None, hidden=False, datasource_id=None):
        """For internal use only
        PARAM_NOT_EXTERNALLY_DOCUMENTED
        """

        super(DataSource, self).__init__(eureqa)

        if datasource_id is not None:
            self._datasource_id = datasource_id
        if datasource_name is not None:
            self._datasource_name = datasource_name

        self._hidden = hidden
        self._series_count = 0
        self._series_descriptions = []
        self._prepared_data_col_count = 0
        self._prepared_data_row_count = 0
        self._file_name = ''
        self._file_size = 0
        self._file_uploaded_user = ''
        self._file_uploaded_date = ''
        self._series_order_column = None
        self._series_id_column = None

    def _directory_endpoint(self):
        return "/fxp/datasources"
    def _object_endpoint(self):
        return "/fxp/datasources/%s" % (self._datasource_id)
    def _fields(self):
        return ["datasource_id", "datasource_name", "prepared_data_row_count", "prepared_data_col_count", "series_count", "series_descriptions",  "file_name", "file_size", "file_uploaded_user", "file_uploaded_date", "hidden", "series_order_column", "series_order_variable", "series_id_column"]

    @property
    def name(self):
        return self._datasource_name
    @name.setter
    def name(self, val):
        self._datasource_name = val
        self._update()

    @property
    def number_columns(self):
        return self._prepared_data_col_count

    @property
    def number_rows(self):
        return self._prepared_data_row_count

    @property
    def number_series(self):
        return self._series_count

    @property
    def _data_source_id(self):
        return self._datasource_id

    @property
    def _data_file_name(self):
        return self._file_name

    @property
    def _data_file_size(self):
        return self._file_size

    @property
    def _data_file_uploaded_user(self):
        return self._file_uploaded_user

    @property
    def _data_file_uploaded_date(self):
        return self._file_uploaded_date

    @property
    def series_order_column_name(self):
        """ The name of the column that defines the order of the data. This indicates the data is timeseries data and will sort the rows based on this column. Use DataSource.EXISTING_ROW_ORDER to use the current row number as the series order.

        """
        return self._series_order_column
    @series_order_column_name.setter
    def series_order_column_name(self, val):
        self._update_metadata(series_id_column_name=self.series_id_column_name, series_order_column_name=val)

    @property
    def series_id_column_name(self):
        """The name of the column that splits data into series based on its values.

        """
        return self._series_id_column

    @property
    def series_order_variable_name(self):
        """The name of the variable that defines the order of the data.  Same as `series_order_column_name` except properly escaped for use as a variable name.

        """
        return self._series_order_variable
    
    @series_id_column_name.setter
    def series_id_column_name(self, val):
        self._update_metadata(series_id_column_name=val, series_order_column_name=self.series_order_column_name)

    def __str__(self):
        return json.dumps(self._to_json(), indent=4)

    def delete(self):
        """Deletes the data source from the server.

        :raise Exception: If the data source is already deleted.
        """
        self._delete()

    def _create(self, file_or_path):
        assert self._datasource_name is not None, "Cannot create DataSource without a name"
        assert not hasattr(self, "_datasource_id"), "Cannot specify DataSources' ID before creation"

        if isinstance(file_or_path, basestring):
            f = open(file_or_path, 'rb')
            file_path = file_or_path
        else:
            f = file_or_path
            file_path = getattr(file_or_path, 'name', str(file_or_path))

        try:
            raw_data = {}
            raw_data['datasource_name'] = self.name
            if self._hidden:
                raw_data['hidden'] = "true"
            else:
                raw_data['hidden'] = "false"
            resp = self._eureqa._session.execute('/fxp/datasources/create_and_upload', 'POST', files={'file': (file_path,f)}, raw_data=raw_data)
            self._from_json(resp.get('datasource'))
        finally:
            if isinstance(file_or_path, basestring):
                f.close()
        self._get_self()

    def _update_metadata(self, series_id_column_name, series_order_column_name):
        self._series_id_column = series_id_column_name
        self._series_order_column = series_order_column_name
        self._update()

    def download_data_file(self, file_path):
        """Downloads the originally uploaded data from the server.

        :param str file_path: the filepath at which to save the data

        """
        result = self._eureqa._session.execute('/fxp/datasources/%s/download' % self._data_source_id, 'GET', raw_returnfile=file_path)

    def get_variables(self):
        """Retrieves from the server a list of variables in a datasource.

        :return:
            A list of the same variables as visible in Eureqa UI.
            Including all derived variables.
        :rtype: list of str
        """
        endpoint = '/fxp/datasources/%s/variables?sort=[{"key":"index"}]' % self._datasource_id
        self._eureqa._session.report_progress('Getting variable details for datasource: \'%s\'.' % self.name)
        body = self._eureqa._session.execute(endpoint, 'GET')
        return [x['variable_name'] for x in body]

    def get_searches(self):
        """Retrieves from the server a list of searches associated with the data source.

        :return: The list of all searches associated with the data source.
        :rtype: list of :class:`~eureqa.search.Search`
        """

        endpoint = '/fxp/datasources/%s/searches' % self._datasource_id
        self._eureqa._session.report_progress('Getting searches for datasource: \'%s\'.' % self.name)
        body = self._eureqa._session.execute(endpoint, 'GET')
        return [Search(x, self._eureqa, self) for x in body]

    def create_search(self, search_settings, _hidden = False):
        """Creates a new search with settings from a :any:`SearchSettings` object.

        :param SearchSettings search_settings: the settings for creating a new search.
        :return: A :class:`~eureqa.search.Search` object which represents a newly create search on the server.
        :rtype: ~eureqa.search.Search
        """

        endpoint = "/fxp/datasources/%s/searches" % self._datasource_id
        body = search_settings._to_json()
        body['hidden'] = _hidden
        self._eureqa._session.report_progress('Creating search for datasource: \'%s\'.' % self.name)
        result = self._eureqa._session.execute(endpoint, 'POST', body)
        search_id = result['search_id']
        return self._eureqa._get_search_by_search_id(self._datasource_id, search_id)

    def evaluate_expression(self, expressions, _data_split='all'):
        warnings.warn("This function has been deprecated.  Please use `Eureqa.evaluate_expression()` instead.", DeprecationWarning)
        return self._eureqa.evaluate_expression(self, expressions, _data_split=_data_split)

    def _compute_series_indicator(self):
        """For internal use only.

        Compute an indicator column which indicates the series which each row belongs to, as an integer from 0 to (num_series-1).

        This code was written with the assumption that it would be applied to the entire datasource, as opposed to the training or validation split.
        """
        indicator = []
        for i,series_desc in enumerate(self._series_descriptions):
            indicator += [i]*series_desc['series_size']
        return indicator

    def create_variable(self, expression, variable_name):
        """Adds a new variable to the data_source with values from evaluating the given expression.

        :param str expression: the expression to evaluate to fill in the values
        :param str variable_name: what to name the new variable
        """
        endpoint = '/fxp/datasources/%s/variables' % self._datasource_id
        body = {'datasource_id': self._datasource_id,
                'expression': expression,
                'variable_name': variable_name}
        result = self._eureqa._session.execute(endpoint, 'POST', body)
        self.__dict__ = self._eureqa.get_data_source_by_id(self._datasource_id).__dict__

    def get_variable_details(self, variable_name):
        """Retrieves the details for the requested variable from the data_source.

        :param str variable_name: the name of the variable to get the details for
        :return:
            The object representing the variable details
        :rtype: VariableDetails
        """
        endpoint = '/fxp/datasources/%s/variables/%s' % (self._datasource_id, urllib.quote_plus(base64.b64encode('%s-_-%s' % (self._datasource_id, variable_name))))
        self._eureqa._session.report_progress('Getting variable details for datasource: \'%s\'.' % self.name)
        body = self._eureqa._session.execute(endpoint, 'GET')
        return VariableDetails(body, self)

    def get_variable(self, variable_name):
        warnings.warn("'get_variable()' function deprecated; please call as 'get_variable_details()' instead", DeprecationWarning)
        return self.get_variable_details(variable_name)
