from master import input_processing, response_generator
from flask import Flask, request, jsonify, Response
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
@app.route('/response/v1', methods=['POST'])
def receive_data():
    try:
        # Get required inputs
        media_input, latitude, longitude = input_processing(request)

        # Generate response plan
        def generate():
            for output in response_generator(media_input, latitude, longitude):
                yield f"{output}\n\n"

        return Response(generate(), mimetype='text/event-stream')

    except Exception as e:
        err = "Internal server error encountered"
        print(f"error: {err}\n{e}")
        return jsonify(
            {"error": err}
        )
    
    return jsonify({
        "status":"success"
        }
    )

if __name__ == '__main__':
    app.run(debug=True)