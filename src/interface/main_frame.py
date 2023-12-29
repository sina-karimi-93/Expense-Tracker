
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QVBoxLayout


class MainFrame(QFrame):
    """
    Main Frame of the app that contains
    other frames and widgets
    """
    def __init__(self) -> None:
        super().__init__()
        self.init_ui()
    

    def init_ui(self) -> None:
        """
        Initialize widgets
        """
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)