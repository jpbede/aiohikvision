"""Exceptions for Hikvision."""


class HikvisionError(Exception):
    """Generic error occurred in Hikvision package."""


class HikvisionConnectionError(HikvisionError):
    """Error occurred while communicating to the Hikvision ISAPI."""


class HikvisionConnectionTimeoutError(HikvisionError):
    """Timeout occurred while connecting to the Hikvision ISAPI."""


class HikvisionInvalidCredentialsError(HikvisionError):
    """Given token is invalid."""
