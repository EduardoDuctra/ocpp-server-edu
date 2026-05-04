from pytz import timezone, utc
from datetime import datetime


def localTimeZone(*args):
    utc_dt = utc.localize(datetime.utcnow())
    my_tz = timezone("America/Sao_Paulo")
    converted = utc_dt.astimezone(my_tz)
    return converted.timetuple()


def localTimeZoneString():
    utc_dt = utc.localize(datetime.utcnow())
    my_tz = timezone("America/Sao_Paulo")
    converted = utc_dt.astimezone(my_tz)
    return converted.strftime('%d/%m/%Y-%H:%M:%Ss')