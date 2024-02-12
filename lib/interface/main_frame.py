
from .widgets import Frame
from .widgets import Vertical
from .widgets import Horizontal

class InputsFrame(Frame):

    def __init__(self) -> None:
        super().__init__(layout=Vertical)

    


class MainFrame(Frame):
    """
    Main Frame of the app that contains
    other frames and widgets
    """
    def __init__(self) -> None:
        super().__init__(layout=Horizontal)

    