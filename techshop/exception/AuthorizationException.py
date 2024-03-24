class AuthorizationException(Exception):
    def __init__(self, message="Unauthorized access"):
        super().__init__(message)