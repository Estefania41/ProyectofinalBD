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
INSERT INTO dim_teams (name) VALUES 
('Real Madrid'),
('Barcelona'),
('Atlético Madrid'),
('Manchester City'),
('Liverpool'),
('Bayern Munich'),
('PSG'),
('Juventus');
-- Insertar fechas de ejemplo
INSERT INTO dim_dates (date, year, month, day, day_of_week, is_weekend) VALUES 
('2023-01-15', 2023, 1, 15, 6, TRUE),
('2023-02-20', 2023, 2, 20, 1, FALSE),
('2023-03-12', 2023, 3, 12, 6, TRUE),
('2023-04-05', 2023, 4, 5, 2, FALSE),
('2023-05-21', 2023, 5, 21, 6, TRUE);
-- Insertar estadísticas de ejemplo
INSERT INTO dim_match_stats (possession_home, shots_on_target_home, shots_on_target_away) VALUES 
(60.5, 7, 3),
(45.2, 4, 6),
(52.1, 5, 5),
(38.7, 2, 8),
(65.3, 8, 2),
(50.0, 6, 6);
-- Insertar partidos de ejemplo
INSERT INTO facts_matches (home_team_id, away_team_id, home_score, away_score, stats_id, date_id, competition_id) VALUES 
(1, 2, 3, 1, 1, 1, 1),
(3, 1, 1, 2, 2, 2, 1),
(4, 5, 2, 2, 3, 3, 2),
(6, 7, 4, 0, 4, 4, 3),
(8, 6, 1, 3, 5, 5, 4),
(2, 3, 2, 1, 6, 1, 1);
