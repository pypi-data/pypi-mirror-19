"""
This module defines the custom exception for this module.

Author: Vincent Medina, EveryMundo, 2016
Email: vincent@everymundo.com
"""
# Standard library packages
from typing import AnyStr


# Package Exception
class DatacoreException(Exception):
    """
    Datacore exception handler, base class.
    This is a very basic error handler specific to this module.
    """
    def __init__(self, code: AnyStr, message: AnyStr, *args, **kwargs) \
            -> None:
        """
        :param code: BriefErrorMsg
        :param message: Error message in more verbose detail.
        """
        self.code = code
        self.message = message
        super().__init__(*args, **kwargs)

    def __str__(self, *args, **kwargs) -> str:
        """
        Sets the human readable string casting of this class. Overrides Exception.__str__().
        :param args:
        :param kwargs:
        :return:
        """
        string = "{c}, {r}".format(c=self.code, r=self.message)
        if args:
            string += ", {a}".format(a=args)
        if kwargs:
            string += ", {k}".format(k=kwargs)
        return string

    def __repr__(self, *args, **kwargs) -> str:
        """
        Sets the verbose string representation of this class. Overwrites Exception.__repr__()
        :param args:
        :param kwargs:
        :return:
        """
        representation = "({c}, {r}, {a},".format(
            # Custom attributes
            c=self.code,
            r=self.message,
            # Standard attributes
            a=self.args
        )
        if args:
            representation += " {a},".format(a=args)
        if kwargs:
            representation += " {k},".format(k=kwargs)
        representation += ")"
        return representation

    @classmethod
    def from_error(cls, error: Exception, code: AnyStr=None, message: AnyStr=None) \
            -> "DatacoreException":
        """
        This returns an exception from an existing error object.
        :param error:
        :param code:
        :param message:
        :return:
        """
        # If we do not have code or message, synthesize them from the error args
        if not code:
            code = error.args[0]
        if not message:
            message = error.args[1]
        # Extract the args
        args = error.args
        # Return exception object
        exception = DatacoreException(code, message, *args)
        # But first create its traceback.
        exception.__traceback__ = error.__traceback__
        return exception
