from flask import Flask
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


AUDIO_URL = 'https://static.deepgram.com/examples/Bueller-Life-moves-pretty-fast.wav' 
@app.route("/audio_interpret")
def audio_interpret():
    # DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
    # dg_client = Deepgram(DEEPGRAM_API_KEY)
    # print(DEEPGRAM_API_KEY)
    # response = dg_client.transcription.sync_prerecorded(
    #     { 'url': AUDIO_URL}, 
    #     {
    #     "model": "nova-2", 
    #     "language": "en", 
    #     "smart_format": True, 
    #     }, 
    # ) 
    
    # text = response["results"]["channels"][0]["alternatives"][0]["transcript"]

    # text = "Undertake a task with unspecified details, occurring on a date yet to be discovered, and an undefined level of urgency."

    # interpreted_prompt = get_interpretation_from_prompt(text)

    # result = {
    #     "original_text": text,
    #     "interpreted_prompt": interpreted_prompt
    # }

    

    result = process_audio(AUDIO_URL)

    interpreted_result = get_interpretation_from_prompt("update columne 3 to 4 from 5 nov to 6 dec this year")

    return interpreted_result


if __name__ == "__main__":
    print("Running app.py directly")
    app.run(debug=True)