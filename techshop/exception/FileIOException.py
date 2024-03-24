class FileIOException(Exception):
    def __init__(self, message="Error during file I/O"):
        super().__init__(message)
