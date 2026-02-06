-- Create database for Indian weather-transport analysis
CREATE DATABASE india_weather_db;

-- Connect to the database
\c india_weather_db;

-- Create main fact table
CREATE TABLE india_transport_delays (
    date DATE NOT NULL,
    city VARCHAR(50) NOT NULL,
    route_id VARCHAR(100) NOT NULL,
    route_name VARCHAR(200),
    avg_delay_minutes FLOAT,
    total_trips INTEGER,
    precipitation FLOAT,
    avg_temp FLOAT,
    temp_max FLOAT,
    temp_min FLOAT,
    humidity FLOAT,
    wind_speed FLOAT,
    weather_condition VARCHAR(50),
    season VARCHAR(50),
    PRIMARY KEY (date, city, route_id)
);

-- Create indexes for better query performance
CREATE INDEX idx_date ON india_transport_delays(date);
CREATE INDEX idx_city ON india_transport_delays(city);
CREATE INDEX idx_weather ON india_transport_delays(weather_condition);
CREATE INDEX idx_season ON india_transport_delays(season);

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE india_weather_db TO postgres;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO postgres;
