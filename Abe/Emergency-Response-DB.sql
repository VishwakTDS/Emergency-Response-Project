-- Wildfire Events
CREATE TABLE wildfire_events (
    event_id SERIAL PRIMARY KEY,
    date DATE,
    location VARCHAR(100),
    cause VARCHAR(50),
    area_burned FLOAT,
    duration INT
);

-- Environmental Conditions
CREATE TABLE environmental_conditions (
    condition_id SERIAL PRIMARY KEY,
    event_id INT REFERENCES wildfire_events(event_id),
    temperature FLOAT,
    humidity FLOAT,
    wind_speed FLOAT,
    precipitation FLOAT
);

-- Response Actions
CREATE TABLE response_actions (
    action_id SERIAL PRIMARY KEY,
    event_id INT REFERENCES wildfire_events(event_id),
    action_type VARCHAR(50),
    resources_used VARCHAR(100),
    outcome VARCHAR(50)
);

-- Historical Data
CREATE TABLE historical_data (
    record_id SERIAL PRIMARY KEY,
    event_id INT REFERENCES wildfire_events(event_id),
    lessons_learned TEXT,
    recommendations TEXT
);

-- Insert Sample Data
INSERT INTO wildfire_events (date, location, cause, area_burned, duration) VALUES
('2025-06-10', '34.0522,-118.2437', 'Lightning', 1500.5, 3),
('2025-06-15', '37.7749,-122.4194', 'Human Activity', 800.0, 2);

INSERT INTO environmental_conditions (event_id, temperature, humidity, wind_speed, precipitation) VALUES
(1, 35.0, 20.0, 15.0, 0.0),
(2, 30.0, 25.0, 10.0, 0.0);

INSERT INTO response_actions (event_id, action_type, resources_used, outcome) VALUES
(1, 'Firefighting', 'Helicopters, Fire Trucks', 'Contained'),
(2, 'Evacuation', 'Fire Trucks, Police', 'Uncontrolled');

INSERT INTO historical_data (event_id, lessons_learned, recommendations) VALUES
(1, 'Rapid response reduced spread.', 'Increase aerial resources.'),
(2, 'Evacuation was delayed.', 'Improve communication channels.');

-- Add foreign key to environmental_conditions table
ALTER TABLE environmental_conditions
ADD CONSTRAINT fk_event_id
FOREIGN KEY (event_id) REFERENCES wildfire_events(event_id);

-- Add foreign key to response_actions table
ALTER TABLE response_actions
ADD CONSTRAINT fk_event_id
FOREIGN KEY (event_id) REFERENCES wildfire_events(event_id);

-- Add foreign key to historical_data table
ALTER TABLE historical_data
ADD CONSTRAINT fk_event_id
FOREIGN KEY (event_id) REFERENCES wildfire_events(event_id);
