from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_nvidia_ai_endpoints import NVIDIARerank
from langchain.schema import Document
import time,json
import os

from uuid import uuid4


# def embedder_reranker(embedding_model, reranker_model, documents,image_summary):
#     try:
#         # Create embeddings
#         embedder = NVIDIAEmbeddings(model=embedding_model, truncate="END")

#         # Store embeddings in vector database
#         start_time = time.time()
#         vectorstore = Chroma.from_documents(
#             documents=documents,
#             embedding=embedder,
#             collection_name="docs",
#             persist_directory="./chroma_db"
#         )

#         if vectorstore:
#             print(f"Vector database was successfully created! Total embeddings indexed: {len(documents)}")
#         else:
#             print("Failed to create the vector database. Please check your input data.")

#         print(f"--- {time.time() - start_time} seconds ---")


#         # 4️⃣  Helper that retrieves, then reranks, then returns 2 docs
#         def get_top2(query: str,
#                      prefetch_k: int = 20) -> list[Document]:
#             """
#             Retrieve `prefetch_k` most similar docs via embeddings, then
#             let the reranker pick the best 2.
#             """
            
#             return best_docs        # always ≤ 2
        

#         # Add reranker
#         # NV_rerank = NVIDIARerank(model=reranker_model, top_n=2)
        
#         initial_docs = vectorstore.similarity_search(image_summary, k=20)
#         best_docs    = NV_rerank.compress_documents(
#                                query=image_summary,
#                                documents=initial_docs)
        
#         print("TOP TWO MATCHES:")
#         for d in top_two_matches:
#             print(d.page_content[:120])

#         return NV_rerank, vectorstore,top_two_matches
    
#     except Exception as e:
#         print(f"An error occurred: {e}")

# import psycopg2
# def connection_sql(dbname):
#     results = None
#     try:
#         conn = psycopg2.connect(
#             dbname=dbname,
#             user=os.environ.get("SQL_USER", ""),
#             password=os.environ.get("SQL_PASSWORD", ""),
#             host="localhost"
#         )

#         cur = conn.cursor()

#         cur.execute('SELECT id, threat_summary,steps_followed FROM wildfire_emergencies')

#         results = cur.fetchall()

#         return results
#     except Exception as e:
#         print(f"Cannot load database: {e}")
#         return None

#     finally:
#         cur.close()

#         if conn:
#             conn.close()

def embedder_reranker(embedding_model, reranker_model, documents_new, image_summary):

    for d in documents_new:
            d.metadata.setdefault("doc_id", str(uuid4()))
    ids = [d.metadata["doc_id"] for d in documents_new]

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
    # print("TOP TWO MATCHES:")
    # for d in top_two:
    #     print(d.page_content)
    vectorstore.persist()
    return top_two