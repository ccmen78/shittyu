def create_quiz(notes):
    """
    Generate quiz questions
    from study notes.

    Parameters
    ----------
    notes : dict

    Returns
    -------
    list
    """

    quiz = []

    for topic, definition in notes.items():

        quiz.append({
            "question": f"What is {topic}?",
            "answer": definition
        })

    return quiz
