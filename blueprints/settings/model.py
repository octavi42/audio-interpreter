from flask import Blueprint, request, jsonify
import os

model_pb = Blueprint('model', __name__)

# In-memory configuration for the current model
current_model = {"name": os.getenv("MODEL_NAME")}

@model_pb.route("/ping", methods=["GET"])
def test():
    return jsonify("pong")

@model_pb.route("/set_model", methods=["POST"])
def set_model():
    if request.method == "POST":
        model_name = request.json.get("model")
        model_files = [file for file in os.listdir("speech_to_text/models") if file.endswith('.py') and not file.startswith('__')]
        model_files = [os.path.splitext(file)[0] for file in model_files]

        if model_name in model_files:
            # Update the in-memory configuration
            current_model["name"] = model_name

            # Update the .env file
            with open('.env', 'r') as env_file:
                existing_env = env_file.readlines()

            for i, line in enumerate(existing_env):
                if line.startswith('MODEL_NAME='):
                    existing_env[i] = f'MODEL_NAME="{model_name}"\n'
                    break

            with open('.env', 'w') as env_file:
                env_file.writelines(existing_env)

            return jsonify({"model_name": model_name})
        else:
            return jsonify({"error": "Model not found, use /get_models to see available models"}), 400
        

@model_pb.route("/get_models", methods=["GET"])
def get_models():
    if request.method == "GET":
        # Get the list of model names
        model_files = [file for file in os.listdir("speech_to_text/models") if file.endswith('.py') and not file.startswith('__')]

        # Return the model names
        return jsonify({"model_names": model_files})
    

@model_pb.route("/get_used_model", methods=["GET"])
def get_used_model():
    if request.method == "GET":

        # Return the model name
        return jsonify({"model_name": current_model["name"]})