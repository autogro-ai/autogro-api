from flask import Blueprint, g, jsonify, request

users_api = Blueprint('users', __name__) 

# Create
@users_api.route('/users', methods=['POST']) 
def create_user():
    db = g.db
    cursor = g.db.cursor()

    cursor.execute('INSERT INTO users (name, email) VALUES (?, ?)', 
              (request.json['name'], request.json['email']))

    return jsonify({'message': 'User created successfully'}), 201

# Read
@users_api.route('/users/<int:id>')
def get_user(id):
    db = g.db
    cursor = g.db.cursor()
    cursor.execute('SELECT * FROM users WHERE userID = %(id)s', {'id': id})
    data = cursor.fetchall() 
    return jsonify(data)
    
# Update  
@users_api.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    db = g.db
    cursor = g.db.cursor()    
    
    cursor.execute('UPDATE users SET name = ?, email = ? WHERE id = ?', 
              (request.json['name'], request.json['email'], id))
    
    return jsonify({'message': 'User updated successfully'})

# Delete
@users_api.route('/users/<int:id>', methods=['DELETE'])  
def delete_user(id):
    db = g.db
    cursor = g.db.cursor()    

    cursor.execute('DELETE FROM users WHERE id = ?', (id,))
    return jsonify({'message': 'User deleted successfully'})