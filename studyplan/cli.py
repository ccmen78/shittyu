# studyplan/cli.py

import argparse
from datetime import datetime

from rich.console import Console
from rich.table import Table

from studyplan import gpa
from studyplan import planner
from studyplan import storage
from studyplan import exam
from studyplan import quiz

console = Console()


def validate_date(date_string):
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def main():

    parser = argparse.ArgumentParser(
        description="StudyPlan - A local CLI assistant"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        help="Sub-commands"
    )

    # --------------------
    # init
    # --------------------

    parser_init = subparsers.add_parser(
        "init",
        help="Set the end date of the term"
    )

    parser_init.add_argument(
        "date",
        help="Date format: YYYY-MM-DD"
    )

    # --------------------
    # add assignment
    # --------------------

    parser_add = subparsers.add_parser(
        "add",
        help="Add a new assignment"
    )

    parser_add.add_argument(
        "name",
        help="Assignment name"
    )

    parser_add.add_argument(
        "--due",
        required=True,
        help="Due date YYYY-MM-DD"
    )

    parser_add.add_argument(
        "--est",
        type=int,
        default=60,
        help="Estimated time (minutes)"
    )

    parser_add.add_argument(
        "--prio",
        choices=["High", "Medium", "Low"],
        default="Medium",
        help="Priority"
    )

    # --------------------
    # study plan
    # --------------------

    parser_plan = subparsers.add_parser(
        "plan",
        help="Get a suggested study plan"
    )

    parser_plan.add_argument(
        "--mins",
        type=int,
        default=120,
        help="Available study time"
    )

    # --------------------
    # GPA
    # --------------------

    parser_gpa = subparsers.add_parser(
        "add-course",
        help="Add a course grade"
    )

    parser_gpa.add_argument(
        "name",
        help="Course name"
    )

    parser_gpa.add_argument(
        "--credits",
        type=float,
        required=True,
        help="Credits"
    )

    parser_gpa.add_argument(
        "--grade",
        required=True,
        help="Grade (e.g., A, B+)"
    )

    parser_calc = subparsers.add_parser(
        "calc-gpa",
        help="Calculate current GPA"
    )

    # --------------------
    # Exam Countdown
    # --------------------

    parser_exam = subparsers.add_parser(
        "exam",
        help="Calculate exam countdown"
    )

    parser_exam.add_argument(
        "--date",
        required=True,
        help="Exam date (YYYY-MM-DD)"
    )

    # --------------------
    # Quiz Generator
    # --------------------

    parser_quiz = subparsers.add_parser(
        "quiz",
        help="Generate quiz questions"
    )

    # --------------------
    # Parse arguments
    # --------------------

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return

    data = storage.load_data()

    # --------------------
    # init
    # --------------------

    if args.command == "init":

        if not validate_date(args.date):
            console.print(
                "[red]Invalid date format. Use YYYY-MM-DD[/red]"
            )
            return

        data["term_end_date"] = args.date

        storage.save_data(data)

        console.print(
            f"[green]✔ Term end date set to {args.date}[/green]"
        )

    # --------------------
    # add assignment
    # --------------------

    elif args.command == "add":

        if not validate_date(args.due):
            console.print(
                "[red]Invalid due date format[/red]"
            )
            return

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

    # --------------------
    # study plan
    # --------------------

    elif args.command == "plan":

        assignments = data.get(
            "assignments",
            []
        )

        plan = planner.suggest_study_plan(
            assignments,
            args.mins
        )

        if not plan:
            console.print(
                "[yellow]No pending assignments.[/yellow]"
            )
            return

        table = Table(
            title=f"Suggested Study Plan ({args.mins} mins)"
        )

        table.add_column(
            "Task Name",
            style="cyan"
        )

        table.add_column(
            "Due Date",
            style="magenta"
        )

        table.add_column(
            "Time",
            justify="right",
            style="green"
        )

        for p in plan:

            table.add_row(
                p["task_name"],
                p["due_date"],
                f"{p['allocated_minutes']} mins"
            )

        console.print(table)

    # --------------------
    # add course
    # --------------------

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

    # --------------------
    # calculate GPA
    # --------------------

    elif args.command == "calc-gpa":

        current_gpa = gpa.calculate_gpa(
            data.get("courses", []),
            data.get("prev_gpa", 0),
            data.get("prev_credits", 0)
        )

        console.print(
            f"[bold green]Estimated GPA: {current_gpa}[/bold green]"
        )

    # --------------------
    # exam countdown
    # --------------------

    elif args.command == "exam":

        if not validate_date(args.date):
            console.print(
                "[red]Invalid date format[/red]"
            )
            return

        days = exam.exam_countdown(
            args.date
        )

        console.print(
            f"[bold blue]{days} days remaining[/bold blue]"
        )

    # --------------------
    # quiz generator
    # --------------------

    elif args.command == "quiz":

        sample_notes = {
            "Accounts Receivable":
            "Money owed by customers",

            "Demand":
            "Relationship between price and quantity demanded"
        }

        questions = quiz.create_quiz(
            sample_notes
        )

        for q in questions:
            console.print(q)


if __name__ == "__main__":
    main()
