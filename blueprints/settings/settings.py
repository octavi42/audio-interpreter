from flask import Blueprint, request, jsonify
from blueprints.settings.model import model_pb
from blueprints.settings.gpt import gpt_pb

# Create a blueprint for settings
settings_pb = Blueprint('settings', __name__)
# Register the model_settings blueprint with the settings blueprint and set its URL prefix
settings_pb.register_blueprint(model_pb, url_prefix='/model')
settings_pb.register_blueprint(gpt_pb, url_prefix='/gpt')
