import os
import time
import mysql.connector
from mysql.connector import errorcode
import requests
from dotenv import load_dotenv
load_dotenv()

# Configuración de la API
API_KEY = '1f21c76952a447f9abf40ace1a8879b4'
BASE_URL = 'http://api.football-data.org/v4/'
# Configuración de la base de datos
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'db'),
    'user': os.getenv('DB_USER', 'futbol_user'),
    'password': os.getenv('DB_PASSWORD', 'futbol_pass'),
    'database': os.getenv('DB_NAME', 'futbol_db'),
    'port': os.getenv('DB_PORT', 3306),
    'auth_plugin': 'mysql_native_password'
}
