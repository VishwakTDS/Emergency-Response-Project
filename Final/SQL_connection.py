import psycopg2
from langchain.docstore.document import Document
import os

def connection_sql(dbname):
    results = None
    try:
        conn = psycopg2.connect(
            dbname=dbname,
            user=os.environ.get("SQL_USER", ""),
            password=os.environ.get("SQL_PASSWORD", ""),
            host="localhost"
        )

        cur = conn.cursor()

        cur.execute('SELECT we.event_id, we.date, we.location, we.cause, we.area_burned, we.duration, ec.temperature, ec.humidity, ' \
                    'ec.wind_speed, ec.precipitation, ra.action_type, ra.resources_used, ra.outcome, hd.lessons_learned, hd.recommendations ' \
                    'FROM wildfire_events we ' \
                    'JOIN environmental_conditions ec ON we.event_id = ec.event_id ' \
                    'JOIN response_actions ra ON we.event_id = ra.event_id ' \
                    'JOIN historical_data hd ON we.event_id = hd.event_id;')

        results = cur.fetchall()

        return results
    
    except Exception as e:
        print(f"Cannot load database: {e}")
        return None

    finally:
        cur.close()

        if conn:
            conn.close()

def preprocess_sql(results):
    documents = []
    for row in results:
        event_id, date, location, cause, area_burned, duration, temperature, humidity, wind_speed, precipitation, action_type, resources_used, outcome, lessons_learned, recommendations = row

        # Create a document for each row
        content = f"""
        Event ID: {event_id}
        Date: {date}
        Location: {location}
        Cause: {cause}
        Area Burned: {area_burned} hectares
        Duration: {duration} days
        Temperature: {temperature}°C
        Humidity: {humidity}%
        Wind Speed: {wind_speed} km/h
        Precipitation: {precipitation} mm
        Action Type: {action_type}
        Resources Used: {resources_used}
        Outcome: {outcome}
        Lessons Learned: {lessons_learned}
        Recommendations: {recommendations}
        """

        doc = Document(
            page_content=content,
            metadata={
                'source': "PostgreSQL Database",
                'event_id': event_id
            }
        )
        documents.append(doc)

    print(f"Loaded {len(documents)} document elements from the database.")

    return documents