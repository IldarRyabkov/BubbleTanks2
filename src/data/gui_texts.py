import data.languages.english as eng
import data.languages.russian as rus


PAUSE_MENU_CAPTION = {
    "English": ['PAUSE'],
    "Russian": ['ПАУЗА']
}

OPTIONS_WINDOW_CAPTION = {
    'Russian': ["Опции"],
    'English': ["Options"]
}

MAP_WINDOW_CAPTION = {
    "English": ['Map'],
    "Russian": ['Карта']
}

STATS_WINDOW_CAPTION = {
    "English": ['Statistics'],
    "Russian": ['Статистика']
}

STATS_WINDOW_TEXTS = {
    "English":
        {
            "labels": [['Main weapon'], ['Second weapon']],
            "description": eng.UPGRADE_TEXT
        },
    "Russian":
        {
            "labels": [['Основное оружие'], ['Второе оружие']],
            "description": rus.UPGRADE_TEXT
        }
}


PLAY_BUTTON_LABEL= {
    "English": ["PLAY"],
    "Russian": ["ИГРАТЬ"]
}

SETTINGS_BUTTON_LABEL = {
    "English": ["Settings"],
    "Russian": ["Настройки"]
}

MAIN_MENU_CAPTION = {
    "English": ['Underwater battles'],
    "Russian": ['Подводные битвы']
}

ROOM_TEXTS = {
    "English": eng.ROOM_TEXTS,
    "Russian": rus.ROOM_TEXTS
}

COOLDOWN_WINDOW_LABELS = {
    "English": [['M:'], ['S:']],
    "Russian": [['О:'], ['В']]
}

HEALTH_WINDOW_TEXTS = {
    "English": {
        "tank": eng.TANK_NAMES,
        "bubbles": [[' bubbles left'], ['Maximum tank']]
    },
    "Russian": {
        "tank": rus.TANK_NAMES,
        "bubbles": [[' пузырей осталось'], ['Максимальный танк']]
    }
}

UPGRADE_BUTTON_TEXTS = {
    "English": {
        "labels": [['Upgrade!'], ['- Main weapon -'], ['- Second weapon -']],
        "texts": eng.UPGRADE_TEXT
    },
    "Russian": {
        "labels": [['Улучшение!'], ['- Основное оружие -'], ['- Второе оружие -']],
        "texts": rus.UPGRADE_TEXT
    }
}

YES_BUTTON_TEXT = {
    "English": ['Yes'],
    "Russian": ['Да']
}

NO_BUTTON_TEXT = {
    "English": ['No'],
    "Russian": ['Нет']
}

VICTORY_MENU_LABELS = {
    "English": [['CONGRATULATIONS!'], ['You passed the game!']],
    "Russian": [['ПОЗДРАВЛЯЕМ!'], ['Ты прошел игру!']]
}

SETTINGS_WINDOW_CAPTIONS = {
    "English": [["Settings"], ["Exit to desktop?"], ["Resolution"],  ["Language"]],
    "Russian": [["Настройки"], ["Выйти из игры"], ["Разрешение"], ["Язык"]]
}

LANGUAGES = ["English"], ["Russian"]

RESOLUTION_WARNING = {
    "English": ["Restart the game to apply the new resolution"],
    "Russian": ["Перезапустите игру, чтобы применить", "новое разрешение"]
}

EXIT_TO_MENU_TEXT = {
    "English": ["Exit to main menu"],
    "Russian": ["Выйти в главное меню"]
}

EXIT_TO_DESKTOP_TEXT = {
    "English": ["Exit to desktop"],
    "Russian": ["Выйти из игры"]
}

BACK_BUTTON_TEXT = {
    "English": ["Back"],
    "Russian": ["Назад"]
}

MASTER_VOLUME_TEXT = {
    "English": ["Master volume"],
    "Russian": ["Громкость"]
}

SOUND_VOLUME_TEXT = {
    "English": ["Sound volume"],
    "Russian": ["Громкость звука"]
}

MUSIC_VOLUME_TEXT = {
    "English": ["Music volume"],
    "Russian": ["Громкость музыки"]
}

RESOLUTION_LABEL = {
    "English": ["Resolution"],
    "Russian": ["Разрешение"]
}

LANGUAGE_LABEL = {
    "English": ["Language"],
    "Russian": ["Язык"]
}



__all__ = [

    "PAUSE_MENU_CAPTION",
    "OPTIONS_WINDOW_CAPTION",
    "MAP_WINDOW_CAPTION",
    "STATS_WINDOW_CAPTION",
    "STATS_WINDOW_TEXTS",
    "SETTINGS_BUTTON_LABEL",
    "PLAY_BUTTON_LABEL",
    "MAIN_MENU_CAPTION",
    "ROOM_TEXTS",
    "COOLDOWN_WINDOW_LABELS",
    "VICTORY_MENU_LABELS",
    "SETTINGS_WINDOW_CAPTIONS",
    "LANGUAGES",
    "RESOLUTION_WARNING",
    "BACK_BUTTON_TEXT",
    "EXIT_TO_MENU_TEXT",
    "EXIT_TO_DESKTOP_TEXT",
    "MASTER_VOLUME_TEXT",
    "SOUND_VOLUME_TEXT",
    "MUSIC_VOLUME_TEXT",
    "RESOLUTION_LABEL",
    "LANGUAGE_LABEL",
    "UPGRADE_BUTTON_TEXTS",
    "HEALTH_WINDOW_TEXTS",
    "YES_BUTTON_TEXT",
    "NO_BUTTON_TEXT"

]
