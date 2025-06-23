import streamlit as st, json
import tempfile, os, time
from agents import agent1_vila, agent2_llama, save_log

st.title("Emergency Vision + Reasoning")

lat = st.text_input("Latitude")
lon = st.text_input("Longitude")
img = st.file_uploader("Photo", type=["jpg","jpeg","png"])

# if "need_next_photo" not in st.session_state:
#     st.session_state.need_next_photo = True         # Start with first upload
# if "cycle_id" not in st.session_state:             # Used to give unique keys
#     st.session_state.cycle_id = 0

if st.button("Submit") and lat and lon and img:
    ext = img.name.split(".")[-1]
    with tempfile.NamedTemporaryFile(delete=False, suffix="."+ext) as tmp:
        tmp.write(img.read())
        tmp_path = tmp.name
   
    vila_out = agent1_vila(lat, lon, [tmp_path])

    os.remove(tmp_path)
    st.subheader("Agent 1 (VILA)"); st.code(vila_out, language="json")

    print(vila_out)

    prompt_content = """
    You are **Emergency-Reasoning-Agent**.

    You receive exactly one JSON object (schema above; "weather" may be missing).

    Return ONE of these JSON commands and nothing else:

    • Drone:
    {"action":"launch_drone","lat":<lat>,"lon":<lon>}

    • First responders:
    {"action":"call_first_responders",
    "agency":"fire_brigade|police|national_guard",
    "lat":<lat>,"lon":<lon>}

    • No emergency:
    {"action":"no_emergency"}

    DECISION RULE
    Let P = hazards.fire.prob  
    - If "weather" present and wind_kph > 25 → P += 0.10  
    - If "weather" present and apparent_c > 32 → P += 0.05
    Clamp P to 1.0.

    - If P ≥ 0.80   → call_first_responders "fire_brigade"  
    - If 0.40 ≤ P < 0.80 → launch_drone  
    - Else (P < 0.40)   → no_emergency

    Output exactly one JSON object, no extra text.

    """

    prompt = [
        {"role":"system",
         "content":prompt_content},
        {"role":"assistant","content":vila_out}
    ]
    nemo_out = agent2_llama(prompt)
    st.subheader("Agent 2 (Nemotron)"); st.code(nemo_out, language="json")

    ok = st.radio("Is Agent 2 correct?", ["Yes","No"], index=None, horizontal=True)
    save_log("llama", prompt, nemo_out, "chosen" if ok=="Yes" else "rejected")

    if '"launch_drone"' in nemo_out:
        st.info("Drone requested, upload next image.")
        # st.rerun()
    else:
        st.success("Cycle finished.")




# if "stage" not in st.session_state:
#     st.session_state.stage = "initial"
#     st.session_state.lat   = None
#     st.session_state.lon   = None

# st.title("Emergency Vision + Reasoning")


# if st.session_state.stage == "initial":
#     lat = st.text_input("Latitude")
#     lon = st.text_input("Longitude")
#     img = st.file_uploader("Photo", type=["jpg","jpeg","png"])

#     if st.button("Submit") and lat and lon and img:

#         ext = img.name.split(".")[-1]
#         with tempfile.NamedTemporaryFile(delete=False, suffix="."+ext) as tmp:
#             tmp.write(img.read())
#             tmp_path = tmp.name
       
#         vila_out = agent1_vila(lat, lon, [tmp_path])

#         os.remove(tmp_path)
       
#         st.subheader("Agent 1 (VILA)"); st.code(vila_out, language="json")

#         prompt_content = """
#     You are **Emergency-Reasoning-Agent**.

#     You receive exactly one JSON object (schema above; "weather" may be missing).

#     Return ONE of these JSON commands and nothing else:

#     • Drone:
#     {"action":"launch_drone","lat":<lat>,"lon":<lon>}

#     • First responders:
#     {"action":"call_first_responders",
#     "agency":"fire_brigade|police|national_guard",
#     "lat":<lat>,"lon":<lon>}

#     • No emergency:
#     {"action":"no_emergency"}

#     DECISION RULE
#     Let P = hazards.fire.prob  
#     - If "weather" present and wind_kph > 25 → P += 0.10  
#     - If "weather" present and apparent_c > 32 → P += 0.05
#     Clamp P to 1.0.

#     - If P ≥ 0.80   → call_first_responders "fire_brigade"  
#     - If 0.40 ≤ P < 0.80 → launch_drone  
#     - Else (P < 0.40)   → no_emergency

#     Output exactly one JSON object, no extra text.

#     """

#         prompt = [
#             {"role":"system",
#             "content":prompt_content},
#             {"role":"assistant","content":vila_out}
#         ]
#         nemo_out = agent2_llama(prompt)
#         st.subheader("Agent 2 (Nemotron)"); st.code(nemo_out, language="json")

#         # feedback buttons
#         col_yes, col_no = st.columns(2)
#         clicked = None

#         if col_yes.button("Correct", key="yes"):
#             clicked = "yes"
#         elif col_no.button("Incorrect", key="no"):
#             clicked = "no"
       
#         if clicked:
#             save_log("nemo", prompt, nemo_out, "chosen" if clicked=="yes" else "rejected")
#             if '"launch_drone"' in nemo_out:
#                 st.session_state.stage = "drone"
#                 print("Switched to drone, first section")
#                 st.session_state.lat   = lat
#                 st.session_state.lon   = lon
#                 st.rerun()
#             else:
#                 st.success("Cycle finished.")
#                 st.session_state.stage = "initial"
#                 print("Switched to initial, first section")
#                 st.session_state.lat   = None
#                 st.session_state.lon   = None
#                 st.rerun()

#         # else:
#             # save_log("nemo", prompt, nemo_out, "rejected" if clicked=="no" else "rejected")

#         # loop control
#         # if '"launch_drone"' in nemo_out:
#         #     st.session_state.stage = "drone"
#         #     st.session_state.lat   = lat
#         #     st.session_state.lon   = lon
#         #     st.rerun()
#         # else:
#         #     st.success("Cycle finished.")

# elif st.session_state.stage == "drone":
#     print("Drone section")
#     st.info("Drone requested - upload next image for confirmation.")
#     drone_img = st.file_uploader("Drone photo", type=["jpg","jpeg","png"], key="drone")

#     if st.button("Submit drone image") and drone_img:
#         lat = st.session_state.lat
#         lon = st.session_state.lon

#         ext = drone_img.name.split(".")[-1]
#         with tempfile.NamedTemporaryFile(delete=False, suffix="."+ext) as tmp:
#             tmp.write(drone_img.read())
#             tmp_path = tmp.name

#         vila_out = agent1_vila(lat, lon, [tmp_path])

#         os.remove(tmp_path)
#         st.subheader("Agent 1 (VILA)"); st.code(vila_out, language="json")

#         prompt_content = """
#     You are **Emergency-Reasoning-Agent**.

#     You receive exactly one JSON object (schema above; "weather" may be missing).

#     Return ONE of these JSON commands and nothing else:

#     • Drone:
#     {"action":"launch_drone","lat":<lat>,"lon":<lon>}

#     • First responders:
#     {"action":"call_first_responders",
#     "agency":"fire_brigade|police|national_guard",
#     "lat":<lat>,"lon":<lon>}

#     • No emergency:
#     {"action":"no_emergency"}

#     DECISION RULE
#     Let P = hazards.fire.prob  
#     - If "weather" present and wind_kph > 25 → P += 0.10  
#     - If "weather" present and apparent_c > 32 → P += 0.05
#     Clamp P to 1.0.

#     - If P ≥ 0.80   → call_first_responders "fire_brigade"  
#     - If 0.40 ≤ P < 0.80 → launch_drone  
#     - Else (P < 0.40)   → no_emergency

#     Output exactly one JSON object, no extra text.

#     """

#         prompt = [
#             {"role":"system",
#             "content":prompt_content},
#             {"role":"assistant","content":vila_out}
#         ]
#         nemo_out = agent2_llama(prompt)

#         st.subheader("Agent 2 (Nemotron)"); st.code(nemo_out, language="json")

#         # ok = st.radio("Is Agent 2 correct?", ["Yes","No"], horizontal=True, key="fb1")
#         # save_log("llama", prompt, nemo_out,
#         #             "chosen" if ok=="Yes" else "rejected")

#         # feedback buttons
#         col_yes, col_no = st.columns(2)
#         clicked = None

#         if col_yes.button("Correct", key="yes"):
#             clicked = "yes"
#         elif col_no.button("Incorrect", key="no"):
#             clicked = "no"
       
#         if clicked:
#             save_log("nemo", prompt, nemo_out, "chosen" if clicked=="yes" else "rejected")
#             if '"launch_drone"' in nemo_out:
#                 st.session_state.stage = "drone"
#                 print("Switched to drone, second section")
#                 st.session_state.lat   = lat
#                 st.session_state.lon   = lon
#                 st.rerun()
#             else:
#                 st.success("Cycle finished.")
#                 st.session_state.stage = "initial"
#                 print("Switched to initial, second section")
#                 st.session_state.lat   = None
#                 st.session_state.lon   = None
#                 st.rerun()
#             # st.success("Cycle finished.")
#             # st.session_state.stage = "initial"
#             # st.session_state.lat   = None
#             # st.session_state.lon   = None
#             # st.rerun()
#         # else:
#         #     save_log("nemo", prompt, nemo_out, "rejected" if clicked=="no" else "rejected")

#         # st.success("Cycle finished.")
#         # st.session_state.stage = "initial"
#         # st.session_state.lat   = None
#         # st.session_state.lon   = None
#         # st.rerun()
