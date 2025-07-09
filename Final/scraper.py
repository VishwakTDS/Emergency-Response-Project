import os
import re
import json
import requests
import numpy as np
import psycopg2
# from dotenv import load_dotenv
from bs4 import BeautifulSoup
from dateutil import parser
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings, NVIDIARerank
from langchain.schema import Document

from config import embedding_model, reranker_model, api_key_nvd, sql_host, sql_database, sql_user, sql_password


# load_dotenv()
NVIDIA_INVOKE_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
# api_key_nvd = os.environ.get("NVIDIA_API_KEY", "")


INCIDENTS = {
    "Oregon_Rowena_Fire_Jun2025": [
       'https://apnews.com/article/oregon-wildfire-interstate-84-8d28833059cd46878080fd7e71444548',
       'https://www.opb.org/article/2025/05/14/an-architect-of-oregons-wildfire-map-on-why-he-now-supports-repealing-it/',
       'https://www.kgw.com/article/news/local/wildfire/oregon-state-fire-marshal-clears-misinformation/283-49abc8db-7d30-4bd9-8b5d-af82a6a3cdc7',
       'https://www.eenews.net/articles/oregon-lawmakers-ready-to-junk-contentious-wildfire-map/',
       'https://www.theguardian.com/us-news/article/2024/jul/27/oregon-wildfire-season',
       'https://www.opb.org/article/2025/05/24/oregon-fire-restrictions-washington-wildfire-bureau-land-management/',
       'https://apnews.com/article/oregon-wildfire-hazard-map-45c0335d93632580e07512a276dea7da',
       'https://www.kgw.com/article/news/local/wildfire/oregon-firefighters-return-north-carolina/283-7e13e4fc-10ad-498a-b4cb-85a5b0845603'
    ],
    "Maui_Kahikinui_Fire_Jun2025": [
      "https://www.theguardian.com/us-news/2025/jun/17/hawaii-maui-wildfire",
      'https://www.foxweather.com/extreme-weather/maui-brush-fire-kahikinui-hawaii-evacuations',
      'https://www.kitv.com/news/local/maui-county-hands-over-kahikinui-fire-control-to-state-of-hawaii/article_e453a5ab-90be-4d81-93d1-aeee87e5f989.html',
      'https://www.butlereagle.com/20250616/fast-moving-brush-fire-on-hawaiis-maui-island-evacuates-about-50-people-no-structures-have-burned/',
      'https://www.kcra.com/article/fast-moving-brush-fire-in-hawaiis-maui-county-evacuates-at-least-105-homes-no-structures-burned/65078861'
    ]
}


def extract_date(soup: BeautifulSoup) -> str:
    selectors = [
      ('meta',{'itemprop':'datePublished'}),
      ('meta',{'name':'pubdate'}),
      ('meta',{'name':'date'}),
      ('meta',{'property':'article:published_time'}),
      ('span',{'class':'update-time'}),
      ('p',{'class':'update-time'})
    ]
    for tag, attrs in selectors:
        el = soup.find(tag, attrs=attrs)
        if not el: continue
        raw = el.get('content') if tag=='meta' and el.has_attr('content') else el.get_text(strip=True)
        try:
            return parser.parse(raw, fuzzy=True).strftime('%Y-%m-%d')
        except:
            return raw
    return "n/a"

def scrape_article(url: str) -> dict:
    try:
        r = requests.get(url, headers={"User-Agent":"Mozilla/5.0"}, timeout=15)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')
        h1 = soup.find('h1')
        headline = h1.get_text(strip=True) if h1 else 'n/a'
        author = 'n/a'
        for tag, cls in [('span','byline__name'), ('p','metadata__byline__author')]:
            el = soup.find(tag, class_=cls)
            if el:
                author = el.get_text(strip=True)
                break
        date = extract_date(soup)
        paras = (soup.find_all('div', class_='paragraph')
                or soup.find_all('div', class_='zn-body__paragraph')
                or soup.find_all('p'))
        content = "\n".join(p.get_text(" ", strip=True) for p in paras)
        return {"url": url, "headline": headline, "author": author, "date": date, "content": content}
    
    except requests.exceptions.RequestException as e:
        print(f"Error scraping article at {url}: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error occurred while scraping article at {url}: {e}")
        return None

# —— LLM CALL —— #
def call_nvidia_llm(prompt: str) -> str:
    resp = requests.post(
        NVIDIA_INVOKE_URL,
        headers={
            "Authorization": f"Bearer {api_key_nvd}",
            "Accept": "application/json",
        },
        json={
            "model":     "nvidia/nemotron-mini-4b-instruct",
            "messages":  [{"role":"user","content":prompt}],
            "max_tokens":1024,
            "temperature":0.2,
            "top_p":     0.7,
        },
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]

# —— RETRIEVAL HELPERS —— #
# embedding_model = "nvidia/nv-embedqa-e5-v5"
# reranker_model = "nvidia/nv-rerankqa-mistral-4b-v3"
embedder = NVIDIAEmbeddings(model=embedding_model, truncate="END")
NV_rerank = NVIDIARerank(
    model=reranker_model,
    api_key=api_key_nvd,
    top_n=20
)
KEYWORDS = ["evacuate","rescue","firefighter","fire","water","emergency", "firebreak", "emergency", "shelter"]

def retrieve_top_k(query, sentences, embeddings, k=50, boost=0.25, pre_k=100):
    q_emb = np.array(embedder.embed_query(query))
    sims = embeddings @ q_emb / (
        np.linalg.norm(embeddings, axis=1) * np.linalg.norm(q_emb)
    )
    for i,s in enumerate(sentences):
        if any(kw in s.lower() for kw in KEYWORDS):
            sims[i] += boost
    idxs = np.argsort(-sims)[:pre_k]
    cands = [sentences[i] for i in idxs]
    docs  = [Document(page_content=t) for t in cands]
    try:
        out = NV_rerank.compress_documents(query=query, documents=docs)
        reranked = [
            d.page_content
            for d in (out["documents"] if isinstance(out, dict) else out)
        ]
    except:
        reranked = cands
    return reranked[:k]

# —— MAIN WORKFLOW —— #
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
    CREATE TABLE IF NOT EXISTS incidents (
      id                           SERIAL PRIMARY KEY,
      incident_name                TEXT,
      incident_type                TEXT,
      severity_level               INTEGER,
      affected_location            TEXT,
      identified_cause             TEXT,
      estimated_economic_loss_usd   BIGINT,
      reported_fatalities          INTEGER,
      reported_injuries            INTEGER,
      incident_summary             TEXT,
      response_measures            TEXT,
      anticipated_developments     TEXT,
      affected_population_estimate INTEGER,
      evacuations_ordered          TEXT,
      infrastructure_impacted      TEXT,
      emergency_status             TEXT,
      responding_agencies          TEXT
    );
    """)
    conn.commit()

    # Process each incident
    for name, urls in INCIDENTS.items():
        # Scrape
        arts = [scrape_article(u) for u in urls]
        arts = [art for art in arts if art is not None]

        # Build sentence list & embeddings
        sents = []
        for art in arts:
            pieces = re.split(r'(?<=[.?!])\s+', art["content"])
            sents += [t.strip() for t in pieces if len(t.strip())>20 or re.search(r"\d",t)]
        embs = np.array(embedder.embed_documents(sents))

        # Retrieve context
        context = "\n".join(retrieve_top_k(
            "Summarize the key facts and response measures",
            sents, embs, k=50
        ))

        # Prompt LLM
        prompt = f"""
You are an information extraction assistant.
Extract only **explicitly stated** facts into JSON—do **not** infer, assume, or hallucinate.
**Return only the JSON object, with no markdown fences, no explanations, and no extra text.**

Here is the schema your output must follow exactly:
{{
  "incident_name" : ""                      // Must be the name of incident in short, sort of like a title, TEXT.
  "incident_type": "",                      // Must be categorised into these categories only:  wildfire, urban fire, crowd-management incident, Undefined)
  "severity_level": 0,                      // 1 to 10 reflecting severity based on described impact; use 0 if unspecified
  "affected_location": "",                  // Region, city, state, etc.
  "identified_cause": "",                   // Cause if mentioned (Look for text which mentions reason for any calamitites or incidents) or mention undefined
  "estimated_economic_loss_usd": 0,         // Numeric, no formatting (e.g., 5000000)
  "reported_fatalities": 0,                 // Number of deaths of people if any or 0
  "reported_injuries": 0,                   // Number of injured of people if any or 0
  "incident_summary": "",                   // 1 or 2 sentence summary of the event. Must highlight main points related mostly to the incident impact and emergency responses
  "response_measures": "",                  // Steps taken in detail (e.g., evacuations, Incident-management, steps, declarations) by first responders or emergency agencies. Make sure to provide detailed information about the steps taken by the responders to handel the incident.
                                            // Provide a bullet numbered list of steps taken by the authorities to manage the incident and also manage the calamity as we need to find how they contained it. Avoid descriptive and unrealted words in response.
  "anticipated_developments": "",           // Future expectations or projections like if the threat is predicted to scale or it is mitigated
  "affected_population_estimate": 0,        // Check if they have mentioned any number of people affected/evacuated or rescured only peoples Not the homes/property etc damaged etc., Only number of people. If not found mention 0
  "evacuations_ordered": "",                // "Yes", "No", or "n/a"
  "infrastructure_impacted": "",            // E.g., roads, power lines, water
  "emergency_status": "",                   // "Declared", "Not Declared", or "n/a"
  "responding_agencies": "",                // Government or official organizations mentioned
}}

Context:
{context}
""".strip()
        raw = call_nvidia_llm(prompt)
        rec = json.loads(re.search(r"\{[\s\S]*\}", raw).group(0))
        rec["incident_name"] = name

        # e) Insert row
        cols = list(rec.keys())
        ph   = ",".join("%s" for _ in cols)
        sql  = f"INSERT INTO incidents ({','.join(cols)}) VALUES ({ph})"
        cur.execute(sql, [rec[c] for c in cols])
        conn.commit()
        # print(f"Inserted '{name}' as id={cur.fetchone()[0] if cur.description else cur.rowcount}")
        print(f"Inserted '{name}'")


    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
