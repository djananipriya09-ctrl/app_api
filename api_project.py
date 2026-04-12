from flask import Flask, request, jsonify
import mysql.connector
import jwt
from functools import wraps
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv(
    'SECRET_KEY', 'your_secret_key_change_this_in_production'
)


# 🔹 DB Connection - AWS RDS with SSL
def get_db_connection():
    db_config = {
        'host': os.getenv('DB_HOST', 'host.docker.internal'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', 'Lohit@12$'),
        'database': os.getenv('DB_NAME', 'users'),
        'port': int(os.getenv('DB_PORT', 3306))
    }

    # Add SSL configuration if certificate is provided
    ssl_ca = os.getenv('DB_SSL_CA')
    if ssl_ca:
        db_config['ssl_disabled'] = False
        db_config['ssl_verify_cert'] = True
        db_config['ssl_verify_identity'] = True
        db_config['ssl_ca'] = ssl_ca

    return mysql.connector.connect(**db_config)


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
            jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except IndexError:
            return jsonify({"error": "Invalid token format"}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)

    return decorated


# 🔹 HEALTH CHECK - For AWS Load Balancer
@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for AWS Load Balancer.
    Returns the health status of the instance.
    No authentication required.
    """
    try:
        # Try to connect to the database to verify it's healthy
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        conn.close()

        return jsonify({
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "service": "User API"
        }), 200

    except Exception as e:
        # If database connection fails, return unhealthy
        return jsonify({
            "status": "unhealthy",
            "timestamp": datetime.utcnow().isoformat(),
            "service": "User API",
            "error": str(e)
        }), 503


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
