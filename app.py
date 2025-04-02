import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

DATABASE = 'mars_resources.db'

def create_connection():
    """Establishes a connection to the database."""
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row  # To fetch rows as dictionaries
    return connection

def close_connection(conn):
    """Close the database connection."""
    if conn:
        conn.close()

@app.route('/')
def homepage():
    """Home route to check if the app is running."""
    return "Welcome to Mars Resource Manager! 🚀"

@app.route('/resources', methods=['GET'])
def get_all_resources():
    """Retrieve all resources."""
    conn = create_connection()
    cursor = conn.execute('SELECT * FROM resources')
    resources = cursor.fetchall()
    close_connection(conn)
    return jsonify({"status": "success", "resources": [dict(row) for row in resources]})

@app.route('/resources/<int:resource_id>', methods=['GET'])
def get_resource_by_id(resource_id):
    """Retrieve a single resource by its ID."""
    conn = create_connection()
    cursor = conn.execute('SELECT * FROM resources WHERE id = ?', (resource_id,))
    resource = cursor.fetchone()
    close_connection(conn)
    if resource:
        return jsonify({"status": "success", "resource": dict(resource)})
    else:
        return jsonify({"status": "error", "message": "Resource not found"}), 404

@app.route('/resources', methods=['POST'])
def create_resource():
    """Create a new resource."""
    data = request.get_json()
    if not data or 'name' not in data or 'quantity' not in data:
        return jsonify({"status": "error", "message": "Missing name or quantity"}), 400

    conn = create_connection()
    cursor = conn.execute(
        'INSERT INTO resources (name, quantity) VALUES (?, ?)',
        (data['name'], data['quantity'])
    )
    conn.commit()
    new_resource = {'id': cursor.lastrowid, 'name': data['name'], 'quantity': data['quantity']}
    close_connection(conn)
    return jsonify({"status": "success", "resource": new_resource}), 201

@app.route('/resources/<int:resource_id>', methods=['PUT'])
def update_resource(resource_id):
    """Update an existing resource."""
    data = request.get_json()
    if not data or 'name' not in data or 'quantity' not in data:
        return jsonify({"status": "error", "message": "Missing name or quantity"}), 400

    conn = create_connection()
    cursor = conn.execute(
        'UPDATE resources SET name = ?, quantity = ? WHERE id = ?',
        (data['name'], data['quantity'], resource_id)
    )
    conn.commit()
    if cursor.rowcount == 0:
        close_connection(conn)
        return jsonify({"status": "error", "message": "Resource not found"}), 404

    updated_resource = {'id': resource_id, 'name': data['name'], 'quantity': data['quantity']}
    close_connection(conn)
    return jsonify({"status": "success", "resource": updated_resource})

@app.route('/resources/<int:resource_id>', methods=['DELETE'])
def delete_resource(resource_id):
    """Delete a resource."""
    conn = create_connection()
    cursor = conn.execute('DELETE FROM resources WHERE id = ?', (resource_id,))
    conn.commit()
    if cursor.rowcount == 0:
        close_connection(conn)
        return jsonify({"status": "error", "message": "Resource not found"}), 404

    close_connection(conn)
    return jsonify({"status": "success", "message": "Resource deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)
