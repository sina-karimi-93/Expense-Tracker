"""
This module has a class to change app
setting and export expenses in excel
and csv.
"""
from typing import Callable
from datetime import datetime
from .widgets import Frame
from .widgets import Vertical
from .widgets import LabelEntry
from .widgets import Button
from .widgets import QGraphicsDropShadowEffect
from .widgets import QColor
from .widgets import DateEntry


class ToolsFrame(Frame):

    def __init__(self,
                 illustration_count: int,
                 default_date: datetime,
                 update_configs: Callable,
                 export_excel: Callable,
                 export_csv: Callable):
        super().__init__(layout=Vertical)
        self.setObjectName("tools-frame")
        self.setup_frame()
        self.init_widgets(illustration_count,
                          default_date,
                          update_configs,
                          export_excel,
                          export_csv)

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
                     illustration_count: int,
                     default_date: datetime,
                     update_configs: Callable,
                     export_excel: Callable,
                     export_csv: Callable) -> None:
        """
        Initializes the widgets.
        """
        self.illustration_count = LabelEntry(label="ILLUSTRATION COUNT",
                                            default_value=illustration_count,
                                            validator="int",
                                            value_limit=(0, 1000),
                                            object_name="entry")
        self.default_from_date = DateEntry(label="DEFAULT FROM DATE",
                                           default_date=default_date,
                                           width=250)
        self.add_stretch()
        self.save_settings_button = Button(label="SAVE SETTINGS",
                                           object_name="add-expense",
                                           callback_function=update_configs,
                                           width=270)
        self.export_excel_button = Button(label="EXPORT EXCEL",
                                          object_name="add-expense",
                                          callback_function=export_excel,
                                          width=270)
        
        self.export_csv_button = Button(label="EXPORT CSV",
                                          object_name="add-expense",
                                          callback_function=export_csv,
                                          width=270)