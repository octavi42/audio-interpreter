# audio-function-claling

The program is a flask server.
The core functionallity and purpose is to interpret an audio file in order to obtain the key data to make modifications to a database.
The server will receive an audio file, it will transcribe it using deepgram, whisper or a costum added model and it will extract the key data using openai.
