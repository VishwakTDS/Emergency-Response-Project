from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable, RunnablePassthrough, RunnableConfig
from langchain_core.runnables import RunnableParallel
from langchain_nvidia_ai_endpoints import ChatNVIDIA

# def cause_prediction_LLM(NV_rerank, vectorstore, cause_prediction_llm_model, image_summary,api_data=None):
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

        

        # --- 3. chain = prompt → model → string -------------------------------
        chain = prompt | llm | StrOutputParser()

        # --- 4. run ------------------------------------------------------------
        result_text = chain.invoke(
            {
                "context":  top2,      # ← your retrieved docs
                "question": image_summary,     # ← e.g. the image summary
                "api_data" : api_data
            }
        )

        # print(result_text)

        # # Prepare the input data for invoking the chain
        # input_data = {
        #     "context": image_summary,  # Assuming this is the context you want to use
            
        #     "api_data": api_data if api_data else "No additional context provided." , # Handle None case
        # }

        # return chain.invoke(image_summary) + chain.invoke("\nMore contextual information(API DATA): " + api_data)
        return result_text


        # print("prompt for cause prediction LLM:")
        # print(image_summary+"\n More contextual information(API DATA): "+api_data)
        # return chain.invoke(image_summary+"\n More contextual information(API DATA): "+api_data)
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None