from database.Tables.Values.Value import Value


class NotFormattedValue(Value):
    def __init__(self, value):
        super().__init__([], format_value=value)