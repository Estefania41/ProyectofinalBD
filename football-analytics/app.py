import os
import dash
from dash import dcc, html, Input, Output, dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import networkx as nx
from sqlalchemy import create_engine, text
import logging
from datetime import datetime
from dotenv import load_dotenv
import time
# Cargar variables de entorno
load_dotenv()

# Configuración básica
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración de recursos externos
external_stylesheets = [
    "https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600&display=swap",
    "https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css"
]

# Configuración de la aplicación
app = dash.Dash(
    __name__,
    title="Análisis de Fútbol",
    update_title="Cargando...",
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True
)

server = app.server

# Layout de la aplicación
app.layout = html.Div(style={'fontFamily': 'Open Sans, sans-serif'}, children=[
    # Header
    html.Div(style={
        'backgroundColor': '#2c3e50', 
        'color': 'white', 
        'padding': '20px', 
        'marginBottom': '20px', 
        'borderRadius': '5px'
    }, children=[
        html.H1("Análisis de Rendimiento en Fútbol", style={'margin': '0'}),
        html.P("Visualización interactiva de estadísticas de partidos", style={'margin': '5px 0 0 0'}),
    ]),
    # Filtros
    html.Div(style={
        'display': 'flex', 
        'flexWrap': 'wrap', 
        'gap': '20px', 
        'marginBottom': '20px', 
        'backgroundColor': '#f8f9fa', 
        'padding': '15px', 
        'borderRadius': '5px'
    }, children=[
        dcc.DatePickerRange(
            id='date-range',
            min_date_allowed=datetime(2020, 1, 1),
            max_date_allowed=datetime.now(),
            start_date=datetime(2023, 1, 1),
            end_date=datetime.now()
        ),
        dcc.Dropdown(
            id='competition-filter', 
            multi=True, 
            placeholder="Todas las competiciones"
        ),
        dcc.Dropdown(
            id='team-filter', 
            multi=True, 
            placeholder="Todos los equipos"
        )
    ]),
 # KPIs
    html.Div(style={
        'display': 'grid', 
        'gridTemplateColumns': 'repeat(auto-fit, minmax(200px, 1fr))', 
        'gap': '15px', 
        'marginBottom': '20px'
    }, children=[
        html.Div(id='total-matches', className='kpi-box'),
        html.Div(id='home-win-rate', className='kpi-box'),
        html.Div(id='avg-possession', className='kpi-box'),
        html.Div(id='goals-per-match', className='kpi-box')
    ]),
    
    # Gráficos
    html.Div(style={
        'display': 'grid', 
        'gridTemplateColumns': '1fr', 
        'gap': '20px', 
        'marginBottom': '20px'
    }, children=[
        dcc.Graph(id='goals-comparison-chart'),
        dcc.Graph(id='results-distribution'),
        dcc.Graph(id='directed-graph')       # Gráfico dirigido
    ]),
    # Tabla de datos
    html.Div(style={'marginBottom': '20px'}, children=[
        html.H3("Detalle de Partidos", style={'marginBottom': '10px'}),
        html.Div(id='matches-table')
    ]),
    
    # Footer
    html.Footer(style={
        'backgroundColor': '#2c3e50', 
        'color': 'white', 
        'padding': '15px', 
        'textAlign': 'center', 
        'borderRadius': '5px'
    }, children=[
        html.P("Football Analytics Dashboard"),
        html.P(f"Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    ])
])
