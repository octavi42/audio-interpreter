from flask import Blueprint, request, jsonify
import os
from utils.audio_interpretation import get_interpretation_from_prompt
from speech_to_text.choose_model import process_audio, process_audio_with_language
from utils.translator import translate

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
        

@speech_tools_pb.route("/interpret_with_language", methods=["POST"])
def audio_interpret_with_language():
    if request.method == "POST":
        # Getting the audio file
        audio_file = request.files.get("audio")
        language = request.form.get("language")

        if audio_file and language:
            # Save the audio file temporarily
            audio_path = "stored_audio/temp_audio.wav"
            audio_file.save(audio_path)

            if language != "english" and language != "arabic":
                return jsonify({"error": "Language not supported, (arabic / english)"}), 400

            # Process the audio and get the result
            result = process_audio_with_language(audio_path, language)

            # Interpret the result
            interpreted_result = get_interpretation_from_prompt(result)

            # Translate title and description if the language is Arabic
            if language == "arabic":
                interpreted_result["result"]["title"] = translate(interpreted_result["result"]["title"], source='en', target='arabic')
                interpreted_result["result"]["description"] = translate(interpreted_result["result"]["description"], source='en', target='arabic')

            # Adding the result to interpreted_result
            interpreted_result.update({"prompt": result})

            # Delete the audio file
            os.remove(audio_path)

            # Return the interpreted result
            return jsonify({"interpreted_result": interpreted_result})

        else:
            return jsonify({"error": "No audio file provided"}), 400
        


@speech_tools_pb.route("/speech_to_text", methods=["POST"])
def speech_to_text():
    if request.method == "POST":
        # Getting the audio file
        audio_file = request.files.get("audio")

        if audio_file:
            # Save the audio file temporarily
            audio_path = "stored_audio/temp_audio.wav"
            audio_file.save(audio_path)

            # Process the audio and get the result
            result = process_audio(audio_path)

            # Delete the audio file
            os.remove(audio_path)

            # Return the interpreted result
            return jsonify({"interpreted_result": result})

        else:
            return jsonify({"error": "No audio file provided"}), 400
        

@speech_tools_pb.route("/speech_to_text_with_language", methods=["POST"])
def speech_to_text_with_language():
    if request.method == "POST":
        # Getting the audio file
        audio_file = request.files.get("audio")
        language = request.form.get("language")

        if audio_file and language:
            # Save the audio file temporarily
            audio_path = "stored_audio/temp_audio.wav"
            audio_file.save(audio_path)

            # Process the audio and get the result
            result = process_audio_with_language(audio_path, language)

            # Delete the audio file
            os.remove(audio_path)

            # Return the interpreted result
            return jsonify({"interpreted_result": result})

        else:
            return jsonify({"error": "No audio file provided"}), 400