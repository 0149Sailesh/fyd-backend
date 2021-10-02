from datetime import datetime


def convertDateToISOFormat(date: datetime):
    """Converts the given datetime obj to a
    ISO format string with Z and T"""
    return date.strftime("%Y-%m-%dT%H:%M:%SZ")
