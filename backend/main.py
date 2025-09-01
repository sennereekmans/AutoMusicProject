import os
import requests
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, HttpUrl, constr
from typing import Optional
from dotenv import load_dotenv
from enum import Enum



load_dotenv()

app = FastAPI()

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

class MusicExtendRequest(BaseModel):
    defaultParamFlag: bool = Field(..., description="True: custom params, False: original audio params")
    audioId: str = Field(..., description="Audio ID of the track to extend")
    model: ModelVersion = Field(..., description="Model version consistent with source track")
    callBackUrl: Optional[HttpUrl] = None

    # Alleen verplicht als defaultParamFlag == True
    prompt: str | None = Field(None, max_length=3000)
    style: str | None = Field(None, max_length=200)
    title: str | None = Field(None, max_length=80)
    continueAt: int | None = Field(None, gt=0, description="Start time in seconds for extension")

    # Optioneel
    negativeTags: str | None = None
    vocalGender: VocalGender | None = None
    styleWeight: float | None = Field(None, ge=0, le=1)
    weirdnessConstraint: float | None = Field(None, ge=0, le=1)
    audioWeight: float | None = Field(None, ge=0, le=1)

class UploadCoverRequest(BaseModel):
    uploadUrl: HttpUrl = Field(..., description="URL waar het audiobestand staat (max 8 minuten)")
    customMode: bool = Field(..., description="True: Custom mode, False: Non-custom mode")
    instrumental: bool = Field(..., description="True: Instrumentaal (geen lyrics)")

    # Altijd verplicht
    model: ModelVersion
    callBackUrl: HttpUrl

    # Alleen verplicht als customMode == False → prompt verplicht (max 400 chars)
    # Alleen verplicht als customMode == True:
    #  - Als instrumental=True: style en title verplicht
    #  - Als instrumental=False: style, title, prompt verplicht (prompt = lyrics)
    prompt: str | None = None
    style: str | None = None
    title: str | None = None

    # Optioneel
    negativeTags: str | None = None
    vocalGender: VocalGender | None = None
    styleWeight: float | None = Field(None, ge=0, le=1)
    weirdnessConstraint: float | None = Field(None, ge=0, le=1)
    audioWeight: float | None = Field(None, ge=0, le=1)

class LyricsRequest(BaseModel):
    prompt: str = Field(..., max_length=1000, description="Beschrijving van de gewenste lyrics")
    callBackUrl: HttpUrl = Field(..., description="Callback URL om de resultaten te ontvangen")


# ----------- ENDPOINTS -----------
@app.post("/generate-song")
def generateSong(song: SongRequest):
    # Non-custom mode vereist alleen prompt
    if not song.prompt:
        raise HTTPException(status_code=400, detail="Prompt is verplicht in non-custom mode.")

    payload = {
        "prompt": song.prompt,
        "customMode": song.customMode,
        "instrumental": song.instrumental,
        "model": song.model
    }

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

    response = requests.post(SUNO_API_URL, json=payload, headers=headers)
    return response.json()

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
        "title": song.title
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

    response = requests.post(SUNO_API_URL, json=payload, headers=headers)
    return response.json()

""" @app.post("/generate-music-callback")
async def handle_callback(request: Request):
    data = await request.json()  # FastAPI gebruikt async om JSON te lezen
    
    code = data.get('code')
    msg = data.get('msg')
    callback_data = data.get('data', {})
    task_id = callback_data.get('task_id')
    callback_type = callback_data.get('callbackType')
    music_data = callback_data.get('data', [])
    
    print(f"Received music generation callback: {task_id}, type: {callback_type}, status: {code}, message: {msg}")
    
    if code == 200:
        # Task completed successfully
        print("Music generation completed")
        
        print(f"Generated {len(music_data)} music tracks:")
        for i, music in enumerate(music_data):
            print(f"Music {i + 1}:")
            print(f"  Title: {music.get('title')}")
            print(f"  Duration: {music.get('duration')} seconds")
            print(f"  Tags: {music.get('tags')}")
            print(f"  Audio URL: {music.get('audio_url')}")
            print(f"  Cover URL: {music.get('image_url')}")
            
            # Download audio file example
            try:
                audio_url = music.get('audio_url')
                if audio_url:
                    response = requests.get(audio_url)
                    if response.status_code == 200:
                        filename = f"generated_music_{task_id}_{i + 1}.mp3"
                        with open(filename, "wb") as f:
                            f.write(response.content)
                        print(f"Audio saved as {filename}")
            except Exception as e:
                print(f"Audio download failed: {e}")
                
    else:
        # Task failed
        print(f"Music generation failed: {msg}")
        
        if code == 400:
            print("Parameter error or content violation")
        elif code == 451:
            print("File download failed")
        elif code == 500:
            print("Server internal error")
    
    # Return 200 status code to confirm callback received
    return JSONResponse(content={'status': 'received'}, status_code=200) """

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
    
@app.post("/extend-music")
def extend_music(req: MusicExtendRequest):
    # Validatie: als defaultParamFlag True is, moeten extra velden aanwezig zijn
    if req.defaultParamFlag:
        if not (req.prompt and req.style and req.title and req.continueAt):
            raise HTTPException(status_code=400, detail="prompt, style, title en continueAt zijn verplicht wanneer defaultParamFlag True is")

    # Payload bouwen voor Suno API
    payload = req.dict(exclude_none=True)
    url = "https://api.sunoapi.org/api/v1/generate/extend"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json())
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post("/upload-cover")
def upload_cover(req: UploadCoverRequest):
    # Validatie logica
    if req.customMode:
        if req.instrumental:
            if not (req.style and req.title):
                raise HTTPException(status_code=400, detail="style en title zijn verplicht in customMode + instrumental=True")
        else:  # instrumental=False
            if not (req.style and req.title and req.prompt):
                raise HTTPException(status_code=400, detail="style, title en prompt zijn verplicht in customMode + instrumental=False")
    else:  # customMode=False
        if not req.prompt:
            raise HTTPException(status_code=400, detail="prompt is verplicht als customMode=False")

    # API-call naar Suno
    url = "https://api.sunoapi.org/api/v1/generate/upload-cover"
    headers = {
        "Authorization": f"Bearer {API_KEY}",  # vervang met jouw API key
        "Content-Type": "application/json"
    }

    payload = req.dict(exclude_none=True)

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json())
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/lyrics")
def generate_lyrics(request: LyricsRequest):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": request.prompt,
        "callBackUrl": str(request.callBackUrl)
    }

    try:
        response = requests.post(SUNO_API_URL, json=payload, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json())
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/credits")
def get_credits():
    headers = {
        "Authorization": f"Bearer {API_KEY}",
    }
    url = "https://api.sunoapi.org/api/v1/generate/credit"
    response = requests.get(url, headers=headers)
    return response

    
