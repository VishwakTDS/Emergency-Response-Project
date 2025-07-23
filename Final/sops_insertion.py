import os
import psycopg2
from psycopg2.extras import RealDictCursor
from config import sql_host, sql_database, sql_user, sql_password


def find_missing_sops():
    conn = psycopg2.connect(
        host     = sql_host,
        port     = os.getenv("SQL_PORT",   "5432"),
        dbname   = sql_database,
        user     = sql_user,
        password = sql_password
    )
    cur = conn.cursor(cursor_factory=RealDictCursor)

    # 1) fetch all threat_id, threat_name, threat_cause
    cur.execute("SELECT threat_id, threat_name, threat_cause FROM threats;")
    threats = cur.fetchall()

    report = []

    for th in threats:
        tid, tname, tcause = th["threat_id"], th["threat_name"], th["threat_cause"]
        # 2) collect all agencies that responded to incidents of this type/cause
        cur.execute("""
            SELECT responding_agencies
            FROM incidents
            WHERE incident_type = %s
              AND identified_cause = %s
        """, (tname, tcause))
        rows = cur.fetchall()
        agencies = set()
        for r in rows:
            for a in (r["responding_agencies"] or "").split(","):
                a = a.strip()
                if a:
                    agencies.add(a)

        if not agencies:
            # no historical incidents -> skip or note
            continue

        # resolve agency names to IDs
        cur.execute("SELECT agency_id, agency_name FROM agencies WHERE agency_name = ANY(%s)",
                    (list(agencies),))
        ag_rows = cur.fetchall()
        name_to_id = {r["agency_name"]: r["agency_id"] for r in ag_rows}

        # 3) for each ICS level 1-5, ask which agencies lack a SOP
        for level in range(1, 6):
            cur.execute("""
                SELECT agency_id
                  FROM sops
                 WHERE threat_id = %s
                   AND ics_level = %s
                   AND agency_id  = ANY(%s)
            """, (tid, level, list(name_to_id.values())))
            have = {r["agency_id"] for r in cur.fetchall()}

            for ag_name, ag_id in name_to_id.items():
                if ag_id not in have:
                    report.append({
                        "threat_name":   tname,
                        "threat_cause":  tcause,
                        "ics_level":     level,
                        "agency_name":   ag_name
                    })

    cur.close()
    conn.close()
    return report

if __name__ == "__main__":
    missing = find_missing_sops()
    if not missing:
        print("✅ All agencies have SOPs for every ICS level 1–5.")
    else:
        print("Missing SOPs for these tuples:\n")
        for m in missing:
            print(f" • Threat={m['threat_name']} / Cause={m['threat_cause']}  "
                  f"– ICS {m['ics_level']}  – Agency={m['agency_name']}")
