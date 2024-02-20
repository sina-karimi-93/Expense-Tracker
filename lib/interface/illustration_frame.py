"""
This module contains frames for illustrate
the expenses.
"""
from typing import Callable
from datetime import datetime
from .widgets import Horizontal
from .widgets import Vertical
from .widgets import ScrollArea
from .widgets import Frame
from .widgets import DateEntry
from .widgets import LabelEntry
from .widgets import Label
from .widgets import Button
from .widgets import QGraphicsDropShadowEffect
from .widgets import QColor
from .widgets import HorizontalTable
from lib.constants import TABLE_HEADERS
from lib.constants import DOLLAR_ICON_PATH
from lib.constants import ITEMS_ICON_PATH
from lib.data_handler import DataHandler

class IllustrationFrame(Frame):
    """
    This frame is for showing the inserted
    expenses, filter them based on different
    items.
    """
    def __init__(self,
                 data_handler: DataHandler,
                 configs: dict) -> None:
        super().__init__(layout=Vertical)
        self.data_handler = data_handler
        self.setObjectName("illustration-frame")
        self.setup_frame()
        self.is_show_details = False
        self.init_widgets(data_handler.get_all(),
                          configs)

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
                     all_expenses: list,
                     configs: dict) -> None:
        """
        Initializes the widgets.
        """
        self.illustration_filter = IllustrationFiltersFrame(
            self.illustration_filters_callback,
            configs)
        self.add_stretch()
        self.table = HorizontalTable(editable=True, min_height=500)
        self.table.insert_data(TABLE_HEADERS, all_expenses)
        self.illustration_detail = IlusstrationDetailsFrame(self.data_handler,
                                                            all_expenses)
        self.illustration_detail.setVisible(self.is_show_details)
        self.add_stretch()
        total_price = self.data_handler.get_total_price(all_expenses)
        total_items = len(all_expenses)
        self.illustration_summary = IllustrationSummaryFrame(total_price,
                                                             total_items,
                                                             self.show_overall_detail_callback)

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
        self.illustration_detail.init_widgets(expenses)

        total_price = self.data_handler.get_total_price(expenses)
        total_items = len(expenses)
        self.illustration_summary.update_summary(total_price, total_items)
    
    def show_overall_detail_callback(self) -> None:
        """
        This is a callback method for button in
        illustration summary to switch between
        showing the table data or detail data
        """
        self.table.setVisible(self.is_show_details)
        self.is_show_details = not self.is_show_details
        self.illustration_detail.setVisible(self.is_show_details)

class IllustrationFiltersFrame(Frame):
    """
    This frame has widgets to filter the
    expense for showing in the illustration
    frame.
    """

    def __init__(self,
                 filters_callback: Callable,
                 configs: dict) -> None:
        super().__init__(layout=Horizontal)

        self.init_widgets(filters_callback, configs)
    
    def init_widgets(self,
                     filters_callback: Callable,
                     configs: dict) -> None:
        """
        Initializes the widgets.
        """
        from_date = configs.get("default_from_date",
                                datetime(day=1,month=1, year=2023))
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


class IlusstrationDetailsFrame(Frame):
    """
    This frame is for generating widgets
    for each expense to show them day by day
    """

    def __init__(self,
                 data_handler: DataHandler,
                 expenses: list) -> None:
        super().__init__(layout=Vertical)
        self.data_handler = data_handler
        self.setMinimumHeight(500)
        self.init_widgets(expenses)

    def init_widgets(self,
                     expenses: list) -> None:
        """
        Initializes the widgets
        """
        self.remove_all_widgets()
        self.container = Frame(layout=Vertical)
        self.scrollarea = ScrollArea(child=self.container)
        grouped_expenses = self.data_handler.group_expenses_by_date(expenses)
        for date, group in grouped_expenses.items():
            detail_frame = IllustrationDetailFrame(date, group)
            setattr(self.container, str(date), detail_frame)

class IllustrationDetailFrame(Frame):
    """
    This frame is for showing the expenses
    in a day.
    """

    def __init__(self,
                 date: datetime,
                 expenses: list) -> None:
        super().__init__(layout=Vertical)
        self.setFixedHeight(230)
        self.setup_frame()
        self.init_widgets(date, expenses)

    def setup_frame(self) -> None:
        """
        Setup frame size, color and
        """
        effect = QGraphicsDropShadowEffect(self)
        effect.setOffset(0, 0)
        effect.setColor(QColor("#434b4e"))
        effect.setBlurRadius(20)
        self.setGraphicsEffect(effect)

    def init_widgets(self,
                     date: datetime,
                     expenses: list) -> None:
        """
        Initializes the widgets.
        """
        string_date = date.strftime("%Y-%m-%d / %a")
        self.date = Label(string_date,
                          object_name="expense-detail-date")
        self.container = Frame(layout=Horizontal)
        
        self.scrollarea = ScrollArea(self.container)
        for index, expense in enumerate(expenses):
            expense_card = IllustrationDetailCard(expense)
            setattr(self.container, f"expense_{index}", expense_card)
        self.container.add_stretch()

class IllustrationDetailCard(Frame):
    """
    This frame is for showing an expense
    detail in a card.
    """
    def __init__(self, expense: dict) -> None:
        super().__init__(layout=Vertical)
        self.setObjectName("expense-card")
        self.setFixedSize(150, 150)
        self.init_widgets(expense)

    def init_widgets(self, expense: dict) -> None:
        """
        Initializes thw widgets.
        ---------------------------------
        -> Params
            expense: dict
        """
        self.title = Label(expense["title"][:14], object_name="expense-card-label")
        self.price = Label(expense["price"], object_name="expense-card-label")
        self.quantity = Label(expense["quantity"], object_name="expense-card-label")
        self.overall_price = Label(expense["overall_price"], object_name="expense-card-label")
        self.category = Label(expense["category"], object_name="expense-card-label")

class IllustrationSummaryFrame(Frame):
    """
    This class contains widgets to show
    the summary of the expenses such as
    total price, number of items and...
    """

    def __init__(self,
                 total_price: float,
                 total_items: int,
                 show_overall_detail_callback: Callable) -> None:
        super().__init__(layout=Horizontal)

        self.init_widgets(total_price,
                          total_items,
                          show_overall_detail_callback)
    
    def init_widgets(self,
                     total_price: float,
                     total_items: int,
                     show_overall_detail_callback: Callable) -> None:
        """
        Initialize the widgets
        ---------------------------------------
        -> Params
            total_price: float,
            total_items: int
        """
        self.total_price_icon = Label("")
        self.total_price_icon.set_image(DOLLAR_ICON_PATH,(27,27))
        self.total_price = Label("")

        self.add_stretch()

        self.total_items_icon = Label("")
        self.total_items_icon.set_image(ITEMS_ICON_PATH,(27,27))
        self.total_items = Label("")
        
        self.add_stretch()

        self.button = Button("OVERALL / DETAIL",
                             callback_function=show_overall_detail_callback, 
                             width=200,
                             object_name="overall-detail")

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
        self.total_price.change_text(f"TOTAL PRICE ${'{:,}'.format(total_price)}")
        self.total_items.change_text(f"TOTAL ITEMS {total_items}")