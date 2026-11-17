# studyplan/gpa.py

# Simple mapping of letter grades to GPA points
GRADE_POINTS = {
    "A+": 4.3, "A": 4.0, "A-": 3.7,
    "B+": 3.3, "B": 3.0, "B-": 2.7,
    "C+": 2.3, "C": 2.0, "C-": 1.7,
    "D": 1.0, "F": 0.0
}

def calculate_gpa(courses, prev_gpa=0.0, prev_credits=0.0):
    """Calculate the credit-weighted GPA."""
    total_credits = prev_credits
    total_points = prev_gpa * prev_credits

    for course in courses:
        grade = str(course.get("grade", "F")).upper()
        credits = float(course.get("credits", 0))
        points = GRADE_POINTS.get(grade, 0.0)
        
        total_credits += credits
        total_points += points * credits

    if total_credits == 0:
        return 0.0
    
    return round(total_points / total_credits, 2)
