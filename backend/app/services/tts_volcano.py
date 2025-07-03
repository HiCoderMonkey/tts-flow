import requests
import json
import base64
import wave
import os

def tts_volcano_stream(text, voice, platform, wav_path, relative_path):
    headers = {
        "X-Api-App-Id": platform.config.get("appid"),
        "X-Api-Access-Key": platform.config.get("access_token"),
        "X-Api-Resource-Id": platform.config.get("resource_id"),
        "X-Api-App-Key": "aGjiRDfUWi",
        "Content-Type": "application/json",
        "Connection": "keep-alive"
    }
    payload = {
        "user": {"uid": "12345"},
        "req_params": {
            "text": text,
            "speaker": voice.role_id,
            "additions": "{}",
            "audio_params": {
                "format": "pcm",
                "sample_rate": 24000
            }
        }
    }
    session = requests.Session()
    audio_data = bytearray()
    try:
        response = session.post("https://openspeech.bytedance.com/api/v3/tts/unidirectional",
                                headers=headers, json=payload, stream=True)
        for chunk in response.iter_lines(decode_unicode=True):
            if not chunk:
                continue
            data = json.loads(chunk)
            if data.get("code", 0) == 0 and "data" in data and data["data"]:
                chunk_audio = base64.b64decode(data["data"])
                audio_data.extend(chunk_audio)
                # 流式返回
                yield {"data": data["data"], "type": "pcm", "end": False}
            if data.get("code", 0) == 20000000:
                break
            if data.get("code", 0) > 0:
                yield {"data": str(data), "type": "error", "end": True}
                return
        # 保存为wav
        os.makedirs(os.path.dirname(wav_path), exist_ok=True)
        with wave.open(wav_path, 'wb') as wavfile:
            wavfile.setnchannels(1)
            wavfile.setsampwidth(2)
            wavfile.setframerate(24000)
            wavfile.writeframes(audio_data)
        yield {"data": relative_path, "type": "wav_path", "end": True}
    finally:
        response.close()
        session.close() 