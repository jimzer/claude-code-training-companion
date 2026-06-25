"""Sample app with intentional issues for agent demos."""
import sqlite3
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Issue 1: Hardcoded secret
SECRET_KEY = "super-secret-key-123"
app.config["SECRET_KEY"] = SECRET_KEY

# Issue 2: SQL injection vulnerability
@app.route("/users/<username>")
def get_user(username):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    # BAD: SQL injection!
    cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")
    user = cursor.fetchone()
    conn.close()
    if user:
        return jsonify({"username": user[1], "email": user[2]})
    return jsonify({"error": "Not found"}), 404


# Issue 3: No input validation
@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, email) VALUES (?, ?)",
        (data["username"], data["email"]),
    )
    conn.commit()
    conn.close()
    return jsonify({"created": True}), 201


# Issue 4: Debug endpoint left in production
@app.route("/debug/env")
def debug_env():
    return jsonify(dict(os.environ))


# Issue 5: Overly broad exception handling
@app.route("/process")
def process_data():
    try:
        data = request.args.get("data")
        result = int(data) * 2
        return jsonify({"result": result})
    except:
        return jsonify({"error": "Something went wrong"}), 500


if __name__ == "__main__":
    app.run(debug=True)
