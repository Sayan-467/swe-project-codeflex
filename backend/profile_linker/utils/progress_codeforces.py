def calculate_progress_codeforces(current_rating, problem_rating, hints_used):
    """
    Calculates Codeforces progress:
    - current_rating: user's current rating
    - problem_rating: difficulty of the problem
    - hints_used: number of hints used
    """

    # Validation
    if current_rating <= 0 or problem_rating <= 0:
        return 0.0, "Insufficient data to calculate progress."

    # Difficulty ratio (clamped)
    difficulty_ratio = problem_rating / current_rating
    difficulty_ratio = max(0.3, min(2.0, difficulty_ratio))

    # Base progress curve:
    #   Easier problem (<1x rating) gives partial progress
    #   Equal difficulty gives ~0.6
    #   Harder problem (>1.5x rating) gives near 1.0
    if difficulty_ratio < 1:
        base_score = 0.4 * difficulty_ratio + 0.2
    else:
        base_score = min(1.0, 0.6 + 0.3 * (difficulty_ratio - 1))

    # Penalty per hint
    penalty = 0.1 * hints_used
    score = base_score - penalty

    # Clamp to [0, 1]
    score = max(0.0, min(1.0, score))

    # Feedback
    if score >= 0.8:
        feedback = "🔥 Excellent! You tackled a tough problem confidently."
    elif score >= 0.5:
        feedback = "💪 Nice work! Try reducing hints for better mastery."
    elif score > 0:
        feedback = "📘 Keep practicing — focus on problems near your rating."
    else:
        feedback = "❗ Too many hints or too easy. Try a tougher one!"

    return round(score, 2), feedback
