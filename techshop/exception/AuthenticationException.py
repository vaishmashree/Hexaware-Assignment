class AuthenticationException(Exception):
    def __init__(self, message="Authentication failed"):
        super().__init__(message)