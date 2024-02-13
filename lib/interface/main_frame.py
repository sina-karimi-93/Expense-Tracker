

from datetime import datetime
from .widgets import Qt
from PyQt5.QtWidgets import QAbstractSpinBox
from .widgets import Frame
from .widgets import Vertical
from .widgets import Horizontal
from .widgets import LabelEntry
from .widgets import LabelCombobox
from .widgets import LabelCombobox
from .widgets import QGraphicsDropShadowEffect
from .widgets import QColor
from .widgets import QDateEdit


class AddExpenceFrame(Frame):

    def __init__(self):
        super().__init__(layout=Vertical)
        
        self.setup_frame()

        self.init_widgets()

    def setup_frame(self) -> None:
        """
        Setup frame size, color and
        """
        self.setMinimumWidth(300)
        self.setMaximumWidth(450)
        effect = QGraphicsDropShadowEffect(self)
        effect.setOffset(0, 0)
        effect.setColor(QColor("#434b4e"))
        effect.setBlurRadius(15)
        self.setGraphicsEffect(effect)
    
    def init_widgets(self) -> None:
        """
        Initializes the widgets
        """
        self.title = LabelEntry(label="TITLE")
        self.price = LabelEntry(label="PRICE")
        self.quantity = LabelEntry(label="QUANTITY",
                                   default_value=1)
        self.category = LabelEntry(label="Category")

        self.date = QDateEdit(calendarPopup=False)
        self.date.setDateTime(datetime.now())
        effect = QGraphicsDropShadowEffect(self)
        effect.setColor(QColor("#f89fa2"))
        effect.setOffset(0, 0)
        effect.setBlurRadius(10)
        self.date.setGraphicsEffect(effect)
        self.date.setAlignment(Qt.AlignCenter)
        self.date.setButtonSymbols(QAbstractSpinBox.NoButtons)



        self.add_stretch()

class TestFrame(Frame):
    def __init__(self) -> None:
        super().__init__(layout=Vertical)
        self.setup_frame()

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

class MainFrame(Frame):
    """
    Main Frame of the app that contains
    other frames and widgets
    """
    def __init__(self) -> None:
        super().__init__(layout=Horizontal)
        self.setContentsMargins(5,5,5,5)
        self.add_expence_frame = AddExpenceFrame()

        self.add_stretch()
        self.iii = TestFrame()


    