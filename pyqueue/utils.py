"""
General purpose utility library..
"""
from string import Template


class DeltaTemplate(Template):
    """
    Template for formatting timedelta
    """
    delimiter = "%"


def strfdelta(tdelta, fmt):
    """
    Used to format `datetime.timedelta` objects. Works just like `strftime`

    >>> strfdelta(duration, '%H:%M:%S')

    param tdelta: Time duration which is an instance of datetime.timedelta
    param fmt: The pattern to format the timedelta with
    returns: str
    """
    substitutes = dict()
    hours, rem = divmod(tdelta.total_seconds(), 3600)
    minutes, seconds = divmod(rem, 60)

    substitutes["H"] = '{:02d}'.format(int(hours))
    substitutes["M"] = '{:02d}'.format(int(minutes))
    substitutes["S"] = '{:02d}'.format(int(seconds))
    return DeltaTemplate(fmt).substitute(**substitutes)
