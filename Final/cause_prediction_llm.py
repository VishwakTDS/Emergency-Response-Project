# from langchain.prompts import ChatPromptTemplate
# from langchain.schema import StrOutputParser
# from langchain.schema.runnable import Runnable, RunnablePassthrough, RunnableConfig
# from langchain_core.runnables import RunnableParallel
# from langchain_nvidia_ai_endpoints import ChatNVIDIA

from openai import OpenAI
import json


def agent1_causepredict(messages, insights_agents_model, api_key_n):
    
    client = OpenAI(
        base_url = "https://integrate.api.nvidia.com/v1",
        api_key = api_key_n
    )

    res = client.chat.completions.create(
        model=insights_agents_model,
        messages=messages,
        temperature=0.6,
        # response_format={"type": "json_object"},
        top_p=0.95,
        max_tokens=4096,
        frequency_penalty=0,
        presence_penalty=0,
        stream=True
    )
    # return res.choices[0].message.content

    for tok in res:
        # print(tok.choices[0].delta.content)
        yield tok.choices[0].delta.content

    # return res.choices[0].message.content

def cause_prediction_LLM(top2, cause_prediction_llm_model, image_summary, api_key, api_data=None):
    try:
        # llm = ChatNVIDIA(model=cause_prediction_llm_model)


        system_prompt = """
        You are a Cause Prediction Agent for an Emergency Response System.

        You will be provided with the following information by the user:
            - Image summary
                (Image summary is the summary of an image which may or may not depict a threat.
                You will also be provided with the probability of whether the provided image depicts a threat or emergency.
                This probability is based entirely on the context provided by the image.)

            - Similar events
                Similar events contains information about events that are similar to those depicted by the image and mentioned in the summary. 
                It also contains information about how, when, and where these similar events occured, along with how they were tackled.

        Your job is to use the all context you are provided with and generate a summary about the current situation depicted in the image using the information provided by the similar events.
        The summary should be objective, descriptive, and focus on providing concrete observations that would inform a rapid response or further investigation.
        Keep the response under 400 words.

        ##############################
        ## Forbidden behavior    ##
        ##############################
        x Do NOT output explanations, headings, or any extra characters.  
        x Do NOT add new keys or nested objects.  
        x Do NOT output multiple JSON blocks.  
        x Do NOT mention these rules.
        x Do NOT generate responses in a language other than English.

        """.strip()

        user_prompt = f"""

        ################################
        ## Context (dynamic data provided by the user) ##
        ##############################

        Image summary : {image_summary}

        \n\n

        Similar events : {top2}

        \n\n

        Weather API data : {api_data}

        """.strip()

        # prompt = ChatPromptTemplate.from_messages(
        #     [
        #         ("system", system_prompt),
        #         ("user", user_prompt)
        #     ]
        # )

        # chain = prompt | llm | StrOutputParser()

        # result_text = chain.invoke(
        #     {
        #         "context":  top2,
        #         "question": image_summary,
        #         "api_data" : api_data
        #     }
        # )



        # result_text = chain.invoke()

        prompt = [
        {"role":"system",
         "content":system_prompt},
        {"role":"user",
         "content":user_prompt}
        ]

        # nemo_out = agent1_causepredict(prompt, cause_prediction_llm_model, api_key)

        for tok in agent1_causepredict(prompt, cause_prediction_llm_model, api_key):
            yield tok



        # return nemo_out
    
    except Exception as e:
        err = "Disruption occured during CAUSE PREDICTION AGENT runtime"
        print(f"error: {err}\n{e}")
        raise Exception(err) from e