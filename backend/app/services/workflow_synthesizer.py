import json
import os
import wave
import numpy as np
import zipfile
from typing import Dict, List, Optional, Generator
from fastapi.responses import StreamingResponse
from app.models.tts_flow import TTSFlow
from app.models.tts_voice import TTSVoice
from app.models.tts_platform import TTSPlatform
from app.services.tts_volcano import tts_volcano_stream
from app.core.constants import AppConstants


class Node:
    """节点数据结构"""
    def __init__(self, node_data: Dict):
        self.id = node_data.get('id')
        self.type = node_data.get('type')
        self.properties = node_data.get('properties', {})
        self.next: Optional[Node] = None


class EventType:
    """事件类型常量"""
    START = "start"                    # 开始
    NODE = "node"                      # 节点
    NODE_TASK = "node_task"            # 节点内生成任务
    AUDIO_CONCAT = "audio_concat"      # 音频拼接
    ZIP_PACKAGE = "zip_package"        # ZIP打包
    END = "end"                        # 结束


class WorkflowSynthesizer:
    """工作流音频合成器"""
    
    def __init__(self, flow: TTSFlow):
        self.flow = flow
        self.flow_config = flow.flow_config or {}
        self.nodes: List[Node] = []
        self.node_map: Dict[str, Node] = {}
        self.voice = None
        self.platform = None
        self.audio_files: List[str] = []  # 收集所有音频文件路径
        self.wav_dir = os.path.join(AppConstants.STATIC_DIR, "tts_wav", str(self.flow.id))
        self.processed_count = 0  # 已处理节点计数
        self.total_nodes = 0      # 总节点数
        
    async def _load_voice_and_platform(self):
        """加载音色和平台信息"""
        if not self.flow.voiceId:
            raise Exception("工作流未配置音色")
            
        self.voice = await TTSVoice.get(self.flow.voiceId)
        if not self.voice:
            raise Exception("音色不存在")
            
        self.platform = await TTSPlatform.get(self.voice.platform_id)
        if not self.platform:
            raise Exception("平台不存在")
    
    def _parse_workflow(self):
        """解析工作流配置，构建节点链表"""
        logic_list = self.flow_config.get('logicList', [])
        if not logic_list:
            raise Exception("工作流配置为空")
            
        logic = logic_list[0]  # 取第一个逻辑
        nodes_data = logic.get('nodes', [])
        edges_data = logic.get('edges', [])
        
        # 构建节点映射
        for node_data in nodes_data:
            node = Node(node_data)
            self.nodes.append(node)
            self.node_map[node.id] = node
        
        # 构建节点链表关系
        for edge in edges_data:
            source_id = edge.get('sourceNodeId')
            target_id = edge.get('targetNodeId')
            
            if source_id in self.node_map and target_id in self.node_map:
                source_node = self.node_map[source_id]
                target_node = self.node_map[target_id]
                source_node.next = target_node
    
    def _find_start_node(self) -> Optional[Node]:
        """找到开始节点"""
        for node in self.nodes:
            if node.type == 'event-node':
                return node
        return None
    
    def _yield_event(self, data: Dict, code: int = 0, type: str = EventType.NODE):
        """生成事件流数据"""
        return f"data: {json.dumps({'data': data, 'code': code, 'type': type}, ensure_ascii=False)}\n\n"
    
    def _get_progress_data(self, current_node_name: str = ""):
        """获取进度数据"""
        return {
            'processed': self.processed_count,
            'total': self.total_nodes,
            'percentage': round((self.processed_count / self.total_nodes * 100) if self.total_nodes > 0 else 0, 1),
            'currentNode': current_node_name
        }
    
    def _concatenate_audio_files(self, audio_files: List[str], output_path: str):
        """拼接多个音频文件"""
        if not audio_files:
            return
            
        # 读取第一个文件获取音频参数
        with wave.open(audio_files[0], 'rb') as first_wav:
            channels = first_wav.getnchannels()
            sample_width = first_wav.getsampwidth()
            sample_rate = first_wav.getframerate()
        
        # 拼接所有音频数据
        all_audio_data = bytearray()
        
        for audio_file in audio_files:
            if os.path.exists(audio_file):
                with wave.open(audio_file, 'rb') as wav_file:
                    # 确保音频参数一致
                    if (wav_file.getnchannels() == channels and 
                        wav_file.getsampwidth() == sample_width and 
                        wav_file.getframerate() == sample_rate):
                        audio_data = wav_file.readframes(wav_file.getnframes())
                        all_audio_data.extend(audio_data)
                    else:
                        print(f"警告: 音频文件 {audio_file} 参数不匹配，跳过")
        
        # 保存拼接后的音频
        with wave.open(output_path, 'wb') as output_wav:
            output_wav.setnchannels(channels)
            output_wav.setsampwidth(sample_width)
            output_wav.setframerate(sample_rate)
            output_wav.writeframes(all_audio_data)
    
    def _create_zip_archive(self, source_dir: str, zip_path: str):
        """创建ZIP压缩包"""
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(source_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    # 计算相对路径，避免在ZIP中包含完整路径
                    arcname = os.path.relpath(file_path, source_dir)
                    zipf.write(file_path, arcname)
    
    async def _process_tts_node(self, node: Node) -> Generator[str, None, None]:
        """处理TTS文本节点"""
        properties = node.properties
        node_content = properties.get('nodeContentData', {})
        audio_url = node_content.get('audioUrl')
        text = node_content.get('text', '')
        node_name = properties.get('name', '')
        
        # 返回节点信息
        yield self._yield_event({
            'nodeId': node.id,
            'nodeName': node_name,
            'nodeType': 'ttsTextChunk',
            'text': text,
            'audioUrl': audio_url,
            'progress': self._get_progress_data(node_name)
        }, 0, EventType.NODE)
        
        if not text:
            yield self._yield_event({
                'error': '文本内容为空',
                'progress': self._get_progress_data(node_name)
            }, 1, EventType.NODE_TASK)
            return
        
        # 检查是否已有音频文件（只有文件真实存在才直接返回，否则继续生成新音频）
        if audio_url:
            static_path = os.path.join(AppConstants.STATIC_DIR, audio_url.lstrip('/'))
            if os.path.exists(static_path):
                yield self._yield_event({
                    'status': '使用已有音频文件',
                    'audioUrl': audio_url,
                    'progress': self._get_progress_data(node_name)
                }, 0, EventType.NODE_TASK)
                self.audio_files.append(static_path)
                return
            # 文件不存在则自动生成新音频（继续往下执行）
        
        # 生成新音频
        os.makedirs(self.wav_dir, exist_ok=True)
        wav_path = os.path.join(self.wav_dir, f"{node.id}_{node_name}.wav")
        relative_path = f"tts_wav/{self.flow.id}/{node.id}_{node_name}.wav"
        
        yield self._yield_event({
            'status': '开始生成音频',
            'progress': self._get_progress_data(node_name)
        }, 0, EventType.NODE_TASK)
        
        try:
            if getattr(self.platform, "type", None) == "volcano":
                for chunk in tts_volcano_stream(
                    text=text,
                    voice=self.voice,
                    platform=self.platform,
                    wav_path=wav_path,
                    relative_path=relative_path
                ):
                    # 为每个chunk添加进度信息
                    yield self._yield_event({
                        'status': f'{node.id}_{node_name}_生成中...',
                        'progress': self._get_progress_data(node_name)
                    }, 0, EventType.NODE_TASK)
            else:
                raise Exception("暂不支持该平台类型的TTS合成")
            # 添加到音频文件列表
            self.audio_files.append(wav_path)
        except Exception as e:
            yield self._yield_event({
                'error': str(e),
                'progress': self._get_progress_data(node_name)
            }, 1, EventType.NODE_TASK)
    
    async def _process_space_node(self, node: Node) -> Generator[str, None, None]:
        """处理留白节点"""
        properties = node.properties
        node_content = properties.get('nodeContentData', {})
        duration = node_content.get('duration', 3)  # 默认3秒
        node_name = properties.get('name', '')
        
        # 返回节点信息
        yield self._yield_event({
            'nodeId': node.id,
            'nodeName': node_name,
            'nodeType': 'spaceVoid',
            'duration': duration,
            'progress': self._get_progress_data(node_name)
        }, 0, EventType.NODE)
        
        # 生成空白音频
        os.makedirs(self.wav_dir, exist_ok=True)
        wav_path = os.path.join(self.wav_dir, f"{node.id}_{node_name}.wav")
        
        # 生成指定时长的空白音频
        sample_rate = 24000
        samples = int(duration * sample_rate)
        silence = np.zeros(samples, dtype=np.int16)
        
        with wave.open(wav_path, 'wb') as wavfile:
            wavfile.setnchannels(1)
            wavfile.setsampwidth(2)
            wavfile.setframerate(sample_rate)
            wavfile.writeframes(silence.tobytes())
        
        # 添加到音频文件列表
        self.audio_files.append(wav_path)
        
        yield self._yield_event({
            'status': '空白音频生成完成',
            'duration': duration,
            'progress': self._get_progress_data(node_name)
        }, 0, EventType.NODE_TASK)
    
    async def _process_node(self, node: Node) -> Generator[str, None, None]:
        """处理单个节点"""
        if not node or not node.properties:
            return
            
        node_type = node.properties.get('type')
        if not node_type:
            return
        
        if node_type == 'ttsTextChunk':
            async for event in self._process_tts_node(node):
                yield event
        elif node_type == 'spaceVoid':
            async for event in self._process_space_node(node):
                yield event
        # 可以扩展其他节点类型
    
    def synthesize_all(self) -> StreamingResponse:
        """开始合成整个工作流音频"""
        async def event_generator():
            try:
                # 加载音色和平台信息
                await self._load_voice_and_platform()
                
                # 解析工作流
                self._parse_workflow()
                
                # 计算需要处理的节点数量（排除事件节点）
                self.total_nodes = len([node for node in self.nodes if node.type != 'event-node']) + 1
                
                # 返回开始事件
                yield self._yield_event({
                    'totalNodes': self.total_nodes,
                    'progress': self._get_progress_data()
                }, 0, EventType.START)
                
                # 找到开始节点
                current_node = self._find_start_node()
                if not current_node:
                    yield self._yield_event({
                        'error': '未找到开始节点',
                        'progress': self._get_progress_data()
                    }, 1, EventType.END)
                    return
                
                # 处理节点链表
                while current_node:
                    if current_node.type != 'event-node':  # 跳过事件节点
                        async for event in self._process_node(current_node):
                            yield event

                    self.processed_count += 1
                    
                    current_node = current_node.next
                
                # 拼接所有音频文件
                if self.audio_files:
                    yield self._yield_event({
                        'status': '开始拼接音频文件',
                        'progress': self._get_progress_data("音频拼接")
                    }, 0, EventType.AUDIO_CONCAT)
                    
                    # 确保目录存在
                    os.makedirs(self.wav_dir, exist_ok=True)
                    
                    # 拼接音频
                    combined_audio_path = os.path.join(self.wav_dir, "tts_all.wav")
                    self._concatenate_audio_files(self.audio_files, combined_audio_path)
                    
                    yield self._yield_event({
                        'status': '音频拼接完成',
                        'combinedAudioPath': combined_audio_path,
                        'audioCount': len(self.audio_files),
                        'progress': self._get_progress_data("音频拼接完成")
                    }, 0, EventType.AUDIO_CONCAT)
                    
                    # 创建ZIP压缩包
                    yield self._yield_event({
                        'status': '开始创建ZIP压缩包',
                        'progress': self._get_progress_data("ZIP打包")
                    }, 0, EventType.ZIP_PACKAGE)
                    
                    zip_path = os.path.join(AppConstants.STATIC_DIR, "tts_wav", f"{self.flow.id}.zip")
                    self._create_zip_archive(self.wav_dir, zip_path)
                    
                    # 返回ZIP下载路径
                    zip_download_path = f"/static/tts_wav/{self.flow.id}.zip"
                    yield self._yield_event({
                        'status': 'ZIP压缩包创建完成',
                        'zipPath': zip_download_path,
                        'downloadUrl': zip_download_path,
                        'progress': self._get_progress_data("ZIP打包完成")
                    }, 0, EventType.ZIP_PACKAGE)
                
                self.processed_count += 1
                # 返回结束事件
                yield self._yield_event({
                    'processedNodes': self.processed_count,
                    'status': '合成完成',
                    'audioFiles': len(self.audio_files),
                    'zipDownloadPath': f"/static/tts_wav/{self.flow.id}.zip" if self.audio_files else None,
                    'progress': self._get_progress_data("处理完成")
                }, 0, EventType.END)
                
            except Exception as e:
                yield self._yield_event({
                    'error': str(e),
                    'progress': self._get_progress_data()
                }, 1, EventType.END)
        return StreamingResponse(
            event_generator(),
            media_type="text/event-stream; charset=utf-8",
            headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
        ) 