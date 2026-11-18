# studyplan/cli.py
import argparse
from rich.console import Console
from rich.table import Table
from studyplan import gpa, planner, storage

console = Console()

def main():
    parser = argparse.ArgumentParser(description="StudyPlan - A local CLI assistant")
    subparsers = parser.add_subparsers(dest="command", help="Sub-commands")

    # init
    parser_init = subparsers.add_parser("init", help="Set the end date of the term")
    parser_init.add_argument("date", help="Date format: YYYY-MM-DD")

    # add
    parser_add = subparsers.add_parser("add", help="Add a new assignment")
    parser_add.add_argument("name", help="Assignment name")
    parser_add.add_argument("--due", required=True, help="Due date YYYY-MM-DD")
    parser_add.add_argument("--est", type=int, default=60, help="Estimated time (minutes)")
    parser_add.add_argument("--prio", choices=["High", "Medium", "Low"], default="Medium", help="Priority")

    # plan
    parser_plan = subparsers.add_parser("plan", help="Get a suggested study plan")
    parser_plan.add_argument("--mins", type=int, default=120, help="Available study time")

    # add-course & calc-gpa
    parser_gpa = subparsers.add_parser("add-course", help="Add a course grade")
    parser_gpa.add_argument("name", help="Course name")
    parser_gpa.add_argument("--credits", type=float, required=True, help="Credits")
    parser_gpa.add_argument("--grade", required=True, help="Grade (e.g., A, B+)")

    parser_calc = subparsers.add_parser("calc-gpa", help="Calculate current GPA")

    args = parser.parse_args()
    data = storage.load_data()

    if args.command == "init":
        data["term_end_date"] = args.date
        storage.save_data(data)
        console.print(f"[green]✔️ Term end date set to {args.date}[/green]")

    elif args.command == "add":
        data["assignments"].append({
            "name": args.name, "due_date": args.due, 
            "est_minutes": args.est, "priority": args.prio, "completed": False
        })
        storage.save_data(data)
        console.print(f"[green]✔️ Added assignment: {args.name}[/green]")

    elif args.command == "plan":
        plan = planner.suggest_study_plan(data["assignments"], args.mins)
        if not plan:
            console.print("[yellow]No pending assignments.[/yellow]")
            return
        table = Table(title=f"Suggested Study Plan (Total {args.mins} mins)")
        table.add_column("Task Name", style="cyan")
        table.add_column("Due Date", style="magenta")
        table.add_column("Time", justify="right", style="green")
        for p in plan:
            table.add_row(p["task_name"], p["due_date"], f"{p['allocated_minutes']} mins")
        console.print(table)

    elif args.command == "add-course":
        data["courses"].append({"name": args.name, "credits": args.credits, "grade": args.grade})
        storage.save_data(data)
        console.print(f"[green]✔️ Added course: {args.name}[/green]")

    elif args.command == "calc-gpa":
        current_gpa = gpa.calculate_gpa(data["courses"], data["prev_gpa"], data["prev_credits"])
        console.print(f"[bold green]Estimated GPA: {current_gpa}[/bold green]")

if _name_ == "_main_":
    main()
