from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_nvidia_ai_endpoints import NVIDIARerank
from langchain.schema import Document

from uuid import uuid4

def embedder_reranker(embedding_model, reranker_model, documents_new, image_summary):
    ids = [str(d.metadata['event_id']) for d in documents_new]
    embedder = NVIDIAEmbeddings(model=embedding_model, truncate="END")
   
    vectorstore = Chroma.from_documents(
        documents=documents_new,
        embedding=embedder,
        ids=ids,
        collection_name="threat_summary_docs",
        persist_directory="./chroma_db"
    )

    reranker = NVIDIARerank(model=reranker_model, top_n = 2)

    def get_top2(query: str, prefetch_k: int = 5):
        cand = vectorstore.similarity_search(query, k=prefetch_k)
        return reranker.compress_documents(query=query, documents=cand)

    top_two = get_top2(image_summary)
    
    return top_two