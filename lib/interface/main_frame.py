

from datetime import datetime
from .utils import load_json
from .utils import write_json
from lib.constants import EXPENSES_FILE_PATH
from lib.constants import CONFIGS_FILE_PATH
from lib.errors import DataValidationFailed
from lib.data_handler import DataHandler
from .widgets import Frame
from .widgets import Horizontal
from .widgets import MessageBox
from .add_expense_frame import AddExpenseFrame
from .illustration_frame import IllustrationFrame
from .tools_frame import ToolsFrame
from .utils import log


class MainFrame(Frame):
    """
    Main Frame of the app that contains
    other frames and widgets
    """
    def __init__(self,
                 data_handler: DataHandler) -> None:
        super().__init__(layout=Horizontal)
        self.setContentsMargins(5, 5, 5, 5)

        self.configs = self.load_configs()
        self.data_handler = data_handler(EXPENSES_FILE_PATH,
                                        self.configs.get("illustration_count", 100))

        self.add_expense_frame = AddExpenseFrame(add_expense_callback=self.add_expense_callback)

        self.illustration_frame = IllustrationFrame(self.data_handler,
                                                    self.configs)
        
        illustration_count = self.configs.get("illustration_count", 100)
        default_date = self.configs.get("default_from_date",
                                        datetime(year=2023, month=1, day=1))
        self.tools_frame = ToolsFrame(illustration_count,
                                      default_date,
                                      self.update_configs,
                                      self.export_excel,
                                      self.export_csv)
        self.add_stretch()

    def load_configs(self) -> dict:
        """
        Loads the config file.
        """
        try:
            return load_json(CONFIGS_FILE_PATH)
        except FileNotFoundError:
            return dict()


    def add_expense_callback(self) -> None:
        """
        Callback method for add_expense_frame
        button for collecting the values and
        save the exense.
        """
        try:
            self.add_expense_frame.validate_widgets()
            values = self.add_expense_frame.get_values()
            self.data_handler.add_expense(values)
            self.illustration_frame.illustration_filters_callback()
        except DataValidationFailed as error:
            log(error, error=error, level=2, color="red")
            error = str(error).replace("_", " ")
            MessageBox(self,
                       "high",
                       title="Error",
                       message=error)
    
    def update_configs(self) -> None:
        """
        This method is for updating the config file
        and calls from tools frame.
        """
        try:
            self.tools_frame.validate_widgets()
            configs = self.tools_frame.get_values()
            self.configs.update(configs)
            write_json(CONFIGS_FILE_PATH, self.configs)
        except DataValidationFailed as error:
            log(error, error=error, level=2, color="red")
            error = str(error).replace("_", " ")
            MessageBox(self,
                       "high",
                       title="Error",
                       message=error)
    
    def export_excel(self) -> None:
        """
        Export the current filtered expenses to
        the excel file.
        """

    def export_csv(self) -> None:
        """
        Export the current filtered expenses to
        the csv file.
        """