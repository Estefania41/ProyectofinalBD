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
