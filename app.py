from flask import Flask

app = Flask(__name__)

# Load config
app.config.from_object('config.DevelopmentConfig')

# Initialize database
from db import init_db
init_db(app)

# Blueprints and routes
from resources.users import users_api # Import the api 
app.register_blueprint(users_api) # Register the blueprint

    
if __name__ == '__main__':
    app.run()