
from os import getcwd

CWD = getcwd()

CSS_COLORS_FILE_PATH = f"{CWD}/lib/css/colors.css"
CSS_FILE_PATH = f"{CWD}/lib/css/style.css"


# ====================================== Patterns ======================================
LENGTH_VALIDATION_PATTERN = "[a-zA-Z\\d\\s.]+"
DRIVER_VALIDATION_PATTERN = "[a-zA-Z\\d\\s()-]+"
LINE_TYPE_VALIDATION_PATTERN = "[a-zA-Z\\d-()]+"

# ====================================== Widgets Validators ======================================
ONLY_STRING_PATTERN = "[a-zA-Z\\d,]+"
ONLY_STRING_HIPHEN_PATTERN = "[a-zA-Z\\d,-]+"
ONLY_STRING_SPACE_PATTERN = "[a-zA-Z\\s\\d,]+"
ONLY_STRING_UPPERCASE_PATTERN = "[A-Z\\d,]+"
SECTION_NAME_PATTERN = "([A-Z]+[,]|[A-Z]+[\\d]+[,])+"
ONLY_INT_PATTERN = r"[\d]+"
ONLY_MULTIPLE_INT_PATTERN = r"[\d,]+"
ONLY_FLOAT_PATTERN = r"[\d.]+"
SECTION_NAMES_DROP_PATTERN = "[A-Z]{1,2}[\\d]{1,2}"
EMAIL_PATTERN = "[a-zA-Z\\d@._-]+"
USERNAME_PATTERN = "[a-zA-Z\\d._-]+"