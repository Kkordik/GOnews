from database.Tables.Values.Value import Value


class SecureValue(Value):
    # replace_marker = '%s'
    replace_marker = '?'

    def __init__(self, value):
        super().__init__([value], format_value=self.replace_marker)
