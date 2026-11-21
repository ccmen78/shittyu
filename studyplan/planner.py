from datetime import date


def suggest_study_plan(
    assignments,
    available_minutes
):
    """
    Suggest a study plan based on
    due dates and priorities.

    Parameters
    ----------
    assignments : list
        List of assignment dictionaries

    available_minutes : int
        Available study time

    Returns
    -------
    list
        Suggested study plan
    """

    if available_minutes <= 0:
        return []

    pending = [

        task

        for task in assignments

        if not task.get(
            "completed",
            False
        )

    ]

    priority_weight = {

        "High": 3,
        "Medium": 2,
        "Low": 1

    }

    pending.sort(

        key=lambda task: (

            task.get(
                "due_date",
                "9999-12-31"
            ),

            -priority_weight.get(
                task.get(
                    "priority",
                    "Low"
                ),
                1
            )

        )

    )

    plan = []

    remaining_time = available_minutes

    for task in pending:

        if remaining_time <= 0:
            break

        est_time = max(

            task.get(
                "est_minutes",
                30
            ),

            0

        )

        allocated_time = min(
            est_time,
            remaining_time
        )

        plan.append({

            "task_name":
            task.get(
                "name",
                "Untitled Task"
            ),

            "due_date":
            task.get(
                "due_date",
                "Unknown"
            ),

            "allocated_minutes":
            allocated_time

        })

        remaining_time -= allocated_time

    return plan
