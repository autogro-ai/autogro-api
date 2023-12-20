from flask import Flask, redirect, render_template, request, url_for, g, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, login_user, logout_user, UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
import mysql.connector
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import json
import datetime
from dotenv import load_dotenv
from pathlib import Path
import os
# from tools.email_sender import EmailSender
# from enums import MessageType

app = Flask(__name__)
app.config["DEBUG"] = True
ma = Marshmallow(app)
cors = CORS(app)


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
    'password': '',
    'host': 'autogro.mysql.pythonanywhere-services.com',
    'port': '3306',
    'database': '',
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

# Endpoint for user registration
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"message": "Please provide username, email, and password"}), 400

    # Check if the username or email already exists
    for user in users:
        if user["username"] == username:
            return jsonify({"message": "Username already exists"}), 400
        if user["email"] == email:
            return jsonify({"message": "Email already exists"}), 400

    # Store the user data (you should use a real database for this)
    new_user = {
        "username": username,
        "email": email,
        "password": password
    }
    users.append(new_user)

    conn = get_db()
    cur = conn.cursor()
    insert_query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
    cur.execute(insert_query, (username, email, password))
    print(insert_query, 'Sucess')
    # Check if the user is already in the autogro_app_api table
    cur.execute('SELECT username FROM autogro_app_api WHERE username = %s', (username,))
    existing_user = cur.fetchone()

    if not existing_user:
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


        # This creates default values for users when they register through the app
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Create a dictionary with all parameters and initialize them
        user_data = {
            "accessed": now,
            "balance_ph": None,
            "enable_tds_meter": None,
            "enable_web_api": None,
            "id": 1,
            "ideal_ph": None,
            "number_of_soil_sensors": None,
            "ph_balance_interval": None,
            "ph_balance_retry": None,
            "ph_balance_water_limit": None,
            "ph_sensor_enabled": None,
            "ph_sensor_port": None,
            "ph_spread": None,
            "ph_valve_time": None,
            "pump_url": None,
            "room_temperature": None,
            "sensor_time_api": None,
            "sensor_url": None,
            "soil_dry": None,
            "soil_wet": None,
            "tds_samples": None,
            "username": "sam",
            "valve1_active": "True",
            "valve1_duration": "69",
            "valve1_time": "100",
            "valve2_active": "",
            "valve2_duration": "",
            "valve2_time": "",
            "valve3_active": None,
            "valve3_duration": None,
            "valve3_time": None,
            "valve4_active": None,
            "valve4_duration": None,
            "valve4_time": None,
            "valve5_active": None,
            "valve5_duration": None,
            "valve5_time": None,
            "water_refresh_cycle": None,
            "water_refresh_cycle_length": None
        }

        # Now you can update specific fields as needed
        user_data["balance_ph"] = 123.45  # Update balance_ph, for example
        user_data["enable_tds_meter"] = True  # Update enable_tds_meter, for example
        user_data["enable_web_api"] = False  # Update enable_web_api, for example
        user_data["id"] = 2  # Update id, for example
        user_data["ph_balance_interval"] = 60  # Update ph_balance_interval, for example
        user_data["ph_balance_retry"] = 3  # Update ph_balance_retry, for example
        user_data["ph_balance_water_limit"] = 500  # Update ph_balance_water_limit, for example
        user_data["ph_sensor_enabled"] = True  # Update ph_sensor_enabled, for example
        user_data["ph_sensor_port"] = "/dev/ttyUSB0"  # Update ph_sensor_port, for example
        user_data["ph_spread"] = 0.1  # Update ph_spread, for example
        user_data["ph_valve_time"] = 10  # Update ph_valve_time, for example
        user_data["pump_url"] = "http://example.com/pump"  # Update pump_url, for example
        user_data["room_temperature"] = 25.0  # Update room_temperature, for example
        user_data["sensor_time_api"] = "http://example.com/sensor-time"  # Update sensor_time_api, for example
        user_data["sensor_url"] = "http://example.com/sensor"  # Update sensor_url, for example
        user_data["soil_dry"] = 300  # Update soil_dry, for example
        user_data["soil_wet"] = 700  # Update soil_wet, for example
        user_data["tds_samples"] = 5  # Update tds_samples, for example
        user_data["valve2_active"] = "False"  # Update valve2_active, for example
        user_data["valve2_duration"] = "50"  # Update valve2_duration, for example
        user_data["valve3_active"] = "Yes"  # Update valve3_active, for example
        user_data["valve3_duration"] = "60"  # Update valve3_duration, for example
        user_data["valve3_time"] = "250"  # Update valve3_time, for example
        user_data["valve4_active"] = "True"  # Update valve4_active, for example
        user_data["valve4_duration"] = "70"  # Update valve4_duration, for example
        user_data["valve4_time"] = "300"  # Update valve4_time, for example
        user_data["valve5_active"] = "False"  # Update valve5_active, for example
        user_data["valve5_duration"] = "80"  # Update valve5_duration, for example
        user_data["valve5_time"] = "350"  # Update valve5_time, for example
        user_data["water_refresh_cycle"] = "Daily"  # Update water_refresh_cycle, for example
        user_data["water_refresh_cycle_length"] = "10 hours"  # Update water_refresh_cycle_length, for example

        try:
            cur.execute('INSERT INTO autogro_app_api (username, valve1_active, valve1_time, valve1_duration, valve2_active, valve2_time, valve2_duration, valve3_active, valve3_time, valve3_duration, valve4_active, valve4_time, valve4_duration, valve5_active, valve5_time, valve5_duration, water_refresh_cycle, water_refresh_cycle_length, ph_sensor_enabled, balance_ph, ideal_ph, ph_spread, ph_valve_time, ph_balance_interval, ph_balance_water_limit, ph_balance_retry, ph_sensor_port, enable_web_api, pump_url, sensor_url, enable_tds_meter, tds_samples, room_temperature, sensor_time_api, soil_dry, soil_wet, number_of_soil_sensors, accessed) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (
                user_data["username"], user_data["valve1_active"], user_data["valve1_time"], user_data["valve1_duration"], user_data["valve2_active"], user_data["valve2_time"], user_data["valve2_duration"], user_data["valve3_active"], user_data["valve3_time"], user_data["valve3_duration"], user_data["valve4_active"], user_data["valve4_time"], user_data["valve4_duration"], user_data["valve5_active"], user_data["valve5_time"], user_data["valve5_duration"], user_data["water_refresh_cycle"], user_data["water_refresh_cycle_length"], user_data["ph_sensor_enabled"], user_data["balance_ph"], user_data["ideal_ph"], user_data["ph_spread"], user_data["ph_valve_time"], user_data["ph_balance_interval"], user_data["ph_balance_water_limit"], user_data["ph_balance_retry"], user_data["ph_sensor_port"], user_data["enable_web_api"], user_data["pump_url"], user_data["sensor_url"], user_data["enable_tds_meter"], user_data["tds_samples"], user_data["room_temperature"], user_data["sensor_time_api"], user_data["soil_dry"], user_data["soil_wet"], user_data["number_of_soil_sensors"], user_data["accessed"]
            ))
            conn.commit()
        except Exception as e:
            print("Error inserting data:", e)
            conn.rollback()
        finally:
            cur.close()
            conn.close()
        # now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return "App Data inserted to API Successfully"

    else:
        return "Unsupported HTTP method"



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


        # try:
        #     cur.execute('INSERT INTO autogro_app_api (username, valve1_active, valve1_time, valve1_duration, valve2_active, valve2_time, valve2_duration, valve3_active, valve3_time, valve3_duration, valve4_active, valve4_time, valve4_duration, valve5_active, valve5_time, valve5_duration, water_refresh_cycle, water_refresh_cycle_length, ph_sensor_enabled, balance_ph, ideal_ph, ph_spread, ph_valve_time, ph_balance_interval, ph_balance_water_limit, ph_balance_retry, ph_sensor_port, enable_web_api, pump_url, sensor_url, enable_tds_meter, tds_samples, room_temperature, sensor_time_api, soil_dry, soil_wet, number_of_soil_sensors, accessed) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (username, valve1_active, valve1_time, valve1_duration, valve2_active, valve2_time, valve2_duration, valve3_active, valve3_time, valve3_duration, valve4_active, valve4_time, valve4_duration, valve5_active, valve5_time, valve5_duration, water_refresh_cycle, water_refresh_cycle_length, ph_sensor_enabled, balance_ph, ideal_ph, ph_spread, ph_valve_time, ph_balance_interval, ph_balance_water_limit, ph_balance_retry, ph_sensor_port, enable_web_api, pump_url, sensor_url, enable_tds_meter, tds_samples, room_temperature, sensor_time_api, soil_dry, soil_wet, number_of_soil_sensors, accessed))
        #     conn.commit()
        #     print("API setting has been updated from app")
        # except Exception as e:
        #     print("Error inserting data:", e)
        #     conn.rollback()
        # finally:
        #     cur.close()
        #     conn.close()
        # return "API setting has been updated from app"

    else:
        return "Unsupported HTTP method"


###########################################


########### OG Pump ###########
# @app.route('/get_test_data', methods=["GET"])
# def get_test_data():
#     page = request.args.get('page', default=1, type=int)
#     items_per_page = 100
#     conn = get_db()
#     cur = conn.cursor()
#     # Calculate the offset based on the page number and items per page
#     offset = (page - 1) * items_per_page
#     # Retrieve the data for the current page
#     cur.execute(f'SELECT pump_status, flow_meter_rotations, valve_1, accessed from send_data_test')
#     row_headers = [x[0] for x in cur.description]
#     results = cur.fetchall()
#     json_data = []
#     for result in results:
#         json_data.append(dict(zip(row_headers, result)))
#     return jsonify(json_data)
#     return json.dumps(json_data)





if __name__ == "__main__":
    app.run(debug=True)