-- init.sql
CREATE DATABASE IF NOT EXISTS futbol_db;

USE futbol_db;
-- Tabla de competiciones
CREATE TABLE IF NOT EXISTS dim_competitions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- Tabla de equipos
CREATE TABLE IF NOT EXISTS dim_teams (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);
-- Tabla de fechas
CREATE TABLE IF NOT EXISTS dim_dates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    year INT,
    month INT,
    day INT,
    day_of_week INT,
    is_weekend BOOLEAN
);
-- Tabla de estadísticas de partidos
CREATE TABLE IF NOT EXISTS dim_match_stats (
    id INT AUTO_INCREMENT PRIMARY KEY,
    possession_home FLOAT,
    shots_on_target_home INT,
    shots_on_target_away INT
);
-- Tabla de hechos de partidos
CREATE TABLE IF NOT EXISTS facts_matches (
    id INT AUTO_INCREMENT PRIMARY KEY,
    home_team_id INT,
    away_team_id INT,
    home_score INT,
    away_score INT,
    stats_id INT,
    date_id INT,
    competition_id INT,
    FOREIGN KEY (home_team_id) REFERENCES dim_teams(id),
    FOREIGN KEY (away_team_id) REFERENCES dim_teams(id),
    FOREIGN KEY (stats_id) REFERENCES dim_match_stats(id),
    FOREIGN KEY (date_id) REFERENCES dim_dates(id),
    FOREIGN KEY (competition_id) REFERENCES dim_competitions(id)
);
-- Insertar datos de ejemplo
INSERT INTO dim_competitions (name) VALUES 
('La Liga'),
('Premier League'),
('Bundesliga'),
('Serie A'),
('Ligue 1');
