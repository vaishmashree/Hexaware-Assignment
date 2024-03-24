class ConcurrencyException(Exception):
    def __init__(self, message="Concurrency issue occurred"):
        super().__init__(message)