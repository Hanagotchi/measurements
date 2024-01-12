class EmptyPackageError(Exception):
    def __init__(self, empty_folds: list):
        self.empty_folds = empty_folds
        super().__init__(f"Package received with empty folds: {self.empty_folds}.")