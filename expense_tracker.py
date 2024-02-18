"""
Main module of the program that shows
the GUI.
"""
from lib import QApplication
from lib import QMainWindow
from lib import DataHandler
from lib import MainFrame
from lib import load_css
from lib import CSS_FILE_PATH
from lib import CSS_COLORS_FILE_PATH

class MainWindow(QMainWindow):
    """
    Customized QMainWindow.
    """

    theme = load_css(CSS_FILE_PATH,
                     CSS_COLORS_FILE_PATH)

    def __init__(self) -> None:
        super().__init__()
        self.setup_window()
        self.init_ui()
    
    def init_ui(self) -> None:
        """
        Initialize ui widgets such as central widget,
        toolbar and, etc.
        """
        self.main_frame = MainFrame(data_handler=DataHandler)
        self.setCentralWidget(self.main_frame)

    def setup_window(self) -> None:
        """
        Setup window title, size and icon.
        """
        self.setWindowTitle("Expense Tracker")
        self.setGeometry(500, 300, 1550, 700)
        self.setFixedWidth(1600)
        self.setMinimumHeight(700)
        self.setStyleSheet(self.theme)

def run_app() -> None:
    """
    Create an qt application and instance
    of the main window to show the GUI.
    """
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

if __name__ == "__main__":
    run_app()