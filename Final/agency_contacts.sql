-- 1. Create the agency_contact table
CREATE TABLE IF NOT EXISTS agency_contact (
    contact_id SERIAL PRIMARY KEY,
    agency_id INT NOT NULL REFERENCES agencies(agency_id),
    state_name TEXT NOT NULL,
    email TEXT NOT NULL,
    UNIQUE (agency_id, state_name)
);

-- 2. List of 50 US states with full name and state code
WITH states(state_name, state_code) AS (
    VALUES
    ('Alabama', 'AL'),
    ('Alaska', 'AK'),
    ('Arizona', 'AZ'),
    ('Arkansas', 'AR'),
    ('California', 'CA'),
    ('Colorado', 'CO'),
    ('Connecticut', 'CT'),
    ('Delaware', 'DE'),
    ('Florida', 'FL'),
    ('Georgia', 'GA'),
    ('Hawaii', 'HI'),
    ('Idaho', 'ID'),
    ('Illinois', 'IL'),
    ('Indiana', 'IN'),
    ('Iowa', 'IA'),
    ('Kansas', 'KS'),
    ('Kentucky', 'KY'),
    ('Louisiana', 'LA'),
    ('Maine', 'ME'),
    ('Maryland', 'MD'),
    ('Massachusetts', 'MA'),
    ('Michigan', 'MI'),
    ('Minnesota', 'MN'),
    ('Mississippi', 'MS'),
    ('Missouri', 'MO'),
    ('Montana', 'MT'),
    ('Nebraska', 'NE'),
    ('Nevada', 'NV'),
    ('New Hampshire', 'NH'),
    ('New Jersey', 'NJ'),
    ('New Mexico', 'NM'),
    ('New York', 'NY'),
    ('North Carolina', 'NC'),
    ('North Dakota', 'ND'),
    ('Ohio', 'OH'),
    ('Oklahoma', 'OK'),
    ('Oregon', 'OR'),
    ('Pennsylvania', 'PA'),
    ('Rhode Island', 'RI'),
    ('South Carolina', 'SC'),
    ('South Dakota', 'SD'),
    ('Tennessee', 'TN'),
    ('Texas', 'TX'),
    ('Utah', 'UT'),
    ('Vermont', 'VT'),
    ('Virginia', 'VA'),
    ('Washington', 'WA'),
    ('West Virginia', 'WV'),
    ('Wisconsin', 'WI'),
    ('Wyoming', 'WY')
)

-- 3. Insert agency × state combinations with updated email domain
INSERT INTO agency_contact (agency_id, state_name, email)
SELECT 
    a.agency_id,
    s.state_name,
    LOWER(REPLACE(a.agency_name, ' ', '')) 
        || LOWER(s.state_code) 
        || '@emergency' 
        || LOWER(s.state_code) 
        || '.com' AS email
FROM 
    agencies a
CROSS JOIN 
    states s
ORDER BY 
    a.agency_id, s.state_name;