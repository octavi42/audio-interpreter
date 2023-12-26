from openai import OpenAI
client = OpenAI()
from pathlib import Path

class Openai():
    def __init__(self, api_key):
        super().__init__()
        self.api_key = api_key

    def process_audio(self, audio_url):
        
        transcript = client.audio.translations.create(
            model="whisper-1", 
            file=Path(audio_url),
            response_format="text"
        )

        return transcript