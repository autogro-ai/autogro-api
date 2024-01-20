from datetime import datetime
import json
from flask import Blueprint, g, jsonify, request

gro_component_data_api = Blueprint('gro_component_data', __name__) 

# List 100 Recent instrumentations
@gro_component_data_api.route('/gro_devices/<int:deviceID>/getComponentData', methods=['GET'])
def list_recent(deviceID):
    db = g.db
    cursor = g.db.cursor()
    cursor.execute(f'SELECT * FROM gro_data_{deviceID} LIMIT 100')

    # Fetch all rows as a list of dictionaries without modifying the timestamp
    columns = [col[0] for col in cursor.description]
    data = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return jsonify(data)

# Create
@gro_component_data_api.route('/gro_devices/<int:deviceID>/reportComponentData', methods=['POST']) 
def insert_component_data(deviceID):
    
    data = request.get_json();

    bodyDeviceID = data['deviceID']

    if deviceID != int(bodyDeviceID):
        return ["device mismatch"], 400

    db = g.db
    cursor = g.db.cursor()


    componentID = data['componentID']  
    componentTypeID = data['componentTypeID']
    measurementType = data['measurementType']
    componentData = data['data'] 
    tag = data['tag'] 
        
    # Convert the input string to a datetime object
    input_datetime_obj = datetime.strptime(data['timestamp'], '%m-%d-%Y %H:%M:%S')

    # Format the datetime object for MySQL insertion
    timestamp = input_datetime_obj.strftime('%Y-%m-%d %H:%M:%S')

    tableName = f'gro_data_{deviceID}'

    cursor.execute(f'INSERT INTO {tableName} (deviceID, componentID, componentTypeID, measurementType, data, timestamp, tag) VALUES (%s, %s, %s, %s, %s, %s, %s)', (bodyDeviceID, componentID, componentTypeID, measurementType, componentData, timestamp, tag))

    metricID = cursor.lastrowid

    db.commit()

    return [metricID], 201

# Read a metric
@gro_component_data_api.route('/gro_component_data/<int:deviceID>/<int:componentID>/<int:measurementType>')
def get_component_data(deviceID, componentID, measurementType):
    cursor = g.db.cursor()
    cursor.execute('SELECT data, timestamp, tag FROM gro_component_data WHERE deviceID = %(deviceID)s AND componentID = %(componentID)s AND measurementType = %(measurementType)s LIMIT 100', {'deviceID': deviceID, 'componentID': componentID, 'measurementType': measurementType })
    data = cursor.fetchall() 
    return jsonify(data)