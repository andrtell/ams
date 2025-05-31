from datetime import datetime, timedelta


def now():
    return datetime.now()


def hours_ago(hours=1):
    return datetime.now() - timedelta(hours=hours)


def days_ago(days=1):
    return datetime.now() - timedelta(days=days)


def weeks_ago(weeks=1):
    return datetime.now() - timedelta(weeks=weeks)


def new_date_range(after, before):
    curr = after
    while curr < before - timedelta(hours=1):
        yield curr
        curr += timedelta(hours=1)
    yield before


def new_date_intervals(after, before):
    range = list(new_date_range(after, before))
    return zip(range, range[1:])
