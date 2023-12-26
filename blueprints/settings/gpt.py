from flask import Blueprint, request, jsonify
import os

gpt_pb = Blueprint('gpt', __name__)

@gpt_pb.route("/set_gpt_model", methods=["POST"])
def set_gpt_model():
    if request.method == "POST":
        # Getting the model name
        model_name = request.json.get("model")

        # Check if modles name is in the list of model names
        if model_name:
            # Set the MODEL_NAME environment variable
            os.environ["GPT_MODEL"] = model_name

            # Read existing environment variables from .env file
            with open('.env', 'r') as env_file:
                existing_env = env_file.readlines()

            # Update the MODEL_NAME in the list
            for i, line in enumerate(existing_env):
                if line.startswith('GPT_MODEL='):
                    existing_env[i] = f'GPT_MODEL="{model_name}"\n'
                    break

            # Write the entire .env file with the updated content
            with open('.env', 'w') as env_file:
                env_file.writelines(existing_env)

            # Return the model name
            return jsonify({"model_name": model_name})

        else:
            return jsonify({"error": "No not found, use /get_models to see avaiable models"}), 400
        

@gpt_pb.route("/get_gpt_model", methods=["GET"])
def get_gpt_models():
    if request.method == "GET":
        # Return the model names
        return jsonify({"gpt_model": os.getenv('GPT_MODEL')})