from flask import Blueprint, g, jsonify, request

user_keys_api = Blueprint('user_keys', __name__) 

# Create
@user_keys_api.route('/user_keys/<int:id>/keys', methods=['POST']) 
def assign_user_keys(id):
    db = g.db
    cursor = db.cursor()    

    userData = request.get_json();

    api_key = userData['api_key']
    api_secret = userData['api_secret']

    cursor.execute('INSERT INTO user_api_keys (userID, api_key, api_secret) VALUES (%s, %s, %s)', (id, api_key, api_secret) )   
 
    db.commit()

    return jsonify({'message': 'API keys assigned to user successfully'}), 201

# Read
@user_keys_api.route('/users/<int:id>/keys', methods=['GET'])
def get_user_keys(id):
    db = g.db
    cursor = db.cursor()    

    cursor.execute('SELECT * FROM user_api_keys WHERE userID = %(id)s', {'id': id})
    data = cursor.fetchall() 
    return jsonify(data)

# Delete
@user_keys_api.route('/users/<int:id>/keys/<string:api_key>', methods=['DELETE'])  
def remove_user_keys(id, api_key):
    db = g.db
    cursor = db.cursor()    
   
    cursor.execute('DELETE FROM user_api_keys WHERE (userID) = %(id)s AND (api_key) = %(api_key)s', {'id': id, 'api_key': api_key})

    db.commit()
    return jsonify({'message': 'Key removed successfully'})