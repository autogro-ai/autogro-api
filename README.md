# AutoGro API v1

The AutoGro API offers access to the backend database

## Resource CRUD Endpoints

User 
Device
Sensor

## Security

CORS Restricted, API-Key + Secret, TLS, Logging
SqlInjection filtering

## Setup

In MySQL:
 - Import the DB_SETUP.sql into a new DB
 - Add a user for the API execution - only allow SELECT, INSERT, UPDATE, DELETE

Copy .env.example into new file .env and edit:

#Execution Mode -'Development Testing or Production'
AG_RUN_MODE='Development'

#API Server
AG_API_SERVER_HOST='localhost'
AG_API_SERVER_PORT='5010'

AG_DB_HOST='localhost'
AG_DB_PORT='8889'
AG_DB_NAME='autogro'
AG_DB_USER='needs to match what you created in the DB'
AG_DB_PASSWORD='HUf1ZT$cDYFcO8nYu!FH'

# Start the API Server

py app.py

# Add a new user

POSTMAN:  localhost:8889
