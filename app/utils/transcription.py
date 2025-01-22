import assemblyai as aai
from dotenv import load_dotenv
import os

load_dotenv()

aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")  

def transcribe_audio(audio_url: str) -> str:
    """
    Transcribes an audio file using AssemblyAI and returns the transcript.
    """
    try:
        config = aai.TranscriptionConfig(speaker_labels=True)
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio_url, config)

        # Combine all utterances into a single string with speaker labels
        transcript_text = "\n".join(
            f"Speaker {utterance.speaker}: {utterance.text}" for utterance in transcript.utterances
        )
        return transcript_text

    except Exception as e:
        print(f"Error in transcribing audio: {e}")
        return None
