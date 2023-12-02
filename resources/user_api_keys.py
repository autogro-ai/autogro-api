from flask import Blueprint  

users_api = Blueprint('user_api_keys', __name__) 


# Create
@app.route('/api/users/<int:id>/keys', methods=['POST']) 
def assign_user_keys():
    c.execute('INSERT INTO user_api_keys (userID, api_key, api_secret) VALUES (?, ?)', 
              (request.json['userID'], request.json['api_key'], , request.json['api_secret']))
    conn.commit()
    return jsonify({'message': 'API keys assigned to user successfully'}), 201

# Read
@app.route('/api/users/<int:id>/keys')
def get_user_keys(id):
    c.execute('SELECT * FROM user_api_keys WHERE userID = ?', (id,))
    data = c.fetchall() 
    return jsonify(data)

# Update  
@app.route('/api/users/<int:id>/keys', methods=['PUT'])
def update_user_keys(id):
    c.execute('UPDATE user_api_keys SET name = ?, email = ? WHERE id = ?', 
              (request.json['name'], request.json['email'], id))
    conn.commit() 
    return jsonify({'message': 'User updated successfully'})

# Delete
@app.route('/api/users/<int:userID>/keys/<string:api_key>', methods=['DELETE'])  
def remove_user_keys(id, api_key):
    c.execute('DELETE FROM user_api_keys WHERE userID = ? AND api_key = ?', (id, api_key))
    conn.commit()
    return jsonify({'message': 'User deleted successfully'})