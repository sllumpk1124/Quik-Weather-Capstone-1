-- Table: users
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(128) NOT NULL
    first_login BOOLEAN DEFAULT TRUE
);

-- Table: cities
CREATE TABLE cities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    country VARCHAR(50),
    latitude FLOAT CHECK (latitude >= -90 AND latitude <= 90),
    longitude FLOAT CHECK (longitude >= -180 AND longitude <= 180)
);

-- Table: weather
CREATE TABLE weather (
    id SERIAL PRIMARY KEY,
    city_id INTEGER REFERENCES cities(id) ON DELETE CASCADE UNIQUE,
    current_temp FLOAT,
    current_conditions VARCHAR(50),
    high_temp FLOAT,
    low_temp FLOAT,
    forecast JSON,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: favorites
CREATE TABLE favorites (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    city_id INTEGER REFERENCES cities(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT user_city_uc UNIQUE (user_id, city_id)
);


