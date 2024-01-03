import requests
import neuralspace as ns

class Ns():
    def __init__(self, api_key):
        super().__init__()
        self.api_key = api_key

    def process_audio(self, audio, language=""):
        vai = ns.VoiceAI(api_key=self.api_key)
        if language == "":
            config = {
                'file_transcription': {
                    'mode': 'advanced',
                }
            }
        else:
            config = {
                'file_transcription': {
                    'mode': 'advanced',
                    'language_id': language,
                }
            }

        # Create a new file transcription job
        job_id = vai.transcribe(file=audio, config=config)
        # result = vai.get_job_status(job_id)
        result = vai.poll_until_complete(job_id)

        return result["data"]["result"]["transcription"]["transcript"]