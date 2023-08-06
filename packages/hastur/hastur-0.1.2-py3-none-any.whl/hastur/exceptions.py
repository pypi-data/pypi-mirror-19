# -*- coding: utf-8 -*-
"""
This module provides custom Exceptions for hastur.
"""


class Error(Exception):
    """Base class for hastur errors."""
    def __init__(self, *args, **kwargs):
        pass


class ExcessiveObservationsError(Error):
    """
    An error thrown when an observation is appended
    to an arm that is full.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)


class InsufficientObservationsError(Error):
    """
    An error thrown when there are too few
    observations on an arm.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

if __name__ == "__main__":
    pass
    