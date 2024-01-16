# AutoGro API v1

### STATUS : DRAFT

The AutoGro API provides basic CRUD access to the backend database that holds Users and Device data

# QuickStart

Run this API locally by installing Docker Desktop, and then running: 

``` docker-compose up --build ```

This will bring up the application using the default settings -- running at localhost:5010

Run Postman using the sample provided under the Testing folder. Use environment 'local'

# Deploy to AWS

### TODO : CDK
The instances are currently manually deployed with the following configurations:

api-server
 - .012/hour
 - 1GB/1GHz
 - python flask application
 - Security : Port 5010/22 restricted to whitelist

api-db-server
 - .012/hour
 - 1GB/1GHz
 - Security Port 3306/22 exposed only to private IP of api-server

# Technology

### API Service 
A python flask API service using mysql-connector for DB connection

### API Database
MySQL database

## Containerized

Dockerfiles are available for the db and api-service.  To build and run, from the ./deploy folder: 

```
docker-compose build
docker-compose up --build
```
Access the local API by opening postman and switching environments to 'local'.  The defaults in the Postman will direct you to the correct port.

## RESTful Resource Endpoints

The following endpoints are currently available.  

- User 
- Device
- Sensor

Each resource path follows the following pattern:

/{resource}s --> Gives a listing of all resources
/{resource}s/{resourceID} --> Gives access to the resource


## Security

CORS Restricted, API-Key + Secret, TLS, Logging
SqlInjection filtering

## Manual Setup

To setup manually, copy the SQL into a new DB and edit the .env file accordingly.

In MySQL:
 - Import the DB_SETUP.sql into a new DB

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

POSTMAN:  localhost:5010
