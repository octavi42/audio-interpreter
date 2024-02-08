
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

## Security

### JWT Authentication

To ensure the security of the API, all routes, with the exception of `/ping`, are protected using JWT (JSON Web Tokens) authentication. This requires clients to include a valid JWT in the request header to access the protected endpoints.

#### Obtaining a JWT

Currently, the documentation does not specify a method for obtaining a JWT within this system. Typically, a separate authentication endpoint is used to exchange user credentials for a JWT. Ensure you have a valid JWT, obtained through the prescribed method for your application, before attempting to access protected routes.

#### Sending Requests with JWT

When making requests to protected endpoints, include the JWT in the request's `Authorization` header, prefixed with `Bearer`. Here's the format you should use in your HTTP request headers:

```
Authorization: Bearer <your_jwt_token_here>
```

#### Token Secret Key

It's crucial for the JWT's secret key to match the secret key configured on the server. This secret ensures the integrity and authenticity of the tokens. Keep this key secure and do not expose it in public repositories or client-side code.

### Public Endpoints

The `/ping` route is an example of a public endpoint that does not require JWT authentication. This can be used to verify the server status without needing authentication.

## Usage Instructions

- Ensure the Flask server is running.
- Use the appropriate API routes for audio interpretation, transcription, and model management. For all routes except for public endpoints like `/ping`, include a JWT in the `Authorization` header as described in the Security section.
- For adding custom models, follow the guidelines under the Scalability section.
