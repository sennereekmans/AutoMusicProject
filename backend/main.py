import os
import requests
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, HttpUrl, constr
from typing import Optional
from dotenv import load_dotenv
from enum import Enum
import time


load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # of ["*"] voor alle origins
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],  # Alle headers
)

API_KEY = os.getenv('API_KEY')
SUNO_API_URL = os.getenv('SUNO_API_URL')

# ----------- MODELS -----------
class ModelVersion(str, Enum):
    V3_5 = "V3_5"
    V4 = "V4"
    V4_5 = "V4_5"

class VocalGender(str, Enum):
    m = "m"
    f = "f"

class SongRequest(BaseModel):
    prompt: str
    customMode: bool = False
    instrumental: bool = False
    model: ModelVersion = ModelVersion.V3_5  # default
    negativeTags: Optional[str] = None
    vocalGender: Optional[VocalGender] = None
    styleWeight: Optional[float] = None
    weirdnessConstraint: Optional[float] = None
    audioWeight: Optional[float] = None
    callBackUrl: Optional[str] = None

class CustomSongRequest(BaseModel):
    prompt: Optional[str] = None  # Mag leeg zijn als instrumental=True, prompt=lyrics als intrumental=False
    style: str
    title: str
    instrumental: bool = False
    model: ModelVersion = ModelVersion.V3_5  # default
    negativeTags: Optional[str] = None
    vocalGender: Optional[VocalGender] = None
    styleWeight: Optional[float] = None
    weirdnessConstraint: Optional[float] = None
    audioWeight: Optional[float] = None
    callBackUrl: Optional[HttpUrl] = None

class LyricsRequest(BaseModel):
    prompt: str = Field(..., max_length=1000)

class MusicVideoRequest(BaseModel):
    taskId: str
    audioId: str
    author: Optional[str] = None
    domainName: Optional[str] = None

# ----------- ENDPOINTS -----------
@app.post("/generate-song")
def generateSong(song: SongRequest):
    print("In endpoint")
    # Non-custom mode vereist alleen prompt
    if not song.prompt:
        raise HTTPException(status_code=400, detail="Prompt is verplicht in non-custom mode.")

    payload = {
        "prompt": song.prompt,
        "customMode": song.customMode,
        "instrumental": song.instrumental,
        "model": song.model,
        "callBackUrl": "http://localhost:8000/song-callback"
    }

    if song.negativeTags: payload["negativeTags"] = song.negativeTags
    if song.vocalGender: payload["vocalGender"] = song.vocalGender
    if song.styleWeight is not None: payload["styleWeight"] = song.styleWeight
    if song.weirdnessConstraint is not None: payload["weirdnessConstraint"] = song.weirdnessConstraint
    if song.audioWeight is not None: payload["audioWeight"] = song.audioWeight

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    print("sending post request")
    # ✅ Suno API request
    response = requests.post(SUNO_API_URL, json=payload, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    result = response.json()
    print("API response JSON:", result)

    task_id = result.get("data", {}).get("taskId")
    if not task_id:
        raise HTTPException(status_code=500, detail="Geen taskId ontvangen van Suno API.")

    response2 = poll_music_task(token=API_KEY, task_id=task_id, url="https://api.sunoapi.org/api/v1/generate/record-info")
    return response2

@app.post("/generate-customsong")
def generateCustomSong(song: CustomSongRequest):
    # Validatie volgens regels
    if song.instrumental:
        if not song.style or not song.title:
            raise HTTPException(status_code=400, detail="Style en title zijn verplicht als instrumental=True.")
    else:
        if not song.prompt or not song.style or not song.title:
            raise HTTPException(status_code=400, detail="Prompt, style en title zijn verplicht als instrumental=False.")

    payload = {
        "customMode": True,
        "instrumental": song.instrumental,
        "model": song.model,
        "style": song.style,
        "title": song.title,
        "callBackUrl": "http://localhost:8000/song-callback"
    }

    if not song.instrumental and song.prompt:
        payload["prompt"] = song.prompt

    if song.negativeTags: payload["negativeTags"] = song.negativeTags
    if song.vocalGender: payload["vocalGender"] = song.vocalGender
    if song.styleWeight is not None: payload["styleWeight"] = song.styleWeight
    if song.weirdnessConstraint is not None: payload["weirdnessConstraint"] = song.weirdnessConstraint
    if song.audioWeight is not None: payload["audioWeight"] = song.audioWeight
    if song.callBackUrl: payload["callBackUrl"] = song.callBackUrl

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    print("sending post request")
    # ✅ Suno API request
    response = requests.post(SUNO_API_URL, json=payload, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    result = response.json()
    print("API response JSON:", result)

    task_id = result.get("data", {}).get("taskId")
    if not task_id:
        raise HTTPException(status_code=500, detail="Geen taskId ontvangen van Suno API.")

    response2 = poll_music_task(token=API_KEY, task_id=task_id, url="https://api.sunoapi.org/api/v1/generate/record-info")
    return response2



@app.get("/check-status/{task_id}")
def checkStatus(task_id: str):
    if task_id != "":
        headers = {
            "Authorization": f"Bearer {API_KEY}",
        }
        statusURL = SUNO_API_URL + "/record-info?taskId=" + task_id
        response = requests.post(statusURL, headers=headers)
        return response.json()
    else:
        return {"error": "No taskId found. Generate a song first."} 
    


    
@app.post("/lyrics")
def generate_lyrics(request: LyricsRequest):
    url = "https://api.sunoapi.org/api/v1/lyrics"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": request.prompt,
        "callBackUrl": "http://localhost:8000/song-callback"
    }

    try:
        print("sending post request")
        response = requests.post(url, json=payload, headers=headers)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        result = response.json()
        print("API response JSON:", result)

        data = result.get("data")
        if not data or not isinstance(data, dict) or "taskId" not in data:
            raise HTTPException(status_code=500, detail="Geen geldige data ontvangen van Suno API.")

        task_id = data["taskId"]
        response2 = poll_music_task(token=API_KEY, task_id=task_id, url="https://api.sunoapi.org/api/v1/lyrics/record-info")
        return response2

    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

    
@app.get("/credits")
def get_credits():
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    url = "https://api.sunoapi.org/api/v1/generate/credit"
    response = requests.get(url, headers=headers)
    return response.json()


@app.post("/generate-music-video")
def generate_music_video(request: MusicVideoRequest):
    url = "https://api.sunoapi.org/api/v1/mp4/generate"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "taskId": request.taskId,
        "audioId": request.audioId,
        "callBackUrl": "http://localhost:8000/song-callback"
    }

    if request.author:
        payload["author"] = request.author
    if request.domainName:
        payload["domainName"] = request.domainName

    try:
        print("sending post request for music video")
        response = requests.post(url, json=payload, headers=headers)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        result = response.json()
        print("API response JSON:", result)
        if not result or "data" not in result:
            raise HTTPException(status_code=500, detail=f"Geen geldige data ontvangen van Suno API: {result}")

        task_id = result["data"].get("taskId")
        if not task_id:
            raise HTTPException(status_code=500, detail=f"Geen taskId ontvangen van Suno API: {result}")

        # Poll video task status
        response2 = poll_video_task(
            token=API_KEY,
            task_id=task_id,
            url="https://api.sunoapi.org/api/v1/mp4/record-info"
        )
        return response2

    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----------- FUNCTIONS -----------    
def poll_music_task(token: str, task_id: str, url= str, interval: int = 20, max_attempts: int = 50):
    url1 = url
    headers = {"Authorization": f"Bearer {token}"}
    params = {"taskId": task_id}

    for attempt in range(max_attempts):
        try:
            response = requests.get(url1, headers=headers, params=params)
            data = response.json()
            print(f"[Attempt {attempt+1}] Status: {data.get('data', {}).get('status')}")

            if not data or "data" not in data:
                time.sleep(interval)
                continue

            status = data.get("data", {}).get("status")

            if status in [
                "SUCCESS",
                "GENERATE_AUDIO_FAILED",
                "CREATE_TASK_FAILED",
                "CALLBACK_EXCEPTION",
                "SENSITIVE_WORD_ERROR"
            ]:
                return data  # Geef volledige response terug

        except Exception as e:
            print(f"Error in poll_music_task: {e}")

        time.sleep(interval)

    return {"error": "Timeout: Task did not complete in time"}


# ----------- FUNCTIONS -----------    
def poll_video_task(token: str, task_id: str, url= str, interval: int = 20, max_attempts: int = 50):
    url1 = url
    headers = {"Authorization": f"Bearer {token}"}
    params = {"taskId": task_id}

    for attempt in range(max_attempts):
        try:
            response = requests.get(url1, headers=headers, params=params)
            data = response.json()
            print(f"[Attempt {attempt+1}] Status: {data.get('data', {}).get('status')}")

            if not data or "data" not in data:
                time.sleep(interval)
                continue

            status = data.get("data", {}).get("successFlag")

            if status in [
                "SUCCESS",
                "GENERATE_AUDIO_FAILED",
                "CREATE_TASK_FAILED",
                "CALLBACK_EXCEPTION",
                "SENSITIVE_WORD_ERROR"
            ]:
                return data  # Geef volledige response terug

        except Exception as e:
            print(f"Error in poll_music_task: {e}")

        time.sleep(interval)

    return {"error": "Timeout: Task did not complete in time"}