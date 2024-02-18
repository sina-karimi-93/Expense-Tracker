
from datetime import datetime
from typing import Callable
from lib.constants import TABLE_HEADERS
from lib.constants import DATE_FORMAT
from lib.constants import DOLLAR_ICON_PATH
from lib.constants import ITEMS_ICON_PATH
from lib.constants import EXPENSES_FILE_PATH
from lib.errors import DataValidationFailed
from lib.data_handler import DataHandler
from .widgets import Frame
from .widgets import Vertical
from .widgets import Horizontal
from .widgets import LabelEntry
from .widgets import Label
from .widgets import Button
from .widgets import QGraphicsDropShadowEffect
from .widgets import QColor
from .widgets import DateEntry
from .widgets import HorizontalTable
from .widgets import Stretch
from .utils import log

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
        effect.setBlurRadius(20)
        self.setGraphicsEffect(effect)
    
    def init_widgets(self,
                    add_expense_callback: Callable) -> None:
        """
        Initializes the widgets
        """
        self.title = LabelEntry(label="TITLE",
                                validator="string",
                                object_name="entry")
        self.price = LabelEntry(label="PRICE",
                                validator="decimal",
                                callback_func=self.set_overall_callback,
                                object_name="entry")
        self.quantity = LabelEntry(label="QUANTITY",
                                   default_value=1,
                                   validator="int",
                                   callback_func=self.set_overall_callback,
                                   object_name="entry")
        self.overall_price = LabelEntry(label="OVERALL PRICE",
                                        default_value=0,
                                        editable=False,
                                        validator="decimal",
                                        object_name="entry")
        self.category = LabelEntry(label="CATEGORY",
                                   validator="string",
                                   object_name="entry")
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

class IllustrationFiltersFrame(Frame):
    """
    This frame has widgets to filter the
    expense for showing in the illustration
    frame.
    """

    def __init__(self, filters_callback: Callable) -> None:
        super().__init__(layout=Horizontal)

        self.init_widgets(filters_callback)
    
    def init_widgets(self,
                     filters_callback: Callable) -> None:
        """
        Initializes the widgets.
        """
        from_date = datetime(day=1,month=1, year=2023)
        self.from_date = DateEntry(label="FROM DATE",
                                   default_date=from_date,
                                   width=200,
                                   callback_func=filters_callback)
        self.to_date = DateEntry(label="TO DATE",
                                 width=200,
                                 callback_func=filters_callback)
        self.title = LabelEntry(label="TITLE",
                                width=200,
                                validator="string",
                                object_name="entry",
                                callback_func=filters_callback)
        self.category = LabelEntry(label="CATEGORY",
                                   width=200,
                                   validator="string",
                                   object_name="entry",
                                   callback_func=filters_callback)

    def get_filters(self) -> dict:
        """
        Returns the widgets values. Check if
        non-date widgets are empty remove them
        from the return.
        """
        values = self.get_values()
        if not values["title"].replace(" ", ""):
            values.pop("title")
        if not values["category"].replace(" ", ""):
            values.pop("category")
        return values

class IllustrationSummaryFrame(Frame):
    """
    This class contains widgets to show
    the summary of the expenses such as
    total price, number of items and...
    """

    def __init__(self,
                 total_price: float,
                 total_items: int) -> None:
        super().__init__(layout=Horizontal)

        self.init_widgets(total_price,
                          total_items)
    
    def init_widgets(self,
                     total_price: float,
                     total_items: int) -> None:
        """
        Initialize the widgets
        ---------------------------------------
        -> Params
            total_price: float,
            total_items: int
        """
        self.add_stretch()
        self.total_price_icon = Label("")
        self.total_price_icon.set_image(DOLLAR_ICON_PATH,(27,27))
        self.total_price = Label("")

        self.add_stretch()

        self.total_items_icon = Label("")
        self.total_items_icon.set_image(ITEMS_ICON_PATH,(27,27))
        self.total_items = Label("")
        
        self.add_stretch()

        self.update_summary(total_price, total_items)
    
    def update_summary(self,
                       total_price: float,
                       total_items: int) -> None:
        """
        Update the widgets values.
        ---------------------------------------
        -> Params
            total_price: float,
            total_items: int
        """
        self.total_price.change_text(f"TOTAL PRICE {total_price}")
        self.total_items.change_text(f"TOTAL ITEMS {total_items}")
        

class IllustrationFrame(Frame):
    """
    This frame is for showing the inserted
    expenses, filter them based on different
    items.
    """

    def __init__(self,
                 data_handler: DataHandler) -> None:
        super().__init__(layout=Vertical)
        self.data_handler = data_handler
        self.setObjectName("illustration-frame")
        self.setup_frame()
        self.init_widgets(data_handler.get_all())

    def setup_frame(self) -> None:
        """
        Setup frame size, color and
        """
        self.setMinimumWidth(950)
        self.setMaximumWidth(1500)
        effect = QGraphicsDropShadowEffect(self)
        effect.setOffset(0, 0)
        effect.setColor(QColor("#434b4e"))
        effect.setBlurRadius(20)
        self.setGraphicsEffect(effect)

    def init_widgets(self,
                     all_expenses: list) -> None:
        """
        Initializes the widgets.
        """

        self.illustration_filter = IllustrationFiltersFrame(
            self.illustration_filters_callback)

        self.table = HorizontalTable(editable=True)
        self.table.insert_data(TABLE_HEADERS, all_expenses)

        total_price = self.data_handler.get_total_price(all_expenses)
        total_items = len(all_expenses)
        self.illustration_summary = IllustrationSummaryFrame(total_price,
                                                             total_items)

    def illustration_filters_callback(self) -> None:
        """
        This methos is a callback for the widgets
        in the IllustrationFiltersFrame to filter
        the data based on the user inputs.
        """
        values = self.illustration_filter.get_filters()
        expenses = self.data_handler.filter_data(filters=values)
        self.table.clear()
        self.table.insert_data(TABLE_HEADERS, expenses)

        total_price = self.data_handler.get_total_price(expenses)
        total_items = len(expenses)
        self.illustration_summary.update_summary(total_price, total_items)

class MainFrame(Frame):
    """
    Main Frame of the app that contains
    other frames and widgets
    """
    def __init__(self,
                 data_handler: DataHandler) -> None:
        super().__init__(layout=Horizontal)
        self.data_handler = data_handler(EXPENSES_FILE_PATH)
        self.setContentsMargins(5,5,5,5)
        self.add_expense_frame = AddExpenseFrame(add_expense_callback=self.add_expense_callback)

        self.add_stretch()
        self.illustration_frame = IllustrationFrame(self.data_handler)

    def add_expense_callback(self) -> None:
        """
        Callback method for add_expense_frame
        button for collecting the values and
        save the exense.
        """
        try:
            self.add_expense_frame.validate_widgets()
            values = self.add_expense_frame.get_values()
            values["date"] = values["date"].strftime(DATE_FORMAT)
            self.data_handler.add_expense(values)
            self.illustration_frame.illustration_filters_callback()
        except DataValidationFailed as error:
            print(error)
    