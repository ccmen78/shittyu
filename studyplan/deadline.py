from datetime import date


def days_left(deadline):
    """
    Calculate the number of days
    remaining before a deadline.
    """

    target = date.fromisoformat(deadline)

    return (target - date.today()).days


def urgency_level(deadline):
    """
    Determine deadline urgency level.
    """

    days = days_left(deadline)

    if days <= 3:
        return "High Priority"

    elif days <= 7:
        return "Medium Priority"

    else:
        return "Low Priority"
