class RowNotFoundError(Exception):
    def __init__(self, primary_key, name_table):
        self.primary_key = primary_key
        self.name_table = name_table
        super().__init__(
            f"Row with id = {self.primary_key} not \
            found in {self.name_table.upper()} table.")
