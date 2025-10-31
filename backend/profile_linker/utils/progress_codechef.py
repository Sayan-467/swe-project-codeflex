def calculate_progress_codechef(rating, problem_difficulty, hints_used):
    """
    Calculates progress for CodeChef users based on:
    - rating: current user rating
    - problem_difficulty: problem rating
    - hints_used: number of hints used
    """
    if not rating or not problem_difficulty:
        return 0.0, "Insufficient data to calculate progress."

    # Ratio of problem difficulty to user's rating
    difficulty_ratio = problem_difficulty / rating
    difficulty_ratio = max(0.1, min(1.5, difficulty_ratio))

    base_score = difficulty_ratio
    penalty = 0.15 * hints_used

    score = base_score - penalty
    score = max(0.0, min(1.0, score))

    if score >= 0.8:
        feedback = "Fantastic! Great problem for your skill level."
    elif score >= 0.5:
        feedback = "Good progress. Try fewer hints next time."
    else:
        feedback = "Keep practicing — focus on easier problems first."

    return round(score, 2), feedback
