import argparse
from datetime import datetime

from rich.console import Console
from rich.table import Table

from studyplan import (
    gpa,
    planner,
    storage,
    exam,
    quiz,
    deadline
)

from studyplan.timer import StudySession

console = Console()


def validate_date(date_string):
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def main():

    parser = argparse.ArgumentParser(
        description="StudyPlan - Student Productivity Toolkit"
    )

    subparsers = parser.add_subparsers(
        dest="command"
    )

    # -------------------
    # Init
    # -------------------

    parser_init = subparsers.add_parser(
        "init",
        help="Set term end date"
    )

    parser_init.add_argument(
        "date"
    )

    # -------------------
    # Assignment
    # -------------------

    parser_add = subparsers.add_parser(
        "add",
        help="Add assignment"
    )

    parser_add.add_argument(
        "name"
    )

    parser_add.add_argument(
        "--due",
        required=True
    )

    parser_add.add_argument(
        "--est",
        type=int,
        default=60
    )

    parser_add.add_argument(
        "--prio",
        choices=["High", "Medium", "Low"],
        default="Medium"
    )

    # -------------------
    # Planner
    # -------------------

    parser_plan = subparsers.add_parser(
        "plan",
        help="Generate study plan"
    )

    parser_plan.add_argument(
        "--mins",
        type=int,
        default=120
    )

    # -------------------
    # GPA
    # -------------------

    parser_course = subparsers.add_parser(
        "add-course",
        help="Add course"
    )

    parser_course.add_argument(
        "name"
    )

    parser_course.add_argument(
        "--credits",
        type=float,
        required=True
    )

    parser_course.add_argument(
        "--grade",
        required=True
    )

    subparsers.add_parser(
        "calc-gpa",
        help="Calculate GPA"
    )

    # -------------------
    # Exam Countdown
    # -------------------

    parser_exam = subparsers.add_parser(
        "exam",
        help="Exam countdown"
    )

    parser_exam.add_argument(
        "--date",
        required=True
    )

    # -------------------
    # Homework Deadline
    # -------------------

    parser_deadline = subparsers.add_parser(
        "deadline",
        help="Check deadline"
    )

    parser_deadline.add_argument(
        "--date",
        required=True
    )

    # -------------------
    # Quiz Generator
    # -------------------

    subparsers.add_parser(
        "quiz",
        help="Generate quiz"
    )

    # -------------------
    # Study Timer
    # -------------------

    parser_time = subparsers.add_parser(
        "add-time",
        help="Add study minutes"
    )

    parser_time.add_argument(
        "minutes",
        type=int
    )

    subparsers.add_parser(
        "study-hours",
        help="Show total study hours"
    )

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return

    data = storage.load_data()

    # -------------------
    # Init
    # -------------------

    if args.command == "init":

        if not validate_date(args.date):
            console.print(
                "[red]Invalid date format[/red]"
            )
            return

        data["term_end_date"] = args.date

        storage.save_data(data)

        console.print(
            f"[green]✔ Term end date set to {args.date}[/green]"
        )

    # -------------------
    # Add Assignment
    # -------------------

    elif args.command == "add":

        assignments = data.get(
            "assignments",
            []
        )

        assignments.append({
            "name": args.name,
            "due_date": args.due,
            "est_minutes": args.est,
            "priority": args.prio,
            "completed": False
        })

        data["assignments"] = assignments

        storage.save_data(data)

        console.print(
            f"[green]✔ Added assignment: {args.name}[/green]"
        )

    # -------------------
    # Study Plan
    # -------------------

    elif args.command == "plan":

        plan = planner.suggest_study_plan(
            data.get("assignments", []),
            args.mins
        )

        table = Table(
            title="Suggested Study Plan"
        )

        table.add_column("Task")
        table.add_column("Due Date")
        table.add_column("Minutes")

        for item in plan:

            table.add_row(
                item["task_name"],
                item["due_date"],
                str(item["allocated_minutes"])
            )

        console.print(table)

    # -------------------
    # Add Course
    # -------------------

    elif args.command == "add-course":

        courses = data.get(
            "courses",
            []
        )

        courses.append({
            "name": args.name,
            "credits": args.credits,
            "grade": args.grade
        })

        data["courses"] = courses

        storage.save_data(data)

        console.print(
            f"[green]✔ Added course: {args.name}[/green]"
        )

    # -------------------
    # Calculate GPA
    # -------------------

    elif args.command == "calc-gpa":

        result = gpa.calculate_gpa(
            data.get("courses", [])
        )

        console.print(
            f"[bold green]GPA: {result}[/bold green]"
        )

    # -------------------
    # Exam Countdown
    # -------------------

    elif args.command == "exam":

        days = exam.exam_countdown(
            args.date
        )

        console.print(
            f"[blue]{days} days remaining[/blue]"
        )

    # -------------------
    # Homework Deadline
    # -------------------

    elif args.command == "deadline":

        days = deadline.days_left(
            args.date
        )

        priority = deadline.urgency_level(
            args.date
        )

        console.print(
            f"Days Remaining: {days}"
        )

        console.print(
            f"Priority: {priority}"
        )

    # -------------------
    # Quiz Generator
    # -------------------

    elif args.command == "quiz":

        notes = {
            "Demand":
            "Relationship between price and quantity demanded",

            "Accounts Receivable":
            "Money owed by customers"
        }

        result = quiz.create_quiz(
            notes
        )

        console.print(result)

    # -------------------
    # Add Study Time
    # -------------------

    elif args.command == "add-time":

        data["study_minutes"] = (
            data.get(
                "study_minutes",
                0
            )
            + args.minutes
        )

        storage.save_data(data)

        console.print(
            f"[green]Added {args.minutes} minutes[/green]"
        )

    # -------------------
    # Show Total Hours
    # -------------------

    elif args.command == "study-hours":

        session = StudySession()

        session.add_time(
            data.get(
                "study_minutes",
                0
            )
        )

        console.print(
            f"[bold green]Total Study Hours: "
            f"{session.total_hours()}[/bold green]"
        )


if __name__ == "__main__":
    main()
