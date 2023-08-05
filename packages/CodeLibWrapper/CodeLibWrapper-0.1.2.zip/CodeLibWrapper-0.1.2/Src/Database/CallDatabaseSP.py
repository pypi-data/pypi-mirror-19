# -*- coding:utf-8 -*-
from pymssql import *


class CallDatabaseSP:
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = 0.1
    ROBOT_LIBRARY_FORMAT = 'reST'

    def __init__(self):
        pass

    def call_procedure(self, name, parameters):
        """
        call stored procedure with in and out parameters
        @param name: name of procedure
        @param parameters: parameters as tuple as example of
        ('in_value',('STRING','out_var_to_init'),('NUMBER', 'out_var_to_init'),'in_value')
        """
        cur = None

        try:
            cur = self._dbconnection.cursor()
            # process parameters
            parsed_parameters = []
            for i, item in enumerate(parameters):
                if item.lower() in ("string", "number"):
                    exec "%s = cur.var(self.db_api_2.%s);parsed_parameters.append(%s);" % (
                        item + str(i), item.upper(), item + str(i))
                else:
                    parsed_parameters.append(item)
            input_output = tuple(parsed_parameters)
            cur.callproc(name, input_output)
            # backward processing to cx_Oracle.* type
            parsed_parameters = []
            for i, item in enumerate(list(input_output)):
                if isinstance(item, self.db_api_2.NUMBER) or isinstance(item, self.db_api_2.STRING):
                    parsed_parameters.append(item.getvalue());
                else:
                    parsed_parameters.append(item)
            self._dbconnection.commit()
            return parsed_parameters
        finally:
            if cur:
                self._dbconnection.rollback()
