class PaymentFailedException(Exception):
    def __init__(self, message="Payment failed"):
        super().__init__(message)