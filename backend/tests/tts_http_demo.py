import requests
import json
import base64
import os
import wave

# python版本：==3.11

# -------------客户需要填写的参数----------------
appID = "8592039908"
accessKey = "6Xnc-gmrf7Vczt2pHoxKBDatQQobLJdX"
resourceID = "volc.service_type.10029"
text = "这是一段测试文本，用于测试字节大模型语音合成http单向流式接口效果。"
# ---------------请求地址----------------------
url = "https://openspeech.bytedance.com/api/v3/tts/unidirectional"

def tts_http_stream():
    headers = {
        "X-Api-App-Id": appID,
        "X-Api-Access-Key": accessKey,
        "X-Api-Resource-Id": resourceID,
        "X-Api-App-Key": "aGjiRDfUWi",
        "Content-Type": "application/json",
        "Connection": "keep-alive"
    }

    additions = {
        "disable_markdown_filter": True,
        "enable_language_detector": True,
        "enable_latex_tn": True,
        "disable_default_bit_rate": True,
        "max_length_to_filter_parenthesis": 0,
        "cache_config": {
            "text_type": 1,
            "use_cache": True
        }
    }

    additions_json = json.dumps(additions)

    payload = {
        "user": {"uid": "12345"},
        "req_params": {
            "text": text,
            "speaker": "zh_female_wanqudashu_moon_bigtts",
            "additions": additions_json,
            "audio_params": {
                "format": "pcm",
                "sample_rate": 24000
            }
        }
    }
    session = requests.Session()
    try:
        response = session.post(url, headers=headers, json=payload, stream=True)
        # 打印response headers
        # print(f"code: {response.status_code} header: {response.headers}")

        # 用于存储音频数据
        audio_data = bytearray()
        total_audio_size = 0
        for chunk in response.iter_lines(decode_unicode=True):
            if not chunk:
                continue
            data = json.loads(chunk)
            print(f"json data:{data}")
            if data.get("code", 0) == 0 and "data" in data and data["data"]:
                chunk_audio = base64.b64decode(data["data"])
                audio_size = len(chunk_audio)
                total_audio_size += audio_size
                audio_data.extend(chunk_audio)
            if data.get("code", 0) == 20000000:
                break
            if data.get("code", 0) > 0:
                print(f"error response:{data}")
                break

        # 保存pcm音频文件
        if audio_data:
            os.makedirs("tts", exist_ok=True)
            pcm_file = os.path.join("tts/", f"tts_test.pcm")
            with open(pcm_file, "wb") as f:
                f.write(audio_data)
            print(f"PCM文件大小: {len(audio_data) / 1024:.2f} KB")
            os.chmod(pcm_file, 0o644)

            # 自动转为wav文件
            wav_file = os.path.join("tts/", f"tts_test.wav")
            with wave.open(wav_file, 'wb') as wavfile:
                wavfile.setnchannels(1)        # 单声道
                wavfile.setsampwidth(2)        # 16bit = 2字节
                wavfile.setframerate(24000)    # 采样率
                wavfile.writeframes(audio_data)
            print(f"已生成wav文件: {wav_file}")
            os.chmod(wav_file, 0o644)

    except Exception as e:
        print(f"请求失败: {e}")
    finally:
        response.close()
        session.close()


if __name__ == "__main__":
    tts_http_stream()
