from datetime import date


def exam_countdown(exam_date):
    """
    Calculate the number of days remaining
    until an exam.

    Parameters
    ----------
    exam_date : str
        Date in YYYY-MM-DD format

    Returns
    -------
    int
        Days remaining until the exam
    """

    exam = date.fromisoformat(exam_date)

    return (exam - date.today()).days
