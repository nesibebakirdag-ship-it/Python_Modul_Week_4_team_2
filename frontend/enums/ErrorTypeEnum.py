from enum import Enum

class ErrorType(Enum):
    INVALID = 0
    EMPTY = 1
    USERNOTFOUND = 2
    OTHER=3


ERROR_MAP = {
    "User not found": ErrorType.USERNOTFOUND,
    "Invalid password": ErrorType.INVALID,
    "Empty username or password": ErrorType.EMPTY,
}

ERROR_TEXT = {
    ErrorType.EMPTY: "Empty username or password",
    ErrorType.USERNOTFOUND: "User not found",
    ErrorType.INVALID: "Invalid password",
    ErrorType.OTHER: "There is a problem"
}