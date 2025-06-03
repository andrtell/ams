from datetime import datetime, timedelta


def hour(count: int):
    return datetime.now() - timedelta(hours=count)


def day(count: int):
    return datetime.now() - timedelta(days=count)


def week(count: int):
    return datetime.now() - timedelta(weeks=count)
