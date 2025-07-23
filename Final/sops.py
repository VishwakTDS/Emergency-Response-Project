import os
import re
import json
import psycopg2
from config import sql_host, sql_database, sql_user, sql_password

def main():
    conn = psycopg2.connect(
        host     = sql_host,
        port     = os.getenv("SQL_PORT",   "5432"),
        dbname   = sql_database,
        user     = sql_user,
        password = sql_password
    )
    cur = conn.cursor()

    # Create table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS threats (
        threat_id                 SERIAL PRIMARY KEY,
        threat_name               TEXT    NOT NULL,
        threat_cause              TEXT  NOT NULL,
        UNIQUE (threat_name, threat_cause)
        );
                
    CREATE TABLE IF NOT EXISTS agencies (
            agency_id           SERIAL PRIMARY KEY,
            agency_name         TEXT NOT NULL UNIQUE
        );
                
    CREATE TABLE IF NOT EXISTS sops (
            sop_id              SERIAL PRIMARY KEY,
            threat_id           INTEGER NOT NULL
                REFERENCES  threats(threat_id) ON DELETE CASCADE,
            ics_level           INTEGER NOT NULL,
            agency_id           INTEGER NOT NULL
                REFERENCES agencies(agency_id) ON DELETE CASCADE,
            standard_operating_procedure        TEXT NOT NULL,
            resources_required  TEXT,
            UNIQUE (threat_id, ics_level, agency_id)
        );

    """)
    conn.commit()

    print(f"Created SOPs table")
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()

