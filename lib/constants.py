
from os import getcwd

CWD = getcwd()

DATE_FORMAT = "%d-%m-%Y"
TABLE_HEADERS = ["Title", "Price", "Quantity",
                "Overall Price", "Categoty",
                "Date"]

EXPENSES_FILE_PATH = f"{CWD}/lib/data/data.json"
CSS_COLORS_FILE_PATH = f"{CWD}/lib/css/colors.css"
CSS_FILE_PATH = f"{CWD}/lib/css/style.css"


# ====================================== Patterns ======================================
LENGTH_VALIDATION_PATTERN = "[a-zA-Z\\d\\s.]+"
DRIVER_VALIDATION_PATTERN = "[a-zA-Z\\d\\s()-]+"
LINE_TYPE_VALIDATION_PATTERN = "[a-zA-Z\\d-()]+"

# ====================================== Widgets Validators ======================================
ONLY_STRING_SPACE_PATTERN = "[a-zA-Z\\s\\d,]+"

DOLLAR_ICON_PATH = f"{CWD}/lib/icons/dollar.png"
ITEMS_ICON_PATH = f"{CWD}/lib/icons/items.png"