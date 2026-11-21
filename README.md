# StudyPlan (Group 78)
**StudyPlan** is a local CLI app and Python API designed for AI Agents to help students organize assignment deadlines, plan study time, track courses, and estimate GPA. 

## 👥 Team Members (Group 78)

* **[ZHU ZIWEN]** - Core Logic (GPA) ,Documentation 
* **[MA CHINGHONG]** - Planner & Algorithm 
* **[WILLIAM LIU]** - Storage & File I/O 
* **[HUNG TSZKIT]** - CLI Interface, debug & Init
* **[WU ZIHAN]** - Packaging & testing

## 💡 Motivation & Innovation
Traditional planners require manual UI interactions. **StudyPlan** is built for the **Agentic Coding** era. By providing a clean Python API and local JSON storage, an LLM Agent can easily call `studyplan.suggest_study_plan()` to generate personalized schedules for students while ensuring complete data privacy (data stays local in `~/.studyplan/data.json`).

## 🚀 Installation
```bash
pip install studyplan-group78

##💻 CLI Usage
#Initialize Term End Date
studyplan init 2026-12-31

#Add Assignment
studyplan add "CS1302 Project" --due 2026-11-20 --est 120 --prio High

#Generate Study Plan
studyplan plan --mins 90

Example Output
┏━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ Task Name        ┃ Due Date   ┃ Time     ┃
┣━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━╋━━━━━━━━━━┫
┃ CS1302 Project   ┃ 2026-11-20 ┃ 90 mins  ┃
┗━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━┻━━━━━━━━━━┛

#Add Course
studyplan add-course "Calculus" --credits 4 --grade A

#Calculate GPA
studyplan calc-gpa

Example Output
Estimated GPA: 4.0

#Homework Deadline Manager
studyplan deadline --date 2026-12-01

Example Output
Days Remaining: 19
Priority: Low Priority

#Exam Countdown
studyplan exam --date 2026-12-20

Example Output
38 days remaining

#Quiz Generator
studyplan quiz

Example Output
Q: What is Demand?
A: Relationship between price and quantity demanded

#Study Timer
studyplan add-time 120
studyplan study-hours

Example Output
Total Study Hours: 2.0

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

#📚 Homework Deadline Manager
#Track assignment deadlines and determine task urgency.

days = studyplan.days_left(
    "2026-12-01"
)

print(days)
Output
19
Check Urgency
import studyplan

priority = studyplan.urgency_level(
    "2026-11-15"
)

print(priority)
Output
High Priority

Priority Levels
Days Remaining	Priority
0 – 3	High Priority
4 – 7	Medium Priority
More than 7	Low Priority
Use Case
Students can identify urgent assignments and better manage their study schedules.

#⏱ Study Timer
#Track study sessions and monitor productivity.

session = studyplan.StudySession()

session.add_time(120)

print(session.total_hours())

Output
2.0

Multiple Study Sessions
import studyplan

session = studyplan.StudySession()

session.add_time(60)
session.add_time(45)
session.add_time(30)

print(session.total_minutes())
print(session.total_hours())

Output
135

2.25
Use Case
Students can record study sessions and monitor how much time they spend studying.



