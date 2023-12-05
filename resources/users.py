from flask import Blueprint, g, jsonify, request
from tools.email_sender import EmailSender
from enums import MessageType

users_api = Blueprint('users', __name__) 

# List
@users_api.route('/users', methods=['GET'])
def list_users():
    db = g.db
    cursor = g.db.cursor()
    cursor.execute('SELECT userID, FirstName, LastName, EmailAddress, active FROM users')
    data = cursor.fetchall() 
    return jsonify(data)

# Create
@users_api.route('/users', methods=['POST']) 
def create_user():
    db = g.db
    cursor = g.db.cursor()

    userData = request.get_json();

    firstName = userData['firstName']
    lastName = userData['lastName']  
    emailAddress = userData['emailAddress']


    cursor.execute('INSERT INTO users (FirstName, LastName, EmailAddress) VALUES (%s, %s, %s)', (firstName, lastName, emailAddress))
    
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

#Send out welcome email

def sendEmail(message_type, user_info, device_info):

    email_sender = EmailSender()
    subject = ""
    body = ""
    recipient_email = user_info['emailAddress']    
    sendAsHTML = True

    name =  f"{user_info['firstName']}  {user_info['lastName']}"

    if message_type == MessageType.DEVICE_USER_INVITED:
        subject = f"AutoGro Invitation to join a new device"
        body = f"Hello {name},\n\n"\
                f"You have been invited to manage a new device: {device_info['name']}!\n\n"\
                f"Login to manage the device: https://autogroai.com/"


    # Call the send_email method from EmailSender
    email_sender.send_email(recipient_email, subject, body)    
    email_sender.send_email(
        to=recipient_email,
        subject=subject,
        body=body, sendAsHTML=True
    )