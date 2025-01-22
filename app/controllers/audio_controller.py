from app.utils.audio_intelligence import process_audio_tasks

def transcribe_and_process_audio(transcription: str) -> dict:
    """
    Controller function to process transcription through GPT-4 tasks.
    """
    try:
        return process_audio_tasks(transcription)
    except Exception as e:
        print(f"Error in processing audio: {e}")
        return {"error": str(e)}
