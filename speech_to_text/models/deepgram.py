import os
from speech_to_text.models import ModelBase
from deepgram import Deepgram as DeepgramAPI

class Deepgram(ModelBase):
    def __init__(self, api_key):
        super().__init__()
        self.api_key = api_key

    def process_audio(self, audio_url, model="nova-2", language="en", smart_format=True):
        # Simulating the use of the API key and audio URL
        print(f"API Key: {self.api_key}")
        print(f"Audio URL: {audio_url}")

        # Create an instance of the Deepgram API client
        dg_client = DeepgramAPI(self.api_key)

        # Make the transcription request
        response = dg_client.transcription.sync_prerecorded(
            {'url': audio_url},
            {
                "model": model,
                "language": language,
                "smart_format": smart_format,
            },
        )
        

        return response["results"]["channels"][0]["alternatives"][0]["transcript"],
            

    def internal_process(self, audio, env, model="nova-2", language="en", smart_format=True):
        print()
        print("Deepgram env")
        print(env)

        dg_client = Deepgram(env)
        response = dg_client.transcription.sync_prerecorded(
            {'url': audio},
            {
                "model": model,
                "language": language,
                "smart_format": smart_format,
            },
        )

        text = response["results"]["channels"][0]["alternatives"][0]["transcript"]

        result = {
            "original_text": text,
        }

        return text
