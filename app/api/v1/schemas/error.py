class InvalidData(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class NotFound(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class InvalidFileName(InvalidData):
    def __init__(self, message="Invalid file name"):
        self.message = message
        super().__init__(self.message)
