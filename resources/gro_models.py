import datetime
from flask import Blueprint, g, jsonify, request

users_api = Blueprint('users', __name__) 

# List
@users_api.route('/gromodels', methods=['GET'])
def list_models():
    db = g.db
    cursor = g.db.cursor()
    cursor.execute('SELECT * FROM gro_models')
    data = cursor.fetchall() 
    return jsonify(data)

# Create
@users_api.route('/gromodels', methods=['POST']) 
def create_user():
    db = g.db
    cursor = g.db.cursor()

    userData = request.get_json();

    name = userData['name']
    modelNumber = userData['modelNumber']  
    modelVersion = userData['modelVersion']
    modelReleaseDate = datetime.strptime(userData['modelReleaseDate'], '%Y-%m-%d %H:%M:%S')
    modelCodeName = userData['modelCodeName'] 
    modelFamily = userData['modelFamily'] 
    components = userData['components'] 



    cursor.execute('INSERT INTO gro_models (name, modelNumber, modelVersion, modelCodeName, modelFamily, modelReleaseDate, components) VALUES ( %s, %s, %s, %s, %s, %s)', (name, modelNumber))
    
    userID = cursor.lastrowid

    db.commit()

    return jsonify({'userID': userID, 'message': 'User created successfully'}), 201

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
    
    query = """
            UPDATE users  
            SET
            FirstName = IF( %(new_FirstName)s <> FirstName, %(new_FirstName)s, FirstName), 
            LastName = IF( %(new_LastName)s <> LastName, %(new_LastName)s, LastName), 
            EmailAddress = IF( %(new_EmailAddress)s <> EmailAddress, %(new_EmailAddress)s, EmailAddress) 
            WHERE userID = %(userID)s
            """

    data = {  
        "new_FirstName": request.json['firstName'],
        "new_LastName": request.json['lastName'],
        "new_EmailAddress": request.json['emailAddress'],
        "userID": id
    }
    

    cursor.execute(query, data)    

    db.commit()

    msg = 'User updated successfully'

    return jsonify({'message': msg})

# DEACTIVATE by way of DELETE
@users_api.route('/users/<int:id>', methods=['DELETE'])  
def delete_user(id):
    db = g.db
    cursor = g.db.cursor()    

    query = "UPDATE users SET active = %s WHERE userID = %s"
    active_value = 0

    cursor.execute(query, (active_value, id))  
    db.commit()  

    return jsonify({'message': 'User deactivated'})

# DEACTIVATE
@users_api.route('/users/<int:id>/Deactivate', methods=['PUT'])  
def deactivate_user(id):
    db = g.db
    cursor = g.db.cursor()    

    query = "UPDATE users SET active = %s WHERE userID = %s"
    active_value = 0

    cursor.execute(query, (active_value, id))  
    db.commit()  

    return jsonify({'message': 'User Deactivated'})

# ACTIVATE
@users_api.route('/users/<int:id>/Activate', methods=['PUT'])  
def activate_user(id):
    db = g.db
    cursor = g.db.cursor()    

    query = "UPDATE users SET active = %s WHERE userID = %s"
    active_value = 1

    cursor.execute(query, (active_value, id))  
    db.commit()  

    return jsonify({'message': 'User Activated'})