from flask import Flask, request, jsonify
import assemblyai as aai
import os

app = Flask(__name__)

# Set AssemblyAI API Key
aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY", "ec692034e7774a169850a6a88d013cc4")


# Route for audio transcription
@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    try:
        # Check if the audio file is present
        if 'audio' not in request.files:
            return jsonify({"error": "No audio file provided"}), 400

        # Get the audio file from the request
        audio_file = request.files['audio']

        # Save the file temporarily
        audio_file.save(audio_file.filename)

        # Initialize transcriber and transcribe
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio_file.filename)

        # Delete the temp file after transcription
        os.remove(audio_file.filename)

        # Check for transcription errors
        if transcript.status == aai.TranscriptStatus.error:
            return jsonify({"error": transcript.error}), 500

        # Return the transcription text
        return jsonify({"transcript": transcript.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
