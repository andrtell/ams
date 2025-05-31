from datetime import datetime

from src import period


def format_datetime(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%S")


def with_search(q, search_term):
    return {**q, "q": search_term}


def with_after(q, after):
    return {**q, "published-after": format_datetime(after)}


def with_before(q, before):
    return {**q, "published-before": format_datetime(before)}


def with_offset(q, offset):
    return {**q, "offset": offset}


def with_limit(q, limit):
    return {**q, "limit": limit}


def update_query(q, search=None, after=None, before=None, offset=None, limit=None):
    if search is not None:
        q = with_search(q, search)

    if after is not None:
        q = with_after(q, after)

    if before is not None:
        q = with_before(q, before)

    if offset is not None:
        q = with_offset(q, offset)

    if limit is not None:
        q = with_limit(q, limit)

    return q


def next_page(q):
    return with_offset(q, q["offset"] + q["limit"])


def new_query(**kwargs):
    return update_query({}, **kwargs)


def to_intervals(q, date_intervals):
    for after, before in date_intervals:
        yield update_query(q, after=after, before=before)


def past_hours(hours=1, **kwargs):
    return to_intervals(new_query(**kwargs), period.new_date_intervals(period.hours_ago(hours), period.now()))


def past_days(days=1, **kwargs):
    return to_intervals(new_query(**kwargs), period.new_date_intervals(period.days_ago(days), period.now()))


def past_weeks(weeks=1, **kwargs):
    return to_intervals(new_query(**kwargs), period.new_date_intervals( period.weeks_ago(weeks), period.now()))
