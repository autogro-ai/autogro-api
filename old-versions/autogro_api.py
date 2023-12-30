from flask import Flask, redirect, render_template, request, url_for, g, jsonify
import mysql.connector
import json
import datetime
from dotenv import load_dotenv
from pathlib import Path
import os
# from tools.email_sender import EmailSender
# from enums import MessageType

app = Flask(__name__)
app.config["DEBUG"] = True

load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)
now = datetime.datetime.now()

#AutoGro DB Variables & Config
# db_user = os.environ['db_user']
# db_pass = os.environ['db_pass']
# db_host = os.environ['db_host']
# db_db = os.environ['db_db']
# discord_key = os.environ['discord_key']


# AutoGro DB
DB_CONFIG = {
    'user': 'autogro',
    'password': 'yellow???876',
    'host': 'autogro.mysql.pythonanywhere-services.com',
    'port': '3306',
    'database': 'autogro$autogro_db',
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


valid_api_key = "test"

def require_api_key(func):
    def wrapper(*args, **kwargs):
        api_key = request.headers.get("Authorization")
        if api_key == valid_api_key:
            return func(*args, **kwargs)
        else:
            return jsonify({"error": "Unauthorized"}), 401
    return wrapper

@app.route('/protected', methods=['GET'])
@require_api_key
def protected_resource():
    return jsonify({"message": "This is a protected resource"})



##### OG Rig #####
@app.route('/og_autogro_sensor', methods=["GET"])
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
@app.route('/og_pump_autogro', methods=["GET"])
def og_pump_autogro():
    page = request.args.get('page', default=1, type=int)
    items_per_page = 100
    conn = get_db()
    cur = conn.cursor()
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
@app.route("/autogro_send_sensor_data", methods=["POST"])
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
        print("Deprecated: autogro_send_sensor_data successfully")
    except Exception as e:
        print("Error inserting data:", e)
        conn.rollback()
    finally:
        cur.close()
        conn.close()
    return "Deprecated: autogro_send_sensor_data data inserted correctly"


######### OG AutoGro Send Pump Data#########
@app.route("/autogro_send_pump_data", methods=["POST"])
def autogro_send_pump_data():
    conn = get_db()
    cur = conn.cursor()
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
        conn.commit()
        print("Deprecated: autogro_send_pump_data sent succesfully")
    except Exception as e:
        print("Error inserting data:", e)
        conn.rollback()
    finally:
        cur.close()
        conn.close()
    return "Deprecated: autogro_send_pump_data sent succesfully"



####TEST for APP #####
######### OG AutoGro Send Pump Data#########
@app.route("/send_data_test", methods=["POST"])
def send_data_test():
    conn = get_db()
    cur = conn.cursor()
    pump_status = request.json.get("pump_status")
    flow_meter_rotations = request.json.get("flow_meter_rotations")
    valve_1 = request.json.get("valve_1")
    accessed = request.json.get("accessed")
    print('Pump status: ', pump_status)
    try:
        cur.execute('INSERT INTO send_data_test (pump_status, flow_meter_rotations, valve_1, accessed) VALUES (%s, %s, %s, %s)', (pump_status, flow_meter_rotations, valve_1, accessed))
        conn.commit()
        print("Data inserted successfully")
    except Exception as e:
        print("Error inserting data:", e)
        conn.rollback()
    finally:
        cur.close()
        conn.close()
    return "Data inserted successfully"

users = []

##### AutoGro APP API

@app.route("/autogro_app_api/<username>", methods=["GET", "POST", "PUT"])
def autogro_app_api(username):
    if request.method == "GET":
        page = request.args.get('page', default=1, type=int)
        items_per_page = 100
        conn = get_db()
        cur = conn.cursor()

        # Calculate the offset based on the page number and items per page
        offset = (page - 1) * items_per_page

        # Retrieve the data for the current page for the specified username
        cur.execute('SELECT * from autogro_app_api WHERE username = %s', (username,))
        row_headers = [x[0] for x in cur.description]
        results = cur.fetchall()

        json_data = []
        for result in results:
            json_data.append(dict(zip(row_headers, result)))

        return jsonify(json_data)

    elif request.method == "POST":
        # Handle POST request here
        conn = get_db()
        cur = conn.cursor()
        username = request.json.get("username")
        valve1_active = request.json.get("valve1_active")
        valve1_time = request.json.get("valve1_time")
        valve1_duration = request.json.get("valve1_duration")
        valve2_active = request.json.get("valve2_active")
        valve2_time = request.json.get("valve2_time")
        valve2_duration = request.json.get("valve2_duration")
        valve3_active = request.json.get("valve3_active")
        valve3_time = request.json.get("valve3_time")
        valve3_duration = request.json.get("valve3_duration")
        valve4_active = request.json.get("valve4_active")
        valve4_time = request.json.get("valve4_time")
        valve4_duration = request.json.get("valve4_duration")
        valve5_active = request.json.get("valve5_active")
        valve5_time = request.json.get("valve5_time")
        valve5_duration = request.json.get("valve5_duration")
        water_refresh_cycle = request.json.get("water_refresh_cycle")
        water_refresh_cycle_length = request.json.get("water_refresh_cycle_length")
        ph_sensor_enabled = request.json.get("ph_sensor_enabled")
        balance_ph = request.json.get("balance_ph")
        ideal_ph = request.json.get("ideal_ph")
        ph_spread = request.json.get("ph_spread")
        ph_valve_time = request.json.get("ph_valve_time")
        ph_balance_interval = request.json.get("ph_balance_interval")
        ph_balance_water_limit = request.json.get("ph_balance_water_limit")
        ph_balance_retry = request.json.get("ph_balance_retry")
        ph_sensor_port = request.json.get("ph_sensor_port")
        enable_web_api = request.json.get("enable_web_api")
        pump_url = request.json.get("pump_url")
        sensor_url = request.json.get("sensor_url")
        enable_tds_meter = request.json.get("enable_tds_meter")
        tds_samples = request.json.get("tds_samples")
        room_temperature = request.json.get("room_temperature")
        sensor_time_api = request.json.get("sensor_time_api")
        soil_dry = request.json.get("soil_dry")
        soil_wet = request.json.get("soil_wet")
        number_of_soil_sensors = request.json.get("number_of_soil_sensors")
        accessed = request.json.get("accessed")
        try:
            update_query = """
            UPDATE autogro_app_api
            SET
            valve1_active = COALESCE(%s, valve1_active),
            valve1_time = COALESCE(%s, valve1_time),
            valve1_duration = COALESCE(%s, valve1_duration),
            valve2_active = COALESCE(%s, valve2_active),
            valve2_time = COALESCE(%s, valve2_time),
            valve2_duration = COALESCE(%s, valve2_duration),
            valve3_active = COALESCE(%s, valve3_active),
            valve3_time = COALESCE(%s, valve3_time),
            valve3_duration = COALESCE(%s, valve3_duration),
            valve4_active = COALESCE(%s, valve4_active),
            valve4_time = COALESCE(%s, valve4_time),
            valve4_duration = COALESCE(%s, valve4_duration),
            valve5_active = COALESCE(%s, valve5_active),
            valve5_time = COALESCE(%s, valve5_time),
            valve5_duration = COALESCE(%s, valve5_duration),
            water_refresh_cycle = COALESCE(%s, water_refresh_cycle),
            water_refresh_cycle_length = COALESCE(%s, water_refresh_cycle_length),
            ph_sensor_enabled = COALESCE(%s, ph_sensor_enabled),
            balance_ph = COALESCE(%s, balance_ph),
            ideal_ph = COALESCE(%s, ideal_ph),
            ph_spread = COALESCE(%s, ph_spread),
            ph_valve_time = COALESCE(%s, ph_valve_time),
            ph_balance_interval = COALESCE(%s, ph_balance_interval),
            ph_balance_water_limit = COALESCE(%s, ph_balance_water_limit),
            ph_balance_retry = COALESCE(%s, ph_balance_retry),
            ph_sensor_port = COALESCE(%s, ph_sensor_port),
            enable_web_api = COALESCE(%s, enable_web_api),
            pump_url = COALESCE(%s, pump_url),
            sensor_url = COALESCE(%s, sensor_url),
            enable_tds_meter = COALESCE(%s, enable_tds_meter),
            tds_samples = COALESCE(%s, tds_samples),
            room_temperature = COALESCE(%s, room_temperature),
            sensor_time_api = COALESCE(%s, sensor_time_api),
            soil_dry = COALESCE(%s, soil_dry),
            soil_wet = COALESCE(%s, soil_wet),
            number_of_soil_sensors = COALESCE(%s, number_of_soil_sensors),
            accessed = COALESCE(%s, accessed)
            WHERE username = %s
            """
        #     update_query = """
        #     UPDATE autogro_app_api
        #     SET valve1_active = %s, valve1_time = %s, valve1_duration = %s,
        #         valve2_active = %s, valve2_time = %s, valve2_duration = %s,
        #         valve3_active = %s, valve3_time = %s, valve3_duration = %s,
        #         valve4_active = %s, valve4_time = %s, valve4_duration = %s,
        #         valve5_active = %s, valve5_time = %s, valve5_duration = %s,
        #         water_refresh_cycle = %s, water_refresh_cycle_length = %s,
        #         ph_sensor_enabled = %s, balance_ph = %s, ideal_ph = %s,
        #         ph_spread = %s, ph_valve_time = %s, ph_balance_interval = %s,
        #         ph_balance_water_limit = %s, ph_balance_retry = %s,
        #         ph_sensor_port = %s, enable_web_api = %s, pump_url = %s,
        #         sensor_url = %s, enable_tds_meter = %s, tds_samples = %s,
        #         room_temperature = %s, sensor_time_api = %s, soil_dry = %s,
        #         soil_wet = %s, number_of_soil_sensors = %s, accessed = %s
        #     WHERE username = %s
        # """
            # Execute the SQL UPDATE statement
            cur.execute(update_query, (
                valve1_active, valve1_time, valve1_duration,
                valve2_active, valve2_time, valve2_duration,
                valve3_active, valve3_time, valve3_duration,
                valve4_active, valve4_time, valve4_duration,
                valve5_active, valve5_time, valve5_duration,
                water_refresh_cycle, water_refresh_cycle_length,
                ph_sensor_enabled, balance_ph, ideal_ph,
                ph_spread, ph_valve_time, ph_balance_interval,
                ph_balance_water_limit, ph_balance_retry,
                ph_sensor_port, enable_web_api, pump_url,
                sensor_url, enable_tds_meter, tds_samples,
                room_temperature, sensor_time_api, soil_dry,
                soil_wet, number_of_soil_sensors, accessed, username))

            conn.commit()
            print("API setting has been updated from app")
        except Exception as e:
            print("Error updating data:", e)
            conn.rollback()
        finally:
            cur.close()
            conn.close()
        return "API setting has been updated from app"

    else:
        return "Unsupported HTTP method"




if __name__ == "__main__":
    app.run(debug=True)
