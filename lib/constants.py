
from os import getcwd

CWD = getcwd()

CSS_COLORS_FILE_PATH = f"{CWD}/lib/css/colors.css"
CSS_FILE_PATH = f"{CWD}/lib/css/style.css"


# ====================================== Patterns ======================================
LENGTH_VALIDATION_PATTERN = "[a-zA-Z\\d\\s.]+"
DRIVER_VALIDATION_PATTERN = "[a-zA-Z\\d\\s()-]+"
LINE_TYPE_VALIDATION_PATTERN = "[a-zA-Z\\d-()]+"

# ====================================== Widgets Validators ======================================
ONLY_STRING_SPACE_PATTERN = "[a-zA-Z\\s\\d,]+"