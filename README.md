
# audio-function-calling

The program is a Flask server designed to interpret audio files for key data extraction and database modifications. It receives an audio file, transcribes it using Deepgram, Whisper, or a custom-added model, and extracts key data using OpenAI.

## Functionality:

### NAVIGATE to /settings:
#### NAVIGATE to /model:
- POST request to `/set_model`:
  - Change the audio model used (Deepgram, OpenAI, or a custom-added model).
  - Include in body as JSON: `"model": "(model you want to set)"`
  - Response: `{"model_name": model_name}`
- GET request to `/get_models`:
  - Retrieve all available model names.
- GET request to `/get_used_model`:
  - Obtain the currently used model.

#### NAVIGATE to /gpt:
- POST request to `/set_gpt_model`:
  - Change the GPT model used.
  - Include in body as JSON: `"model": "(model you want to set)"`
  - Response: `{"model_name": model_name}`
- GET request to `/get_gpt_model`:
  - Retrieve the currently used GPT model.

### NAVIGATE to /audio_tools:
- POST request to `/interpret`:
  - Interpret an audio file.
  - Include in body an audio file with key "audio".
  - Response: JSON object with `interpreted_result` that includes transcription, relevance, and other key data.
- POST request to `/interpret_with_language`:
  - Similar to `/interpret` but with language specification for translation purposes.
  - Include "language" in the form data along with the audio file.
  - Response: JSON object with `interpreted_result` including translated titles and descriptions if applicable.
- POST request to `/speech_to_text`:
  - Convert speech in an audio file to text.
  - Include in body an audio file with key "audio".
  - Response: JSON object with `interpreted_result` containing the transcribed text.
- POST request to `/speech_to_text_with_language`:
  - Similar to `/speech_to_text` but with language specification.
  - Include "language" in the form data along with the audio file.
  - Response: JSON object with `interpreted_result` containing the transcribed text.

## Scalability:
- Additional text processing services can be added; the current models are from Deepgram and OpenAI.
- Models are added in the `speech_to_text/models` directory.
- The file name is crucial for the functionality of the model.
- If an API key is needed, include it in the .env file as: `"(name of the file)_API_KEY"`.
- Each model file must have a `process_audio` function for text extraction from audio. 
- See `example.py` in `speech_to_text/models` for custom model implementation examples.

## New Routes and Functionalities:

### `/interpret`:
- Transcribes and interprets an audio file.
- POST a WAV audio file with the key "audio".
- Returns a comprehensive JSON object with transcription, relevance, and detailed interpretation of the audio content.

### `/interpret_with_language`:
- Similar to `/interpret`, but for specific language support (e.g., Arabic).
- Translates the interpreted content if necessary.
- POST a WAV audio file with the key "audio" and specify the "language".

### `/speech_to_text`:
- Transcribes audio to text without further interpretation.
- POST a WAV audio file with the key "audio".
- Returns the transcription result as text.

### `/speech_to_text_with_language`:
- Transcribes audio to text in a specified language.
- POST a WAV audio file with the key "audio" and specify the "language".
- Ideal for multilingual audio content.

## Usage Instructions:
- Ensure the Flask server is running.
- Use appropriate API routes for audio interpretation, transcription, and model management.
- For adding custom models, follow the guidelines under the Scalability section.
