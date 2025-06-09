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
def get_headers():
    return {'X-Auth-Token': API_KEY}
def connect_db(max_retries=5, retry_delay=5):
    """Conexión a la base de datos con reintentos"""
    for attempt in range(max_retries):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            print("✅ Conexión exitosa a MySQL")
            return conn
        except mysql.connector.Error as err:
            print(f"⚠️ Intento {attempt + 1} de {max_retries}: Error de conexión - {err}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
   raise Exception("❌ No se pudo conectar a la base de datos")
def setup_database(conn):
        """Crear tablas si no existen con sintaxis corregida"""
    tables = {
        'dim_competitions': """
            CREATE TABLE IF NOT EXISTS dim_competitions (
                id INT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                code VARCHAR(10),
                area_name VARCHAR(100)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """,
        'dim_teams': """
            CREATE TABLE IF NOT EXISTS dim_teams (
                id INT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                short_name VARCHAR(50),
                tla VARCHAR(10),
                crest_url VARCHAR(255)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """,
                'dim_dates': """
            CREATE TABLE IF NOT EXISTS dim_dates (
                id DATE PRIMARY KEY,
                day INT,
                month INT,
                year INT,
                day_of_week INT
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """,
        'dim_match_stats': """
            CREATE TABLE IF NOT EXISTS dim_match_stats (
                id INT AUTO_INCREMENT PRIMARY KEY,
                possession_home INT,
                shots_home INT,
                shots_on_target_home INT,
                shots_away INT,
                shots_on_target_away INT,
                corners_home INT,
                corners_away INT,
                fouls_home INT,
                fouls_away INT
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """,
