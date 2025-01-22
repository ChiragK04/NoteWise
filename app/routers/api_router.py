from fastapi import APIRouter, UploadFile, HTTPException
from app.controllers.upload_controller import handle_audio_upload
from app.controllers.transcription_controller import transcribe_audio
from app.controllers.audio_controller import transcribe_and_process_audio

router = APIRouter()

@router.post("/upload-audio/")
async def upload_audio_endpoint(file: UploadFile):
    """
    Endpoint to upload an audio file and return its AssemblyAI audio URL.
    """
    try:
        # Handle audio file upload and retrieve the AssemblyAI audio URL
        audio_url = handle_audio_upload(file)
        if not audio_url:
            raise HTTPException(status_code=500, detail="Failed to upload file.")
        return {"audio_url": audio_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

@router.post("/transcribe-audio/")
async def transcribe_audio_endpoint(audio_url: str):
    """
    Endpoint to transcribe an audio file using its AssemblyAI URL.
    """
    try:
        # Transcribe the audio using its URL
        transcription_results = transcribe_audio(audio_url)
        return {"transcription": transcription_results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during transcription: {e}")
    
@router.post("/process-audio/")
async def process_audio_endpoint(audio_url: str):
    """
    Endpoint to transcribe an audio file using its AssemblyAI URL,
    then pass the transcription to OpenAI GPT-4 for task generation.
    """
    try:
        # Transcribe and process the audio using GPT-4
        result = transcribe_and_process_audio(audio_url)
        if not result:
            raise HTTPException(status_code=500, detail="Failed to process audio.")
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    
@router.post("/process-audio-with-transcript-and-data-analysis/")
async def process_audio(file: UploadFile):
    """
    Endpoint to upload an audio file, transcribe it with speaker labels,
    and process it with GPT-4 tasks.
    """
    try:
        # Step 1: Handle audio upload and get the AssemblyAI URL
        audio_url = handle_audio_upload(file)
        if not audio_url:
            raise HTTPException(status_code=500, detail="Failed to upload file.")
        
        # Step 2: Transcribe the audio and return speaker-labeled transcription
        transcription = transcribe_audio(audio_url)
        if not transcription:
            raise HTTPException(status_code=500, detail="Failed to transcribe audio.")
        
        # Step 3: Process the transcription with GPT-4 tasks
        task_results = transcribe_and_process_audio(audio_url)
        if not task_results:
            raise HTTPException(status_code=500, detail="Failed to process transcription.")

        # Return combined result
        return {
            "audio_url": audio_url,
            "transcription": transcription,
            "gpt_tasks": task_results["result"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")