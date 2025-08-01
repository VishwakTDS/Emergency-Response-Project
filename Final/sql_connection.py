from config import sql_user, sql_password, sql_host

import psycopg2
from langchain.docstore.document import Document

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