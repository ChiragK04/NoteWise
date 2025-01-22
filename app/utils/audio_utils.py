import requests

def upload_audio(file_path: str) -> str:
    """
    Upload an audio file to AssemblyAI and return the audio URL.
    """
    API_KEY = "07559d91143243abb3b00382c0309153"  
    url = "https://api.assemblyai.com/v2/upload"
    headers = {"authorization": API_KEY}

    with open(file_path, 'rb') as f:
        response = requests.post(url, headers=headers, files={"file": f})
        response.raise_for_status()
        return response.json().get("upload_url")
