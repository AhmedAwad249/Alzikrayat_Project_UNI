from datetime import datetime, timezone


def timeAgo(value):
    """Convert a datetime into relative time. like (3 days ago, 4 hours ago)"""

    if not value:
        return ""

    if isinstance(value, str):
        try:
            value = datetime.fromisoformat(value)
        except ValueError:
            return value

    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)

    now = datetime.now(timezone.utc)
    seconds = int((now - value).total_seconds())

    if seconds < 60:
        return "just now"

    minutes = seconds // 60

    if minutes < 60:
        return (
            "1 minute ago"
            if minutes == 1
            else f"{minutes} minutes ago"
        )

    hours = minutes // 60

    if hours < 24:
        return (
            "1 hour ago"
            if hours == 1
            else f"{hours} hours ago"
        )

    days = hours // 24

    if days < 7:
        return (
            "1 day ago"
            if days == 1
            else f"{days} days ago"
        )

    weeks = days // 7

    if days < 30:
        return (
            "1 week ago"
            if weeks == 1
            else f"{weeks} weeks ago"
        )

    months = days // 30

    if days < 365:
        return (
            "1 month ago"
            if months == 1
            else f"{months} months ago"
        )

    years = days // 365

    return (
        "1 year ago"
        if years == 1
        else f"{years} years ago"
    )