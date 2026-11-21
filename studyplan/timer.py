class StudySession:
    """
    Track study time in minutes
    and convert it to hours.
    """

    def __init__(self):
        self.minutes = 0

    def add_time(self, minutes):

        if minutes < 0:
            raise ValueError(
                "Minutes cannot be negative."
            )

        self.minutes += minutes

    def total_minutes(self):
        return self.minutes

    def total_hours(self):
        return round(
            self.minutes / 60,
            2
        )
