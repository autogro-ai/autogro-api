from flask import Blueprint, g, jsonify, request

user_keys_api = Blueprint('user_keys', __name__) 


# Create
@user_keys_api.route('/users/<int:id>/keys', methods=['POST']) 
def assign_user_keys():
    db = g.db
    cursor = db.cursor()    

    cursor.execute('INSERT INTO user_api_keys (userID, api_key, api_secret) VALUES (?, ?, ?)',
                    (request.json['userID'], request.json['api_key'], request.json['api_secret'])
                    )

 
    return jsonify({'message': 'API keys assigned to user successfully'}), 201

# Read
@user_keys_api.route('/users/<int:id>/keys')
def get_user_keys(id):
    db = g.db
    cursor = db.cursor()    

    cursor.execute('SELECT * FROM user_api_keys WHERE userID = ?', (id,))
    data = cursor.fetchall() 
    return jsonify(data)

# Update  
@user_keys_api.route('/users/<int:id>/keys', methods=['PUT'])
def update_user_keys(id):
    db = g.db
    cursor = db.cursor()    

    cursor.execute('UPDATE user_api_keys SET name = ?, email = ? WHERE id = ?', 
              (request.json['name'], request.json['email'], id))
  
    return jsonify({'message': 'User updated successfully'})

# Delete
@user_keys_api.route('/users/<int:userID>/keys/<string:api_key>', methods=['DELETE'])  
def remove_user_keys(id, api_key):
    db = g.db
    cursor = db.cursor()    
   
    cursor.execute('DELETE FROM user_api_keys WHERE userID = ? AND api_key = ?', (id, api_key))
    return jsonify({'message': 'User deleted successfully'})