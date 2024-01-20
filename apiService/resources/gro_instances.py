import datetime
import json
from flask import Blueprint, g, jsonify, request
from tools.email_sender import EmailSender
from enums import MessageType

groinstances_api = Blueprint('gro_instances', __name__) 

# List
@groinstances_api.route('/gro_devices', methods=['GET'])
def list_groinstances():
    db = g.db
    cursor = g.db.cursor()
    cursor.execute('SELECT * from gro_instances')
    # Fetch all rows as a list of dictionaries
    columns = [col[0] for col in cursor.description]
    data = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return jsonify(data)


# Create
@groinstances_api.route('/gro_devices', methods=['POST']) 
def create_gro_component_type():
    cursor = g.db.cursor()
    gro_component_typeData = request.get_json();

    name = gro_component_typeData['name']
    ownerID = gro_component_typeData['ownerID']   
    serialNumber = gro_component_typeData['serialNumber']
    modelID = gro_component_typeData['modelID']
    accessPolicy = json.dumps(gro_component_typeData['accessPolicy'])

    components = json.dumps(gro_component_typeData['components']) 

    cursor.execute('INSERT INTO gro_instances (ownerID, name, serialNumber, components, accessPolicy, modelID) VALUES (%s, %s, %s, %s, %s, %s)', (ownerID, name, serialNumber, components, accessPolicy, modelID))
    
    createdID = cursor.lastrowid

    g.db.commit()

    return jsonify({'GRO Device ID': createdID, 'message': 'Gro Device created successfully'}), 201


# Update  
@groinstances_api.route('/gro_devices/<int:id>', methods=['PUT'])
def update_gro_componentType(id):
    cursor = g.db.cursor()    
    
    query = """
            UPDATE gro_instances  
            SET
            name = IF( %(new_name)s <> name, %(new_name)s, name), 
            serialNumber = IF( %(new_serialNumber)s <> serialNumber, %(new_serialNumber)s, serialNumber), 
            components = IF( %(new_components)s <> components, %(new_components)s, components),
            accessPolicy = IF( %(new_accessPolicy)s <> accessPolicy, %(new_accessPolicy)s, accessPolicy), 
            modelID = IF( %(new_modelID)s <> modelID, %(new_modelID)s, modelID) 
            WHERE instanceID = %(instanceID)s
            """

    data = {  
        "new_name": request.json['name'],
        "new_serialNumber": request.json['serialNumber'],
        "new_components": json.dumps(request.json['components']),
        "new_accessPolicy": json.dumps(request.json['accessPolicy']),
        "new_modelID": request.json['modelID'],        
        "instanceID": id
    }
    
    cursor.execute(query, data)    

    g.db.commit()
    msg = 'Gro Device Instance updated successfully'

    return jsonify({'message': msg})

#Health Check
@groinstances_api.route('/gro_devices/<int:instanceID>/health', methods=['GET'])  
def device_healthCheck(instanceID):
    cursor = g.db.cursor()
    query = f'SELECT lastUpdate FROM gro_instances WHERE instanceID={instanceID}'
    cursor.execute(query)

    health = cursor.fetchone()

    if health:
        # Assuming 'lastUpdate' is a datetime column, convert it to string if needed
        last_update_str = health[0].strftime('%Y-%m-%d %H:%M:%S') if health[0] else None
        return jsonify({'lastUpdate': last_update_str})



#Heartbeat
@groinstances_api.route('/gro_devices/<int:instanceID>/heartbeat', methods=['PUT'])  
def device_heartBeat(instanceID):

    db = g.db
    cursor = g.db.cursor()
    query = 'UPDATE `gro_instances` SET `lastUpdate`=NOW() WHERE instanceID=%s'
    cursor.execute(query, (instanceID,))

    g.db.commit()

    return [], 201

# ASSIGN USER TO DEVICE
@groinstances_api.route('/gro_devices/<int:instanceID>/AssignOwner/<int:ownerID>', methods=['PUT'])  
def device_assign_user(instanceID, ownerID):

    accessPolicyData = request.get_json();
    #{ ownerID: int, access: [ { userID: int, access: string } ] }

    cursor = g.db.cursor()    

    query = "UPDATE gro_instances SET ownerID = %s WHERE instanceID = %s"

    cursor.execute(query, (ownerID, instanceID))  
    g.db.commit()  

    return jsonify({'message': 'User assigned to gro instance'})


#########################################
##########  V1 API Adapter  #############
#########################################
'''
This code takes in the old format and breaks out into the correct component entry
There will be one entry into gro_data_1 for each sensor type
'''

#########################################
##########  v1 GET SENSOR DATA  #############
#########################################

@groinstances_api.route('/og_autogro_sensor', methods=["GET"])
def og_autogro_sensor():
    holder_data = []
    cursor = g.db.cursor()

    sqlStatement = f"SELECT MAX(timestamp) AS accessed_str,  MAX(CASE WHEN componentTypeID=3 THEN data END) as ph, MAX(CASE WHEN componentTypeID=4 AND componentID=4001 THEN data END) as soil_1_wet,  MAX(CASE WHEN componentTypeID=4 AND componentID=4002 THEN data END) as soil_2_wet,  MAX(CASE WHEN componentTypeID=4 AND componentID=4003 THEN data END) as soil_3_wet, MAX(CASE WHEN componentTypeID=4 AND componentID=4004 THEN data END) as soil_4_wet,  MAX(CASE WHEN componentTypeID=4 AND componentID=4005 THEN data END) as soil_5_wet, MAX(CASE WHEN componentTypeID=7 THEN data END) as tds FROM gro_data_1 WHERE data IS NOT NULL"

    cursor.execute(sqlStatement)
    row_headers=[x[0] for x in cursor.description] #this will extract row headers
    results = cursor.fetchall()
    print(results)
    # holder_data = holders_schema.dump(results)
    print(holder_data)
    json_data=[]
    for result in results:
        json_data.append(dict(zip(row_headers,result)))
    return jsonify(json_data)
    return json.dumps(json_data)
# new format @groinstances_api.route('/gro_devices/<string:deviceID>/components/<string:componentTypeID>/<string:componentID>', methods=["GET"])


###########################################
##########  V1 GET PUMP DATA  #############
###########################################

@groinstances_api.route('/og_pump_autogro', methods=["GET"])
def og_pump_autogro():

    cursor = g.db.cursor()    
    page = request.args.get('page', default=1, type=int)
    items_per_page = 100
    

    # Calculate the offset based on the page number and items per page
    offset = (page - 1) * items_per_page

    sqlStatement = f"SELECT MAX(CASE WHEN componentTypeID=6 THEN data END) as pump_status, MAX(CASE WHEN componentTypeID = 2 THEN data END) AS flow_meter_rotations, MAX(CASE WHEN componentTypeID = 5 AND componentID = 5001 THEN data END) AS valve_1, MAX(CASE WHEN componentTypeID = 5 AND componentID = 5002 THEN data END) AS valve_2, MAX(CASE WHEN componentTypeID = 5 AND componentID = 5003 THEN data END) AS valve_3, MAX(CASE WHEN componentTypeID = 5 AND componentID = 5004 THEN data END) AS valve_4, MAX(CASE WHEN componentTypeID = 5 AND componentID = 5005 THEN data END) AS valve_5, DATE_FORMAT(NOW(), '%Y-%m-%d %H:%i:%s') AS accessed_str FROM gro_data_1 WHERE data IS NOT NULL;"
    
    cursor.execute(sqlStatement)

    # OG cursor.execute(f'SELECT pump_status,flow_meter_rotations, valve_1, valve_2, valve_3, valve_4, valve_5, CAST(accessed AS CHAR) AS accessed_str FROM og_pump_autogro ORDER BY id DESC LIMIT 100')

    row_headers=[x[0] for x in cursor.description] #this will extract row headers
    results = cursor.fetchall()
    print(results)
    # holder_data = holders_schema.dump(results)
    json_data=[]
    for result in results:
        json_data.append(dict(zip(row_headers,result)))
    return jsonify(json_data)
    return json.dumps(json_data)

########################################
##### V1 DEVICE POSTING HANDLERS ########
########################################

##### OG Send Sensor Data #####
@groinstances_api.route("/autogro_send_sensor_data", methods=["POST"])
def autogro_send_sensor_data():

    cursor = g.db.cursor()
    soil_1_wet = request.form.get("soil_1_wet")
    soil_2_wet = request.form.get("soil_2_wet")
    soil_3_wet = request.form.get("soil_3_wet")
    soil_4_wet = request.form.get("soil_4_wet")
    soil_5_wet = request.form.get("soil_5_wet")
    tds = request.form.get("tds")
    ph = request.form.get("ph")

    deviceID = 1
    tag = "using api v1"

    db = g.db
    cursor = g.db.cursor()


    data = [
        (1, 3000, 3, 1, ph, tag),
        (1, 7001, 7, 1, tds, tag),
        (1, 4001, 4, 1, soil_1_wet, tag),
        (1, 4002, 4, 1, soil_2_wet, tag),
        (1, 4003, 4, 1, soil_3_wet, tag),
        (1, 4004, 4, 1, soil_4_wet, tag),
        (1, 4005, 4, 1, soil_5_wet, tag),        
    ]

    tableName = f'gro_data_{deviceID}'

    sql = (f'INSERT INTO {tableName} (deviceID, componentID, componentTypeID, measurementType, data, tag) VALUES (%s, %s, %s, %s, %s, %s)')
  
    cursor.executemany(sql, data)


    updatedRows = []
    metricID = cursor.lastrowid
    updatedRows.append(metricID)

    db.commit()

    return updatedRows, 201


######### OG AutoGro Send Pump Data#########
@groinstances_api.route("/autogro_send_pump_data", methods=["POST"])
def autogro_send_pump_data():

    cursor = g.db.cursor()
    pump_status = request.form.get("pump_status")
    flow_meter_rotation = request.form.get("flow_meter_rotation")

    valve_1 = request.form.get("valve_1")
    valve_2 = request.form.get("valve_2")
    valve_3 = request.form.get("valve_3")
    valve_4 = request.form.get("valve_4")
    valve_5 = request.form.get("valve_5")

    deviceID = 1
    tag = "using api v1"
    current_timestamp = datetime.datetime.now()
    # Format the timestamp as 'YYYY-MM-DD HH:MM:SS'
    formatted_timestamp = current_timestamp.strftime('%Y-%m-%d %H:%M:%S')
    

    db = g.db
    cursor = g.db.cursor()


    data = [
        (1, 5001, 5, 1, valve_1, formatted_timestamp, tag),
        (1, 5002, 5, 1, valve_2, formatted_timestamp, tag),
        (1, 5003, 5, 1, valve_3, formatted_timestamp, tag),
        (1, 5004, 5, 1, valve_4, formatted_timestamp, tag),
        (1, 5005, 5, 1, valve_5, formatted_timestamp, tag),                             
        (1, 2001, 2, 1, flow_meter_rotation, formatted_timestamp, tag),
        (1, 6001, 6, 1, pump_status, formatted_timestamp, tag)   
    ]

    tableName = f'gro_data_{deviceID}'

    sql = (f'INSERT INTO {tableName} (deviceID, componentID, componentTypeID, measurementType, data, timestamp, tag) VALUES (%s, %s, %s, %s, %s, %s, %s)')
  
    cursor.executemany(sql, data)


    updatedRows = []
    metricID = cursor.lastrowid
    updatedRows.append(metricID)

    db.commit()

    return updatedRows, 201
