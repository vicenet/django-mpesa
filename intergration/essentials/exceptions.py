class MpesaException(Exception):
    """Base exception class for Mpesa-related errors."""


class MpesaConfigurationException(MpesaException):
    """Exception raised for configuration errors in the Mpesa integration."""


class MpesaConnectionError(MpesaException):
    """Exception raised for connection errors with the Mpesa API."""


class MpesaError(MpesaException):
    """Exception raised for general errors related to the Mpesa integration."""


class IllegalPhoneNumberException(MpesaException):
    """Exception raised for illegal phone number format."""


class MpesaAPIError(MpesaException):
    """Exception raised for errors returned by the Mpesa API."""


class MpesaValidationError(MpesaAPIError):
    """Exception raised for validation errors returned by the Mpesa API."""


class MpesaTransactionError(MpesaAPIError):
    """Exception raised for transaction errors returned by the Mpesa API."""


class MpesaReversalError(MpesaAPIError):
    """Exception raised for reversal errors returned by the Mpesa API."""
