# studyplan/planner.py

def suggest_study_plan(assignments, available_minutes):
    """Suggest a study plan based on due dates and priorities."""
    pending = [a for a in assignments if not a.get("completed", False)]
    priority_weight = {"High": 3, "Medium": 2, "Low": 1}
    
    # Sort by due date then priority
    pending.sort(key=lambda x: (x.get("due_date", "9999-12-31"), -priority_weight.get(x.get("priority", "Low"), 1)))
    
    plan = []
    remaining_time = available_minutes
    
    for task in pending:
        if remaining_time <= 0:
            break
            
        est_time = task.get("est_minutes", 30)
        allocated_time = min(est_time, remaining_time)
        
        plan.append({
            "task_name": task["name"],
            "due_date": task.get("due_date", "Unknown"),
            "allocated_minutes": allocated_time
        })
        
        remaining_time -= allocated_time
        
    return plan
