#!/usr/bin/env python3
"""
测试工作流音频打包接口
"""

import asyncio
import json
from app.services.workflow_synthesizer import WorkflowSynthesizer
from app.models.tts_flow import TTSFlow

async def test_workflow_synthesizer():
    """测试工作流合成器"""
    
    # 模拟工作流数据
    flow_data = {
        "id": "test_flow_id",
        "name": "测试工作流",
        "voiceId": "test_voice_id",
        "voiceName": "测试音色",
        "flow_config": {
            "logicList": [
                {
                    "nodes": [
                        {
                            "id": "init_d5u3jguc2zk0000",
                            "type": "event-node",
                            "properties": {
                                "componentId": "page_init",
                                "componentName": "pageInit",
                                "name": "开始"
                            }
                        },
                        {
                            "id": "logic_14agv6mk9gsg000",
                            "type": "common-node",
                            "properties": {
                                "type": "ttsTextChunk",
                                "name": "TTS文本分段-01",
                                "componentName": "ttsTextChunk",
                                "nodeContentData": {
                                    "text": "这是测试文本。",
                                    "audioUrl": None
                                }
                            }
                        },
                        {
                            "id": "logic_65o91hmnuac0000",
                            "type": "common-node",
                            "properties": {
                                "type": "spaceVoid",
                                "name": "留白01",
                                "componentName": "spaceVoid",
                                "nodeContentData": {
                                    "duration": 2
                                }
                            }
                        }
                    ],
                    "edges": [
                        {
                            "sourceNodeId": "init_d5u3jguc2zk0000",
                            "targetNodeId": "logic_14agv6mk9gsg000"
                        },
                        {
                            "sourceNodeId": "logic_14agv6mk9gsg000",
                            "targetNodeId": "logic_65o91hmnuac0000"
                        }
                    ]
                }
            ]
        }
    }
    
    # 创建模拟的工作流对象
    flow = TTSFlow(**flow_data)
    
    # 创建合成器
    synthesizer = WorkflowSynthesizer(flow)
    
    # 测试解析工作流
    try:
        synthesizer._parse_workflow()
        print("✅ 工作流解析成功")
        print(f"节点数量: {len(synthesizer.nodes)}")
        
        # 测试找到开始节点
        start_node = synthesizer._find_start_node()
        if start_node:
            print(f"✅ 找到开始节点: {start_node.id}")
        else:
            print("❌ 未找到开始节点")
            
    except Exception as e:
        print(f"❌ 工作流解析失败: {e}")

if __name__ == "__main__":
    asyncio.run(test_workflow_synthesizer()) 