from fastapi import APIRouter
from app.utils.response import success

router = APIRouter(prefix="/role", tags=["角色"])

# ttsFlowList mock 数据
MOCK_TTS_FLOW_LIST = [
    {
        "path": "/tts-flow",
        "component": "#",
        "name": "TTSFlow",
        "meta": {},
        "children": [
            {
                "path": "index",
                "component": "views/TTSFlow/index",
                "name": "TTSFlowPage",
                "meta": {
                    "title": "router.ttsFlow",
                    "icon": "vi-mdi:text-to-speech"
                }
            },
            {
                "path": "canvas/:id",
                "component": "views/TTSFlow/FlowCanvas",
                "name": "TTSFlowCanvas",
                "meta": {
                    "title": "流程配置",
                    "noTagsView": True,
                    "noCache": True,
                    "hidden": True,
                    "canTo": True,
                    "activeMenu": "/tts-flow/index"
                }
            }
        ]
    },
    {
        "path": "/tts-resource",
        "component": "#",
        "name": "TTSResource",
        "meta": {
            "title": "router.ttsResource",
            "icon": "vi-mdi:database-cog",
            "alwaysShow": True
        },
        "children": [
            {
                "path": "platform",
                "component": "views/TTSResource/TTSPlatform/TTSPlatform",
                "name": "TTSPlatform",
                "meta": {
                    "title": "router.ttsPlatform"
                }
            },
            {
                "path": "voice",
                "component": "views/TTSResource/TTSVoice/TTSVoice",
                "name": "TTSVoice",
                "meta": {
                    "title": "router.ttsVoice"
                }
            }
        ]
    }
]

@router.get("/list")
def get_role_list():
    return success(MOCK_TTS_FLOW_LIST) 