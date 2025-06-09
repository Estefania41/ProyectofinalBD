-- init.sql
CREATE DATABASE IF NOT EXISTS futbol_db;

USE futbol_db;
-- Tabla de competiciones
CREATE TABLE IF NOT EXISTS dim_competitions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
