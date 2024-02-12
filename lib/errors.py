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


class FailedGetOrderInfo(GUIBaseException):
    """
    Raise when epicor api can't find any info for the
    given sale order
    """


class CommaError(GUIBaseException):
    """
    Raise when last item of an entry or combobox
    is comma.
    """


class RowNotExists(GUIBaseException):
    """
    Raise when the given Row number is not exists in GUI
    """


class FixtureDefinitionError(GUIBaseException):
    """
    Raises when entred data in database not following the
    logic structure
    """


class WidgetValueError(GUIBaseException):
    """
    Raise when widget's value is empty.
    """


class DataValidationFailed(GUIBaseException):
    """
    Raise when widgets are null.
    """


class LimitationError(GUIBaseException):
    """
    Raise when the input lower or greater than the
    min and max value
    """


class ConnectionFailedInterfaceAPI(GUIBaseException):
    """
    Raises when interface api server not responding
    """


class ConnectionFailedCalculationAPI(GUIBaseException):
    """
    Raises when dot caluclattion api server not responding
    """


class ConnectionFailedStorageAPI(GUIBaseException):
    """
    Raises when dot storage api server not responding
    """


class ConnectionFailedParserAPI(GUIBaseException):
    """
    Raises when parser api not responding
    """


class ConfigurationFailed(GUIBaseException):
    """
    Raises when user selection is invalid.
    """


class FailedToGenerateBoardNom(GUIBaseException):
    """
    Raises when couldn't get the board information from the
    lx generator api
    """


class TotalPowerDropLimit(GUIBaseException):
    """
    Raised when sum of powers in a group is greater than 10.
    """


class FailedCollectData(GUIBaseException):
    """
    Raise when user wants to store the data
    """


class ConnectionFailedEpicorAPI(GUIBaseException):
    """
    Raise when epicor server didn't responding
    """


class InvalidDropSections(GUIBaseException):
    """
    Raise when inserted sections in drops is not
    in calculation results sections.
    """


class InvalidSectionsCounts(GUIBaseException):
    """
    Raise when number of drops in a group and
    number of inserted sections are gerater than
    one.
    """


class ConnectionFailedLXBoards(GUIBaseException):
    """
    Raises when couldn't connect to LX Generator
    Boards server
    """


class ConnectionFailedGetWiringBlock(GUIBaseException):
    """
    Raises when couldn't connect to Wiring Block
    Boards server
    """


class ConnectionFailedLabelDataAPI(GUIBaseException):
    """
    Raises when couldn't connect to label server.
    (databse viewer)
    """


class FailedGetSaleOrders(GUIBaseException):
    """
    Raises when couldn't getting all sale orders.
    Used for service related to database viewver.
    """


class FailedGetLines(GUIBaseException):
    """
    Raises when couldn't getting all lines.
    Used for service related to database viewver.
    """


class FailedGetCalculationData(GUIBaseException):
    """
    Raises when couldn't getting a calculation data.
    Used for service related to database viewver.
    """


class FailedDeleteCalculationData(GUIBaseException):
    """
    Raises when couldn't delete a calculation data.
    Used for service related to database viewver.
    """


class FailedUpdateCalculationData(GUIBaseException):
    """
    Raises when couldn't updating a calculation data.
    Used for service related to database viewver.
    """


class FailedLogCaclulationResult(GUIBaseException):
    """
    Failed to log caclulation result
    """


class CalculationError(GUIBaseException):
    """
    raises when caclulation api can't provide
    driver information
    """


class FailedGetOrderData(GUIBaseException):
    """
    raises when couldn't find any order data
    based on the sale order and line.
    """


class InvalidOrdercode(GUIBaseException):
    """
    Raises when user inserted invalid ordercode.
    """


class NotFoundBoard(GUIBaseException):
    """
    Raises when couldn't find any board.
    """


class InvalidDriverDataType(GUIBaseException):
    """
    Raises when user insert wrong data type 
    in database viewer.
    """


class FailedConnectToBracketsServer(GUIBaseException):
    """
    Raises when couldn't connect to the brackets api
    """


class NotFoundBrackets(GUIBaseException):
    """
    Raises when couldn't find any bracket data.
    """


class NotFoundHistory(GUIBaseException):
    """
    Raises when couldn't find any record for the history
    """


class FailedGetLinesData(GUIBaseException):
    """
    Raises when couldn't find any line data with
    desired sale order.
    """


class FailedSaveCalculationDataError(GUIBaseException):
    """
    Raises when couldn't save the calculation data due
    to internal error in api and database.
    """


class TableCellNotFoundError(GUIBaseException):
    """
    Raises when item_getter in Table class couldn't
    find the desired cell. It usually happens in 
    Vertical Table when table is inserting data and
    the table callback calls by each inserting cell.
    """


class RGBWBomInfoNotFoundError(GUIBaseException):
    """
    Raises in database viewer when wants to fetch
    rgbw_bom_info key from calculation result.
    """


class ConnectionFailedAuthenticationAPI(GUIBaseException):
    """
    Raises when couldn't connect to the authentication api.
    """


class AuthenticateError(GUIBaseException):
    """
    Raises when couldn't authenticate user.
    """


# ============================ Product Configurator Panel Errors ===========================

class ConfigurationFailed(GUIBaseException):
    """
    Raises when couldn't configurate the order
    data.
    """

class InvalidOrdercode(GUIBaseException):
    """
    Raises when user inserted invalid order code.
    """

class ConnectionFailedInterpreterAPI(GUIBaseException):
    """
    Raises when couldn't connect to the interpreter
    api.
    """

class InvalidFamilyError(GUIBaseException):
    """
    Raises when user select wrong family
    in product configurator panel.
    """
    
class InvalidLuminaireIDError(GUIBaseException):
    """
    Raises when user select wrong luminaire id
    in product configurator panel.
    """

class FixtureNotFoundError(GUIBaseException):
    """
    Raises when didn't find any fixture data
    in product configurator panel.
    """

class ConfiguratorError(GUIBaseException):
    """
    Raises when face configurator error in
    product configurator panel
    """

class FailedUpdatePartNumbersError(GUIBaseException):
    """
    Raises when couldn't update the part numbers
    """

class NotSupportedFixtureError(GUIBaseException):
    """
    Raises when user wants to load a fixture
    that currently doesn't support in the interface.
    """

class InvalidFileContentError(GUIBaseException):
    """
    Raises when the file doesn't have required data.
    """

class SectionNameError(DataValidationFailed):
    """
    Raises when user inserted repeated section name 
    in linear group sections.
    """

class MisMatchDirectionError(DataValidationFailed):
    """
    Raises when direction in the sections
    is not match with the direction in the
    fixture data.
    """