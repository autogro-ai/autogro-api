from flask import Blueprint  

users_api = Blueprint('users', __name__) 


# Create
@app.route('/api/users', methods=['POST']) 
def create_user():
    c.execute('INSERT INTO users (name, email) VALUES (?, ?)', 
              (request.json['name'], request.json['email']))
    conn.commit()
    return jsonify({'message': 'User created successfully'}), 201

# Read
@app.route('/api/users/<int:id>')
def get_user(id):
    c.execute('SELECT * FROM users WHERE id = ?', (id,))
    data = c.fetchall() 
    return jsonify(data)

# Update  
@app.route('/api/users/<int:id>', methods=['PUT'])
def update_user(id):
    c.execute('UPDATE users SET name = ?, email = ? WHERE id = ?', 
              (request.json['name'], request.json['email'], id))
    conn.commit() 
    return jsonify({'message': 'User updated successfully'})

# Delete
@app.route('/api/users/<int:id>', methods=['DELETE'])  
def delete_user(id):
    c.execute('DELETE FROM users WHERE id = ?', (id,))
    conn.commit()
    return jsonify({'message': 'User deleted successfully'})