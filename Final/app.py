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

from master import input_processing, response_generator
from flask import Flask, request, Response, stream_with_context
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

@app.route('/response/v1', methods=['POST'])
def receive_data():
    try:
        media_input, latitude, longitude = input_processing(request)

        def generate():
            for chunk in response_generator(media_input, latitude, longitude):
                # each chunk is already a dict or list
                yield f"data: {json.dumps(chunk, ensure_ascii=False)}\n\n"

        return Response(
            stream_with_context(generate()),
            mimetype="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "X-Accel-Buffering": "no"
            }
        )

    except Exception as e:
        print(f"error: Internal server error encountered\n{e}")
        payload = {"error": "Internal server error encountered"}
        return Response(f"data: {json.dumps(payload)}\n\n", status=500, mimetype="text/event-stream")

if __name__ == '__main__':
    app.run(debug=True)

