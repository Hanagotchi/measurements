class EmptyPackageError(Exception):
    def __init__(self, empty_folds: list):
        self.empty_folds = empty_folds
        super().__init__((
            "Package received with empty "
            f"folds: {self.empty_folds}."
        ))
