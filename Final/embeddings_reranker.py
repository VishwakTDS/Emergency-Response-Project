from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_nvidia_ai_endpoints import NVIDIARerank
from langchain.schema import Document
from sql_connection import get_threat_data, get_incidents_by_ids, get_incident_by_name

def embedder_reranker(embedding_model, reranker_model, image_summary, location):
    threat = image_summary["threat_type"]
    summaries = get_threat_data(threat, location)

    if not summaries:
        return None

    docs = [Document(page_content=s, metadata={"event_id": i}) for i, s in summaries]

    embedder = NVIDIAEmbeddings(model=embedding_model, truncate="END")
    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=embedder,
        ids=[str(d.metadata["event_id"]) for d in docs],
        collection_name=f"threat_{threat}",
        persist_directory="./chroma_db"
    )

    reranker   = NVIDIARerank(model=reranker_model, top_n=2)
    candidates = vectorstore.similarity_search(image_summary["image_summary"], k=2)
    rerank_out = reranker.compress_documents(
        query=image_summary["image_summary"],
        documents=candidates
    )
    best_docs = rerank_out.get("documents", rerank_out) if isinstance(rerank_out, dict) else rerank_out
    top_ids   = [int(d.metadata["event_id"]) for d in best_docs[:5]]

    # Fetch & format full records
    full_records = get_incidents_by_ids(top_ids)
    if not full_records:
        return get_incident_by_name('Default Wildfire Incident')
    return full_records

def format_incidents(incidents):
    lines = []
    for idx, inc in enumerate(incidents, start=1):
        lines.append(f"{idx}. {inc['incident_name']}")
        lines.append(f"Type: {inc['incident_type']}")
        lines.append(f"ICS-Level: {inc['ics_level']}")
        lines.append(f"Location: {inc['location']}")
        lines.append(f"Weather: {inc['weather']}")
        lines.append(f"Resources: {inc['resources_required']}")
        lines.append(f"Identified Cause: {inc['identified_cause']}")
        lines.append(f"Summary: {inc['incident_summary']}")
        
        lines.append("Response Measures:")
        for num, step in enumerate(inc['response_measures'].split("\n"), start=1):
            text = step.lstrip("0123456789.) ").strip()
            lines.append(f"     {num}) {text}")
        
        lines.append(f"Anticipated Developments: {inc['anticipated_developments']}")
        lines.append(f"Responding Agencies: {inc['responding_agencies']}")
        lines.append("")

    return "\n".join(lines).strip()

