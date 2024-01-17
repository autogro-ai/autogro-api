import json
from flask import Blueprint, g, jsonify, request
from tools.email_sender import EmailSender
from enums import MessageType

gro_component_types_api = Blueprint('gro_component_types', __name__) 

# List
@gro_component_types_api.route('/gro_component_types', methods=['GET'])
def list_gro_component_types():
    db = g.db
    cursor = g.db.cursor()
    cursor.execute('SELECT componentTypeID, name, measurementTypes, defaultSettings FROM gro_component_types')
    # Fetch all rows as a list of dictionaries
    columns = [col[0] for col in cursor.description]
    data = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return jsonify(data)

# Create
@gro_component_types_api.route('/gro_component_types', methods=['POST']) 
def create_gro_component_type():
    cursor = g.db.cursor()
    gro_component_typeData = request.get_json();

    name = gro_component_typeData['name']
    measurementTypes = json.dumps(gro_component_typeData['measurementTypes']) 
    defaultSettings = json.dumps(gro_component_typeData['defaultSettings'])

    cursor.execute('INSERT INTO gro_component_types (name, measurementTypes, defaultSettings) VALUES (%s, %s, %s)', (name, measurementTypes, defaultSettings))
    
    gro_component_typeID = cursor.lastrowid

    g.db.commit()

    return jsonify({'gro_component_typeID': gro_component_typeID, 'message': 'Gro ComponentID created successfully'}), 201

# Read
@gro_component_types_api.route('/gro_component_types/<int:id>')
def get_gro_componentType(id):
    cursor = g.db.cursor()
    cursor.execute('SELECT * FROM gro_component_types WHERE componentTypeID = %(id)s', {'id': id})
    
    data = cursor.fetchall() 
    return data
    
# Update  
@gro_component_types_api.route('/gro_component_types/<int:id>', methods=['PUT'])
def update_gro_componentType(id):
    cursor = g.db.cursor()    
    
    query = """
            UPDATE gro_component_types  
            SET
            name = IF( %(new_name)s <> name, %(new_name)s, name), 
            measurementTypes = IF( %(new_measurementTypes)s <> measurementTypes, %(new_measurementTypes)s, measurementTypes), 
            defaultSettings = IF( %(new_defaultSettings)s <> defaultSettings, %(new_defaultSettings)s, defaultSettings) 
            WHERE componentTypeID = %(componentTypeID)s
            """

    data = {  
        "new_name": request.json['name'],
        "new_measurementTypes": request.json['measurementTypes'],
        "new_defaultSettings": request.json['defaultSettings'],
        "componentTypeID": id
    }
    
    cursor.execute(query, data)    

    g.db.commit()
    msg = 'Gro Componenet updated successfully'

    return jsonify({'message': msg})

# DEACTIVATE by way of DELETE
@gro_component_types_api.route('/gro_component_types/<int:id>', methods=['DELETE'])  
def delete_gro_componenent_type(id):

    cursor = g.db.cursor()    

    query = "UPDATE gro_component_types SET active = %s WHERE componentTypeID = %s"
    active_value = 0

    cursor.execute(query, (active_value, id))  
    g.db.commit()  

    return jsonify({'message': 'Gro Component deactivated'})

# DEACTIVATE
@gro_component_types_api.route('/gro_component_types/<int:id>/Deactivate', methods=['PUT'])  
def deactivate_gro_component_type(id):

    cursor = g.db.cursor()    

    query = "UPDATE gro_component_types SET active = %s WHERE componentTypeID = %s"
    active_value = 0

    cursor.execute(query, (active_value, id))  
    g.db.commit()  

    return jsonify({'message': 'Gro Component Type Deactivated'})

# ACTIVATE
@gro_component_types_api.route('/gro_component_types/<int:id>/Activate', methods=['PUT'])  
def activate_gro_component_type(id):

    cursor = g.db.cursor()    

    query = "UPDATE gro_component_types SET active = %s WHERE componentTypeID = %s"
    active_value = 1

    cursor.execute(query, (active_value, id))  
    g.db.commit()  

    return jsonify({'message': 'Gro Component Type Activated'})
