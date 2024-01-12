class InvalidInsertionError(Exception):
    def __init__(self, item, name_table):
        self.item = item
        self.name_table = name_table
        super().__init__(f"Failed to insert {self.item} in {self.name_table.upper()} table.")