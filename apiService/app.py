import os
from flask import Flask, g
from config import Config
from db import get_db, get_db_OG
from dotenv import load_dotenv

load_dotenv()

print(os.getenv('AG_DB_HOST'))

app = Flask(__name__)

print('starting the api server...')
   
def load_apis():
    # Blueprints and routes
    from resources.users import users_api
    app.register_blueprint(users_api)

    from resources.user_api_keys import user_keys_api 
    app.register_blueprint(user_keys_api)

    from resources.gro_models import gromodels_api 
    app.register_blueprint(gromodels_api)    

    from resources.gro_instances import groinstances_api 
    app.register_blueprint(groinstances_api)    

    from resources.gro_component_types import gro_component_types_api 
    app.register_blueprint(gro_component_types_api)    

    from resources.gro_component_data import gro_component_data_api 
    app.register_blueprint(gro_component_data_api)        





# Attach the get_db function to the application context
@app.before_request
def before_request():
    db = getattr(g, 'db', None)
    if db is None:    
        g.db = get_db()
        #g.dbog = get_db_OG()

@app.teardown_request
def teardown_request(exception):
    # Close the cursor if it exists in the 'g' object
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()    
    ''' dbog = getattr(g, 'dbog', None)
    if dbog is not None:
        dbog.cursor().close()           
    '''

if __name__ == '__main__':
    app.config['AG_RUN_MODE'] = os.getenv('AG_RUN_MODE', 'development')
    app.config.from_object(Config())
    load_apis()

    
    app.run(host=Config.ServerHost, port=Config.ServerPort)