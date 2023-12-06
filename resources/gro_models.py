from datetime import datetime
import json
from flask import Blueprint, g, jsonify, request

gromodels_api = Blueprint('gromodels', __name__) 

# List
@gromodels_api.route('/gromodels', methods=['GET'])
def list_models():
    db = g.db
    cursor = g.db.cursor()
    cursor.execute('SELECT * FROM gro_models')
    
    # Fetch all rows as a list of dictionaries
    columns = [col[0] for col in cursor.description]
    data = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    return jsonify(data)

# Create
@gromodels_api.route('/gromodels', methods=['POST']) 
def create_gromodel():
    db = g.db
    cursor = g.db.cursor()

    data = request.get_json();

    name = data['name']
    modelNumber = data['modelNumber']  
    modelVersion = data['modelVersion']
    modelCodeName = data['modelCodeName'] 
    modelFamilyName = data['modelFamilyName'] 
        

    # Convert the input string to a datetime object
    input_datetime_obj = datetime.strptime(data['modelReleaseDate'], '%m-%d-%Y %H:%M:%S')

    # Format the datetime object for MySQL insertion
    modelReleaseDate = input_datetime_obj.strftime('%Y-%m-%d %H:%M:%S')

    
    #todo make sure this is structured correctly
    components = json.dumps(data['components']) 

    cursor.execute('INSERT INTO gro_models (name, modelNumber, modelVersion, modelCodeName, modelFamilyName, modelReleaseDate, components) VALUES ( %s, %s, %s, %s, %s, %s, %s)', (name, modelNumber, modelVersion, modelCodeName, modelFamilyName, modelReleaseDate, components))
    
    growModelID = cursor.lastrowid

    db.commit()

    return jsonify({'gromodelID': growModelID, 'message': 'New Gromodel created successfully'}), 201

# Read
@gromodels_api.route('/gromodels/<int:id>')
def get_gromodel(id):
    cursor = g.db.cursor()
    cursor.execute('SELECT * FROM gro_models WHERE modelID = %(id)s', {'id': id})
    data = cursor.fetchall() 
    return jsonify(data)
    
# Update  
@gromodels_api.route('/gromodels/<int:id>', methods=['PUT'])
def update_gro_model(id):

    cursor = g.db.cursor()    
    
    query = """
        UPDATE gro_models  
        SET
        name = IF( %(new_name)s <> name, %(new_name)s, name), 
        modelNumber = IF( %(new_modelNumber)s <> modelNumber, %(new_modelNumber)s, modelNumber), 
        modelVersion = IF( %(new_modelVersion)s <> modelVersion, %(new_modelVersion)s, modelVersion),            
        modelCodeName = IF( %(new_modelCodeName)s <> modelCodeName, %(new_modelCodeName)s, modelCodeName),
        modelFamilyName = IF( %(new_modelFamilyName)s <> modelFamilyName, %(new_modelFamilyName)s, modelFamilyName),
        modelReleaseDate = IF( %(new_modelReleaseDate)s <> modelReleaseDate, %(new_modelReleaseDate)s, modelReleaseDate),
        components = IF( %(new_components)s <> components, %(new_components)s, components) 
        WHERE modelID = %(modelID)s
    """

    # Assuming request.json['modelReleaseDate'] is in the format '12-05-2023 19:00:00'
    incoming_datetime_str = request.json['modelReleaseDate']

    # Convert the incoming datetime string to a datetime object
    incoming_datetime_obj = datetime.strptime(incoming_datetime_str, '%m-%d-%Y %H:%M:%S')

    # Format the datetime object to the MySQL-compatible format
    formatted_datetime_str = incoming_datetime_obj.strftime('%Y-%m-%d %H:%M:%S')

    data = {  
        "new_name": request.json['name'],
        "new_modelNumber": request.json['modelNumber'],
        "new_modelVersion": request.json['modelVersion'],
        "new_modelCodeName": request.json['modelCodeName'],        
        "new_modelFamilyName": request.json['modelFamilyName'],
        "new_modelReleaseDate": formatted_datetime_str,
        "new_components": json.dumps(request.json['components']),
        "modelID": id
    }

    cursor.execute(query, data)    

    g.db.commit()

    msg = 'Gro Model updated successfully'

    return jsonify({'message': msg})

# DEACTIVATE by way of DELETE
@gromodels_api.route('/gromodel/<int:id>', methods=['DELETE'])  
def delete_gromodel(id):

    cursor = g.db.cursor()    

    query = "UPDATE gro_models SET active = %s WHERE modelID = %s"
    active_value = 0

    cursor.execute(query, (active_value, id))  
    g.db.commit()  

    return jsonify({'message': 'Gro Model deactivated'})

# DEACTIVATE
@gromodels_api.route('/gromodels/<int:id>/Deactivate', methods=['PUT'])  
def deactivate_gro_model(id):

    cursor = g.db.cursor()    

    query = "UPDATE gro_models SET active = %s WHERE modelID = %s"
    active_value = 0

    cursor.execute(query, (active_value, id))  
    g.db.commit()  

    return jsonify({'message': 'Gro Model deactivated'})

# ACTIVATE
@gromodels_api.route('/gromodels/<int:id>/Activate', methods=['PUT'])  
def activate_gro_model(id):

    cursor = g.db.cursor()    

    query = "UPDATE gro_models SET active = %s WHERE modelID = %s"
    active_value = 1

    cursor.execute(query, (active_value, id))  
    g.db.commit()  

    return jsonify({'message': 'Gro Model Activated'})