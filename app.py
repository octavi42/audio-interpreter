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


@app.route("/set_model", methods=["POST"])
def set_model():
    if request.method == "POST":
        # Getting the model name
        model_name = request.json.get("model")

        # Get the list of model names
        model_files = [file for file in os.listdir("speech_to_text/models") if file.endswith('.py') and not file.startswith('__')]
        model_files = [os.path.splitext(file)[0] for file in model_files]

        print(model_files)
        print(model_name)

        # Check if modles name is in the list of model names
        if model_name in model_files:
            # Set the environment variable
            os.environ["MODEL_NAME"] = model_name

            # Return the model name
            return jsonify({"model_name": model_name})

        else:
            return jsonify({"error": "No not found, use /get_models to see avaiable models"}), 400
        

@app.route("/get_models", methods=["GET"])
def get_models():
    if request.method == "GET":
        # Get the list of model names
        model_files = [file for file in os.listdir("speech_to_text/models") if file.endswith('.py') and not file.startswith('__')]

        # Return the model names
        return jsonify({"model_names": model_files})
    

@app.route("/get_used_model", methods=["GET"])
def get_used_model():
    if request.method == "GET":
        # Get the model name
        model_name = os.getenv("MODEL_NAME")

        # Return the model name
        return jsonify({"model_name": model_name})


@app.route("/audio_interpret", methods=["POST"])
def audio_interpret():
    if request.method == "POST":
        # Getting the audio file
        audio_file = request.files.get("audio")

        if audio_file:
            # Save the audio file temporarily
            audio_path = "stored_audio/temp_audio.wav"
            audio_file.save(audio_path)

            # Process the audio and get the result
            result = process_audio(audio_path)

            # Interpret the result
            interpreted_result = get_interpretation_from_prompt(result)

            # adding the result to interpreted_result
            interpreted_result.update({"prompt": result})

            # Delete the audio file
            os.remove(audio_path)

            # Return the interpreted result
            return jsonify({"interpreted_result": interpreted_result})

        else:
            return jsonify({"error": "No audio file provided"}), 400
        

if __name__ == "__main__":
    print("Running app.py directly")
    app.run(debug=True)