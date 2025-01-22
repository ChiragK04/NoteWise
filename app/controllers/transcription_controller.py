from app.utils.transcription import transcribe_audio

def get_transcription(audio_url: str) -> str:
    """
    Controller function to transcribe audio.
    """
    try:
        return transcribe_audio(audio_url)
    except Exception as e:
        print(f"Error in getting transcription: {e}")
        return None
