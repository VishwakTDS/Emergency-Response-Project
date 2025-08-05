from config import sql_user, sql_password, sql_host, sql_database
import os
import psycopg2
from langchain.docstore.document import Document
from psycopg2.extras import RealDictCursor


def connection_sql(dbname):
    results = None
    try:
        conn = psycopg2.connect(
            dbname=dbname,
            user=sql_user,
            password=sql_password,
            host=sql_host
        )

        cur = conn.cursor()

        cur.execute('SELECT * FROM wildfire_emergencies')

        results = cur.fetchall()

        return results
    
    except Exception as e:
        err = "Unable to load database"
        print(f"error: {err}\n{e}")
        raise Exception(err) from e

    finally:
        cur.close()

        if conn:
            conn.close()


def preprocess_summary_sql(results):
    documents_new = []
    for row in results:
        (incident_id,
         threat_name,
         threat_summary,
         steps_followed,
         resources,
         priority,
         cause,
         first_responders,
         location,
         weather,
         date_occurred,
         time_occurred) = row
        
        content = f"""{threat_summary}"""

        doc = Document(
            page_content=content,
            metadata={
                'source': "PostgreSQL Database",
                'event_id': incident_id,
                'steps_followed':steps_followed
            }
        )
        documents_new.append(doc)

    return documents_new


def preprocess_whole_sql(results,event_ids):
    documents = []
    for row in results:
        (incident_id,
         threat_name,
         threat_summary,
         steps_followed,
         resources,
         priority,
         cause,
         first_responders,
         location,
         weather,
         date_occurred,
         time_occurred) = row
        
        if incident_id in event_ids:
            # Create a document for each row
            content = f"""
            Incident ID   : {incident_id}
            Date / Time   : {date_occurred} {time_occurred}
            Location      : {location}
            Threat Name   : {threat_name}
            Priority      : {priority}
            Cause         : {cause}
            Weather       : {weather}

            Threat Summary
            --------------
            {threat_summary}

            Steps Followed
            --------------
            {steps_followed}

            First Responders : {first_responders}
            Resources Used   : {resources}
            """.strip()

            doc = Document(
                page_content=content,
                metadata={
                    'source': "PostgreSQL Database",
                    'event_id': incident_id
                }
            )
            documents.append(doc)

    return documents


def fetch_threat_info():
    conn = psycopg2.connect(
        host     = sql_host,
        port     = os.getenv("SQL_PORT",   "5432"),
        dbname   = sql_database,
        user     = sql_user,
        password = sql_password
    )
    cur = conn.cursor()

    cur.execute("SELECT DISTINCT threat_name from threats;")
    valid_types = [row[0] for row in cur.fetchall()]
    type_options = ", ".join(f'"{t}"' for t in valid_types + ["Undefined"])

    cur.close()
    conn.close()

    return type_options

def get_threat_data(threat_type, location):
    conn = psycopg2.connect(
        host     = sql_host,
        port     = os.getenv("SQL_PORT",   "5432"),
        dbname   = sql_database,
        user     = sql_user,
        password = sql_password
    )
    cur = conn.cursor()

    if location:
        cur.execute(
            """
            SELECT id, incident_summary
              FROM incidents
             WHERE incident_type = %s
               AND location ILIKE %s
            """,
            (threat_type, f"%{location}%")
        )
        rows = cur.fetchall()
        if rows:
            cur.close()
            return rows
        # else fall through to unfiltered

    cur.execute(
        "SELECT id, incident_summary FROM incidents WHERE incident_type = %s;",
        (threat_type,)
    )
    rows = cur.fetchall()
    cur.close()
    return rows


def fetch_valid_causes(threat_type: str) -> list[str]:
    conn = psycopg2.connect(
        host     = sql_host,
        port     = os.getenv("SQL_PORT",   "5432"),
        dbname   = sql_database,
        user     = sql_user,
        password = sql_password
    )
    cur = conn.cursor()
    cur.execute(
        """
        SELECT threat_cause
          FROM threats
         WHERE threat_name ILIKE %s
           AND threat_cause <> 'Undefined'
        """,
        (threat_type,)
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [r[0] for r in rows]


def get_incidents_by_ids(incident_ids):
    conn = conn = psycopg2.connect(
        host     = sql_host,
        port     = os.getenv("SQL_PORT",   "5432"),
        dbname   = sql_database,
        user     = sql_user,
        password = sql_password
    )
    cur = conn.cursor()
    cur.execute("""
        SELECT 
          id, incident_name, incident_type, ics_level,
          location, weather, resources_required,
          identified_cause, incident_summary,
          response_measures, anticipated_developments,
          responding_agencies
        FROM incidents
        WHERE id = ANY(%s)
        ORDER BY array_position(%s, id);
    """, (incident_ids, incident_ids))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    cols = [
        "id", "incident_name", "incident_type", "ics_level",
        "location", "weather", "resources_required",
        "identified_cause", "incident_summary",
        "response_measures", "anticipated_developments",
        "responding_agencies"
    ]
    return [dict(zip(cols, row)) for row in rows]


def get_incident_by_name(name):
    conn = conn = psycopg2.connect(
        host     = sql_host,
        port     = os.getenv("SQL_PORT",   "5432"),
        dbname   = sql_database,
        user     = sql_user,
        password = sql_password
    )
    cur = conn.cursor()
    cur.execute(
        """
        SELECT
          id, incident_name, incident_type, ics_level,
          location, weather, resources_required,
          identified_cause, incident_summary,
          response_measures, anticipated_developments,
          responding_agencies
        FROM incidents
        WHERE incident_name = %s
        """,
        (name,)
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    cols = [
        "id", "incident_name", "incident_type", "ics_level",
        "location", "weather", "resources_required",
        "identified_cause", "incident_summary",
        "response_measures", "anticipated_developments",
        "responding_agencies"
    ]
    return [dict(zip(cols, row)) for row in rows]


# def fetch_sops(threat_type: str, threat_cause: str, ics_level: int, agencies: list[str]) -> dict:
#     tt = threat_type.strip()
#     tc = threat_cause.strip()
#     ags = [a.strip() for a in agencies if a and isinstance(a, str)]

#     if not ags or tt.lower() == "undefined" or tc.lower() == "undefined":
#         print(f"[fetch_sops] skipping lookup: threat_type={tt}, cause={tc}, agencies={ags}")
#         return None
    
#     conn = conn = psycopg2.connect(
#         host     = sql_host,
#         port     = os.getenv("SQL_PORT",   "5432"),
#         dbname   = sql_database,
#         user     = sql_user,
#         password = sql_password
#     )
#     cur  = conn.cursor(cursor_factory=RealDictCursor)

#     sql = """
#     SELECT a.agency_name,
#            s.standard_operating_procedure AS procedure,
#            s.resources_required        AS resources
#       FROM threats t
#       JOIN sops    s ON s.threat_id = t.threat_id
#       JOIN agencies a ON a.agency_id = s.agency_id
#      WHERE t.threat_name  ILIKE %s
#        AND t.threat_cause ILIKE %s
#        AND s.ics_level    = %s
#        AND a.agency_name  = ANY(%s)
#     """

#     cur.execute(sql, (tt, tc, ics_level, ags))
#     rows = cur.fetchall()
#     cur.close()
#     conn.close()

#     if not rows:
#         return None

#     result = {
#         row["agency_name"]: {
#             "procedure": row["procedure"],
#             "resources": row["resources"]
#         }
#         for row in rows
#     }

#     return result

# import os
# import psycopg2
# from psycopg2.extras import RealDictCursor

# def fetch_sops(threat_type: str,
#                threat_cause: str,
#                ics_level: int,
#                agencies: list[str]) -> dict:
    
#     tt = threat_type.strip()
#     tc = threat_cause.strip()
#     ags = [a.strip() for a in agencies if isinstance(a, str) and a.strip()]

#     if tt.lower() == "undefined" or tc.lower() == "undefined":
#         print(f"[fetch_sops] skipping: undefined threat_type or cause: {tt}, {tc}")
#         return {}

#     if not ags:
#         print(f"[fetch_sops] skipping: no agencies provided")
#         return {}

#     if not isinstance(ics_level, int) or not (1 <= ics_level <= 5):
#         print(f"[fetch_sops] skipping: invalid ics_level = {ics_level}")
#         return {}

#     conn = psycopg2.connect(
#         host     = sql_host,
#         port     = os.getenv("SQL_PORT", "5432"),
#         dbname   = sql_database,
#         user     = sql_user,
#         password = sql_password
#     )
#     cur = conn.cursor(cursor_factory=RealDictCursor)

#     cur.execute("SELECT agency_name FROM agencies WHERE agency_name = ANY(%s);", (ags,))
#     valid_ags = [r["agency_name"] for r in cur.fetchall()]
#     if not valid_ags:
#         print(f"[fetch_sops] skipping: none of the agencies exist in DB: {ags}")
#         cur.close()
#         conn.close()
#         return {}

#     sql = """
#     SELECT a.agency_name,
#            s.standard_operating_procedure AS procedure,
#            s.resources_required        AS resources
#       FROM threats t
#       JOIN sops    s ON s.threat_id = t.threat_id
#       JOIN agencies a ON a.agency_id = s.agency_id
#      WHERE t.threat_name  ILIKE %s
#        AND t.threat_cause ILIKE %s
#        AND s.ics_level    = %s
#        AND a.agency_name  = ANY(%s)
#     """
#     cur.execute(sql, (tt, tc, ics_level, valid_ags))
#     rows = cur.fetchall()
#     cur.close()
#     conn.close()

#     if not rows:
#         print(f"[fetch_sops] no SOPs found for {tt}/{tc}/L{ics_level} @ {valid_ags}")
#         return {}

#     return {
#         row["agency_name"]: {
#             "procedure": row["procedure"],
#             "resources": row["resources"]
#         }
#         for row in rows
#     }


def fetch_sops(threat_type, threat_cause, ics_level, agencies):

    tt = threat_type.strip()
    tc = threat_cause.strip()
    ags = [a.strip() for a in agencies if isinstance(a, str) and a.strip()]

    if not ags:
        print(f"[fetch_sops] skipping: no agencies provided")
        return {}

    if not isinstance(ics_level, int) or not (1 <= ics_level <= 5):
        print(f"[fetch_sops] skipping: invalid ics_level = {ics_level}")
        return {}

    conn = psycopg2.connect(
        host     = sql_host,
        port     = os.getenv("SQL_PORT", "5432"),
        dbname   = sql_database,
        user     = sql_user,
        password = sql_password
    )
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("SELECT DISTINCT threat_name FROM threats WHERE threat_name ILIKE %s", (tt,))
    if cur.rowcount == 0:
        tt = "Undefined"
    cur.execute("SELECT DISTINCT threat_cause FROM threats WHERE threat_name = %s AND threat_cause ILIKE %s", (tt, tc))
    if cur.rowcount == 0:
        tc = "Undefined"

    cur.execute("SELECT agency_name FROM agencies WHERE agency_name = ANY(%s);", (ags,))
    valid_ags = [r["agency_name"] for r in cur.fetchall()]
    if not valid_ags:
        print(f"[fetch_sops] skipping: none of the agencies exist in DB: {ags}")
        cur.close()
        conn.close()
        return {}

    sql = """
    SELECT
      a.agency_name,
      s.standard_operating_procedure AS procedure,
      s.resources_required        AS resources
    FROM threats t
    JOIN sops    s ON s.threat_id   = t.threat_id
    JOIN agencies a ON a.agency_id  = s.agency_id
    WHERE t.threat_name  = %s
      AND t.threat_cause = %s
      AND s.ics_level    = %s
      AND a.agency_name  = ANY(%s)
    """
    cur.execute(sql, (tt, tc, ics_level, valid_ags))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    if not rows:
        print(f"[fetch_sops] no SOPs found for {tt}/{tc}/L{ics_level} @ {valid_ags}")
        return {}

    return {
        row["agency_name"]: {
            "procedure": row["procedure"],
            "resources": row["resources"]
        }
        for row in rows
    }
