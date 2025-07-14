from master import input_processing, response_generator
from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS
import json


app = Flask(__name__)
CORS(app)
@app.route('/response/v1', methods=['POST'])
def receive_data():
    try:
        # Get required inputs
        media_input, latitude, longitude = input_processing(request)

        # Generate response plan
        def generate():
            for chunk in response_generator(media_input, latitude, longitude):
                if isinstance(chunk, (dict, list)):
                    chunk = json.dumps(chunk, ensure_ascii=False)
                else:
                    chunk = str(chunk)

                yield chunk

        return Response(
            stream_with_context(generate()),
            content_type="text/event-stream; charset=utf-8",
            headers={
                "Cache-Control": "no-cache",
                "X-Accel-Buffering": "no"
    }
)

    except Exception as e:
        err = "Internal server error encountered"
        print(f"error: {err}\n{e}")
        return jsonify(
            {"error": err}
        )
    
    return jsonify({
        "status":"success",
        "agent1":agent1,
        "agent2":agent2
        }
    )

if __name__ == '__main__':
    app.run(debug=True)