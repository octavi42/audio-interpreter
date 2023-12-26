import os
import mimetypes
from speech_to_text.models import ModelBase
from deepgram import Deepgram as DeepgramAPI

class Deepgram(ModelBase):
    def __init__(self, api_key):
        super().__init__()
        self.api_key = api_key
    

    def process_audio(self, audio, model="nova-2", language="en", smart_format=True):
        source = self.get_source(audio)

        # Create an instance of the Deepgram API client
        dg_client = DeepgramAPI(self.api_key)

        # Make the transcription request
        response = dg_client.transcription.sync_prerecorded(
            source,
            {
                "model": model,
                "language": language,
                "smart_format": smart_format,
            },
        )
        
        result = response["results"]["channels"][0]["alternatives"][0]["transcript"]

        return result


    def get_source(self, audio):
        if audio.startswith('http'):
            # file is remote
            # Set the source
            source = {
            'url': audio
            }
        else:
            with open(audio, 'rb') as audio_file:
                # Determine MIME type
                mime_type, _ = mimetypes.guess_type(audio)
                if mime_type is None:
                    # Set a default MIME type if it cannot be determined
                    mime_type = 'application/octet-stream'

                # Set the source
                source = {
                    'buffer': audio_file.read(),
                    'mimetype': mime_type
                }

        return source