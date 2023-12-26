from flask import Flask, request, jsonify
import json
from dotenv import load_dotenv
from blueprints.settings.settings import settings_pb
from blueprints.functions.speech_tools import speech_tools_pb


app = Flask(__name__)
app.register_blueprint(settings_pb, url_prefix='/settings')
app.register_blueprint(speech_tools_pb, url_prefix='/audio_tools')

load_dotenv()


@app.route("/ping")
def ping():
    return json.dumps({"message": "pong"})


if __name__ == "__main__":
    print("Running app.py directly")
    app.run(debug=True)