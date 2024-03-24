class InvalidDataException(Exception):
    def __init__(self, message="Invalid data provided"):
        super().__init__(message)