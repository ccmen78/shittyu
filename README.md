# StudyPlan (Group 78)
**StudyPlan** is a local CLI app and Python API designed for AI Agents to help students organize assignment deadlines, plan study time, track courses, and estimate GPA. 

## 👥 Team Members (Group 78)

* **[ZHU ZIWEN(ccmen78)]** - Core Logic (GPA)& Documentation
* **[HUNG TSZ KIT]** - Planner & Algorithm & debug
* **[Name 3]** - Storage & File I/O
* **[Name 4]** - CLI Interface
* **[Name 5]** - Packaging & Init
* **[Name 6]** - Demo & testing

## 💡 Motivation & Innovation
Traditional planners require manual UI interactions. **StudyPlan** is built for the **Agentic Coding** era. By providing a clean Python API and local JSON storage, an LLM Agent can easily call `studyplan.suggest_study_plan()` to generate personalized schedules for students while ensuring complete data privacy (data stays local in `~/.studyplan/data.json`).

## 🚀 Installation
```bash
pip install studyplan-group78

## 💻 CLI Usage
# Initialize term end date
studyplan init 2026-12-31

# Add an assignment
studyplan add "CS1302 Project" --due 2026-11-20 --est 120 --prio High

# Get a suggested study plan (e.g., 90 minutes available today)
studyplan plan --mins 90

# Add course and calculate GPA
studyplan add-course "Calculus" --credits 4 --grade A
studyplan calc-gpa

##🐍 Python API Usage (For AI Agents)
import studyplan

# Generate study plan
tasks = [

    {
        "name": "Essay",
        "due_date": "2026-11-20",
        "est_minutes": 90,
        "priority": "High"
    },

    {
        "name": "Math Homework",
        "due_date": "2026-11-25",
        "est_minutes": 60,
        "priority": "Medium"
    }

]

plan = studyplan.suggest_study_plan(
    tasks,
    available_minutes=120
)

print(plan)

# Calculate GPA
courses = [{"name": "CS", "credits": 4, "grade": "A"}]
gpa = studyplan.calculate_gpa(courses)
print(gpa)

#📅 Exam Countdown
#Calculate the number of days remaining until upcoming exams.

days = studyplan.exam_countdown(
    "2026-12-20"
)

print(days)

#❓ Quiz Generator
#Generate flashcard-style quiz questions from study notes.

notes = {
    "Accounts Receivable":
    "Money owed by customers"}

quiz = studyplan.create_quiz(
    notes)

print(quiz)


