"""
Module contains all the widgets class to create UI with Qt library
"""
from datetime import datetime
from typing import Any
from typing import Union
from typing import NewType
from PyQt5.QtWidgets import QAbstractSpinBox
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QVBoxLayout as Vertical
from PyQt5.QtWidgets import QHBoxLayout as Horizontal
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QCompleter
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QDateEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QCursor
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QIntValidator
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QSize
from PyQt5.QtCore import QRegExp
from PyQt5.QtCore import QSortFilterProxyModel
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
        data[-1] = datetime.strftime(data[-1], DATE_FORMAT)
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

class DateEntry(Frame):

    def __init__(self,
                 label: str = "",
                 default_date: datetime = datetime.now(),
                 layout: object = Vertical,
                 align_center: bool = True,
                 width: int = 280,
                 frame_width: int = 0,
                 calendarPopup: bool = False,
                 callback_func: callable = void_function,
                 use_effect: bool = True,
                 effect_color: str = "#f89fa2",
                 effect_blur_radius: int = 15) -> None:
        super().__init__(layout=layout)
        if align_center:
            self.main_layout.setAlignment(Qt.AlignCenter)
        if frame_width:
            self.setFixedWidth(frame_width)
        self.label = Label(label=label)
        self.date_entry = QDateEdit(calendarPopup=calendarPopup)
        self.date_entry.setDisplayFormat("dd/MM/yyyy")
        self.date_entry.setMinimumWidth(width)
        self.date_entry.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.date_entry.setAlignment(Qt.AlignCenter)
        self.date_entry.setDateTime(default_date)
        self.date_entry.dateChanged.connect(callback_func)
        if use_effect:
            effect = QGraphicsDropShadowEffect(self.date_entry)
            effect.setColor(QColor(effect_color))
            effect.setOffset(0, 0)
            effect.setBlurRadius(effect_blur_radius)
            self.date_entry.setGraphicsEffect(effect)
        
    def get_value(self) -> datetime:
        """
        Returns the date entry value as datetime
        object.
        """
        return datetime(*self.date_entry.date().getDate())
    
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
    "string": ONLY_STRING_SPACE_PATTERN
}
