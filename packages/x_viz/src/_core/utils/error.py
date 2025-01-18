"""Contain the project specific error classes."""


class SpectrumError(Exception):
    """The app top error."""


class MissingFileError(SpectrumError, FileNotFoundError):
    """Cannot find the required file."""


class ParsingError(SpectrumError):
    """Failed to parse a file."""


class MissingSpectrumError(SpectrumError):
    """The expected spectrum is missing."""


class InputError(SpectrumError):
    """Unexpected or incorrect inputs of a function."""
