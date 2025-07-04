from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.models.tts_flow import TTSFlow
from app.models.tts_voice import TTSVoice
from app.models.tts_platform import TTSPlatform
from app.services.tts_volcano import tts_volcano_stream
from app.core.constants import AppConstants
import os
import json

router = APIRouter(prefix="/tts-synthesize", tags=["TTS合成"])

class TTSRequest(BaseModel):
    flow_id: str
    text: str
    node_id: str
    node_name: str

def _event_data(data):
    return f"data: {json.dumps(data,ensure_ascii=False)}\n\n"



@router.post("/synthesize")
async def tts_synthesize(req: TTSRequest):
    flow = await TTSFlow.get(req.flow_id)
    if not flow:
        def err():
            yield _event_data({'data': 'flow not found', 'type': 'error', 'end': True})
        return StreamingResponse(err())
    voice_id = flow.voiceId
    if not voice_id:
        def err():
            yield _event_data({'data': 'voiceId not set', 'type': 'error', 'end': True})
        return StreamingResponse(err())
    voice = await TTSVoice.get(voice_id)
    if not voice:
        def err():
            yield _event_data({'data': 'voice not found', 'type': 'error', 'end': True})
        return StreamingResponse(err())
    platform = await TTSPlatform.get(voice.platform_id)
    if not platform:
        def err():
            yield _event_data({'data': 'platform not found', 'type': 'error', 'end': True})
        return StreamingResponse(err())
    if platform.type == "volcano":
        wav_dir = os.path.join(AppConstants.STATIC_DIR, "tts_wav", req.flow_id)
        os.makedirs(wav_dir, exist_ok=True)
        wav_path = os.path.join(wav_dir, f"{req.node_id}_{req.node_name}.wav")
        def event_generator():
            for chunk in tts_volcano_stream(
                text=req.text,
                voice=voice,
                platform=platform,
                wav_path=wav_path,
                relative_path=f"tts_wav/{req.flow_id}/{req.node_id}_{req.node_name}.wav"
            ):
                yield _event_data(chunk)
        return StreamingResponse(event_generator())
    else:
        def err():
            yield _event_data({'data': 'not implemented', 'type': 'error', 'end': True})
        return StreamingResponse(err()) 