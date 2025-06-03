from datetime import datetime, timedelta


def make(start: datetime, end: datetime = None):
    return (start, end or datetime.now())


def count_hours(start: datetime, end: datetime):
    diff = end - start
    return (diff.days * 24) + (diff.seconds // 3600)


def hourly_timestamp(start: datetime, end: datetime):
    timestamps = [start + timedelta(hours=hour) for hour in range(count_hours(start, end))]
    timestamps.append(end)
    return timestamps


def split_by_hour(start: datetime, end: datetime):
    timestamps = hourly_timestamp(start, end)
    return zip(timestamps, timestamps[1:])