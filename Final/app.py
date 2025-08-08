# from master import input_processing, response_generator
# from flask import Flask, request, jsonify
# from flask_cors import CORS


# app = Flask(__name__)
# CORS(app)
# @app.route('/response/v1', methods=['POST'])
# def receive_data():
#     try:
#         # Get required inputs
#         media_input, latitude, longitude = input_processing(request)

#         # Generate response plan
#         for chunk in response_generator(media_input, latitude, longitude):
#             # each `chunk` is a JSON‐string like {"type": "...", "data": "..."}
#             print("STREAM CHUNK:", chunk)

#     except Exception as e:
#         err = "Internal server error encountered"
#         print(f"error: {err}\n{e}")
#         return jsonify(
#             {"error": err}
#         )
    
#     return jsonify({
#         "status":"success"
#         }
#     )
    

# if __name__ == '__main__':
#     app.run(debug=True)

# from master import input_processing, response_generator
# from flask import Flask, request, Response, stream_with_context
# from flask_cors import CORS
# import json

# app = Flask(__name__)
# CORS(app)

# @app.route('/response/v1', methods=['POST'])
# def receive_data():
#     try:
#         media_input, latitude, longitude = input_processing(request)

#         def generate():
#             for chunk in response_generator(media_input, latitude, longitude):
#                 # each chunk is already a dict or list
#                 yield f"data: {json.dumps(chunk, ensure_ascii=False)}\n\n"

#         return Response(
#             stream_with_context(generate()),
#             mimetype="text/event-stream",
#             headers={
#                 "Cache-Control": "no-cache",
#                 "X-Accel-Buffering": "no"
#             }
#         )

#     except Exception as e:
#         print(f"error: Internal server error encountered\n{e}")
#         payload = {"error": "Internal server error encountered"}
#         return Response(f"data: {json.dumps(payload)}\n\n", status=500, mimetype="text/event-stream")

# if __name__ == '__main__':
#     app.run(debug=True)

from fastapi import FastAPI, Form, UploadFile
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
from typing import Annotated, Optional
from master import response_generator, input_processing
import json
from uuid import UUID, uuid4
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

class EmergencyInput(BaseModel):
    id: Optional[UUID] = None
    latitude: float
    longitude: float
    input_media: UploadFile

# requests = {}

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/response/v1")
def receive_data(data: Annotated[EmergencyInput, Form()]):
    try:
        data.id = uuid4()

        temp_media = input_processing(data)

        def generate():
            for chunk in response_generator(temp_media.name, data.latitude, data.longitude):
                if isinstance(chunk, (dict, list)):
                    # print(f"\n\nChunk inside dict or list\nType: {type(chunk)}\nContent: {chunk}\n\n")
                    chunk = json.dumps(chunk, ensure_ascii=False)
                else:
                    # print(f"\n\nChunk inside normal\nType: {type(chunk)}\nContent: {chunk}\n\n")
                    chunk = str(chunk)

                yield chunk

        return StreamingResponse(generate(),
            media_type="text/event-stream; charset=utf-8",
            headers={
                "Cache-Control": "no-cache",
                "X-Accel-Buffering": "no"
            }
        )

    except Exception as e:
        print(f"error: Internal server error encountered\n{e}")
        payload = {"error": "Internal server error encountered"}
        # return Response(f"data: {json.dumps(payload)}\n\n", status=500, mimetype="text/event-stream")
    
    return JSONResponse({
        "status":"success"
        }
    )
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=5000, reload=True)