"""
Main module of the program that shows
the GUI.
"""
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow


class MainWindow(QMainWindow):
    """
    Customized QMainWindow.
    """

    def __init__(self) -> None:
        super().__init__()
        self.setup_window()
    
    def setup_window(self) -> None:
        """
        Setup window title, size and icon.
        """
        self.setWindowTitle("Expense Tracker")
        self.setGeometry(500, 300, 1300, 700)

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