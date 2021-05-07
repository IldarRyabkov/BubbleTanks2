import data.languages.english as eng
import data.languages.russian as rus


PAUSE_MENU_CAPTIONS = {
    "English": eng.PAUSEMENU_CAPTION,
    "Russian": rus.PAUSEMENU_CAPTION
}


OPTIONS_WINDOW_TEXTS = {
    'quit_button':
        {
            'English': eng.OPTIONSWINDOW_QUIT_BUTTON,
            'Russian': rus.OPTIONSWINDOW_QUIT_BUTTON
        },
    'labels':
        {
            'Russian': (
                rus.OPTIONSWINDOW_CAPTION,
                rus.OPTIONSWINDOW_LABEL_MUSIC,
                rus.OPTIONSWINDOW_LABEL_SOUND
            ),
            'English': (
                eng.OPTIONSWINDOW_CAPTION,
                eng.OPTIONSWINDOW_LABEL_MUSIC,
                eng.OPTIONSWINDOW_LABEL_SOUND
            )
        }
}

MAP_WINDOW_CAPTIONS = {
    "English": eng.MAPWINDOW_CAPTION,
    "Russian": rus.MAPWINDOW_CAPTION
}

STATS_WINDOW_TEXTS = {
    "English":
        {
            "captions": eng.STATSWINDOW_CAPTIONS,
            "description": eng.UPGRADE_TEXT
        },
    "Russian":
        {
            "captions": rus.STATSWINDOW_CAPTIONS,
            "description": rus.UPGRADE_TEXT
        }
}

SIDE_BUTTON_TEXTS = {
    "stats_button": {
        "English": eng.STATSBUTTON_TEXT,
        "Russian": rus.STATSBUTTON_TEXT
    },
    "options_button": {
        "English": eng.OPTIONSBUTTON_TEXT,
        "Russian": rus.OPTIONSBUTTON_TEXT
    },
    "map_button": {
    "English": eng.MAPBUTTON_TEXT,
    "Russian": rus.MAPBUTTON_TEXT
    }
}


PLAY_BUTTON_TEXTS = {
    "English": eng.PLAY_BUTTON,
    "Russian": rus.PLAY_BUTTON
}


MAIN_MENU_CAPTIONS = {
    "English": eng.MAIN_MENU_CAPTION,
    "Russian": rus.MAIN_MENU_CAPTION
}

ROOM_TEXTS = {
    "English": eng.ROOM_TEXTS,
    "Russian": rus.ROOM_TEXTS
}

COOLDOWN_WINDOW_LABELS = {
    "English": eng.WINDOW_COOLDOWN_LABELS,
    "Russian": rus.WINDOW_COOLDOWN_LABELS
}

HEALTH_WINDOW_TEXTS = {
    "English": {
        "tank": eng.TANK_NAMES,
        "bubbles": eng.BUBBLES_TEXTS
    },
    "Russian": {
        "tank": rus.TANK_NAMES,
        "bubbles": rus.BUBBLES_TEXTS
    }
}

UPGRADE_BUTTON_TEXTS = {
    "English": {
        "labels": eng.UPGRADEMENU_LABELS,
        "texts": eng.UPGRADE_TEXT
    },
    "Russian": {
        "labels": rus.UPGRADEMENU_LABELS,
        "texts": rus.UPGRADE_TEXT
    }
}


VICTORY_MENU_TEXTS = {
    "English": {
        "labels": eng.VICTORYMENU_LABELS,
        "button": eng.VICTORYMENU_BUTTON
    },
    "Russian": {
        "labels": rus.VICTORYMENU_LABELS,
        "button": rus.VICTORYMENU_BUTTON
    }
}


__all__ = [

    "PAUSE_MENU_CAPTIONS",
    "OPTIONS_WINDOW_TEXTS",
    "MAP_WINDOW_CAPTIONS",
    "STATS_WINDOW_TEXTS",
    "SIDE_BUTTON_TEXTS",
    "PLAY_BUTTON_TEXTS",
    "MAIN_MENU_CAPTIONS",
    "ROOM_TEXTS",
    "COOLDOWN_WINDOW_LABELS",
    "VICTORY_MENU_LABELS"

]
