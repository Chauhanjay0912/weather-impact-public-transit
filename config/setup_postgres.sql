-- PostgreSQL Setup for Weather Transport Analysis

-- Create database
CREATE DATABASE weather_db;

-- Connect to database
\c weather_db;

-- Create weather data table
CREATE TABLE IF NOT EXISTS weather_data (
    id SERIAL PRIMARY KEY,
    city VARCHAR(50),
    temperature FLOAT,
    temp_celsius FLOAT,
    humidity FLOAT,
    condition VARCHAR(100),
    wind_speed FLOAT,
    weather_severity VARCHAR(20),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create weather statistics table
CREATE TABLE IF NOT EXISTS weather_stats (
    city VARCHAR(50) PRIMARY KEY,
    avg_temp FLOAT,
    max_wind FLOAT,
    records INT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create transport delays table
CREATE TABLE IF NOT EXISTS transport_delays (
    id SERIAL PRIMARY KEY,
    date DATE,
    city VARCHAR(50),
    route_id VARCHAR(50),
    route_name VARCHAR(100),
    avg_delay_minutes FLOAT,
    total_trips INT,
    weather_condition VARCHAR(50)
);

-- Create indexes
CREATE INDEX idx_weather_city ON weather_data(city);
CREATE INDEX idx_weather_timestamp ON weather_data(timestamp);
CREATE INDEX idx_delays_date ON transport_delays(date);
CREATE INDEX idx_delays_city ON transport_delays(city);

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO postgres;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO postgres;
