from database.Database import Database
from database.Tables.Values.SecureValue import SecureValue
from database.Tables.Values.NotFormattedValue import NotFormattedValue


class Table:
    def __init__(self, name: str, db: Database, columns: list):
        self.__name = name
        self.db = db
        self.__columns = columns

    def get_table_name(self):
        return self.__name


class MysqlTable(Table):
    async def execute_tb(self, command: str, values: list = None):
        """
        Execute any given command and return dict with values

        :param command: MySQL executable command
        :param values: Values to replace %s
        :return: dict with values
        """
        res = await self.db.execute_db(command, values)
        results = []
        for row in res:
            results.append(dict(zip(self.__columns, row)))
        return results

    def __check_parameters(self, parameters: dict) -> dict:
        """
        Checking if given columns in parameters dict exist in table.

        :param parameters: dict of structure {"column_name": value}
        :return: {"column_name": value}
        """
        for column in parameters.keys():
            # Checking if given columns in parameters exist in table and adding values to list
            if column in self.__columns:
                if not isinstance(parameters[column], NotFormattedValue):
                    parameters[column] = SecureValue(parameters[column])
            else:
                raise Exception("In table '{}' is no such column: '{}'".format(self.__name, column))
        return parameters

    @staticmethod
    def _create_where_expression(where_vals_dict: dict, logical_expr: str, prefix: str = 'WHERE') -> tuple:
        """
        where_vals_dict: dict ("column_name": SecureValue / NotFormattedValue)
        return: tuple(where_string, where_values)
        in which where_string is a part of sql command
        and where_values is a list of vales to replace %s
        """
        if len(where_vals_dict) != 0:
            where_str = prefix
            where_equations = []
            where_values = []
            for column in where_vals_dict.keys():
                where_values += where_vals_dict[column].value
                where_equations.append(" {}={} ".format(column, where_vals_dict[column].format_value))
            where_str += logical_expr.join(where_equations)
        else:
            where_str = ""
            where_values = []

        return where_str, where_values

    async def select_vals(self, command: str = "SELECT * FROM {}", logical_expr: str = "AND", ending_text: str = "",
                          **where):
        """
        Selects all from table can be executed with WHERE using AND or other logical_expression

        :param command: MySQL executable command
        :param logical_expr: logical expression 'AND'/'OR'...
        :param ending_text: text to add after where expression
        :param where: optional parameters for WHERE expression
        :return: dict with values if they are
        """
        where = self.__check_parameters(where)

        # Create string WHERE expression
        where_str, where_values = self._create_where_expression(where, logical_expr)

        return await self.execute_tb("{} {} {}".format(command.format(self.__name), where_str, ending_text),
                                     where_values)

    async def delete_line(self, command: str = "DELETE FROM {} WHERE {}", logical_expr: str = "AND", **where):
        """
        Deletes all from table must be executed with WHERE, you may use AND or other logical_expression

        :param command: MySQL executable command
        :param logical_expr: logical expression 'AND'/'OR'...
        :param where: optional parameters for WHERE expression
        :return: dict with values if they are
        """
        where = self.__check_parameters(where)

        if len(where) == 0:
            raise Exception("No where arguments given. It is impossible to delete all from table")

        # Create string WHERE expression
        where_str, where_values = self._create_where_expression(where, logical_expr,  prefix="")

        return await self.execute_tb(command.format(self.__name, where_str), where_values)

    async def insert_vals(self, command: str = "INSERT IGNORE INTO {}({}) VALUES ({})", **columns_vals):
        """
        Insert values in table.

        :param columns_vals: parameters for INSERT must consist new data.
        :param command: MySQL command for inserting new values
        :return: list of fetched rows if they are
        """
        if len(columns_vals) == 0:
            raise Exception("No parameters given")

        columns_vals = self.__check_parameters(columns_vals)

        unpack_columns = ', '.join(columns_vals.keys())

        values = []
        for column in columns_vals.keys():
            values += columns_vals[column].value

        replace_chars = ', '.join(val.format_value for val in columns_vals.values())

        return await self.execute_tb(
            command=command.format(
                self.__name,
                unpack_columns,
                replace_chars
            ),
            values=values
        )

    async def launch_table(self,  *args, **kwargs):
        pass

    async def update_val(self, where: dict, command: str = "UPDATE {} SET {} WHERE {}", logical_expr: str = "AND",
                         **column_new_vals):
        where = self.__check_parameters(where)
        column_new_vals = self.__check_parameters(column_new_vals)

        if len(column_new_vals) == 0:
            raise Exception("No new arguments given. It is impossible to update table without them")
        where_str, where_vals = self._create_where_expression(where, logical_expr, prefix="")
        new_vals_str, new_vals = self._create_where_expression(column_new_vals, logical_expr, prefix="")

        return await self.execute_tb(command.format(self.__name, new_vals_str, where_str), new_vals + where_vals)


class SqliteTable(Table):
    def execute_tb(self, command: str, values: list = None):
        """
        Execute any given command and return dict with values

        :param command: MySQL executable command
        :param values: Values to replace %s
        :return: dict with values
        """
        res = self.db.execute_db(command, values)
        results = []
        for row in res:
            results.append(dict(zip(self.__columns, row)))
        return results

    def __check_parameters(self, parameters: dict) -> dict:
        """
        Checking if given columns in parameters dict exist in table.

        :param parameters: dict of structure {"column_name": value}
        :return: {"column_name": value}
        """
        for column in parameters.keys():
            # Checking if given columns in parameters exist in table and adding values to list
            if column in self.__columns:
                if not isinstance(parameters[column], NotFormattedValue):
                    parameters[column] = SecureValue(parameters[column])
            else:
                raise Exception("In table '{}' is no such column: '{}'".format(self.__name, column))
        return parameters

    @staticmethod
    def _create_where_expression(where_vals_dict: dict, logical_expr: str, prefix: str = 'WHERE') -> tuple:
        """
        where_vals_dict: dict ("column_name": SecureValue / NotFormattedValue)
        return: tuple(where_string, where_values)
        in which where_string is a part of sql command
        and where_values is a list of vales to replace %s
        """
        if len(where_vals_dict) != 0:
            where_str = prefix
            where_equations = []
            where_values = []
            for column in where_vals_dict.keys():
                where_values += where_vals_dict[column].value
                where_equations.append(" {}={} ".format(column, where_vals_dict[column].format_value))
            where_str += logical_expr.join(where_equations)
        else:
            where_str = ""
            where_values = []

        return where_str, where_values

    def select_vals(self, command: str = "SELECT * FROM {}", logical_expr: str = "AND", ending_text: str = "",
                    **where):
        """
        Selects all from table can be executed with WHERE using AND or other logical_expression

        :param command: MySQL executable command
        :param logical_expr: logical expression 'AND'/'OR'...
        :param ending_text: text to add after where expression
        :param where: optional parameters for WHERE expression
        :return: dict with values if they are
        """
        where = self.__check_parameters(where)

        # Create string WHERE expression
        where_str, where_values = self._create_where_expression(where, logical_expr)

        return self.execute_tb("{} {} {}".format(command.format(self.__name), where_str, ending_text),
                               where_values)

    def delete_line(self, command: str = "DELETE FROM {} WHERE {}", logical_expr: str = "AND", **where):
        """
        Deletes all from table must be executed with WHERE, you may use AND or other logical_expression

        :param command: MySQL executable command
        :param logical_expr: logical expression 'AND'/'OR'...
        :param where: optional parameters for WHERE expression
        :return: dict with values if they are
        """
        where = self.__check_parameters(where)

        if len(where) == 0:
            raise Exception("No where arguments given. It is impossible to delete all from table")

        # Create string WHERE expression
        where_str, where_values = self._create_where_expression(where, logical_expr,  prefix="")

        return self.execute_tb(command.format(self.__name, where_str), where_values)

    def insert_vals(self, command: str = "INSERT IGNORE INTO {}({}) VALUES ({})", **columns_vals):
        """
        Insert values in table.

        :param columns_vals: parameters for INSERT must consist new data.
        :param command: MySQL command for inserting new values
        :return: list of fetched rows if they are
        """
        if len(columns_vals) == 0:
            raise Exception("No parameters given")

        columns_vals = self.__check_parameters(columns_vals)

        unpack_columns = ', '.join(columns_vals.keys())

        values = []
        for column in columns_vals.keys():
            values += columns_vals[column].value

        replace_chars = ', '.join(val.format_value for val in columns_vals.values())

        return self.execute_tb(
            command=command.format(
                self.__name,
                unpack_columns,
                replace_chars
            ),
            values=values
        )

    def launch_table(self,  *args, **kwargs):
        pass

    def update_val(self, where: dict, command: str = "UPDATE {} SET {} WHERE {}", logical_expr: str = "AND",
                         **column_new_vals):
        where = self.__check_parameters(where)
        column_new_vals = self.__check_parameters(column_new_vals)

        if len(column_new_vals) == 0:
            raise Exception("No new arguments given. It is impossible to update table without them")
        where_str, where_vals = self._create_where_expression(where, logical_expr, prefix="")
        new_vals_str, new_vals = self._create_where_expression(column_new_vals, logical_expr, prefix="")

        return self.execute_tb(command.format(self.__name, new_vals_str, where_str), new_vals + where_vals)
