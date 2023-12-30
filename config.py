import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    AG_RUN_MODE = 'Development'
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DebugMode = True
    ServerHost='localhost'
    ServerPort='5000'

    dbHostName = os.getenv('AG_DB_HOST')
    dbPortNumber = os.getenv('AG_DB_PORT')
    dbName = os.getenv('AG_DB_NAME')
    dbUser = os.getenv('AG_DB_USER')
    dbPassword = os.getenv('AG_DB_PASSWORD')

    dbOGName = os.getenv('AG_DB_OG_NAME')
    dbOGUser = os.getenv('AG_DB_OG_USER')
    dbOGPassword = os.getenv('AG_DB_OG_PASSWORD')    
