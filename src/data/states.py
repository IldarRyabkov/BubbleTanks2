class MainMenuStates:
    MAIN_PAGE = 0
    SETTINGS = 1
    CREDITS = 2
    LANGUAGES = 3
    RESOLUTIONS = 4
    EXIT = 5
    NEW_GAME = 6
    LOAD_GAME = 7
    OVERRIDE_SAVE = 8
    DELETE_SAVE = 9


class PauseMenuStates:
    STATS = 0
    MAP = 1
    OPTIONS = 2
    DIALOG_MENU = 3
    DIALOG_DESKTOP = 4


class UpgradeMenuStates:
    MAIN_STATE = 0


class VictoryMenuStates:
    MAIN_STATE = 0


class UpgradeButtonType:
    LEFT = 0
    CENTER = 1
    RIGHT = 2
    WIDE_LEFT = 3
    WIDE_RIGHT = 4


class PopupWindowStates:
    CLOSED = 0
    OPENING = 1
    CLOSING = 2
    OPENED = 3


__all__ = [

    "MainMenuStates",
    "PauseMenuStates",
    "UpgradeMenuStates",
    "VictoryMenuStates",
    "UpgradeButtonType",
    "PopupWindowStates"

]