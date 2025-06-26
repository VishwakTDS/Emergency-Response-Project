from master import input_processing, response_generator
from flask import Flask, request, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
@app.route('/response/v1', methods=['POST'])
def receive_data():
    try:
        # Get required inputs
        media_input, latitude, longitude = input_processing(request)

        # Generate response plan
        response_generator(media_input, latitude, longitude)

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