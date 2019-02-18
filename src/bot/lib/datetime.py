from datetime import datetime
import pytz

def get_datetime(json) -> datetime:
    """ Returns the UTC creation datetime of the status as a Python object.

    "created_at":"Thu Apr 06 15:24:15 +0000 2017"
    
    """
    datetime_string = json["created_at"]
    return datetime.strptime(datetime_string, "%a %b %d %H:%M:%S +0000 %Y")

def get_datetime_tz(json) -> datetime:
    """ Returns the UTC creation datetime of the status as a Python object.

    "created_at":"Thu Apr 06 15:24:15 +0000 2017"
    
    """
    datetime_string = json["created_at"]
    datetime_with_tz = datetime.strptime(datetime_string, "%a %b %d %H:%M:%S %z %Y")
    datetime_in_utc = datetime_with_tz.astimezone(pytz.utc)
    return datetime_in_utc