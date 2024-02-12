"""
Utils module contain classes and functions helper
-> classes:
        SingleTon:
             single ton base class
        SharedObject:
             single ton share object will helps to reduce complexity
             by sharing methods in unbound way
        DataFormater:
             struct and format the interface data
        DropsMapping:
             create structure for drops(dict)



-> functions:
         get_requests:
              send http GET requests

         get_wiring_block:
              fetch wiring block data from drive works

         load_file:
               function to load json files from disk

         check_image_exists:
               will check if the given image file path exists
               we used this function because Qt not raising any error if
               the it cannot open the image file

"""
import re
import csv
from json import dumps
from json import load
from time import strftime
from os import system
from pprint import pprint
from typing import Any
from typing import Generator
from traceback import print_tb
from ..errors import InvalidLogLevel


def void_function(*args, **kwargs) -> None:
    pass


class Logger:
    """
    act as advance print function for debugging the code
    ----------------------------------------------------
    @properties
            debug: activate and deactivate output
            level: level of printing details
    @methods

    """
    colors = {
        "default": '\033[0m',
        "red": '\033[91m',
        "green": '\033[92m',
        "blue": '\033[94m',
        "yellow": '\033[93m',
        "purple": '\033[95m',
        "cyan": '\033[96m',
    }
    debug = True
    level = 1
    time_stamp_format = "[%H:%M:%S]:"

    def __init__(self) -> None:
        self.levels = {1: self.level_one,
                       2: self.level_two,
                       3: self.level_three}
        self.pretty_printer = pprint
    
    def __call__(self,
                 *args,
                 pretty: bool = False,
                 level: str = 1,
                 color: str = "default",
                 **kwargs):
        """
        debug print the args and error traceback base on the detail level
        -------------------------------------------------------------------
        -> Params:
                prrety:
                        pprint the args
                level:
                        level_one:
                                normal print with time stamp
                        level_two:
                                details of the catched error
                                with line and cause of error
        """
        if not self.debug:
            return
        try:
            self.levels[level](pretty=pretty, color=color, *args, **kwargs)
        except KeyError as err:
            print(self.colors["default"], err)
            raise SystemError("Invalid Level name for debugging")

    def level_one(self,
                  *args,
                  pretty: bool,
                  color: str,
                  **kwargs) -> None:
        """
        print given argument with time stamp
        """
        time_stamp = strftime(self.time_stamp_format)
        if pretty:
            print(self.colors[color], time_stamp, end="\t")
            self.pretty_printer(*args)
            print(self.colors["default"], end="")
            return
        print(self.colors[color],
              time_stamp,
              *args,
              self.colors["default"])

    def level_two(self,
                  *args,
                  error: object,
                  pretty: bool,
                  color: str) -> None:
        """
        print traceback of the catched error from try,
        except block
        ----------------------------------------------
        -> Params:
                *args
                 error: object,
                 pretty: bool,
                 color: str
        """
        self.level_one(*args, error, pretty=pretty, color=color)
        print_tb(error.__traceback__)

    def level_three(self,
                    *args,
                    pretty: bool,
                    color: str,
                    **kwargs) -> None:
        """
        Print debugging messages
        -------------------------------------------------
        -> Params:
                *args
                 error
        """
        self.level_one(*args, pretty=pretty, color=color, **kwargs)

    def disable_logger(self) -> None:
        """
        disable the debug mode
        """
        self.debug = False

    def disable_log_level(self, level: int) -> None:
        """
        disable logger base on the give level
        --------------------------------------
        -> Params:
                level
        @raises:
             InvalidLogLevel
        """
        if not self.levels.get(level):
            raise InvalidLogLevel(f"invalid level -> <{level}>")
        self.levels[level]
        self.levels[level] = self.void_function

    def void_function(self, *args, **kwargs) -> None:
        """
        replace function for log leves when
        we want to disable logger base on function levels
        """

    def compile_mode(self) -> None:
        """
        change default ouput to normal print fucntion.
        there is bug with python pprint module, which is
        cause program crash after compilation
        """
        self.pretty_printer = print


log = Logger()
# log.disable_log_level(2)
log.disable_log_level(3)


class Notification:
    """
    Handles showing the notifications in the app with
    two tools, namely StatusBar and NotificationBox(floating)
    """
    @classmethod
    def add_messenger(cls, messenger: callable, name: str) -> None:
        setattr(cls, name, messenger)

def load_file(path: str, mode: str = "r") -> any:
    """
    open and return content of the file
    base on given path
    -> Params:
            path
            mode: reading mode
    <- Return:
            content of file text or bytes
    """
    with open(path, mode) as file:
        data = file.read()
    return data

def load_css(css_path: str,
             css_colors_path: str) -> str:
    """
    Open css style sheeet file, replace the
    css variables with the values in css
    variables file and return the css.
    -----------------------------------------
    -> Params
        css_path: str → path to css file
        css_colors_path: str → path to colors file
    <- Return
        str: css
    """
    css = load_file(css_path)
    css_colors = load_file(css_colors_path)
    pattern = r"--[a-zA-Z\d]*: [#a-zA-Z\d]*"
    css_colors = re.findall(pattern, css_colors)
    mapping = dict()
    for variable in css_colors:
        name, value = variable.split(":")
        mapping[name] = value
    for variable, value in mapping.items():
        css = css.replace(variable, value)
    return css
    

def write_file(path: str, data: Any, mode: str = "w", ) -> any:
    """
    open and return content of the file
    base on given path
    -> Params:
            path
            mode: reading mode
    <- Return:
            content of file text or bytes
    """
    with open(path, mode) as file:
        file.write(data)


def load_json(path: str) -> any:
    """
    Open json file and return it as dict
    """
    with open(path, "r") as file:
        data = load(file)
    return data

def write_json(path: str, data: dict) -> None:
    """
    Save data to a json file
    """
    data = dumps(data, indent=4)
    with open(path, 'w') as file:
        file.write(data)

def read_csv(path: str) -> Generator:
    """
    Open csv file and read it
    """
    data = None
    with open(path, 'r', encoding='UTF8') as file:
        data = csv.reader(file)
        yield from data

def force_close_app(app_name: str) -> None:
    """
    Use windows command line to close the app
    even some of background processings like
    updating are running.
    """
    system(f"TASKKILL /IM {app_name}.exe")