from flask import Flask, jsonify, request
from datetime import datetime
from utils.codeforces_api import fetch_codeforces_profile
from utils.codechef_scraper import fetch_codechef_profile
import sqlite3
import os

app = Flask(__name__)

DB_PATH = "progress.db"


# -------------------------
# 📦 Database Setup
# -------------------------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        platform TEXT,
        handle TEXT,
        problem_rating INTEGER,
        hints_used INTEGER,
        progress_score REAL,
        feedback TEXT,
        timestamp TEXT
    )
    """)
    conn.commit()
    conn.close()


def save_progress(platform, handle, problem_rating, hints_used, progress_score, feedback):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO progress (platform, handle, problem_rating, hints_used, progress_score, feedback, timestamp)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (platform, handle, problem_rating, hints_used, progress_score, feedback,
          datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()


def fetch_progress_history(handle, platform):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT timestamp, progress_score FROM progress
    WHERE handle=? AND platform=?
    ORDER BY timestamp ASC
    """, (handle, platform))
    rows = cursor.fetchall()
    conn.close()
    return [{"timestamp": r[0], "score": r[1]} for r in rows]


# -------------------------
# 🧠 Progress Calculations
# -------------------------
def calculate_progress_codeforces(rating, problem_rating, hints_used):
    if not rating or not problem_rating:
        return 0.0, "Insufficient data to calculate progress."

    difficulty_ratio = problem_rating / rating
    difficulty_ratio = max(0.1, min(1.5, difficulty_ratio))
    base_score = difficulty_ratio
    penalty = 0.15 * hints_used
    score = base_score - penalty
    score = max(0.0, min(1.0, score))

    if score >= 0.8:
        feedback = "Excellent! You solved a tough problem efficiently."
    elif score >= 0.5:
        feedback = "Good effort! Try reducing hint usage for better mastery."
    else:
        feedback = "Keep practicing simpler problems before moving up."

    return round(score, 2), feedback


def calculate_progress_codechef(global_rank, problem_rating, hints_used):
    if not global_rank or not problem_rating:
        return 0.0, "Insufficient data to calculate progress."

    skill_factor = max(1, 50000 / global_rank)
    difficulty_ratio = problem_rating / (skill_factor * 100)
    difficulty_ratio = max(0.1, min(1.5, difficulty_ratio))

    base_score = difficulty_ratio
    penalty = 0.15 * hints_used
    score = base_score - penalty
    score = max(0.0, min(1.0, score))

    if score >= 0.8:
        feedback = "Outstanding! You handled a challenging problem very well."
    elif score >= 0.5:
        feedback = "Good progress! Try solving with fewer hints next time."
    else:
        feedback = "Keep working on improving your problem-solving consistency."

    return round(score, 2), feedback


# -------------------------
# 🌐 Endpoints
# -------------------------
@app.route('/progress/codeforces', methods=['POST'])
def progress_codeforces():
    data = request.json
    handle = data.get("handle")
    problem_rating = data.get("problem_rating")
    hints_used = data.get("hints_used", 0)

    user_data = fetch_codeforces_profile(handle)
    if not user_data or not user_data.get("rating"):
        return jsonify({"error": "Invalid Codeforces handle"}), 400

    progress_score, feedback = calculate_progress_codeforces(
        user_data["rating"], problem_rating, hints_used
    )

    save_progress("codeforces", handle, problem_rating, hints_used, progress_score, feedback)
    history = fetch_progress_history(handle, "codeforces")

    return jsonify({
        "platform": "codeforces",
        "user": user_data,
        "problem_rating": problem_rating,
        "hints_used": hints_used,
        "progress_score": progress_score,
        "feedback": feedback,
        "history": history
    })


@app.route('/progress/codechef', methods=['POST'])
def progress_codechef():
    data = request.json
    handle = data.get("handle")
    problem_rating = data.get("problem_rating")
    hints_used = data.get("hints_used", 0)

    user_data = fetch_codechef_profile(handle)
    if not user_data or not user_data.get("global_rank"):
        return jsonify({"error": "Invalid CodeChef handle"}), 400

    global_rank = int(user_data["global_rank"])
    progress_score, feedback = calculate_progress_codechef(global_rank, problem_rating, hints_used)

    save_progress("codechef", handle, problem_rating, hints_used, progress_score, feedback)
    history = fetch_progress_history(handle, "codechef")

    return jsonify({
        "platform": "codechef",
        "user": user_data,
        "problem_rating": problem_rating,
        "hints_used": hints_used,
        "progress_score": progress_score,
        "feedback": feedback,
        "history": history
    })


# -------------------------
# 📈 Progress Graph Endpoint
# -------------------------
@app.route('/progress/history/<platform>/<handle>', methods=['GET'])
def get_progress_history(platform, handle):
    history = fetch_progress_history(handle, platform)
    if not history:
        return jsonify({"error": "No progress data found."}), 404
    return jsonify({
        "platform": platform,
        "handle": handle,
        "history": history
    })


# -------------------------
# 🏁 Run App
# -------------------------
if __name__ == "__main__":
    init_db()
    app.run(debug=True)