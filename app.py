import sqlite3 
from flask import Flask, g, jsonify, request

app = Flask(__name__)
app.config['DATABASE'] = 'mars_resources.db'

def get_db():
    """Connect to the application's configured database."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(_):
    """Closes the database again at the end of the request."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/resources', methods=['GET'])
def get_resources():
    db = get_db()
    cursor = db.execute('SELECT * FROM resources')
    resources = cursor.fetchall()
    return jsonify([dict(resource) for resource in resources])

@app.route('/resources/<int:resource_id>', methods=['GET'])
def get_resource(resource_id):
    db = get_db()
    cursor = db.execute('SELECT * FROM resources WHERE id = ?', (resource_id,))
    resource = cursor.fetchone()
    if resource is None:
        return jsonify({'status': 'error', 'message': 'Resource not found'}), 404
    return jsonify(dict(resource))

@app.route('/resources', methods=['POST'])
def create_resource():
    data = request.get_json()
    if not data or 'name' not in data or 'quantity' not in data:
        return jsonify({'error': 'Missing name or quantity'}), 400
    db = get_db()
    cursor = db.execute(
        'INSERT INTO resources (name, quantity) VALUES (?, ?)',
        (data['name'], data['quantity'])
    )
    db.commit()
    return jsonify(
        {'id': cursor.lastrowid, 'name': data['name'], 'quantity': data['quantity']}
    ), 201

@app.route('/resources/<int:resource_id>', methods=['PUT'])
def update_resource(resource_id):
    data = request.get_json()
    if not data or 'name' not in data or 'quantity' not in data:
        return jsonify({'error': 'Missing name or quantity'}), 400
    db = get_db()
    cursor = db.execute(
        'UPDATE resources SET name = ?, quantity = ? WHERE id = ?',
        (data['name'], data['quantity'], resource_id)
    )
    db.commit()
    if cursor.rowcount == 0:
        return jsonify({'status': 'error', 'message': 'Resource not found'}), 404
    return jsonify(
        {'id': resource_id, 'name': data['name'], 'quantity': data['quantity']}
    )

@app.route('/resources/<int:resource_id>', methods=['DELETE'])
def delete_resource(resource_id):
    db = get_db()
    cursor = db.execute('DELETE FROM resources WHERE id = ?', (resource_id,))
    db.commit()
    if cursor.rowcount == 0:
        return jsonify({'status': 'error', 'message': 'Resource not found'}), 404
    return jsonify({'status': 'success', 'message': 'Resource deleted successfully'})

# ✅ Export for test support
if __name__ != '__main__':
    # Make sure app and get_db can be imported in tests
    __all__ = ['app', 'get_db']

if __name__ == '__main__':
    app.run(debug=True)
