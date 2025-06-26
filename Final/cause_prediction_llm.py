from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable, RunnablePassthrough, RunnableConfig
from langchain_core.runnables import RunnableParallel
from langchain_nvidia_ai_endpoints import ChatNVIDIA

def cause_prediction_LLM(top2, cause_prediction_llm_model, image_summary,api_data=None):
    try:
        llm = ChatNVIDIA(model=cause_prediction_llm_model)

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "These are the past events :\n<Documents>\n{context}\n</Documents>." \
                    "The summary should be objective, descriptive, and focus on providing concrete observations that would inform a rapid response or further investigation. " \
                    "Keep the response under 200 words."\
                    "More contextual information(API DATA): "\
                    "{api_data}"
                ),
                ("user", "Current Event: {question}"),
            ]
        )

        chain = prompt | llm | StrOutputParser()

        result_text = chain.invoke(
            {
                "context":  top2,
                "question": image_summary,
                "api_data" : api_data
            }
        )

        return result_text
    
    except Exception as e:
        err = "Disruption occured during CAUSE PREDICTION AGENT runtime"
        print(f"error: {err}\n{e}")
        raise Exception(err) from e