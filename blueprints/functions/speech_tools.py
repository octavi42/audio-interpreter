from flask import Blueprint, request, jsonify
import os
from utils.audio_interpretation import get_interpretation_from_prompt
from speech_to_text.choose_model import process_audio

speech_tools_pb = Blueprint('speech_tools', __name__)

@speech_tools_pb.route("/interpret", methods=["POST"])
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