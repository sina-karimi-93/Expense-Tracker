"""
Module contains all the widgets class to create UI with Qt library
"""
import re
import csv
from datetime import datetime
from itertools import chain
from typing import Any
from typing import Union
from typing import NewType
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtWidgets import QAbstractSpinBox
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtWidgets import QStatusBar
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QRadioButton
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QToolBar
from PyQt5.QtWidgets import QBoxLayout
from PyQt5.QtWidgets import QVBoxLayout as Vertical
from PyQt5.QtWidgets import QHBoxLayout as Horizontal
from PyQt5.QtWidgets import QGridLayout as Grid
from PyQt5.QtWidgets import QStackedLayout as StackedLayout
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QListView
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QCompleter
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QGraphicsOpacityEffect
from PyQt5.QtWidgets import QGraphicsColorizeEffect
from PyQt5.QtWidgets import QGraphicsBlurEffect
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from PyQt5.QtWidgets import QProgressBar
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QDateEdit

from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QIconEngine
from PyQt5.QtGui import QClipboard
from PyQt5.QtGui import QCursor
from PyQt5.QtGui import QPalette
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QFocusEvent
from PyQt5.QtGui import QIntValidator
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtGui import QValidator
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QDrag

from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QPropertyAnimation
from PyQt5.QtCore import QEasingCurve
from PyQt5.QtCore import QParallelAnimationGroup
from PyQt5.QtCore import QPoint
from PyQt5.QtCore import QRect
from PyQt5.QtCore import QModelIndex
from PyQt5.QtCore import QEvent
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QSize
from PyQt5.QtCore import QRegExp
from PyQt5.QtCore import QSortFilterProxyModel
from PyQt5.QtCore import QDir
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import QMimeData
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaContent
from PyQt5.QtMultimedia import QMediaPlayer
from lib.errors import DataValidationFailed, RowNotExists, TableCellNotFoundError
from .utils import log
from .utils import void_function
from lib.constants import *

CSS = NewType("CSS", str)


def change_widget_status(widget: object, status: str = "normal") -> None:
    """
    Change the color of the widget to show the
    status of the widget.
    """
    states = {
        "normal": "",
        "warning": "#ffae00",
        "error": "#ff0048",
    }
    widget.setStyleSheet(f"border-color:{states[status]};")


class MessageBox(QMessageBox):
    """
    Custom subclass of QMessageBox
    """

    def __init__(self,
                 parent: object,
                 critical_level: str,
                 title: str,
                 message: str,
                 **kwargs) -> None:
        super().__init__(parent=parent, **kwargs)
        message = str(message)
        if critical_level == 'low':
            self.information(self, title, message)
        elif critical_level == 'medium':
            self.warning(self, title, message)
        elif critical_level == 'high':
            self.critical(self, title, message)
        else:
            self.setWindowTitle(title)
            self.setText(message)
            self.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

    def get_answer(self) -> bool:
        """
        Return the result of the message box
        in boolean.
        """
        result = self.exec()
        if result == QMessageBox.Ok:
            return True
        return False


class IntValidator(QIntValidator):

    def validate(self, a0: str, a1: int):
        """
        Overrite this method to add better restriction
        when user type a value.
        It checks if the value user inserted is not in
        the boundaries, then prevent typing more than of
        the boundaries.
        """

        res = super().validate(a0, a1)
        try:
            if not self.bottom() <= int(a0) <= self.top():
                res = (0, a0, a1)
        except ValueError:
            return res
        return res


class DoubleValidator(QDoubleValidator):

    def validate(self, a0: str, a1: int):
        """
        Overrite this method to add better restriction
        when user type a value.
        It checks if the value user inserted is not in
        the boundaries, then prevent typing more than of
        the boundaries.
        """
        res = super().validate(a0, a1)
        try:
            if not self.bottom() <= float(a0) <= self.top():
                res = (0, a0, a1)
        except ValueError:
            return res
        return res


class RegxpValidator(QRegExpValidator):
    """
    Sub class of QRegExpValidator, it will validate
    the widget value base on given regular expression
    pattern.
    ------------------------------------------------
    -> Params:
             pattern
    """

    def __init__(self, pattern: str) -> None:
        super().__init__(QRegExp(pattern))


class WidgetController:
    """
    its helper class(add extra functionalty to subclass).
    helps to keep track of the created widgets
    to make it get their data or removing them
    @methods
       __setattr__ = overridden
       get_widgets()
       remove_widgets()
       add_stretch()
    @usage:
         class Test(WidgetController):
             pass
    """

    def __init__(self) -> None:
        self.widgets = list()

    def add_grid_widget(self, widget: object) -> None:
        """
        Add grid widget when the main layout
        is QGridLayout, this method will override
        the add_widget
        -> Params:
                widget
        """
        grid_positions = widget.grid_positions
        self.main_layout.addWidget(widget, *grid_positions)

    def get_widget_object(self, index: int) -> object:
        """
        Return the widget object by index
        @args
            index:int

        @return
            object
        """
        return self.widgets[index][1]

    def get_widget_name(self, index: int) -> str:
        """
        Return the widget name by index
        @args
            index:int

        @return
            str
        """
        return self.widgets[index][0]

    def get_widget(self, index: int) -> tuple:
        """
        Return the widget name and object by index
        @args
            index:int

        @return
            tuple
        """

        return self.widgets[index]

    def add_widget(self, widget: object) -> None:
        """
        add non grid widget to the main layout
        this method will be replace with
        -> Params:
             widget
        """
        self.main_layout.addWidget(widget)

    def __setattr__(self, name: str, widget: object) -> None:
        """
        overriden __setattr__ to intercept
        object when setattr get called.
        we adding all widgets to widgets list
        by intercepting the coming objects
        -> Params:
                name: attribute name
                obj: attribute object
        """
        super().__setattr__(name, widget)
        try:
            # add to prevent qt log for none object
            # TODO: need to be tested
            if widget == None:
                return
            self.add_widget(widget)
            self.widgets.append((name, widget))
        except TypeError as error:
            log(error=error,
                level=3, 
                color="red")

        except AttributeError as error:
            log(error=error,
                level=3, 
                color="red")

    def get_widgets(self) -> list:
        """
        Return all widgets.
        return ->
            [(name,object),...]
        """
        return self.widgets

    def remove_widget(self, index: int = -1) -> None:
        """
        Remove the widget from layout and class.
        The default index is -1 to remove last widget added.
        params ->
            index: int
        """
        name, widget_obj = self.widgets[index]
        widget_obj.deleteLater()
        delattr(self, name)
        self.widgets.pop(index)
    
    def remove_widget_by_name(self, widget_name: str) -> None:
        """
        Based on the widget attribute name, remove
        it from the widget tree.
        """
        index = 0
        for name, widget_obj in self.widgets:
            if name == widget_name:
                widget_obj.deleteLater()
                delattr(self, name)
                break
            index += 1
        self.widgets.pop(index)

    def remove_all_widgets(self) -> None:
        """
        Remove all the widgests inside the widget list
        """
        for name, widget in self.widgets:
            widget.deleteLater()
            delattr(self, name)
        self.widgets.clear()

    def get_values(self) -> dict:
        """
        Return values of the all the widgets
        as dictionary
        """
        values = {
            name: widget.get_value()
            for name, widget in self.widgets if hasattr(widget, "get_value")
        }
        return values

    def add_stretch(self, strech_factor: int = 1) -> None:
        """
        Adds a stretchable space (a QSpacerItem)
        with zero minimum size and stretch factor
        stretch to the end of this box layout.
        -> params:
                 strech_factor
        """
        self.main_layout.addStretch(strech_factor)

    def validate_widgets(self) -> None:
        """
        iter over the widgets list and call widgets validate
        method.
        """
        for widget_name, widget in self.widgets:
            try:
                result = widget.validate()
                if result != True:
                    raise DataValidationFailed(
                        f"{widget_name.capitalize()} {result}")
            except AttributeError as error:
                log(error=error,
                    level=2, 
                    color="red")

    def get_layout(self) -> object:
        """
        return subclass layout manager class
        (QHBoxLayout or QVBoxLayout)
        """
        return self.main_layout

    def clear_cache(self) -> None:
        """
        Clear cached widgets inside the layout
        """
        self.main_layout.invalidate()

    def clear_values(self) -> None:
        """
        Clear all the widgets values
        """
        for _, widget in self.widgets:
            try:
                func = getattr(widget, "clear_value")
                func()
            except AttributeError as error:
                log(error=error,
                    level=2, 
                    color="red")


class Frame(QFrame, WidgetController):
    """
    Custom Frame class (Qwidget)
    """

    def __init__(self, layout: object, grid_positions: tuple = None, **kwargs):
        super().__init__(**kwargs)
        self.grid_positions = grid_positions
        self.main_layout = layout()

        self.adjustSize()
        self.setLayout(self.main_layout)


class BaseFrame(QFrame, WidgetController):
    """
    this class is used when we have subframe
    or frame contain other frame, the only diffrent
    with normal Frame class is __setattr__ automatically
    add all the subframe widgets to the widget list to
    make it easier get all the widges values
    """

    def __init__(self, layout: object, **kwrags):
        super().__init__(**kwrags)
        self.main_layout = layout()
        self.adjustSize()
        self.setLayout(self.main_layout)

    def __setattr__(self, name: str, widget: object) -> None:
        """
        Overrided __setattr__, widgets gonna be subframes.
        its adding all subframe widgets to the BaseFrame
        widgets list
        """
        super().__setattr__(name, widget)
        try:
            self.sub_frame = widget.get_widgets()
            self.widgets = list(chain(self.widgets, self.sub_frame))
        except AttributeError as error:
            log(error=error,
                level=3, 
                color="red")

    def get_values(self) -> dict:
        """
        Returns Value of the widgets, driver subframe
        and common widget subframe
        """
        values = dict()
        # update the widgets list if any change has been made
        self.widgets = list(chain(self.widgets, self.sub_frame))
        for name, widgets in self.widgets:
            try:
                values[name] = widgets.get_value()
            except AttributeError as error:
                log(error=error,
                    level=2, 
                    color="red")

            except RuntimeError as error:
                log(error=error,
                    level=2, 
                    color="red")

        return values


class Dragable:
    """
    Decorator class for adding drag/drop feature
    to the decorated Frame classes.

    Adds mouseMoveEvent method to the decorated class.
    """

    def __call__(self, widget: QWidget) -> QWidget:
        setattr(widget, "mouseMoveEvent",
                lambda x, y: self.mouseMoveEvent(x, y))
        return widget

    @staticmethod
    def mouseMoveEvent(widget, event):
        """
        Implementing this method to allow the widget
        has drag and drop feature.
        """
        if event.buttons() == Qt.LeftButton:
            drag = QDrag(widget)
            mime = QMimeData()
            drag.setMimeData(mime)

            pixmap = QPixmap(widget.size())
            widget.render(pixmap)
            drag.setPixmap(pixmap)

            drag.exec_(Qt.MoveAction)


class HoverBorder:
    """
    Decorator class for adding two events to the
    widget classes, namely enterEvent and leaveEvent to
    chand the border color when mouse enters and leaves
    the widgets.
    Using staticmethod on enterEvent and leaveEvent methods
    is for we do not need the instance of this class, we just
    want to assign this methods to the new class.
    """

    def __init__(self,
                 enter_color: str = "#F1B300",
                 leave_color: str = "#153b4d") -> None:
        self.enter_color = enter_color
        self.leave_color = leave_color

    def __call__(self, widget: QWidget) -> QWidget:
        setattr(widget, "enterEvent",
                lambda x, y: self.enterEvent(x, self.enter_color, y))
        setattr(widget, "leaveEvent",
                lambda x, y: self.leaveEvent(x, self.leave_color, y))
        return widget

    @staticmethod
    def enterEvent(widget: QWidget, color: str, event):
        """
        Override this method to change border color
        when mouse enter.
        --------------------------------------------
        -> Params
            event: An event which came from PyQt to this method
                   when mouse enters.
        """
        object_name = widget.objectName()
        widget.setStyleSheet(f"""QGroupBox#{object_name} {{
                border-color: {color};
            }}""")

    @staticmethod
    def leaveEvent(widget: QWidget, color: str, event) -> None:
        """
        Override this method to change border color
        when mouse leave.
        --------------------------------------------
        -> Params
            event: An event which came from PyQt to this method
                   when mouse leaves.
        """
        object_name = widget.objectName()
        widget.setStyleSheet(f"""QGroupBox#{object_name} {{
                border-color: {color};
            }}""")

    def mouseMoveEvent(self, e):

        if e.buttons() == Qt.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()
            drag.setMimeData(mime)

            pixmap = QPixmap(self.size())
            self.render(pixmap)
            drag.setPixmap(pixmap)

            drag.exec_(Qt.MoveAction)


class TopLevelWindow(QDialog, WidgetController):
    """
    Top level window sub class of QDialog class
    """

    def __init__(self,
                 layout: object,
                 theme: str = None,
                 **kwargs) -> None:
        super().__init__()
        self.main_layout = layout()
        self.setStyleSheet(theme)
        self.setLayout(self.main_layout)
        window_flags = self.windowFlags() ^ Qt.WindowContextHelpButtonHint
        self.setWindowFlags(window_flags)

    def show_window(self) -> None:
        """
        display commment frame as top window
        """
        self.exec_()

    def change_theme(self, theme: CSS) -> None:
        """
        Change theme of the top level window
        """
        self.setStyleSheet(theme)


class LabelFrame(QGroupBox, WidgetController):
    """
    Custom widget contains a horizontal and vertical layout.
    for fewer code in upper level, each class that
    inherit from this class and add a widget, doesnt
    need to set the widget to layout.setattr of this
    class do this automatically when a attr set to class.
    """

    def __init__(self,
                 layout: object,
                 title: str = None,
                 object_name: str = None,
                 **kwargs):
        """
        params ->
            layout:object
            position:tuple -> using if this widget placed in a grid

        attr ->
            widgets: list
            grid_position: tuple
            main_layout: obj

        """
        super().__init__(**kwargs)
        self.setTitle(title)
        self.main_layout = layout()
        self.setLayout(self.main_layout)
        self.setObjectName(object_name)

    def set_title(self, value: str) -> None:
        """
        Set new title for the frame

        -> Params
            value:str
        """
        self.setTitle(value)


class TopLevel(QDialog):
    """
    Top level window class can be use as popup window.
    """

    def __init__(self, parent: object = None) -> None:
        super().__init__(parent=parent)
        window_flags = self.windowFlags() ^ Qt.WindowContextHelpButtonHint
        self.setWindowFlags(window_flags)


class Toolbar(QToolBar):
    """
    Customized Subclass of Qtoolbar
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setIconSize(QSize(46, 46))

    def contextMenuEvent(self, event: object) -> None:
        """
        override this method to prevent show menu on toolbar
        by right click.
        """
        pass

    def add_button(self,
                   callback_func: callable,
                   icon_path: str,
                   tooltip: str = "",
                   label: str = "") -> None:
        """
        add button to the tool bar
        -> Params:
               label: str
               callback_func
               icon_path
               tooltip
        """
        button = QAction(QIcon(icon_path), label, self)
        button.setToolTip(tooltip)
        button.triggered.connect(callback_func)
        self.addAction(button)
        self.setObjectName("ToolBar")

    def add_widget(self, widget: object) -> None:
        """
        Adds widget to the toolbar
        """
        self.addSeparator()
        self.addWidget(widget)


class Label(QLabel):
    """
    Custom sub class of QLabel
    """

    def __init__(self,
                 label=None,
                 object_name: str = None,
                 grid_positions: tuple = None,
                 *args,
                 **kwargs):
        super().__init__(str(label), *args, **kwargs)
        # self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.setObjectName(object_name)
        self.setAlignment(Qt.AlignCenter)
        self.grid_positions = grid_positions

    def change_text(self, text: str) -> None:
        """
        Change text value of the label
        -> Params:
                text
        """
        try:
            self.setText(text)
        except TypeError:
            self.setText(str(text))

    def get_value(self) -> str:
        """
        Return the label text.

        @return
            str
        """
        return self.text()

    def set_image(self, file_name: str, scale: tuple = (300, 70)) -> None:
        """
        load and display given image file_name inside
        the label
        -> Params:
                filename: image must be inside imgaes folder
        """
        # path = check_image_exists(file_name)
        image = QPixmap(file_name)
        image = image.scaled(*scale,
                             transformMode=Qt.SmoothTransformation)
        self.setPixmap(image)


class Button(QPushButton):
    """
    Custom sub class of PushButton
    """

    def __init__(
        self,
        label: str,
        callback_function: object,
        icon: str = None,
        icon_size: tuple = (20, 20),
        tool_tip: str = None,
        min_width: int = 50,
        width=50,
        object_name: str = None,
        grid_positions: tuple = None,
        **kwargs,
    ):
        super().__init__(label, **kwargs)
        self.setObjectName(object_name)
        self.clicked.connect(callback_function)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        # self.setMinimumWidth(min_width)
        self.setFixedWidth(width)
        self.setToolTip(tool_tip)
        if icon:
            self.setIcon(QIcon(icon))
            self.setIconSize(QSize(*icon_size))
        self.grid_positions = grid_positions


class CheckBox(QCheckBox):
    """
    Custom QtCheckbox widget
    """

    def __init__(self,
                 label: str,
                 callback_func: object = void_function,
                 icon_path: str = None,
                 icon_size: tuple = (15, 15),
                 is_checked: bool = False,
                 object_name: str = None,
                 grid_positions: tuple = None,
                 **kwargs) -> None:
        super().__init__(label, **kwargs)
        self.setChecked(is_checked)
        self.stateChanged.connect(callback_func)
        self.stateChanged.connect(self.on_valid)
        # self.setCheckState(Qt.Checked)
        self.setObjectName(object_name)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setIcon(QIcon(icon_path))
        self.setIconSize(QSize(*icon_size))
        self.grid_positions = grid_positions

    def get_value(self) -> bool:
        """
        return state of the check box
        """
        return self.isChecked()

    def get_state(self) -> bool:
        """
        Return state of the check box
        """
        return self.isChecked()

    def change_state(self, state: int = 2) -> None:
        """
        Change state of the checkbox
        -> Params:
               states: 0 -> unchecked
                       1 -> partially checked
                       2 -> checked
        """
        self.setCheckState(state)
        self.setObjectName("valid")

    def on_valid(self) -> None:
        """
        change the css object name on when is unchecked
        """
        self.setObjectName("valid")

    def on_invalid(self) -> None:
        """
        change the css object name on when is unchecked
        """
        self.setObjectName("invalid")


class ToolbarIconButton(QPushButton):
    """
    Customized QPushButton subclass
    """

    def __init__(
        self,
        label: str = None,
        icon: str = None,
        callback_function: object = None,
        status_tip: str = None,
        **kwargs,
    ):
        super().__init__(label, **kwargs)
        self.clicked.connect(callback_function)
        self.setStatusTip(status_tip)
        self.setIcon(QIcon(icon))
        self.setCursor(QCursor(Qt.PointingHandCursor))
        # self.setObjectName("test")


class DigitValidator:
    """
    Mixing class helper to validato int and float entries
    """

    def get_value(self) -> int:
        """
        Return value of the entry
        """
        try:
            value = self._type(self.text())
            return value
        except (ValueError, TypeError):
            # self.set_value(0)
            return 0

    def validate(self) -> bool:
        """
        Validate this widget
        """
        value = self.text()

        if not value:
            self.on_invalid()
            return "should not be empty."

        if self.not_zero:
            if value == '0' or value == "0.0":
                self.on_invalid()
                return "should not be 0 ."

        self.on_valid()
        return True


class Combobox(QComboBox):
    """
    Custom sub class of Combobox
    -> Params:
          items
          editable
          callback_func
          max_width
          default_item
          validator
    @notes:
         it will create a mapping from the given
         items list to make the searching and setting
         the value easier
    """

    _items_mapping = None

    # TODO: for the future need to find a better way for the
    # widget configs to avoid adding many arguments.
    def __init__(
        self,
        items: list = None,
        editable: bool = True,
        callback_func: object = void_function,
        default_item_index: int = 0,
        default_item: str = None,
        width: int = None,
        min_width: int = None,
        max_width: int = 10000,
        max_length: int = 20,
        tool_tip: str = None,
        validator: object = None,
        value_limit: tuple = None,
        object_name: str = None,
        not_zero: bool = True,
        use_effect: bool = True,
        effect_color: str = "#f89fa2",
        effect_blur_radius: int = 15,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.items = items
        self.editable = editable
        self.setObjectName(object_name)
        self.add_items(items)
        self.setCurrentIndex(default_item_index)
        self.setEditable(editable)
        self.setup_completer()
        self.setToolTip(tool_tip)
        self.currentTextChanged.connect(callback_func)
        self.currentTextChanged.connect(self.on_valid)
        self.setMinimumWidth(min_width)
        self.setMaximumWidth(max_width)
        self.search_set(default_item)
        if width:
            self.setFixedWidth(width)

        if editable:
            self.lineEdit().setAlignment(Qt.AlignCenter)
            self.lineEdit().setMaxLength(max_length)

        if use_effect:
            effect = QGraphicsDropShadowEffect(self)
            effect.setColor(QColor(effect_color))
            effect.setOffset(0, 0)
            effect.setBlurRadius(effect_blur_radius)
            self.setGraphicsEffect(effect)

    def get_items(self) -> list:
        """
        Returns the all items that assigned
        to the combobox.
        """
        return self.items


    def on_invalid(self) -> None:
        """
        When something went wrong in this widget, for example
        user leave the widget empty or add invalid value, then
        change the widget status.
        """
        change_widget_status(self, status="error")

    def on_valid(self) -> None:
        """
        After an error fixed in this widget, this method
        change status of the widget to normal.
        """
        change_widget_status(self, status="normal")

    def _create_mapping(self, items: list) -> None:
        """
        Create a mapping from items, key will be item
        and the value will be index of item
        """
        self._items_mapping = {
            str(value): index
            for index, value in enumerate(items)
        }

    def search_set(self, key: str) -> None:
        """
        search through items mapping if its find
        any match base on given key it will change
        the CurrentIndex
        -> Params:
                key
        """
        try:
            self.setCurrentIndex(self._items_mapping[key])
        except KeyError as error:
            message = f"key {key} not found Can't change current index"
            log(message,
                error=error,
                level=3, 
                color="red")

    def add_items(self, items: list) -> None:
        """
        add items and the callback function to the
        widget
        -> Params:
               items
               callback_func
        """
        try:

            self.clear()
            self._create_mapping(items)
            self.addItems([str(item) for item in items])
        except TypeError as error:
            log(error=error,
                level=2, 
                color="red")

    def set_callbacks(self, *callbacks) -> None:
        """
        Set new callback for the combobox
        """
        for callback in callbacks:
            self.currentTextChanged.connect(callback)

    def get_value(self) -> str:
        """
        Return selected text.
        """
        value = self.currentText()
        return value

    def text(self) -> str:
        """
        return value of the widget. helper
        function for the refactoring code.
        """
        return self.currentText()

    def get_value_index(self) -> int:
        """
        Return selected index.
        """
        return self.currentIndex()

    def setup_completer(self) -> None:
        """
        Setup auto completer for the  combobox.
        it will start give suggestion when text changes inside the
        combobox.
        ------------------------------------------------------------
        QCompleter(attributes):
          setCompletionMode(options):
                              0:PopupCompletion
                                  Current completions are displayed in a popup window.
                              1:InlineCompletion
                                  Completions appear inline (as selected text).
                              2:UnfilteredPopupCompletion
                                  All possible completions are displayed in a popup window
                                  with the most likely suggestion indicated as current.

          setModelSorting(options):
                              0:UnsortedModel
                                  The model is unsorted.
                              1:CaseSensitivelySortedModel
                                  The model is sorted case sensitively.
                              2:CaseInsensitivelySortedMode
                                  The model is sorted case insensitively.

        ----------------------------------------------------------------
        QSortFilterProxyModel can be used for sorting items, filtering out items, or both.
        The model transforms the structure of a source model by mapping the model indexes
        it supplies to new indexes, corresponding to different locations, for views to use.
        This approach allows a given source model to be restructured as far as views are
        concerned without requiring any transformations on the underlying data,
        and without duplicating the data in memory.
        """
        # added to pervemt qt error log
        # Setting a QCompleter on non-editable QComboBox is not allowed.
        # TODO: need to be tested
        if not self.editable:
            return
        filter_model = QSortFilterProxyModel(self)
        filter_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        # filter_model.fil
        filter_model.setSourceModel(self.model())
        completer = QCompleter(filter_model, self)
        completer.setCompletionMode(QCompleter.PopupCompletion)
        completer.setCaseSensitivity(2)
        self.setCompleter(completer)

    def mousePressEvent(self, event) -> None:
        """
        Make widget valid when user click on it
        """
        self.on_valid()
        return super().mousePressEvent(event)


class StringCombobox(Combobox):
    """
    This class is e Combobox class with string validators
    and string validation.
    """

    def __init__(self, validator: str = "string", **kwargs) -> None:
        super().__init__(**kwargs)
        self.currentTextChanged.connect(self.validate)
        self.set_validator(validator)

    def set_validator(self, validator: str) -> None:
        """
        Set validator to widget based on QIntValidator.
        @args
            value_limit:tuple
        """
        self.setValidator(RegxpValidator(pattern=VALIDATORS[validator]))

    def validate(self) -> bool:
        """
        Validate this widget
        """

        value = self.currentText()
        if not value:
            self.on_invalid()
            return "should not be empty."

        if value[-1] == ",":
            self.on_invalid()
            return "should not ends with ',' sign."
        self.on_valid()
        return True


class DigitCombobox(DigitValidator, Combobox):
    """
    Mixing class of DigitValidator and Combobox
    to validate value of the widget(int, float)
    """

    def __init__(self, value_type: object, **kwargs) -> None:
        super().__init__(**kwargs)
        self.currentTextChanged.connect(self.validate)
        self._type = value_type
        self.not_zero = kwargs["not_zero"]


class IntCombobox(DigitCombobox):
    """
    Int Combobox will validate and return int value type
    """

    def __init__(self, value_limit: list, **kwargs) -> None:
        super().__init__(value_type=int, **kwargs)
        self.setValidator(IntValidator(value_limit[0], value_limit[1]))


class FloatCombobox(DigitCombobox):
    """
    Float Combobox will validate and return float value
    """

    def __init__(self, value_limit: list, **kwargs) -> None:
        super().__init__(value_type=float, **kwargs)
        self.setValidator(
            DoubleValidator(float(value_limit[0]), float(value_limit[1]), 20,
                            self))


class LabelCombobox(Frame):
    """
    A custom widget class contains a label and a combobox.
    params ->
            label:str
            items:list
                 -> meta value used when the actual selected
                    value is different than the displayed one
            editable:bool
            callback_func -> object
            default_item
            status_tip
            layout
            max_width
            validator
            validate
    Note:
        comboboxes should have initial items like empty list
        for binding the currentTextChange callback,if items are
        None, callback function will never work!!!!!!!!
    """

    widget_type = {
        "string": StringCombobox,
        "uppercase_string": StringCombobox,
        "int": IntCombobox,
        "decimal": FloatCombobox
    }

    def __init__(
        self,
        label: str,
        layout: object = Vertical,
        items: list = [],
        editable: bool = True,
        default_item_index: int = 0,
        default_item: str = None,
        status_tip: str = None,
        callback_func: object = void_function,
        width: int = None,
        min_width: int = 80,
        max_width: int = 10000,
        frame_width: int = 0,
        max_length: int = 20,
        value_limit: tuple = (0, 2147483647),
        validator: str = None,
        grid_positions: tuple = None,
        tool_tip: str = None,
        object_name: str = None,
        not_zero: bool = None,
        align_center:bool = False,
        use_effect: bool = True,
        effect_color: str = "#f89fa2",
        effect_blur_radius: int = 15,
        **kwargs,
    ):
        super().__init__(layout=layout, **kwargs)
        self.setStatusTip(status_tip)
        self.grid_positions = grid_positions
        self.setObjectName(object_name)
        self.label = Label(label=label)
        self.label.setAlignment(Qt.AlignCenter)
        if align_center:
            self.main_layout.setAlignment(Qt.AlignCenter)

        self.combobox = self.widget_type.get(validator, Combobox)(
            min_width=min_width,
            max_width=max_width,
            width=width,
            max_length=max_length,
            value_limit=value_limit,
            items=items,
            editable=editable,
            callback_func=callback_func,
            default_item_index=default_item_index,
            default_item=default_item,
            validator=validator,
            tool_tip=tool_tip,
            object_name=object_name,
            not_zero=not_zero,
            use_effect=use_effect,
            effect_color=effect_color,
            effect_blur_radius=effect_blur_radius)
        if frame_width:
            self.setFixedWidth(frame_width)
    
    def get_items(self) -> list:
        """
        Returns the combobox all items.
        """
        return self.combobox.get_items()

    def on_invalid(self) -> None:
        """
        When something went wrong in this widget, for example
        user leave the widget empty or add invalid value, then
        change the widget status.
        """
        self.combobox.on_invalid()

    def on_valid(self) -> None:
        """
        After an error fixed in this widget, this method
        change status of the widget to normal.
        """
        self.combobox.on_valid()

    def set_editable(self, editable: bool) -> None:
        """
        Change editable of the combobox
        """
        self.combobox.setEditable(editable)

    def set_callbacks(self, *callbacks) -> None:
        """
        Set new callback for the combobox
        """
        self.combobox.set_callbacks(*callbacks)

    def clear_value(self) -> None:
        """
        Clear selected value
        """
        self.combobox.setCurrentIndex(0)

    def clear_items(self) -> None:
        self.combobox.clear()

    def set_value(self, value: str, index: int = 0) -> None:
        """
        Insert new value to item list of combobox
        -> Params:
               value
               index: default is 0
        """
        self.combobox.setItemText(index, value)
        self.combobox.setCurrentIndex(0)

    def search_set(self, value: str) -> None:
        """
        Automatically set index of the combobbox base on the
        given value.the mapping of the value will be carated
        during the class initialization
        ----------------------------------------------
        -> Params:
                value
        """
        self.combobox.search_set(value)

    def set_exists(self, value: str) -> None:
        """
        Search trough combobox items and change
        the index of combobox if the value is
        inside the items list
        -> Params:
              value: str
        """
        self.combobox.search_set(value)

    def add_items(self, items: list) -> None:
        """
        -> Params:
                 items: list of items (all elements must be string)
        # todo add convert to string functionalty
        # to automatically convert all data types to string
        """
        self.combobox.add_items(items)

    def get_value(self) -> str:
        """
        Return combobox value
        """
        return self.combobox.get_value()

    def get_value_index(self) -> int:
        """
        Return selected index.
        """
        return self.combobox.currentIndex()

    def validate(self) -> bool:
        """
        Validate the combobox
        """

        return self.combobox.validate()

    def set_validate_method(self, method: callable) -> None:
        """
        Set new validate method
        """
        self.combobox.validate = method


class Entry(QLineEdit):
    """
    Customized QLineEdit Subclass
    -> Params:
          tool_tip
          validator: QtValidator
          widths

    @note:
         default event handler is on textChaged

    """

    def __init__(
        self,
        tool_tip: str = None,
        callback_func: object = void_function,
        default_value: str = "",
        place_holder: str = None,
        max_length: int = 50,
        width: int = 0,
        min_width: int = 0,
        max_width: int = 0,
        editable: bool = True,
        is_enable: bool = True,
        is_upper: bool = False,
        object_name: str = None,
        validator: str = None,
        value_limit: tuple = None,
        focus_out_callback: object = void_function,
        key_press_callback: callable = void_function,
        not_zero: bool = None,
        is_password: bool = False,
        grid_positions: tuple = None,
        use_effect: bool = True,
        effect_color: str = "#f89fa2",
        effect_blur_radius: int = 10,
                **kwargs,
            ):
        super().__init__(**kwargs)
        self.setObjectName(object_name)
        self.setToolTip(tool_tip)
        self.setAlignment(Qt.AlignCenter)
        self.setEnabled(is_enable)
        self.setMaxLength(max_length)
        self.setEnabled(editable)
        self.setPlaceholderText(place_holder)
        self.set_value(default_value)
        self.textChanged.connect(callback_func)
        if min_width:
            self.setMinimumWidth(min_width)
        if max_width:
            self.setMaximumWidth(max_width)
        if width:
            self.setFixedWidth(width)
        if is_upper:
            self.textChanged.connect(self.set_upper)
        if is_password:
            self.setEchoMode(QLineEdit.Password)
        self.focus_out_callback = focus_out_callback
        self.key_press_callback = key_press_callback
        self.grid_positions = grid_positions
        if use_effect:
            effect = QGraphicsDropShadowEffect(self)
            effect.setColor(QColor(effect_color))
            effect.setOffset(0, 0)
            effect.setBlurRadius(effect_blur_radius)
            self.setGraphicsEffect(effect)

    def set_callbacks(self, *callbacks) -> None:
        """
        Set new callback to the entry.

        @args
            callback:object
        """
        for callback in callbacks:
            self.textChanged.connect(callback)

    def set_upper(self) -> None:
        """
        Force the user input to be uppercase.
        """
        self.setText(self.text().upper())

    def on_invalid(self) -> None:
        """
        When something went wrong in this widget, for example
        user leave the widget empty or add invalid value, then
        change the widget status.
        """
        change_widget_status(self, status="error")

    def on_valid(self) -> None:
        """
        After an error fixed in this widget, this method
        change status of the widget to normal.
        """
        change_widget_status(self, status="normal")

    def get_value(self) -> str:
        """
        Get entry text.
        """
        value = self.text()
        return value

    def set_value(self, text: str) -> None:
        """
        Add text to entry.
        """
        try:
            self.setText(text)
        except TypeError:
            self.setText(str(text))

    def clear_value(self) -> None:
        """
        Clear the textbox value
        """
        self.clear()

    def focusOutEvent(self, event) -> None:
        self.focus_out_callback()
        return super().focusOutEvent(event)

    def keyPressEvent(self, event) -> None:
        if event.key() == Qt.Key_Return:
            self.key_press_callback(self.text())
        return super().keyPressEvent(event)

    def mousePressEvent(self, event) -> None:
        """
        Make widget valid when user click on it
        """
        self.on_valid()
        return super().mousePressEvent(event)


class StringEntry(Entry):
    """
    This class is e Entry class with string validators
    and string validation.
    """

    def __init__(self, validator: str = "string", **kwargs) -> None:
        super().__init__(**kwargs)
        self.textChanged.connect(self.validate)
        self.set_validator(validator)

    def set_validator(self, validator: str) -> None:
        """
        Set validator to widget based on QIntValidator.
        @args
            value_limit:tuple
        """
        self.setValidator(RegxpValidator(pattern=VALIDATORS[validator]))

    def validate(self) -> bool:
        """
        Validate this widget
        """

        value = self.text()
        if not value:
            self.on_invalid()
            return "should not be empty."

        if value[-1] == ",":
            self.on_invalid()
            return "should not ends with ',' sign."

        self.on_valid()
        return True


class DigitEntry(DigitValidator, Entry):
    """
    Mixing class of DigitValidator and Entry widget
    """

    def __init__(self, value_type: object, **kwargs) -> None:
        super().__init__(**kwargs)
        self.textChanged.connect(self.validate)
        self._type = value_type
        self.not_zero = kwargs["not_zero"]


class IntEntry(DigitEntry):
    """
    IntEntry will accept and return int value
    """

    def __init__(self, value_limit: tuple, **kwargs) -> None:
        super().__init__(value_type=int, **kwargs)
        self.setValidator(IntValidator(value_limit[0], value_limit[1]))


class FloatEntry(DigitEntry):
    """
    Float Entry will accept and return float value
    """

    def __init__(self, value_limit: tuple, **kwargs) -> None:
        super().__init__(value_type=float, **kwargs)
        self.setValidator(
            DoubleValidator(float(value_limit[0]), float(value_limit[1]), 20,
                            self))


class LabelEntry(Frame):
    """
    Labeled Entry .is a frame contains entry
    with label
    -> Params:
          label
          tooltip
          layout: QBOXLAYOUT
          width
          place_hodler
          callback_func: default is void_function function
          **kwargs
    """

    widget_type = {
        "string": StringEntry,
        "email": StringEntry,
        "username": StringEntry,
        "uppercase_string": StringEntry,
        "section_names": StringEntry,
        "string_with_hiphen": StringEntry,
        "string_multiple_int": StringEntry,
        "section_name_pattern": StringEntry,
        "int": IntEntry,
        "decimal": FloatEntry
    }

    #TODO: we taking to many argument, need to refactor again,
    # for example 99% of the entry not going to use is_password flag or 
    # value limit because their type is string.
    def __init__(
        self,
        label: str,
        tool_tip: str = None,
        layout: object = Vertical,
        default_value: str = "",
        max_length: int = 20,
        validator: str = None,
        callback_func: object = void_function,
        width: int = None,
        min_width: int = 0,
        max_width: int = 0,
        frame_width:int= 0,
        place_holder: str = None,
        editable: bool = True,
        object_name: str = None,
        label_object_name: str = None,
        is_upper: bool = False,
        grid_positions: tuple = None,
        value_limit: tuple = (0, 2147483647),
        focus_out_callback: object = void_function,
        key_press_callback: callable = void_function,
        not_zero: bool = None,
        is_password: bool = False,
        align_center: bool = False,
        use_effect: bool = True,
        effect_color: str = "#f89fa2",
        effect_blur_radius: int = 15,
        **kwargs,
    ):
        super().__init__(layout, **kwargs)
        self.label = Label(label, object_name=label_object_name)
        self.label.setAlignment(Qt.AlignCenter)
        if align_center:
            self.main_layout.setAlignment(Qt.AlignCenter)
        self.entry = self.widget_type.get(validator, Entry)(
            width=width,
            min_width=min_width,
            max_width=max_width,
            tool_tip=tool_tip,
            validator=validator,
            default_value=default_value,
            callback_func=callback_func,
            place_holder=place_holder,
            editable=editable,
            max_length=max_length,
            object_name=object_name,
            value_limit=value_limit,
            focus_out_callback=focus_out_callback,
            key_press_callback=key_press_callback,
            is_upper=is_upper,
            not_zero=not_zero,
            is_password=is_password,
            use_effect=use_effect,
            effect_color=effect_color,
            effect_blur_radius=effect_blur_radius)
        self.grid_positions = grid_positions
        if frame_width:
            self.setFixedWidth(frame_width)
    def on_invalid(self) -> None:
        """
        When something went wrong in this widget, for example
        user leave the widget empty or add invalid value, then
        change the widget status.
        """
        self.entry.on_invalid()

    def on_valid(self) -> None:
        """
        After an error fixed in this widget, this method
        change status of the widget to normal.
        """
        self.entry.on_valid()

    def get_value(self) -> object:
        """
        return value of the entry
        """
        return self.entry.get_value()

    def set_value(self, value: str) -> None:
        """
        Set value of the entry
        """
        self.entry.set_value(value)

    def clear_value(self) -> None:
        """
        Clear value of the entry
        """
        self.entry.clear()

    def validate(self) -> bool:
        """
        Validate the entry
        """
        return self.entry.validate()

    def set_validator(self, validator: str) -> None:
        """
        Change validator of the entry.
        ------------------------------------------------
        -> Params
            validator: str
        """
        self.entry.set_validator(validator)

    def set_callbacks(self, *callbacks) -> None:
        """
        Connect a callback to the entry
        ------------------------------------------------
        -> Params
            callbacks: function, method
        """
        self.entry.set_callbacks(*callbacks)

    def disconnect_callbacks(self) -> None:
        """
        Disconnect all entry's callback.
        """
        self.entry.disconnect()


class RadioButton(QRadioButton):
    """
    Custom sub class of RadioButton
    """

    def __init__(self, label: str, status_tip: str = None, **kwargs):
        super().__init__(label, **kwargs)
        self.setStatusTip(status_tip)
        self.is_widget = True


class TextBox(QTextEdit):
    """
    Customized QTextEdit Subclass
    """

    def __init__(self,
                 text: str = "",
                 max_length: int = None,
                 object_name: str = None,
                 is_readonly: bool = False,
                 validator: str = None,
                 width: int = None,
                 height: int = None,
                 grid_positions: tuple = None,
                 **kwargs):
        super().__init__(**kwargs)
        # disabled drag and drop
        # self.setAcceptDrops(False)
        self.grid_positions = grid_positions
        self.setObjectName(object_name)
        self.setPlainText(text)
        self.setReadOnly(is_readonly)
        if max_length:
            self.textChanged.connect(lambda: self.check_length(max_length))
        if validator:
            self.textChanged.connect(lambda: self.validate_callback(validator))
        if height:
            self.setFixedHeight(height)
        if width:
            self.setFixedWidth(width)

    def check_length(self, max_length: int) -> None:
        """
        QTextEdit has not method for adding max length, So
        this method do the max length job and prevent user to
        type more than max_length value.

        @args
            max_length:int
        """
        text = self.toPlainText()
        cursor = self.textCursor()
        if len(text) > max_length:
            self.setPlainText(text[0:-1])
            self.setTextCursor(cursor)

    def validate_callback(self, validator: str) -> None:
        """
        Validator for checking user input
        """
        text = self.toPlainText()
        try:
            last_char = text[-1]
            pattern = VALIDATORS[validator]
            result = re.findall(pattern, last_char)
            if not result:
                cursor = self.textCursor()
                self.setPlainText(text[0:-1])
                self.setTextCursor(cursor)
        except IndexError as error:
            log(error=error,
                level=2, 
                color="red")

    def get_value(self) -> str:
        """
        Get textbox value.
        """
        return self.toPlainText()

    def add_text(self, text: str) -> None:
        """
        Add text to text box
        -> Params:
                text
        """
        self.setPlainText(text)

    def clear_value(self) -> None:
        """
        Remove all the text inside th widget
        """
        self.clear()


class ScrollArea(QScrollArea):
    """
    Custom QScrollArea
    """

    def __init__(self,
                 child: object = None,
                 object_name: str = None,
                 **kwargs):
        super().__init__(**kwargs)

        self.setWidgetResizable(True)
        self.setObjectName(object_name)
        # self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        if child:
            self.setWidget(child)

    def set_widget(self, child: object) -> None:
        """
        Set child for scroll area
        """
        self.setWidget(child)

    def get_widget(self) -> object:
        """
        return child widget
        """
        return self.widget()

    def validate_widgets(self) -> bool:
        """
        validate child widgets
        """
        return self.child.validate_widgets()


class Menu(QMenu):
    """
    This class is subclass of QMenu
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def add_action(self, icon_path: str, title: str,
                   callback_func: object) -> None:
        """
        Adds new action to the menu.

        @args
            icon_path:str
            title:str
            handler:object(method)
        """
        action = QAction(QIcon(icon_path), title, self)
        action.triggered.connect(callback_func)
        self.addAction(action)


class Table(QTableWidget):
    """
    Custom subclass from QTablewidget
    -> Params:
           headers: table header
           current_row
    """

    # horiznotalheadr
    H_HEADER = None
    # veticalHeader
    V_HEADER = None

    def __init__(self,
                 min_width: int = 600,
                 min_height: int = 200,
                 editable:bool=False,
                 table_number: int = 0,
                 selection_mode: object = QTableWidget.SingleSelection,
                 double_click_callback: callable = None,
                 **kwargs) -> None:

        super().__init__(**kwargs)
        edit_trigger=QTableWidget.NoEditTriggers
        if editable:
            edit_trigger=QTableWidget.DoubleClicked
        self.configure(edit_trigger=edit_trigger,
                       selection_mode=selection_mode)
        self.setMinimumSize(min_width, min_height)
        self.sizeIncrement()
        self.menu = Menu()
        self.table_number = table_number
        if double_click_callback:
            self.doubleClicked.connect(double_click_callback)

    def contextMenuEvent(self, event) -> None:
        """
        Overriting this method for showing a context menu
        by right click of the mouse on each row.
        """
        if self.currentRow() > -1:
            # A row is selected
            self.menu.popup(QCursor.pos())

    def configure(self,
                  edit_trigger: object = QTableWidget.NoEditTriggers,
                  selection_mode: object = QTableWidget.SingleSelection,
                  selection_behavior: object = QTableWidget.SelectRows,
                  ) -> None:
        """
        Change config of the widget, config object can be from
        QtableWidget or QAbstractItemView
        -------------------------------------------------------
        -> Params:
                 current_row
                 edit_trigger: Qt Triger object default is QTableWidget.DoubleClicked
                                (to make it ready only set edit_trigger to QTableWidget.NoEditTriggers)
                 selection_mode: Qt selection mode object default is SingleSelection
                 selection_behavior: Qt selection behavior default is SelectRows

        """
        self.setEditTriggers(edit_trigger)
        self.setSelectionMode(selection_mode)
        self.setSelectionBehavior(selection_behavior)
        self.setCurrentCell(0, 0)

    def get_headers(self) -> tuple:
        """
        Return the headers items
        """
        if self.H_HEADER:
            return self.H_HEADER
        return self.V_HEADER

    def is_vertical(self) -> bool:
        """
        Return the table type
        """
        if not self.H_HEADER:
            return True
        return False

    def _convert_item(self, item: str) -> type:
        """
        This method calls from _item_getter() to convert
        the data to its corresponding type.

        @return
            str, float, int
        """
        try:
            return int(item)
        except ValueError:
            try:
                return float(item)
            except ValueError:
                return item

    def _item_getter(self,
                     row: int,
                     column: int,
                     validate: bool = False) -> type:
        """
        This method calls from get_row() method to return an item from
        a row. If validator set to True, it will convert the item to its
        specific type.

        @args
            row: int
            column: int
            validator: bool
        @return
            type(str, float, int)
        """
        try:
            item = self.item(row, column).text()
        except AttributeError:
            raise TableCellNotFoundError(
                f"Couldn't find the item in row {row} and column {column}.")
        if validate:
            item = self._convert_item(item)
        return item

    def convert_before_insert(self, data: list) -> list:
        """
        Convert data from list of non-dict items to
        a list of a dict for inserting into the table.
        ----------------------------------------------
        -> Params
            data: list -> [3, "something", 55,5, "another_something"]
        <- Return
            list of a dict -> [{1:3, 2:"something", 3:55.5, 4:"another_something"}]
        """
        return [{index: i for index, i in enumerate(data)}]


class HorizontalTable(Table):

    def __init__(self,
                 min_width: int = 600,
                 min_height: int = 200,
                 table_number: int = 0,
                 object_name: str = None,
                 selection_mode: object = QTableWidget.SingleSelection,
                 editable:bool=False,
                 edit_callback: callable = None,
                 double_click_callback: callable = None,
                 grid_positions: tuple = None) -> None:
        super().__init__(min_width=min_width,
                         min_height=min_height,
                         selection_mode=selection_mode,
                         editable=editable,
                         double_click_callback=double_click_callback)
        self.setObjectName(object_name)
        self.table_number = table_number
        self.grid_positions = grid_positions
        if editable:
            self.set_callback(edit_callback)

    def set_callback(self, callback: callable) -> None:
        """
        Set callback for cellChange
        """
        if callback:
            self.cellChanged.connect(
                lambda x: callback(x, self.table_number))

    def setup_view(self,
                   h_headers: list = None,
                   row_count: int = 0,
                   column_count: int = 0,
                   has_width: list = None) -> None:
        """
        Setup table info such as number of rows
        and columns and cells view type.
        """
        self.setColumnCount(column_count)
        self.setRowCount(row_count)
        self.setHorizontalHeaderLabels(h_headers)
        self.H_HEADER = tuple(h_headers)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        if not has_width:
            self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def insert_row(self, 
                   data: list,
                   width: Any,
                   row: int = 0) -> None:
        """
        insert the given data row by row, it will clear
        previous inserted data on new insert calls
        -> Params:
                data
                row: row number default is 0
        """
        c_count = self.columnCount()
        for value, column in zip(data, range(c_count)):
            if width:
                try:
                    self.setColumnWidth(column, width[column])
                except TypeError:
                    self.setColumnWidth(column, width)
                except IndexError:
                    pass
            item = QTableWidgetItem(str(value))
            self.setItem(row, column, item)

    def insert_data(self,
                    headers: list,
                    data: list,
                    width: Union[list, int] = None) -> None:
        """
        Insert data into the table.
        ----------------------------------------------
        -> Params
            data: list of dicts
            width: list or int
        """
        self.clear_value()
        self.horizontalHeader().show()
        if not isinstance(data[0], dict):
            data = self.convert_before_insert(data)
        self.setup_view(h_headers=headers,
                        row_count=len(data),
                        column_count=len(headers),
                        has_width=width)
        for row_index, document in enumerate(data):
            value = list(document.values())
            self.insert_row(data=value,
                            width=width,
                            row=row_index)

    def insert_new_row(self, data: tuple) -> None:
        """
        Insert new row to the end of the rows.

        @args
            data:list
        """
        self.setRowCount(self.rowCount() + 1)
        last_row = self.rowCount() - 1
        for col in range(self.columnCount()):
            self.setItem(last_row, col, QTableWidgetItem(data[col]))

    def get_row(self, row: int, validator: bool = False) -> tuple:
        """
        return all the column of the given row as tuple
        ----------------------------------------------
        -> Params:
                row: row number
        """

        # total number of columns for iteration
        try:
            total_column = self.columnCount()
            row = [
                self._item_getter(row, column, validator)
                for column in range(0, total_column)
            ]
            return tuple(row)
        except AttributeError as error:
            max_row = self.rowCount()
            raise RowNotExists(
                f"given row number is invalid, can't be higher than {max_row}"
            ) from error

    def row_as_dict(self, row: int, validator: bool = False) -> dict:
        """
        Return value of the given row as dict by mapping
        the row value with the horizontal header
        -----------------------------------------------
        -> Params:
                row: row number
        """
        row = self.get_row(row, validator)
        value = zip(self.H_HEADER, row)
        return dict(value)

    def get_values(self, validator: bool = False) -> list:
        """
        Return value of the all the rows
        """
        total_rows = self.rowCount()
        if total_rows:
            return [
                self.row_as_dict(row, validator) for row in range(0, total_rows)
            ]

    def get_selected_row(self) -> dict:
        """
        Return selected row.
        """
        row = self.currentRow()
        return {**self.row_as_dict(row), "index": row}

    def get_selected_items(self) -> iter:
        """
        Return all selected cells.
        """
        for cell in self.selectedItems():
            yield cell.text()

    def get_selected_rows(self) -> iter:
        """
        Return selected rows when selection
        mode is multiple.
        -----------------------------------
        <- Return
            Generator
        """
        columns_count = self.columnCount()
        items = tuple(self.get_selected_items())
        for index, _ in enumerate(items):
            if index % columns_count == 0:
                yield dict(zip(self.H_HEADER, items[index:index+columns_count]))

    def clear_value(self) -> None:
        """
        Clear the table
        """
        self.horizontalHeader().hide()
        self.clear()


class VerticalTable(Table):

    def __init__(self,
                 min_width: int = 600,
                 min_height: int = 200,
                 editable:bool=False,
                 selection_mode: object = QTableWidget.SingleSelection) -> None:
        super().__init__(min_width=min_width,
                         min_height=min_height,
                         editable=editable,
                         selection_mode=selection_mode)

    def setup_view(self,
                   v_headers: list = None,
                   row_count: int = 0,
                   column_count: int = 0,
                   has_width: list = None) -> None:
        """
        Setup table info such as number of rows
        and columns and cells view type.
        """
        self.setColumnCount(column_count)
        self.setRowCount(row_count)
        self.setVerticalHeaderLabels(v_headers)
        self.V_HEADER = tuple(v_headers)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.horizontalHeader().hide()

        if not has_width:
            self.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def insert_column(self, data: list, width: Any, column: int = 0) -> None:
        """
        Insert the given data into the table when table is in horizontal
        view.
        """
        r_count = self.rowCount()
        for row in range(r_count):
            self.setItem(row, column, QTableWidgetItem(str(data[row])))
            if width:
                try:
                    self.setColumnWidth(row, width[row])
                except TypeError:
                    self.setColumnWidth(row, width)
                except IndexError:
                    self.setColumnWidth(row, width[0])

    def insert_data(self,
                    data: list,
                    width: Union[list, int] = None,
                    is_headless: bool = False) -> None:
        """
        Insert data into the table.
        ----------------------------------------------
        -> Params
            data: list of dicts
            width: list or int
        """
        self.clear()
        self.verticalHeader().show()
        if not isinstance(data[0], dict):
            data = self.convert_before_insert(data)
        v_headers = list(map(lambda x: str(x), data[0].keys()))
        self.setup_view(v_headers=v_headers,
                        row_count=len(v_headers),
                        column_count=len(data),
                        has_width=width)
        for column_index, document in enumerate(data):
            value = list(document.values())
            self.insert_column(data=value,
                               width=width,
                               column=column_index)
        if is_headless:
            self.verticalHeader().hide()

    def get_values(self) -> dict:
        """
        Collect the data in the table and converts
        it to a dict and return it.
        """
        total_rows = self.rowCount()
        if total_rows:
            data = (
                self._item_getter(i, 0, validate=True) for i in range(total_rows)
            )
            return [dict(zip(self.V_HEADER, data))]


class ListBox(QListWidget):
    """
    Custom subclass of QList Widget
    -> Params:
           items: list of the items
           callback_func
    """

    def __init__(self,
                 items: list,
                 callback_func: object = None,
                 width: int = None,
                 object_name: str = None,
                 grid_positions: tuple = None,
                 is_enable: bool = True,
                 **kw):
        super().__init__(**kw)
        self.add_item(items)
        self.clicked.connect(callback_func)
        self.setObjectName(object_name)
        if width:
            self.setFixedWidth(width)
        self.setEnabled(is_enable)
        self.grid_positions = grid_positions

    def add_item(self, items: list) -> None:
        """
        add items to the list box
        -> Params:
                items
        """
        self.clear()
        for item in items:
            self.addItem(str(item))

    def set_callback(self, *callbacks) -> None:
        """
        Set new callback for the listbox
        """
        for callback in callbacks:
            self.clicked.connect(callback)

    def get_value(self) -> Any:
        """
        Return value of the selected  item
        """
        try:
            return self.currentItem().text()
        except AttributeError as e:
            return None

    def clear_value(self) -> None:
        """
        Clear the listbox values
        """
        self.clear()

    def set_item(self, index: int) -> None:
        """
        Set the current selected item by index.
        """
        self.setCurrentRow(index)

    def set_current_row(self, row) -> None:
        """
        Set the current row of the listbox.

        @args:
            row:int
        """
        self.setCurrentRow(row)

    def set_enable(self, is_enable: bool) -> None:
        """
        Enable/Disable the listbox
        """
        self.setEnabled(is_enable)

    def unselect(self) -> None:
        """
        Unselect the listbox items
        """
        for i in range(self.count()):
            item = self.item(i)
            item.setSelected(False)


class TabBook(QTabWidget):
    """
    Sub class of QTabWidget.
    """

    def __init__(self, 
                 object_name: str = None,
                 grid_positions: tuple = None, 
                 **kwargs) -> None:
        super().__init__(**kwargs)
        self.setObjectName(object_name)
        self.grid_positions = grid_positions
        self.tabBar().setObjectName(object_name)
        # self.setTabPosition(QTabWidget.West)
        # self.setDocumentMode(True)
        # self.setTabShape(QTabWidget.Triangular)
        # self.setTabsClosable(True)
        self.setMovable(True)
        # self.tabCloseRequested.connect(lambda index: self.removeTab(index))
        # self.setStyleSheet("QTabBar::tab { min-width: 150px; }")


class NotificationMessage(Frame):

    status_colors = {
        "normal": "rgba(0  , 83 , 120, 1)",  # Dark Blue
        "success": "rgba(2  , 120, 0  , 1)",  # Green
        "low": "rgba(225, 92 , 0  , 1)",  # Orange
        "medium": "rgba(76 , 0  , 115, 1)",  # Purple
        "high": "rgba(200, 0  , 53 , 1)",  # Red
    }

    def __init__(self, message: str, critical_level: str,
                 remove_callback: object, **kwargs) -> None:
        super().__init__(layout=Vertical, **kwargs)
        self.setObjectName("notification_message")
        self.frame_height = len(message) / 0.95 if len(message) > 150 else 160
        self.setFixedHeight(self.frame_height)
        color = self.status_colors[critical_level]
        self.setStyleSheet(f"background-color:{color};")

        self.message = TextBox(text=message,
                               object_name="notification_message",
                               max_length=500,
                               is_readonly=True)
        self.message.setStyleSheet(f"background-color:transparent;")

        self.progress = Label("", object_name="notification_progress")
        self.progress.setStyleSheet(f"background-color:white;")
        self.progress.setGeometry(0, 0, 10, 0)

        self.remove_callback = remove_callback
        self.setup_animations()

    def setup_animations(self) -> None:
        """
        Setup Animations for this frame.
        """
        self.progress_animation = QPropertyAnimation(
            targetObject=self.progress,
            propertyName=b'geometry',
            startValue=QRect(0, self.frame_height - 40, 0, 10),
            endValue=QRect(0, self.frame_height - 40, 350, 10),
            duration=3500)

        self.effect = QGraphicsOpacityEffect(self, opacity=1.0)
        self.setGraphicsEffect(self.effect)
        self.opacity_animation = QPropertyAnimation(targetObject=self.effect,
                                                    propertyName=b'opacity',
                                                    startValue=1.0,
                                                    endValue=0.0,
                                                    duration=3500)
        self.opacity_animation.setKeyValueAt(0.75, 1)

        self.progress_animation.finished.connect(self.remove_callback)
        self.progress_animation.start()
        self.opacity_animation.start()


class NotificationFrame(Frame):

    def __init__(self, notificationbox_callback: callable, **kwargs) -> None:
        super().__init__(layout=Vertical, **kwargs)
        self.setObjectName("notification")
        self.notificationbox_callback = notificationbox_callback
        self.message_count = 0

    def enterEvent(self, a0) -> None:
        """
        When mouse enters this frame, it will
        pause all NotificationMessage animations.
        It helps user to read the message.
        """
        for _, widget in self.widgets:
            widget.progress_animation.pause()
            widget.opacity_animation.pause()
        return super().enterEvent(a0)

    def leaveEvent(self, a0) -> None:
        """
        When mouse leave this frame, it will
        resume all NotificationMessage animations.
        """
        for _, widget in self.widgets:
            widget.progress_animation.resume()
            widget.opacity_animation.resume()
        return super().leaveEvent(a0)

    def mousePressEvent(self, a0) -> None:
        """
        When user click in this frame, it will
        remove all notifications.
        """
        self.remove_all_widgets()
        self.notificationbox_callback(True)  # setHidden(True)
        return super().mousePressEvent(a0)

    def add_message(self, message: str, critical_level: str) -> None:
        """
        Adds new Message to Notification Frame.

        -> Params
            message:str
            critical_level:str
        """
        self.message_count += 1
        setattr(
            self, f"message{self.message_count}",
            NotificationMessage(message=message,
                                critical_level=critical_level,
                                remove_callback=self.remove_message))

    def remove_message(self) -> None:
        """
        Remove a NotificationMessage and checks if
        there is no message, then call the NotificationBox
        callback to set it hidden
        """
        self.remove_widget(0)
        if not self.widgets:
            self.notificationbox_callback(True)  # setHidden(True)


class FloatingNotification(Frame):

    def __init__(self, parent: object, **kwargs) -> None:
        super().__init__(layout=Vertical, parent=parent, **kwargs)
        self.setFixedSize(440, 800)
        self.setObjectName("notification")
        self.setHidden(True)
        self.scrollarea = ScrollArea(object_name="notification")
        self.scrollarea.verticalScrollBar()
        self.scrollarea.set_widget(NotificationFrame(self.setHidden))

    def show_message(self, message: str, critical_level: str = "high") -> None:
        """
        Add new message to NotificationFrame
        -> Params
            message:str
            critical_level:str
        """
        self.setHidden(False)
        notification_frame = self.scrollarea.get_widget()
        notification_frame.add_message(str(message), critical_level)


class NotificationBar(QStatusBar):

    status_colors = {
        "normal": "#005378",  # Dark Blue
        "success": "#026100",  # Green
        "low": "#D35C00",  # Orange
        "medium": "#4C0073",  # Purple
        "high": "#D90035",  # Red
    }

    def __init__(self) -> None:
        super().__init__()

        self.message = Label(label="App Message",
                             object_name="notificationbar")
        self.addWidget(self.message)
        self.setup_animations()

    def logger(self, message: str) -> None:
        """
        Write errors on a csv file.

        @args
            message:str
        """
        date = datetime.now().strftime("%Y-%m-%d")
        time = datetime.now().strftime("%H:%M:%S")
        row = [date, time, message]

        with open("./lib/log/log.csv", "a") as f:
            csvwriter = csv.writer(f)
            csvwriter.writerow(row)

    def mousePressEvent(self, event) -> None:
        """
        When user clicked on Notificationbar, this method
        will remove the current message and change the status color
        to normall.
        """
        self._message_out_configs()
        self.color_animation.setLoopCount(1)
        self.message_out_position_animation.finished.connect(
            lambda: self.message.change_text(""))

        self.message_out_position_animation.start()
        self.color_animation.start()
        self.color_animation.finished.connect(
            lambda: self.color_animation.setLoopCount(7))

    def setup_animations(self) -> None:
        """
        Add animations to the Notificationbar and message label.
        """
        self.current_color = self.status_colors["normal"]

        self.effect = QGraphicsColorizeEffect(self)
        self.effect.setColor(QColor(self.status_colors["normal"]))
        self.setGraphicsEffect(self.effect)

        # NEW MESSAGE ANIMATIONS
        self.message_in_position_animation = QPropertyAnimation(
            self.message, b"pos")
        self.message_in_position_animation.setDuration(200)

        self.color_animation = QPropertyAnimation(self.effect, b"color")
        self.color_animation.setDuration(200)
        self.color_animation.setLoopCount(5)

        self.in_animations = QParallelAnimationGroup()
        self.in_animations.addAnimation(self.message_in_position_animation)
        self.in_animations.addAnimation(self.color_animation)

        # MESSAGE DISAPEAR ANIMATION
        self.message_out_position_animation = QPropertyAnimation(
            self.message, b"pos")
        self.message_out_position_animation.setDuration(100)

    def _message_in_configs(self, critical_level: str) -> None:
        """
        Set animations configs when it has to appeare in notifcation bar.

        @args
            critical_level:str
        """
        x = self.message.x()
        self.message_in_position_animation.setStartValue(QPoint(x, 20))
        self.message_in_position_animation.setEndValue(QPoint(x, 3))

        start_color = QColor(self.current_color)
        end_color = QColor(self.status_colors.get(critical_level, "#005378"))
        self.color_animation.setStartValue(start_color)
        self.color_animation.setEndValue(end_color)

        self.current_color = end_color

    def _message_out_configs(self) -> None:
        """
        Message animation when it has to disapeare.
        """
        x = self.message.x()
        self.message_out_position_animation.setStartValue(QPoint(x, 3))
        self.message_out_position_animation.setEndValue(QPoint(x, -20))

        start_color = QColor(self.current_color)
        end_color = QColor(self.status_colors["normal"])
        self.color_animation.setStartValue(start_color)
        self.color_animation.setEndValue(end_color)
        self.current_color = self.status_colors["normal"]

    def _change_message(self, message: str) -> None:
        """
        Add now timestamp along with new message to the message label

        @args
            message:str
        """
        # self.logger(message)
        time = datetime.now().strftime("%H:%M:%S")
        message = f"{time} → {message}"
        self.message.change_text(message)

    def _new_message(self, message, critical_level):
        """
        Change label message and start animation to show
        new message with its color.

        @args
            message:str
            critical_level:str

        """
        self._change_message(f"{message}")
        self._message_in_configs(critical_level)
        self.message_out_position_animation.disconnect()
        self.in_animations.start()

    def show_message(self,
                     message: str,
                     critical_level: str = "high") -> None:
        """
        Show new message and set new color to notification bar based
        on critical level.
        """
        message = str(message)
        self._message_out_configs()
        self.message_out_position_animation.finished.connect(
            lambda: (self.message.change_text(""),
                     self._new_message(message, critical_level)))
        self.message_out_position_animation.start()


class SideBar(Frame):
    """
    Animated Side Bar Frame.
    """

    def __init__(self, parent: object, **kwargs) -> None:
        super().__init__(layout=Vertical, parent=parent, **kwargs)

        self.setObjectName('sidebar')
        self.is_open = False
        self.setHidden(True)
        self.setup_animations()

    def setup_animations(self) -> None:
        """
        Setup Animations for this frame.
        """
        self.animation = QPropertyAnimation(self, b'geometry')
        self.animation.setDuration(200)

        self.animation2 = QPropertyAnimation(self, b'geometry')
        self.animation2.setDuration(200)

    def change_coordinates(self,
                           start: tuple,
                           end: tuple,
                           animation_object: QPropertyAnimation) -> None:
        """
        Change the animation setting for the start point and end point.
        it will call start() function after changing the coordinates
        -----------------------------------------------------------
        -> Params:
                start: (x, y, width, height)
                end: (x, y, width, height)
                animation_object: QPropertyAnimation
        """
        animation_object.setStartValue(QRect(*start))
        animation_object.setEndValue(QRect(*end))
        animation_object.start()

    def disconnect_animations(self) -> None:
        """
        Disconnect all methods that connected to the
        animations
        """
        self.animation.disconnect()
        self.animation2.disconnect()

    def _close_sidebar(self,
                       x: float,
                       y: float,
                       height: float) -> None:
        """
        Close side bar animation handler.
        """
        self.change_coordinates(start=(x, y, 350, height),
                                end=(x, y, 400, height),
                                animation_object=self.animation)
        self.animation.finished.connect(
            lambda: self.change_coordinates(start=(x, y, 400, height),
                                            end=(x, y, 0, height),
                                            animation_object=self.animation2))

        self.animation2.finished.connect(self.disconnect_animations)

    def _open_sidebar(self,
                      x: float,
                      y: float,
                      height: float) -> None:
        """
        Close side bar animation handler.
        """
        self.setHidden(False)
        self.change_coordinates(start=(x, y, 0, height),
                                end=(x, y, 400, height),
                                animation_object=self.animation)
        self.animation.finished.connect(
            lambda: self.change_coordinates(start=(x, y, 400, height),
                                            end=(x, y, 350, height),
                                            animation_object=self.animation2))
        self.animation2.finished.connect(self.disconnect_animations)

    def open_close_handler(self) -> None:
        """
        This method handles the animation of this frame.
        """
        x = 0
        y = 55
        height = 800
        if self.is_open:
            self._close_sidebar(x, y, height)
            self.is_open = False
            return
        self._open_sidebar(x, y, height)
        self.is_open = True

    def leaveEvent(self, event: object) -> None:
        """
        override this method to when mouse leave the
        Sidebar area, close the sidebar.
        ---------------------------------------------
        -> Params
            event: object
        """
        self.open_close_handler()

    def add_sub_widget(self,
                       name: str,
                       widget: object,
                       add_stretch_before: bool = False,
                       add_stretch_after: bool = False) -> None:
        """
        Adds new widget to this frame
        ---------------------------------------
        -> Params:
                name
                widget
                add_stretch_before
                add_stretch_after
        """
        if add_stretch_before:
            self.add_stretch()

        setattr(self, name, widget)

        if add_stretch_after:
            self.add_stretch()


class SidebarButton(Button):
    """
    This button will use for in SideBar and like hover method
    when user hover on it, it will move right with animation
    and when unhover it will come back to its actual position.
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.setup_animations()

    def setup_animations(self) -> None:
        """
        Setup Animations for this frame.
        """
        self.animation = QPropertyAnimation(self, b'geometry')
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.InOutBack)

    def change_coordinates(self, start: tuple, end: tuple,
                           animation_object: QPropertyAnimation) -> None:
        """
        Change the animation setting for the start point and end point.
        it will call start() function after changing the coordinates
        -----------------------------------------------------------
        -> Params:
                start: (x, y, width, height)
                end: (x, y, width, height)
                animation_object: QPropertyAnimation
        """
        animation_object.setStartValue(QRect(*start))
        animation_object.setEndValue(QRect(*end))
        animation_object.start()

    def get_current_geometry(self) -> tuple:
        """
        Return the current position of the widget
        """

        return self.x(), self.y(), self.width(), self.height()

    def enterEvent(self, event) -> None:
        """
        When mouse enter the widget, it will goes
        to the right with animation.
        """
        self.xaxis, self.yaxis, self.w, self.h = self.get_current_geometry()
        self.xaxis = 9  # Have to hardcode because if user move mouse very fast on the widget, it will confused
        # self.xaxis += 30
        x = self.xaxis + 30
        self.change_coordinates(start=(self.xaxis, self.yaxis, self.w, self.h),
                                end=(x, self.yaxis, self.w, self.h),
                                animation_object=self.animation)

    def leaveEvent(self, event) -> None:
        """
        When mouse leave the widget, the widget will goes back
        to its main position.
        """
        # self.xaxis += 30
        x = self.xaxis + 30
        self.change_coordinates(start=(x, self.yaxis, self.w, self.h),
                                end=(self.xaxis, self.yaxis, self.w, self.h),
                                animation_object=self.animation)


class DynamicAddRemoveFrame(Frame):
    """
    Frame containe add & remove button
    ----------------------------------
    -> Params:
           add_callback: add button function callback
           remove_callback: remove button function callback
           add_label: add button label default(+)
           remove_label: remove button label default(-)
           **kwargs: Qt Frame widgets options
    """

    def __init__(self,
                 add_callback: callable,
                 remove_callback: callable,
                 add_label: str = "+",
                 remove_label: str = "-",
                 layout: object = Vertical,
                 width: int = 37,
                 **kwargs) -> None:

        super().__init__(layout=layout, **kwargs)
        self.setFixedHeight(80)
        self.add_button = Button(label=add_label,
                                 object_name="add-sub-sections",
                                 callback_function=add_callback,
                                 width=width)

        self.remove_button = Button(label=remove_label,
                                    object_name="add-sub-sections",
                                    callback_function=remove_callback,
                                    width=width)


class ProcessingAnimation(Frame):
    """
    Shows colorized animated circle.
    """

    def __init__(self,
                 parent: object,
                 start_color: str = "#FFB600",
                 end_color: str = "#0058A7",
                 grid_positions: tuple = None) -> None:
        super().__init__(parent=parent, layout=Vertical)
        self.setFixedSize(15, 15)
        self.setStyleSheet("border-radius:7px;")
        self.grid_positions = grid_positions

        self.effect = QGraphicsColorizeEffect()
        self.effect.setColor(QColor("transparent"))
        self.setGraphicsEffect(self.effect)

        self.animation = QPropertyAnimation(targetObject=self.effect,
                                            propertyName=b'color',
                                            duration=400,
                                            loopCount=-1,
                                            startValue=QColor(start_color),
                                            endValue=QColor(end_color))
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)

    def start(self) -> None:
        """
        Start animation.
        """
        self.animation.start()

    def stop(self) -> None:
        """
        Stop animation and set effect color to transparent.
        """
        self.animation.stop()
        self.effect.setColor(QColor("transparent"))


class DateEntry(Frame):

    def __init__(self,
                 label: str = "",
                 layout: object = Vertical,
                 align_center: bool = True,
                 width: int = 280,
                 frame_width: int = 200,
                 calendarPopup: bool = False,
                 use_effect: bool = True,
                 effect_color: str = "#f89fa2",
                 effect_blur_radius: int = 15,) -> None:
        super().__init__(layout=layout)
        if align_center:
            self.main_layout.setAlignment(Qt.AlignCenter)
        self.label = Label(label=label)
        self.date_entry = QDateEdit(calendarPopup=calendarPopup)
        self.date_entry.setMinimumWidth(width)
        self.date_entry.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.date_entry.setAlignment(Qt.AlignCenter)
        self.date_entry.setDateTime(datetime.now())
        if use_effect:
            effect = QGraphicsDropShadowEffect(self.date_entry)
            effect.setColor(QColor(effect_color))
            effect.setOffset(0, 0)
            effect.setBlurRadius(effect_blur_radius)
            self.date_entry.setGraphicsEffect(effect)

    def get_value(self) -> str:
        """
        Returns the date entry value.
        """
        value = self.date_entry.date().getDate()
        return datetime(*value).strftime("%Y-%m-%d")
    
class Stretch(QWidget):

    def __init__(self,
                 horizontal_stretch: QSizePolicy = QSizePolicy.Expanding,
                 vertical_stretch: QSizePolicy = QSizePolicy.Preferred) -> None:
        super().__init__()
        self.setSizePolicy(horizontal_stretch, vertical_stretch)


WIDGETS_LIST = {
    "entry": LabelEntry,
    "combobox": LabelCombobox,
}

VALIDATORS = {
    "string": ONLY_STRING_SPACE_PATTERN,
    # "decimal": JUST_FLOAT_PATTERN
}
