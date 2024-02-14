
from typing import Callable
from lib.errors import DataValidationFailed
from .widgets import Frame
from .widgets import Vertical
from .widgets import Horizontal
from .widgets import LabelEntry
from .widgets import Button
from .widgets import QGraphicsDropShadowEffect
from .widgets import QColor
from .widgets import DateEntry
from .widgets import HorizontalTable
from .utils import log
from .utils import load_json
from .utils import write_json

class AddExpenseFrame(Frame):

    def __init__(self,
                 add_expense_callback: Callable):
        super().__init__(layout=Vertical)
        self.setObjectName("add-expense-frame")
        self.setup_frame()

        self.init_widgets(add_expense_callback=add_expense_callback)

    def setup_frame(self) -> None:
        """
        Setup frame size, color and
        """
        self.setMinimumWidth(250)
        self.setMaximumWidth(400)
        effect = QGraphicsDropShadowEffect(self)
        effect.setOffset(0, 0)
        effect.setColor(QColor("#434b4e"))
        effect.setBlurRadius(15)
        self.setGraphicsEffect(effect)
    
    def init_widgets(self,
                    add_expense_callback: Callable) -> None:
        """
        Initializes the widgets
        """
        self.title = LabelEntry(label="TITLE",
                                validator="string")
        self.price = LabelEntry(label="PRICE",
                                validator="decimal",
                                callback_func=self.set_overall_callback)
        self.quantity = LabelEntry(label="QUANTITY",
                                   default_value=1,
                                   validator="int",
                                   callback_func=self.set_overall_callback)
        self.overall_price = LabelEntry(label="OVERALL PRICE",
                                        default_value=0,
                                        editable=False,
                                        validator="decimal")
        self.category = LabelEntry(label="CATEGORY",
                                   validator="string")
        self.date = DateEntry(label="DATE",
                              width=250)
        
        self.add_stretch()

        self.add_expense_button = Button(label="ADD EXPENSE",
                                         object_name="add-expense",
                                         callback_function=add_expense_callback,
                                         width=270)

    def set_overall_callback(self) -> None:
        """
        Collects quantity and price values
        to calculate the overall price and
        set it to overall price widget.
        """
        price = self.price.get_value() or 0
        quantity = self.quantity.get_value() or 1
        self.overall_price.set_value(price * quantity)

class IllustrationFrame(Frame):
    def __init__(self,
                 test_data: list) -> None:
        super().__init__(layout=Vertical)
        self.setObjectName("illustration-frame")
        self.setup_frame()
        self.init_widgets(test_data)

    def setup_frame(self) -> None:
        """
        Setup frame size, color and
        """
        self.setMinimumWidth(950)
        self.setMaximumWidth(1500)
        effect = QGraphicsDropShadowEffect(self)
        effect.setOffset(0, 0)
        effect.setColor(QColor("#434b4e"))
        effect.setBlurRadius(15)
        self.setGraphicsEffect(effect)

    def init_widgets(self,
                    test_data: list) -> None:
        """
        Initializes the widgets.
        """
        test_data += test_data
        test_data += test_data

        self.table = HorizontalTable(editable=True)
        headers = ["Title", "Price", "Quantity",
                   "Overall Price", "Categoty",
                   "Date"]
        self.table.insert_data(headers, test_data)

class MainFrame(Frame):
    """
    Main Frame of the app that contains
    other frames and widgets
    """
    def __init__(self) -> None:
        super().__init__(layout=Horizontal)
        self.test_data = load_json("./test_data.json") or list()
        self.setContentsMargins(5,5,5,5)
        self.add_expense_frame = AddExpenseFrame(add_expense_callback=self.add_expense_callback)

        self.add_stretch()
        self.iii = IllustrationFrame(self.test_data)

    def add_expense_callback(self) -> None:
        """
        Callback method for add_expense_frame
        button for collecting the values and
        save the exense.
        """
        try:
            self.add_expense_frame.validate_widgets()
            values = self.add_expense_frame.get_values()
            self.test_data.append(values)
            write_json("./test_data.json", self.test_data)
        except DataValidationFailed as error:
            print(error)
    