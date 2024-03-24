class IncompleteOrderException(Exception):
    def __init__(self, message="Incomplete order details"):
        super().__init__(message)