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
# CONFIGURACIÓN DE BASE DE DATOS
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'db'),
    'port': os.getenv('DB_PORT', '3306'),
    'user': os.getenv('DB_USER', 'futbol_user'),
    'password': os.getenv('DB_PASSWORD', 'futbol_pass'),
    'database': os.getenv('DB_NAME', 'futbol_db'),
    'auth_plugin': 'mysql_native_password'
}

def get_db_connection():
    """Establece conexión con la base de datos MySQL con reintentos"""
    max_retries = 5
    retry_delay = 5
    
    for attempt in range(max_retries):
        try:
            engine = create_engine(
                f"mysql+mysqlconnector://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}",
                pool_pre_ping=True,
                pool_recycle=3600,
                connect_args={
                    'connect_timeout': 10,
                    'auth_plugin': DB_CONFIG['auth_plugin']
                }
            )
            logger.info("✅ Conexión exitosa a MySQL")
            return engine
        except Exception as e:
            logger.error(f"⚠️ Intento {attempt + 1} de {max_retries}: Error de conexión - {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
    
    raise ConnectionError("❌ No se pudo conectar a la base de datos después de varios intentos")

def load_match_data():
    """Carga los datos de partidos desde la base de datos"""
    try:
        engine = get_db_connection()
        query = text("""
            SELECT
                ht.name as home_team,
                at.name as away_team,
                fm.home_score,
                fm.away_score,
                ms.possession_home,
                ms.shots_on_target_home,
                ms.shots_on_target_away,
                CONCAT(d.year, '-', LPAD(d.month, 2, '0'), '-', LPAD(d.day, 2, '0')) AS match_date,  -- Crear la fecha
                c.name as competition
            FROM facts_matches fm
            JOIN dim_teams ht ON fm.home_team_id = ht.id
            JOIN dim_teams at ON fm.away_team_id = at.id
            JOIN dim_match_stats ms ON fm.stats_id = ms.id
            JOIN dim_dates d ON fm.date_id = d.id
            JOIN dim_competitions c ON fm.competition_id = c.id
            WHERE fm.home_score IS NOT NULL
            ORDER BY match_date DESC
            LIMIT 1000
        """)
        
        with engine.connect() as conn:
            df = pd.read_sql(query, conn)
        
        if not df.empty:
# Procesamiento de datos
            df['match_date'] = pd.to_datetime(df['match_date'])
            df['result'] = df.apply(
                lambda x: 'Local' if x['home_score'] > x['away_score'] else 
                         'Visitante' if x['home_score'] < x['away_score'] else 'Empate',
                axis=1
            )
            df['total_goals'] = df['home_score'] + df['away_score']
            df['possession_away'] = 100 - df['possession_home']
        
        return df
    except Exception as e:
        logger.error(f"❌ Error al cargar datos: {str(e)}")
        return pd.DataFrame()
    finally:
        if 'engine' in locals():
            engine.dispose()

def create_empty_figure(message):
    # Función mejorada para crear grafos dirigidos
def create_directed_graph(df, graph_type='wins', threshold=3):
    """Crea un grafo dirigido con manejo robusto de errores"""
    try:
        if df.empty or 'home_team' not in df.columns or 'away_team' not in df.columns:
            return create_empty_figure("Datos insuficientes")
        
        G = nx.DiGraph()
        all_teams = pd.unique(df[['home_team', 'away_team']].values.ravel('K'))
        G.add_nodes_from(all_teams)
        # Validar columnas requeridas
        required_cols = ['home_score', 'away_score'] if graph_type in ['wins', 'goals', 'home-away'] else []
        if any(col not in df.columns for col in required_cols):
            return create_empty_figure("Datos requeridos no disponibles")
        
        edge_data = []
        
        if graph_type == 'wins':
            for _, row in df.iterrows():
                if row['home_score'] > row['away_score']:
                    edge_data.append((row['home_team'], row['away_team'], {'weight': 1}))
                elif row['home_score'] < row['away_score']:
                    edge_data.append((row['away_team'], row['home_team'], {'weight': 1}))
        
        elif graph_type == 'goals':
            for _, row in df.iterrows():
                goal_diff = row['home_score'] - row['away_score']
                if goal_diff > 0:
                    edge_data.append((row['home_team'], row['away_team'], {'weight': goal_diff}))
                elif goal_diff < 0:
                    edge_data.append((row['away_team'], row['home_team'], {'weight': abs(goal_diff)}))
        
        elif graph_type == 'home-away':
            home_wins = df[df['result'] == 'Local'].groupby(['home_team', 'away_team']).size()
            away_wins = df[df['result'] == 'Visitante'].groupby(['home_team', 'away_team']).size()
            
            for (home, away), count in home_wins.items():
                if count >= threshold:
                    edge_data.append((home, away, {'weight': count}))
            
            for (home, away), count in away_wins.items():
                if count >= threshold:
                    edge_data.append((away, home, {'weight': count}))
        
    """Crea una figura vacía con un mensaje"""
    return go.Figure(data=[], layout=go.Layout(title=message))
# Añadir relaciones con manejo seguro
        for edge in edge_data:
            try:
                G.add_edge(edge[0], edge[1], **edge[2])
            except Exception as e:
                logger.warning(f"Error añadiendo arista: {str(e)[:200]}")
                continue
# Eliminar nodos aislados
        G.remove_nodes_from(list(nx.isolates(G)))
        
        if len(G.nodes) == 0:
            return create_empty_figure("No hay relaciones significativas")
        
        # Generar visualización con cálculo seguro de pesos
        pos = nx.spring_layout(G, k=0.5, iterations=50)
        edge_weights = [d.get('weight', 1) for _, _, d in G.edges(data=True)]
        max_weight = max(edge_weights) if edge_weights else 1
        
        edge_traces = []
        for edge in G.edges(data=True):
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            
            line_width = 1 + 2 * edge[2].get('weight', 1) / max_weight
            
            edge_trace = go.Scatter(
                x=[x0, x1], y=[y0, y1],
                line=dict(width=line_width, color='#888'),
                hoverinfo='text',
                text=edge[2].get('label', ''),
                mode='lines',
                line_shape='spline'
            )
            edge_traces.append(edge_trace)
        
        node_trace = go.Scatter(
            x=[pos[node][0] for node in G.nodes()],
            y=[pos[node][1] for node in G.nodes()],
            mode='markers+text',
            text=list(G.nodes()),
            textposition="top center",
            marker=dict(
                showscale=True,
                colorscale='Rainbow',
                size=20,
                color=[G.in_degree(node, weight='weight') for node in G.nodes()],
                colorbar=dict(title='Influencia Recibida')
            )
        )
        
        fig = go.Figure(data=edge_traces + [node_trace],
                     layout=go.Layout(
                        title=f'Relaciones entre Equipos - {graph_type}',
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20,l=5,r=5,t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))
        
        return fig
    
    except Exception as e:
        logger.error(f"Error al crear grafo: {str(e)[:200]}")
        return create_empty_figure("Error generando gráfico")
