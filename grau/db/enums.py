from enum import Enum


class HeightUnits(Enum):
    CM = "cm"
    INCH = "inch"
    FEET = "feet"


class WeightUnits(Enum):
    LB = "lbs"
    KG = "kg"
    STONE = "stone"


class DateFormat(Enum):
    YMD = "%Y-%m-%d"  # postgres default
    MDY = "%m-%d-%Y"
    DMY = "%d-%m-%Y"


class TimestampFormat(Enum):
    YMD = "%Y-%m-%dT%H:%M:%S.%fZ"  # postgres default
    MDY = "%m-%d-%YT%H:%M:%S.%fZ"
    DMY = "%d-%m-%YT%H:%M:%S.%fZ"
