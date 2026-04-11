from flask import Flask, request, jsonify
import mysql.connector
import jwt
from functools import wraps
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_change_this_in_production'  # ⚠️ Change in production


# 🔹 DB Connection
def get_db_connection():
    return mysql.connector.connect(
        host="host.docker.internal",  # Access host machine from container
        user="root",
        password="Lohit@12$",
        database="users",
        port=3306
    )


# 🔹 JWT Token Verification Decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({"error": "Token is missing"}), 401

        try:
            # Extract token from "Bearer <token>"
            token = token.split(" ")[1]
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except IndexError:
            return jsonify({"error": "Invalid token format"}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)

    return decorated


# 🔹 LOGIN - Generate JWT Token
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"error": "Username and password required"}), 400

    # ⚠️ In production, verify credentials against database
    # For demo: simple credential check
    if data.get("username") == "admin" and data.get("password") == "admin123":
        token = jwt.encode(
            {
                'username': data.get("username"),
                'exp': datetime.utcnow() + timedelta(hours=24)
            },
            app.config['SECRET_KEY'],
            algorithm='HS256'
        )
        return jsonify({"token": token, "message": "Login successful"}), 200

    return jsonify({"error": "Invalid credentials"}), 401


# CREATE
@app.route('/users', methods=['POST'])
@token_required
def create_user():
    data = request.get_json()

    conn = get_db_connection()
    cursor = conn.cursor()

    query = "INSERT INTO users (name, age) VALUES (%s, %s)"
    values = (data.get("name"), data.get("age"))

    cursor.execute(query, values)
    conn.commit()

    # Get the auto-generated ID
    user_id = cursor.lastrowid

    cursor.close()
    conn.close()

    response = {"id": user_id, "name": data.get("name"),
                "age": data.get("age")}
    return jsonify(response), 201


# READ ALL
@app.route('/users', methods=['GET'])
@token_required
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(users)


# READ ONE
@token_required
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        return jsonify(user)

    return jsonify({"error": "User not found"}), 404


# UPDATE
@token_required
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()

    conn = get_db_connection()
    cursor = conn.cursor()

    query = "UPDATE users SET name = %s, age = %s WHERE id = %s"
    values = (data.get("name"), data.get("age"), user_id)

    cursor.execute(query, values)
    conn.commit()

    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        return jsonify({"error": "User not found"}), 404

    cursor.close()
    conn.close()

    return jsonify({"message": "User updated"})


@token_required
# DELETE
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()

    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        return jsonify({"error": "User not found"}), 404

    cursor.close()
    conn.close()

    return jsonify({"message": "User deleted"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
