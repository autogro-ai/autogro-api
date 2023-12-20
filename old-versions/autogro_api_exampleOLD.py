from flask import Flask, request, g, jsonify

import mysql.connector

import json
import datetime
from dotenv import load_dotenv
from pathlib import Path
import os


app = Flask(__name__)
app.config["DEBUG"] = True

load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

#AutoGro DB Variables & Config
# db_user = os.environ['db_user']
# db_pass = os.environ['db_pass']
# db_host = os.environ['db_host']
# db_db = os.environ['db_db']
# discord_key = os.environ['discord_key']


# AutoGro DB
DB_CONFIG = {
    'user': '',
    'password': '',
    'host': 'localhost',
    'port': '8889',
    'database': 'autogro',
}

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = mysql.connector.connect(**DB_CONFIG)
    return db
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()



##### OG Rig #####
@app.route('/xxx', methods=["GET"])
def og_autogro_sensor():
    holder_data = []
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT soil_1_wet, soil_2_wet, soil_3_wet, soil_4_wet, soil_5_wet, tds, ph, CAST(accessed AS CHAR) AS accessed_str FROM sensor_data_autogro ORDER BY id DESC LIMIT 100')
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


########### OG Pump ###########
@app.route('/xxx', methods=["GET"])
def og_pump_autogro():
    page = request.args.get('page', default=1, type=int)
    items_per_page = 100
    conn = get_db()
    cur = conn.cursor()
    # Calculate the offset based on the page number and items per page
    offset = (page - 1) * items_per_page
    # Retrieve the data for the current page
    cur.execute(f'SELECT pump_status,flow_meter_rotations, valve_1, valve_2, valve_3, valve_4, valve_5, CAST(accessed AS CHAR) AS accessed_str FROM og_pump_autogro LIMIT {items_per_page} OFFSET {offset}')
    row_headers = [x[0] for x in cur.description]
    results = cur.fetchall()
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))
    return jsonify(json_data)
    return json.dumps(json_data)

##### OG Send Sensor Data #####
@app.route("/xxx", methods=["POST"])
def autogro_send_sensor_data():
    conn = get_db()
    cur = conn.cursor()
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
        print("Data inserted successfully")
    except Exception as e:
        print("Error inserting data:", e)
        conn.rollback()
    finally:
        cur.close()
        conn.close()
    return "Data inserted successfully"


######### OG AutoGro Send Pump Data#########
@app.route("/xxx", methods=["POST"])
def autogro_send_pump_data():
    conn = get_db()
    cur = conn.cursor()
    pump_status = request.form.get("pump_status")
    flow_meter_rotations = request.form.get("flow_meter_rotations")
    valve_1 = request.form.get("valve_1")
    valve_2 = request.form.get("valve_2")
    valve_3 = request.form.get("valve_3")
    valve_4 = request.form.get("valve_4")
    valve_5 = request.form.get("valve_5")
    accessed = request.form.get("accessed")
    try:
        cur.execute('INSERT INTO og_pump_autogro (pump_status, flow_meter_rotations, valve_1, valve_2, valve_3, valve_4, valve_5, accessed) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (pump_status, flow_meter_rotations, valve_1, valve_2, valve_3, valve_4, valve_5, accessed))
        conn.commit()
        print("Data inserted successfully")
    except Exception as e:
        print("Error inserting data:", e)
        conn.rollback()
    finally:
        cur.close()
        conn.close()
    return "Data inserted successfully"


#########Evan's Rig##########
# Evan Post Sensor Data
@app.route("/xxx", methods=["POST"])
def evan_sensor_data_autogro():
    conn = get_db()
    cur = conn.cursor()
    soil_1_wet = request.form.get("soil_1_wet")
    soil_2_wet = request.form.get("soil_2_wet")
    soil_3_wet = request.form.get("soil_3_wet")
    soil_4_wet = request.form.get("soil_4_wet")
    soil_5_wet = request.form.get("soil_5_wet")
    tds = request.form.get("tds")
    ph = request.form.get("ph")
    accessed = request.form.get("accessed")
    now = datetime.datetime.now()
    try:
        cur.execute('INSERT INTO evan_sensor_data_autogro (soil_1_wet, soil_2_wet, soil_3_wet, soil_4_wet, soil_5_wet, tds, ph, accessed) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (soil_1_wet, soil_2_wet, soil_3_wet, soil_4_wet, soil_5_wet, tds, ph, accessed))
        conn.commit()
        print("Data inserted successfully")
    except Exception as e:
        print("Error inserting data:", e)
        conn.rollback()
    finally:
        cur.close()
        conn.close()
    return "Data inserted successfully"


######### Evan Pump Send Data #########
@app.route("/xxx", methods=["POST"])
def evan_send_pump_data():
    conn = get_db()
    cur = conn.cursor()
    pump_status = request.form.get("pump_status")
    flow_meter_rotations = request.form.get("flow_meter_rotations")
    valve_1 = request.form.get("valve_1")
    valve_2 = request.form.get("valve_2")
    valve_3 = request.form.get("valve_3")
    valve_4 = request.form.get("valve_4")
    valve_5 = request.form.get("valve_5")
    accessed = request.form.get("accessed")
    try:
        cur.execute('INSERT INTO evan_pump_autogro (pump_status, flow_meter_rotations, valve_1, valve_2, valve_3, valve_4, valve_5, accessed) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (pump_status, flow_meter_rotations, valve_1, valve_2, valve_3, valve_4, valve_5, accessed))
        conn.commit()
        print("Data inserted successfully")
    except Exception as e:
        print("Error inserting data:", e)
        conn.rollback()
    finally:
        cur.close()
        conn.close()
    return "Data inserted successfully"

###### Evan Get Pump Data #####
@app.route('/xxx', methods=["GET"])
def evan_pump_autogro():
    page = request.args.get('page', default=1, type=int)
    items_per_page = 100
    conn = get_db()
    cur = conn.cursor()
    # Calculate the offset based on the page number and items per page
    offset = (page - 1) * items_per_page
    # Retrieve the data for the current page
    cur.execute(f'SELECT pump_status,flow_meter_rotations, valve_1, valve_2, valve_3, valve_4, valve_5, CAST(accessed AS CHAR) AS accessed_str FROM evan_pump_autogro LIMIT {items_per_page} OFFSET {offset}')
    row_headers = [x[0] for x in cur.description]
    results = cur.fetchall()
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))
    return jsonify(json_data)
    return json.dumps(json_data)

##### Evan Get Sensor Data #####
@app.route('/xxx', methods=["GET"])
def evan_autogro_sensor():
    holder_data = []
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT soil_1_wet, soil_2_wet, soil_3_wet, soil_4_wet, soil_5_wet, tds, ph, CAST(accessed AS CHAR) AS accessed_str FROM evan_sensor_data_autogro ORDER BY id DESC LIMIT 100')
    row_headers=[x[0] for x in cur.description] #this will extract row headers
    results = cur.fetchall()
    print(results)
    print(holder_data)
    json_data=[]
    for result in results:
            json_data.append(dict(zip(row_headers,result)))
    return jsonify(json_data)
    return json.dumps(json_data)


if __name__ == "__main__":
    app.run(debug=True)
