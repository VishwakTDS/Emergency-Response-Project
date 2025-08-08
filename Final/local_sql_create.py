import psycopg2
from config import sql_user, sql_password, sql_host, sql_database, sql_port


CONN = dict(
    host=sql_host,
    port=sql_port,
    dbname=sql_database,
    user=sql_user,
    password=sql_password,
)

SCHEMA_SQL = """
-- Agencies
CREATE TABLE IF NOT EXISTS agencies (
  agency_id   SERIAL PRIMARY KEY,
  agency_name TEXT NOT NULL UNIQUE
);

-- Threats
CREATE TABLE IF NOT EXISTS threats (
  threat_id    SERIAL PRIMARY KEY,
  threat_name  TEXT NOT NULL,
  threat_cause TEXT NOT NULL,
  CONSTRAINT uq_threat UNIQUE (threat_name, threat_cause)
);

-- Incidents
CREATE TABLE IF NOT EXISTS incidents (
  id                        SERIAL PRIMARY KEY,
  incident_name             TEXT NOT NULL,
  incident_type             TEXT NOT NULL,
  ics_level                 INT  NOT NULL CHECK (ics_level BETWEEN 1 AND 5),
  location                  TEXT,
  weather                   TEXT,
  resources_required        TEXT,
  identified_cause          TEXT NOT NULL,
  incident_summary          TEXT,
  response_measures         TEXT,
  anticipated_developments  TEXT,
  responding_agencies       TEXT
);

-- SOPs
CREATE TABLE IF NOT EXISTS sops (
  sop_id    SERIAL PRIMARY KEY,
  threat_id INT  NOT NULL REFERENCES threats(threat_id) ON DELETE CASCADE,
  ics_level INT  NOT NULL CHECK (ics_level BETWEEN 1 AND 5),
  agency_id INT  NOT NULL REFERENCES agencies(agency_id) ON DELETE CASCADE,
  standard_operating_procedure TEXT NOT NULL,
  resources_required           TEXT NOT NULL,
  CONSTRAINT uq_sop UNIQUE (threat_id, ics_level, agency_id)
);

-- Agencies Contacts
CREATE TABLE IF NOT EXISTS agency_contact (
    contact_id SERIAL PRIMARY KEY,
    agency_id INT NOT NULL REFERENCES agencies(agency_id),
    agency_name TEXT NOT NULL,
    state_name TEXT NOT NULL,
    email TEXT NOT NULL,
    UNIQUE (agency_id, state_name)
);

"""

def main():
    conn = psycopg2.connect(**CONN)
    try:
        with conn, conn.cursor() as cur:
            cur.execute(SCHEMA_SQL)
        print("Schema created (or already existed).")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
