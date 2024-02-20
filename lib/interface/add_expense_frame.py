"""
This module contains class and widgets for
getting expense info and save it.
"""
from typing import Callable
from .widgets import Frame
from .widgets import Vertical
from .widgets import LabelEntry
from .widgets import Button
from .widgets import QGraphicsDropShadowEffect
from .widgets import QColor
from .widgets import DateEntry

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
        self.setMinimumWidth(305)
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
