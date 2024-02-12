"""
This module contain all the exception classes
"""


class InvalidLogLevel(Exception):
    """
    rasie when given log level is invalid
    """


class GUIBaseException(Exception):
    """
    User interface base exception class
    """

    def __init__(self, message: str = None):
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        return f"{self.message}"

    def __len__(self) -> int:
        return len(self.message)

    @property
    def error_message(self) -> str:
        """
        Return exception error_message
        """
        return self.message

    def to_dict(self) -> dict:
        """
        return error message as dictionary.
        make it easier for the to pass error
        in RestApi
        """
        return {"error": self.message,
                "type": self.__class__.__name__}



class CommaError(GUIBaseException):
    """
    Raise when last item of an entry or combobox
    is comma.
    """


class RowNotExists(GUIBaseException):
    """
    Raise when the given Row number is not exists in GUI
    """


class WidgetValueError(GUIBaseException):
    """
    Raise when widget's value is empty.
    """

class DataValidationFailed(GUIBaseException):
    """
    Raise when widgets are data validation
    goes fail.
    """

class LimitationError(GUIBaseException):
    """
    Raise when the input lower or greater than the
    min and max value
    """


class TableCellNotFoundError(GUIBaseException):
    """
    Raises when item_getter in Table class couldn't
    find the desired cell. It usually happens in 
    Vertical Table when table is inserting data and
    the table callback calls by each inserting cell.
    """

class InvalidFileContentError(GUIBaseException):
    """
    Raises when the file doesn't have required data.
    """