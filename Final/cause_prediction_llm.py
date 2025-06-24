from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable, RunnablePassthrough, RunnableConfig
from langchain_core.runnables import RunnableParallel
from langchain_nvidia_ai_endpoints import ChatNVIDIA

def cause_prediction_LLM(NV_rerank, vectorstore, cause_prediction_llm_model, image_summary):
    try:
        llm = ChatNVIDIA(model=cause_prediction_llm_model)

        retriever = vectorstore.as_retriever(search_kwargs={'k':100})

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "Answer solely based on the following context:\n<Documents>\n{context}\n</Documents>",
                ),
                ("user", "{question}"),
            ]
        )

        reranker = lambda input: NV_rerank.compress_documents(query=input['question'], documents=input['context'])

        chain = (
            RunnableParallel({"context": retriever, "question": RunnablePassthrough()})
            | {"context": reranker, "question": lambda input: input['question']}
            | prompt
            | llm
            | StrOutputParser()
        )

        return chain.invoke(image_summary)
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None