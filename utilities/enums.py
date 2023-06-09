import pycountry
from discord import OptionChoice
from datetime import datetime, timezone, timedelta
from enum import Enum, auto

class BaseEnum():
    @classmethod
    def get_value(clazz: Enum, name: str) -> str:
        for member in clazz:
            if name and member.name == name.upper():
                if isinstance(member.value, int):
                    return member.name.replace('_', ' ').title()
                else:
                    return member.value
        return "Unknown"

    @classmethod
    def get_choices(clazz: Enum) -> list[OptionChoice]:
        return [OptionChoice(name=clazz.get_value(member.name)) for member in clazz]

class MediaFormat(BaseEnum, Enum):
    TV = "TV"
    TV_SHORT = "TV Short"
    MOVIE = auto()
    SPECIAL = auto()
    OVA = "OVA"
    ONA = "ONA"
    MUSIC = auto()
    MANGA = auto()
    NOVEL = auto()
    ONE_SHOT = auto()

class MediaStatus(BaseEnum, Enum):
    FINISHED = auto()
    RELEASING = "On Going"
    NOT_YET_RELEASED = auto()
    CANCELLED = auto()
    HIATUS = auto()

class MediaSeason(BaseEnum, Enum):
    WINTER = auto()
    SPRING = auto()
    SUMMER = auto()
    FALL = auto()

    @staticmethod
    def get_current_season() -> str:
        tz = timezone(timedelta(hours=8), name='Asia/Kuala_Lumpur')
        current_month = datetime.now(tz).month

        if current_month in [12, 1, 2]:
            return MediaSeason.get_value(MediaSeason.WINTER.name)
        elif current_month in [3, 4, 5]:
            return MediaSeason.get_value(MediaSeason.SPRING.name)
        elif current_month in [6, 7, 8]:
            return MediaSeason.get_value(MediaSeason.SUMMER.name)
        else:
            return MediaSeason.get_value(MediaSeason.FALL.name)

class MediaSource(BaseEnum, Enum):
    ORIGINAL = auto()
    MANGA = auto()
    LIGHT_NOVEL = auto()
    VISUAL_NOVEL = auto()
    VIDEO_GAME = auto()
    OTHER = auto()
    NOVEL = auto()
    DOUJINSHI = auto()
    ANIME = auto()
    WEB_NOVEL = auto()
    LIVE_ACTION = auto()
    GAME = auto()
    COMIC = auto()
    MULTIMEDIA_PROJECT = auto()
    PICTURE_BOOK = auto()

class Country():
    @staticmethod
    def get_value(name: str) -> str:
        country = pycountry.countries.get(alpha_2=name)

        if country is None:
            return "Unknown"
        return country.name
    
class RequestMethod(BaseEnum, Enum):
    POST = auto()
    GET = auto()
    
class Game(BaseEnum, Enum):
    GENSHIN = auto()
    STARRAIL = auto()

class Language(BaseEnum, Enum):
    ENGLISH = "en-us"
    CHINESE = "zh-tw"