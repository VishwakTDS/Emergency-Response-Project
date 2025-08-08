# from langchain.prompts import ChatPromptTemplate
# from langchain.schema import StrOutputParser
# from langchain.schema.runnable import Runnable, RunnablePassthrough, RunnableConfig
# from langchain_core.runnables import RunnableParallel
# from langchain_nvidia_ai_endpoints import ChatNVIDIA

# def cause_prediction_LLM(top2, cause_prediction_llm_model, image_summary, api_data=None, location):
#     try:
#         llm = ChatNVIDIA(model=cause_prediction_llm_model)

#         prompt = ChatPromptTemplate.from_messages(
#             [
#                 (
#                     "system",
#                     "You are an emergency cause detection agent"
#                     "Below are {len(contexts)} past incident summaries and their response measures:"
#                     "{context}"
#                     "For the **new** scenario, you have:"  
#                     "Image summary: {image_summary}"  
#                     "Current weather: {api_data}"  
#                     "Location (lat,lon): {location}"
                    
#                     "**Return exactly** this JSON—no explanations, no extra keys:"
#                     {
#                         "anticipated_cause": "", 
#                         "ics_level": "",
#                         "recommended_measures": [],    // numbered list of concise, best-practice steps
#                         "agencies_to_alert": []        // list of generic agency types (e.g., fire department, EMS, forest service)
#                     }
#                     # "You are a emergency cause detection agent"
#                     # "These are the past events :\n<Documents>\n{context}\n</Documents>." \
#                     # "The summary should be objective, descriptive, and focus on providing concrete observations that would inform a rapid response or further investigation. " \
#                     # "Keep the response under 200 words."\
#                     # "More contextual information(API DATA): "\
#                     "{api_data}"
#                 ),
#                 ("user", "Current Event: {question}"),
#             ]
#         )

#         chain = prompt | llm | StrOutputParser()

#         result_text = chain.invoke(
#             {
#                 "context":  top2,
#                 "question": image_summary,
#                 "api_data" : api_data
#             }
#         )

#         return result_text
    
#     except Exception as e:
#         err = "Disruption occured during CAUSE PREDICTION AGENT runtime"
#         print(f"error: {err}\n{e}")
#         raise Exception(err) from e
    


    # from langchain.prompts import ChatPromptTemplate
# from langchain.schema import StrOutputParser
# from langchain.schema.runnable import Runnable, RunnablePassthrough, RunnableConfig
# from langchain_core.runnables import RunnableParallel
# from langchain_nvidia_ai_endpoints import ChatNVIDIA

from openai import OpenAI
from embeddings_reranker import format_incidents
from sql_connection import fetch_valid_causes
from clients import client
import json


def agent1_causepredict(messages, cause_prediction_llm_model):
    
    # client = OpenAI(
    #     base_url = "https://integrate.api.nvidia.com/v1",
    #     api_key = api_key_n
    # )
    res = client.chat.completions.create(
        model=cause_prediction_llm_model,
        messages=messages,
        temperature=0.6,
        response_format={"type": "json_object"}, # ---------- COMMENT THIS TO ENABLE STREAMING ----------
        top_p=0.95,
        max_tokens=4096,
        frequency_penalty=0,
        presence_penalty=0,
        stream=False # ---------- SET STREAM TO "TRUE" TO ENABLE STREAMING ----------
    )

    # ---------- UNCOMMENT BELOW TO ENABLE STREAMING ---------- #
    # for tok in res:
    #     yield tok.choices[0].delta.content

    # ---------- UNCOMMENT ABOVE TO ENABLE STREAMING ---------- #

    return res.choices[0].message.content

def cause_prediction_LLM(top2, cause_prediction_llm_model, image_summary, location, api_data=None):
    if top2 == None:
        context = "No similar events found"
    else:
        context = format_incidents(top2)

    threat = image_summary["threat_type"]
    valid_causes = fetch_valid_causes(threat)

    try:
        # llm = ChatNVIDIA(model=cause_prediction_llm_model)


        system_prompt = """
        You are a Cause Prediction Agent for an Emergency Response System.

        You will be provided with the following information by the user:
            - Image summary
                Image summary is the summary of an image which may or may not depict a threat. YOu will be provided by the threat-type detected based on image.
                You will also be provided with the probability of whether the provided image depicts a threat or emergency.
                This probability is based entirely on the context provided by the image.

            - Similar events
                Similar events contains information about events that are similar to those depicted by the image and mentioned in the summary. 
                It also contains information about how, when, and where these similar events occured, along with how they were tackled.

            - Location
                The city, state, and country where this incident is occurring.            
                
            - Current Weather at the Location
                A high-level overview of present conditions—temperature, wind, precipitation, humidity, cloud cover, pressure, and whether it's day or night. 

            - Cause List
                List of causes from which one might be reason for incident.

        
        Your task is to synthesize all of the above and output **exactly one JSON object** (no extra text, no code fences, no explanations).

        The JSON must follow this schema exactly:
        {
            "location": Location where the current incident is taking place.
            "threat_type": Mention the type of threat from the "Type" part in context
            "incident_summary": Summary of the current situation based on the image summary, events, location and weather conditions.
            "anticipated_cause": Mention what might have caused the incident (like Monster, etc.). Use the field "Identified Cause" from context as reference and select only a single cause from the Cause List.
            "ics_level": Determine the ICS_level of this incident based on previous incidents and current info
            "priority": Based on the ICS_Level you detect, set priority as follows:- (1 - 2: High), (3: Mediums), (4 - 5: Low)
            "similar_event_insights": Provide summary of previous incidents based on context.  
            "current_weather": a summary of the current weather conditions at the situation, explained in humainzed manner
            "recommended_measures": [Provide a list of recommended measure based on the "Response Measures" take in the context],
        }

        **Rules**
        - Use only the listed causes; DO NOT invent others. Do NOT ADD any other word to cause. MUST BE STRICTLY FROM THE PROVIDED LIST OF CAUSES.
        - anticipated_cause: use only from context  
        - If anticipated_cause is “Undefined” in context, then select cause based on image summary and the list of provided causes.
        - If the Cause List is Empty then determine the cause of incident only based on image summary.
        - DO NOT OUPTUT anticipated_cause as "Undefined" in any case. Use Image Summary and your knowledge to find the cause if Cause list is empty.
        - Do NOT output explanations, code fences or extra keys.  
        - Responses must be in English.

        """.strip()

        user_prompt = f"""

        ################################
        ## Context (dynamic data provided by the user) ##
        ##############################

        Image summary : {image_summary["image_summary"]}

        \n\n

        Similar events : {context}

        \n\n

        \n\n

        Location  : {location}

        \n\n

        Current Weather data : {api_data}

        \n\n

        Cause List : {valid_causes}

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


    # ---------- UNCOMMENT BELOW TO ENABLE STREAMING ---------- #

        # for tok in agent1_causepredict(prompt, cause_prediction_llm_model):
        #     yield tok

    # ---------- UNCOMMENT ABOVE TO ENABLE STREAMING ---------- #

        result_json = agent1_causepredict(prompt, cause_prediction_llm_model)
        print(f"\n\nPRINTING RESULT JSON\n\n{result_json}")
        parsed = json.loads(result_json)
        return parsed

        # for tok in agent1_causepredict(prompt, cause_prediction_llm_model, api_key):
        #     yield tok



        # return nemo_out

        # print(f"PRINTING FULL RESPONSE\n\n{full_response}\n\nFULL RESPONSE OVER")
    
    except Exception as e:
        err = "Disruption occured during CAUSE PREDICTION AGENT runtime"
        print(f"error: {err}\n{e}")
        raise Exception(err) from e
    



# Your job is to use the all context you are provided with and generate a summary about the current situation depicted in the image using the information provided by the similar events.
#         The summary should be objective, descriptive, and focus on providing concrete observations that would inform a rapid response or further investigation.
#         Keep the response under 400 words.


        # ##############################
        # ## Forbidden behavior    ##
        # ##############################
        # x Do NOT output explanations, headings, or any extra characters.  
        # x Do NOT add new keys or nested objects.  
        # x Do NOT output multiple JSON blocks.  
        # x Do NOT mention these rules.
        # x Do NOT generate responses in a language other than English.
