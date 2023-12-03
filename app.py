import os
from flask import Flask, g
from config import Config
from db import get_db
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
   
def load_apis():
    # Blueprints and routes
    from resources.users import users_api
    app.register_blueprint(users_api)

    from resources.user_api_keys import user_keys_api 
    app.register_blueprint(user_keys_api)

# Attach the get_db function to the application context
@app.before_request
def before_request():
    g.db = get_db()

@app.teardown_request
def teardown_request(exception):
    # Close the cursor if it exists in the 'g' object
    db = getattr(g, 'db', None)
    if db is not None:
        db.cursor().close()    

if __name__ == '__main__':
    app.config['AG_RUN_MODE'] = os.getenv('AG_RUN_MODE', 'development')
    app.config.from_object(Config())
    load_apis()

    
    app.run(host=Config.ServerHost, port=Config.ServerPort)