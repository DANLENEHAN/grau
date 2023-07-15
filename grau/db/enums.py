from enum import Enum


class ProfileStatus(Enum):
    """
    Enum for user status
    """

    ACTIVE = "active"
    INACTIVE = "inactive"
    DELETED = "deleted"
    BANNED = "banned"


class Gender(Enum):
    """
    Enum for user gender
    """

    MALE = "male"
    FEMALE = "female"


class RequestType(Enum):
    """
    Enum for request type
    """

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


class StatusCode(Enum):
    """
    HTTP response status codes.
    """

    SUCCESS = 200
    CREATED = 201
    ACCEPTED = 202
    NO_CONTENT = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    NOT_FOUND = 404
    CONFLICT = 409
    INTERNAL_SERVER_ERROR = 500


class HeightUnits(Enum):
    """
    Height units.
    """

    CM = "cm"
    INCH = "inch"
    FEET = "feet"


class WeightUnits(Enum):
    """
    Weight units.
    """

    LB = "lbs"
    KG = "kg"
    STONE = "stone"


class DateFormat(Enum):
    """
    Accepted date formats.
    """

    YMD = "%Y-%m-%d"  # postgres default
    MDY = "%m-%d-%Y"
    DMY = "%d-%m-%Y"


class TimestampFormat(Enum):
    """
    Accepted timestamp formats.
    """

    YMD = "%Y-%m-%dT%H:%M:%S.%fZ"  # postgres default
    MDY = "%m-%d-%YT%H:%M:%S.%fZ"
    DMY = "%d-%m-%YT%H:%M:%S.%fZ"
