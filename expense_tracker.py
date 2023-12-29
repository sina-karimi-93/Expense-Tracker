"""
Main module of the program that shows
the GUI.
"""
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from src import MainFrame
from src import open_file
from src import CSS_FILE_PATH

class MainWindow(QMainWindow):
    """
    Customized QMainWindow.
    """

    theme = open_file(CSS_FILE_PATH)

    def __init__(self) -> None:
        super().__init__()
        self.setup_window()
        self.init_ui()
    
    def init_ui(self) -> None:
        """
        Initialize ui widgets such as central widget,
        toolbar and, etc.
        """
        self.main_frame = MainFrame()
        self.setCentralWidget(self.main_frame)

    def setup_window(self) -> None:
        """
        Setup window title, size and icon.
        """
        self.setWindowTitle("Expense Tracker")
        self.setGeometry(500, 300, 1300, 700)
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