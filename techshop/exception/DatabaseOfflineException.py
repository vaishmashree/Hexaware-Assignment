class DatabaseOfflineException(Exception):
    def __init__(self, message="Database is offline"):
        super().__init__(message)