from flask import Flask, request, jsonify
import json
from dotenv import load_dotenv
import os
from utils.audio_interpretation import get_interpretation_from_prompt
from speech_to_text.choose_model import process_audio


app = Flask(__name__)

# load environment variables
load_dotenv()


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/ping")
def ping():
    return json.dumps({"message": "pong"})


@app.route("/audio_interpret", methods=["POST"])
def audio_interpret():
    if request.method == "POST":
        # Assuming the audio data is sent as a file in the request
        audio_file = request.files.get("audio")

        if audio_file:
            # Save the audio file temporarily (you might want to handle this differently in production)
            audio_path = "temp_audio.wav"
            audio_file.save(audio_path)

            # Process the audio and get the result
            result = process_audio(audio_path)

            # Interpret the result
            interpreted_result = get_interpretation_from_prompt(result)

            # Return the interpreted result
            return jsonify({"interpreted_result": interpreted_result})

        else:
            return jsonify({"error": "No audio file provided"}), 400
        

if __name__ == "__main__":
    print("Running app.py directly")
    app.run(debug=True)