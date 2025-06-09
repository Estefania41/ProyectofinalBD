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
