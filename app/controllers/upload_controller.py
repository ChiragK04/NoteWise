import os
from app.utils.audio_utils import upload_audio

def handle_audio_upload(file) -> str:
    """
    Save the uploaded audio file locally, upload to AssemblyAI, and return the audio URL.
    """
    file_path = f"temp_{file.filename}"
    with open(file_path, 'wb') as f:
        f.write(file.file.read())
    
    # Upload the audio file to AssemblyAI
    audio_url = upload_audio(file_path)
    
    # Remove the temporary file after upload
    os.remove(file_path)
    
    return audio_url
