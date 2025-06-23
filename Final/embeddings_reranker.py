from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_nvidia_ai_endpoints import NVIDIARerank
import time
import os

def embedder_reranker(embedding_model, reranker_model, documents):
    try:
        # Create embeddings
        embedder = NVIDIAEmbeddings(model=embedding_model, truncate="END")

        # Store embeddings in vector database
        start_time = time.time()
        vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=embedder,
            collection_name="docs",
            persist_directory="./chroma_db"
        )

        if vectorstore:
            print(f"Vector database was successfully created! Total embeddings indexed: {len(documents)}")
        else:
            print("Failed to create the vector database. Please check your input data.")

        print(f"--- {time.time() - start_time} seconds ---")

        # Add reranker
        NV_rerank = NVIDIARerank(model=reranker_model, top_n=10)

        return NV_rerank, vectorstore
    
    except Exception as e:
        print(f"An error occurred: {e}")