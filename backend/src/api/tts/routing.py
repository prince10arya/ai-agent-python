"""Text-to-Speech routing for email draft reading."""

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import requests
import io

router = APIRouter()


class TTSRequest(BaseModel):
    """Request model for TTS."""
    text: str
    voice: str = "af_heart"
    speed: float = 1.0


@router.post("/speak", tags=["TTS"])
async def text_to_speech(request: TTSRequest):
    """Convert email draft text to speech."""
    try:
        tts_api_url = "http://host.docker.internal:8000/api/tts"
        
        response = requests.post(
            tts_api_url,
            json={
                "text": request.text,
                "voice": request.voice,
                "speed": request.speed
            },
            timeout=30
        )
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail="TTS service failed"
            )
        
        return StreamingResponse(
            io.BytesIO(response.content),
            media_type="audio/wav",
            headers={"Content-Disposition": "attachment; filename=email_draft.wav"}
        )
        
    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=503,
            detail="TTS service unavailable. Make sure TTS server is running on port 8000"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate speech: {str(e)}"
        )
