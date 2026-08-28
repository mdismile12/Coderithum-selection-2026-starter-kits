import sqlite3
import jwt
from flask import Flask, request, jsonify, render_template_string, redirect, url_for

app = Flask(__name__)
JWT_SECRET = "secret123"  # Flaw 4: Hardcoded Weak Secret

# Initialize SQLite in-memory database with pre-seeded vulnerable data
def init_db():
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, email TEXT, role TEXT, secret_note TEXT)")
    cursor.execute("CREATE TABLE feedback (id INTEGER PRIMARY KEY, author TEXT, comment TEXT)")
    
    # Seed data
    cursor.execute("INSERT INTO users VALUES (101, 'alice', 'alice@college.edu', 'student', 'My private grade key: 98812')")
    cursor.execute("INSERT INTO users VALUES (102, 'bob', 'bob@college.edu', 'student', 'Private health note: allergic to peanuts')")
    cursor.execute("INSERT INTO users VALUES (103, 'dean_admin', 'dean@college.edu', 'admin', 'CONFIDENTIAL: Faculty Salary Sheet 2026 Link')")
    
    cursor.execute("INSERT INTO feedback VALUES (1, 'alice', 'Great campus library facilities!')")
    conn.commit()
    return conn

conn = init_db()

# HTML Templates
INDEX_HTML = """
<!質ml>
<html>
<head><title>VulnApp Portal</title></head>
<body style="font-family: sans-serif; padding: 20px;">
    <h2>🏫 Campus Student Portal v1.0</h2>
    <hr>
    <h3>1. Search Students (Try searching by name)</h3>
    <form action="/api/search" method="GET">
        <input type="text" name="q" placeholder="Search student name...">
        <button type="submit">Search</button>
    </form>

    <h3>2. View User Profile</h3>
    <p>View your profile: <a href="/api/user/profile?id=101">View Alice (ID 101)</a></p>

    <h3>3. Campus Feedback Board</h3>
    <p><a href="/feedback">Go to Feedback Board</a></p>
    
    <h3>4. Auth Token Generator</h3>
    <p>Get JWT Token: <a href="/api/login?user=alice">Login as Alice</a></p>
</body>
</html>
"""

FEEDBACK_HTML = """
<!DOCTYPE html>
<html>
<head><title>Campus Feedback</title></head>
<body style="font-family: sans-serif; padding: 20px;">
    <h2>💬 Student Feedback Board</h2>
    <a href="/">← Back to Portal</a>
    <hr>
    <h3>Submit Feedback</h3>
    <form action="/api/feedback" method="POST">
        <input type="text" name="author" placeholder="Your name"><br><br>
        <textarea name="comment" rows="4" cols="50" placeholder="Enter feedback..."></textarea><br><br>
        <button type="submit">Post Feedback</button>
    </form>
    <hr>
    <h3>Recent Feedback Entries:</h3>
    {% for fb in feedbacks %}
        <div style="border: 1px solid #ccc; padding: 10px; margin-bottom: 10px;">
            <strong>{{ fb[1] }}:</strong>
            <p>{{ fb[2] | safe }}</p> <!-- Flaw 3: Rendered with safe filter (Stored XSS) -->
        </div>
    {% endfor %}
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(INDEX_HTML)

# Flaw 1: SQL Injection in search query
@app.route("/api/search", methods=["GET"])
def search():
    query = request.args.get("q", "")
    cursor = conn.cursor()
    # Vulnerable raw string formatting SQL query
    raw_sql = f"SELECT id, username, email, role FROM users WHERE username LIKE '%{query}%'"
    try:
        cursor.execute(raw_sql)
        results = cursor.fetchall()
        return jsonify({"executed_query": raw_sql, "results": results})
    except Exception as e:
        return jsonify({"error": str(e), "executed_query": raw_sql}), 400

# Flaw 2: IDOR (Insecure Direct Object Reference)
@app.route("/api/user/profile", methods=["GET"])
def profile():
    user_id = request.args.get("id")
    cursor = conn.cursor()
    # No auth check verifying if session user matches requested user_id
    cursor.execute("SELECT id, username, email, role, secret_note FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    if user:
        return jsonify({"id": user[0], "username": user[1], "email": user[2], "role": user[3], "secret_note": user[4]})
    return jsonify({"error": "User not found"}), 404

# Flaw 3: Stored XSS Rendering
@app.route("/feedback", methods=["GET"])
def feedback_page():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM feedback")
    feedbacks = cursor.fetchall()
    return render_template_string(FEEDBACK_HTML, feedbacks=feedbacks)

@app.route("/api/feedback", methods=["POST"])
def post_feedback():
    author = request.form.get("author", "Anonymous")
    comment = request.form.get("comment", "")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO feedback (author, comment) VALUES (?, ?)", (author, comment))
    conn.commit()
    return redirect(url_for("feedback_page"))

# Flaw 4: Weak JWT Authentication & Hardcoded Secret
@app.route("/api/login", methods=["GET"])
def login():
    username = request.args.get("user", "alice")
    token = jwt.encode({"user": username, "role": "student"}, JWT_SECRET, algorithm="HS256")
    return jsonify({"message": "Token generated", "token": token, "note": "Decodable with weak secret"})

@app.route("/api/admin/dashboard", methods=["GET"])
def admin_dashboard():
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"error": "Missing Authorization header"}), 401
    try:
        token = auth_header.split(" ")[1]
        decoded = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        if decoded.get("role") == "admin":
            return jsonify({"status": "SUCCESS", "admin_data": "WELCOME DEAN ADMIN: All Exam Papers unlocked."})
        return jsonify({"error": "Forbidden: Requires admin role"}), 403
    except Exception as e:
        return jsonify({"error": f"Invalid Token: {str(e)}"}), 400

if __name__ == "__main__":
    print("Vulnerable Web App running at http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
