from datetime import datetime, timedelta


def hours_ago(hours):
    return datetime.now() - timedelta(hours=hours)


def days_ago(days):
    return datetime.now() - timedelta(days=days)


def flatten(v):
    items = []

    def walk(p, path):
        pre = f"{path}." if path else ""
        match p:
            case dict():
                for k, c in p.items():
                    walk(c, f"{pre}{k}")
            case list():
                for i, c in enumerate(p):
                    walk(c, f"{pre}{i}")
            case _:
                items.append((path, p))

    walk(v, "")

    return items
