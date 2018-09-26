"""Utility class that currently serves two purposes.

1) Hold custom exceptions

2) Hold the summary state enumeration that is project wide defined here;

https://confluence.lsstcorp.org/display/SYSENG/SAL+constraints+and+recommendations
"""
from enum import Enum

__all__ = ['SummaryState', 'CommandNotRecognizedException']


class SummaryState(Enum):
    DISABLED = 1
    ENABLED = 2
    FAULT = 3
    OFFLINE = 4
    STANDBY = 5


class CommandNotRecognizedException(Exception):
    pass
