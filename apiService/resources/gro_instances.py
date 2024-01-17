from flask import Blueprint, g, jsonify, request
from tools.email_sender import EmailSender
from enums import MessageType

groinstances_api = Blueprint('groinstances', __name__) 

# ASSIGN USER TO DEVICE
@groinstances_api.route('/grodevices/<int:instanceID>/AssignOwner/<int:ownerID>', methods=['PUT'])  
def device_assign_user(instanceID, ownerID):

    accessPolicyData = request.get_json();
    #{ ownerID: int, access: [ { userID: int, access: string } ] }

    cursor = g.db.cursor()    

    query = "UPDATE gro_instances SET ownerID = %s WHERE instanceID = %s"

    cursor.execute(query, (ownerID, instanceID))  
    g.db.commit()  

    return jsonify({'message': 'User assigned to gro instance'})

##### GET Device Component Data for g_autogro_sensor #####
@groinstances_api.route('/growdevices/<string:deviceID>/components/<string:componentTypeID>/<string:componentID>', methods=["GET"])
def og_autogro_sensor():
    holder_data = []
    cursor = g.db.cursor()

    cursor.execute('SELECT soil_1_wet, soil_2_wet, soil_3_wet, soil_4_wet, soil_5_wet, tds, ph, CAST(accessed AS CHAR) AS accessed_str FROM sensor_data_autogro ORDER BY id DESC LIMIT 100')
    row_headers=[x[0] for x in cur.description] #this will extract row headers
    results = cur.fetchall()
    print(results)
    # holder_data = holders_schema.dump(results)
    print(holder_data)
    json_data=[]
    for result in results:
        json_data.append(dict(zip(row_headers,result)))
    return jsonify(json_data)
    return json.dumps(json_data)


########## V1 API Adapter #############

########### OG Pump ###########
@groinstances_api.route('/og_pump_autogro', methods=["GET"])
def og_pump_autogro():

    page = request.args.get('page', default=1, type=int)
    items_per_page = 100
    db = g.dbog
    cur = g.dbog.cursor()
    # Calculate the offset based on the page number and items per page
    offset = (page - 1) * items_per_page
    # Retrieve the data for the current page
    cur.execute(f'SELECT pump_status,flow_meter_rotations, valve_1, valve_2, valve_3, valve_4, valve_5, CAST(accessed AS CHAR) AS accessed_str FROM og_pump_autogro ORDER BY id DESC LIMIT 100')
    row_headers=[x[0] for x in cur.description] #this will extract row headers
    results = cur.fetchall()
    print(results)
    # holder_data = holders_schema.dump(results)
    json_data=[]
    for result in results:
        json_data.append(dict(zip(row_headers,result)))
    return jsonify(json_data)
    return json.dumps(json_data)

    # row_headers = [x[0] for x in cur.description]
    # results = cur.fetchall()
    # json_data = []
    # for result in results:
    #     json_data.append(dict(zip(row_headers, result)))
    # return jsonify(json_data)
    # return json.dumps(json_data)

##### OG Send Sensor Data #####
@groinstances_api.route("/autogro_send_sensor_data", methods=["POST"])
def autogro_send_sensor_data():
    db = g.dbog
    cur = g.dbog.cursor()
    soil_1_wet = request.form.get("soil_1_wet")
    soil_2_wet = request.form.get("soil_2_wet")
    soil_3_wet = request.form.get("soil_3_wet")
    soil_4_wet = request.form.get("soil_4_wet")
    soil_5_wet = request.form.get("soil_5_wet")
    tds = request.form.get("tds")
    ph = request.form.get("ph")
    accessed = request.form.get("accessed")
    now = datetime.datetime.now()
    # print(f"Received form data: handles={handles}, count={count}, accessed={accessed}")
    try:
        cur.execute('INSERT INTO sensor_data_autogro (soil_1_wet, soil_2_wet, soil_3_wet, soil_4_wet, soil_5_wet, tds, ph, accessed) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (soil_1_wet, soil_2_wet, soil_3_wet, soil_4_wet, soil_5_wet, tds, ph, accessed))
        conn.commit()
        print("Deprecated: autogro_send_sensor_data successfully")
    except Exception as e:
        print("Error inserting data:", e)
        conn.rollback()
    finally:
        cur.close()
        conn.close()
    return "Deprecated: autogro_send_sensor_data data inserted correctly"


######### OG AutoGro Send Pump Data#########
@groinstances_api.route("/autogro_send_pump_data", methods=["POST"])
def autogro_send_pump_data():
    db = g.dbog
    cur = g.dbog.cursor()
    pump_status = request.form.get("pump_status")
    flow_meter_rotation = request.form.get("flow_meter_rotation")
    print(flow_meter_rotation)
    valve_1 = request.form.get("valve_1")
    valve_2 = request.form.get("valve_2")
    valve_3 = request.form.get("valve_3")
    valve_4 = request.form.get("valve_4")
    valve_5 = request.form.get("valve_5")
    accessed = request.form.get("accessed")
    try:
        cur.execute('INSERT INTO og_pump_autogro (pump_status, flow_meter_rotations, valve_1, valve_2, valve_3, valve_4, valve_5, accessed) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (pump_status, flow_meter_rotation, valve_1, valve_2, valve_3, valve_4, valve_5, accessed))
        db.commit()
        print("Deprecated: autogro_send_pump_data sent succesfully")
    except Exception as e:
        print("Error inserting data:", e)
        db.rollback()
    finally:
        cur.close()
        db.close()
    return "Deprecated: autogro_send_pump_data sent succesfully"



####TEST for APP #####
######### OG AutoGro Send Pump Data#########
@groinstances_api.route("/send_data_test", methods=["POST"])
def send_data_test():
    db = g.dbog
    cur = g.dbog.cursor()
    pump_status = request.json.get("pump_status")
    flow_meter_rotations = request.json.get("flow_meter_rotations")
    valve_1 = request.json.get("valve_1")
    accessed = request.json.get("accessed")
    print('Pump status: ', pump_status)
    try:
        cur.execute('INSERT INTO send_data_test (pump_status, flow_meter_rotations, valve_1, accessed) VALUES (%s, %s, %s, %s)', (pump_status, flow_meter_rotations, valve_1, accessed))
        db.commit()
        print("Data inserted successfully")
    except Exception as e:
        print("Error inserting data:", e)
        db.rollback()
    finally:
        cur.close()
        db.close()
    return "Data inserted successfully"


