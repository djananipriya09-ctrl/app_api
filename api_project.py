from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)


# 🔹 DB Connection
def get_db_connection():
    return mysql.connector.connect(
        host="host.docker.internal",  # Access host machine from container
        user="root",
        password="Lohit@12$",
        database="users",
        port=3306
    )

print("Database connection function defined successfully.")


# CREATE
@app.route('/users', methods=['POST'])
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
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(users)


# READ ONE
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
