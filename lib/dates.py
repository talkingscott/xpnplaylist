"""Date manipulations."""

from typing import Generator

DAYS_IN_MONTH = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def _days_in_month(month_0: int, year: int) -> int:
    """ Returns days in a month (0-indexed).  Hope I got this right. """
    if month_0 != 1:
        return DAYS_IN_MONTH[month_0]
    if (year % 4) == 0 and ((year % 100) != 0 or (year % 400) == 0):
        return DAYS_IN_MONTH[month_0] + 1
    return DAYS_IN_MONTH[month_0]


def dates_for_datespec(datespec: str) -> Generator[str, None, None]:
    """Get all dates for a date spec (yyyy or yyyy-mm or yyyy-mm-dd)."""
    if len(datespec) == 10:
        yield datespec
    elif len(datespec) == 7:
        month0 = int(datespec[5:]) - 1
        year = int(datespec[:4])
        for day0 in range(_days_in_month(month0, year)):
            yield datespec + '-' + ('%02d' % (day0 + 1))
    elif len(datespec) == 4:
        year = int(datespec)
        for month0 in range(12):
            for day0 in range(_days_in_month(month0, year)):
                yield datespec + '-' + ('%02d' % (month0 + 1)) + '-' + ('%02d' % (day0 + 1))
