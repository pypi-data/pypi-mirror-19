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


import json

class VariableDetails:
    """Holds information about a variable. Obtained through the :py:meth:`~eureqa.data_source.DataSource.get_variable_details` method
    of a :py:class:`~eureqa.data_source.DataSource` . Use this class to find mathematic properties of a variable and to change a variable's
    name.

    :var str `~eureqa.variable.VariableDetails.name`: The name of the variable.
    :var str `~eureqa.variable.VariableDetails.expression`: The expression used to create the variable if it is a custom variable
    :var float `~eureqa.variable.VariableDetails.min_value`: The smallest value.
    :var float `~eureqa.variable.VariableDetails.max_value`: The largest value.
    :var float `~eureqa.variable.VariableDetails.mean_value`: The mean value.
    :var float `~eureqa.variable.VariableDetails.standard_deviation`: The standard deviation of the values.
    :var int `~eureqa.variable.VariableDetails.distinct_values`: The number of distinct values.
    :var int `~eureqa.variable.VariableDetails.missing_values`: The number of missing values.
    :var int `~eureqa.variable.VariableDetails.total_rows`: The total rows occupied by the variable.
    :var str `~eureqa.variable.VariableDetails.datatype`: Whether it is a binary or numeric variable
    :var int `~eureqa.variable.VariableDetails.num_zeroes`: The number of zero values.
    :var int `~eureqa.variable.VariableDetails.num_ones`: The number of one values.
    :var `~eureqa.data_source.DataSource` `~eureqa.variable_details.VariableDetails.data_source`: The DataSource the VariableDetails belongs to
    """

    def __init__(self, body, data_source):
        """For internal use only
        PARAM_NOT_EXTERNALLY_DOCUMENTED
        """

        self._id = body['variable_id']
        self.name = body['variable_name']
        self.expression = body.get('expression')
        self.min_value = body['min_value']
        self.max_value = body['max_value']
        self.mean_value = body['mean_value']
        self.standard_deviation = body['standard_deviation']
        self.distinct_values = body['distinct_values']
        self.missing_values = body['missing_values']
        self.num_zeroes = body['num_zeros']
        self.total_rows = body['total_rows']
        self.datatype = body['datatype']
        self.num_ones = body.get('num_ones')
        self.data_source = data_source
        self._body = body

    def _to_json(self):
        body = {
            'variable_id' : self._id,
            'variable_name' : self.name,
            'expression' : self.expression,
            'min_value' : self.min_value,
            'max_value' : self.max_value,
            'mean_value' : self.mean_value,
            'standard_deviation' : self.standard_deviation,
            'distinct_values' : self.distinct_values,
            'missing_values' : self.missing_values,
            'num_zeros' : self.num_zeroes,
            'total_rows' : self.total_rows,
            'datatype' : self.datatype,
            'num_ones' : self.num_ones,
            'datasource_id' : self.data_source._data_source_id,
        }
        return body

    def __str__(self):
        return json.dumps(self._to_json(), indent=4)

class Variable(VariableDetails):
    def __init__(*args, **kwargs):
        warnings.warn("Class 'Variable' has been renamed to 'VariableOptions'", DeprecationWarning)
        super(Variable, self).__init__(*args, **kwargs)
