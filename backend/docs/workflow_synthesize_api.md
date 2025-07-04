# 工作流音频打包接口

## 接口概述

工作流音频打包接口用于将整个 TTS 工作流中的所有节点音频进行合成，支持流式响应，实时返回处理状态。最终会将所有音频拼接成一个完整文件，并打包成 ZIP 文件供下载。

## 接口信息

- **URL**: `GET /api/v1/tts-flows/{flow_id}/synthesize-all`
- **方法**: GET
- **参数**: 
  - `flow_id`: 工作流ID (路径参数)
- **响应**: 流式响应 (Server-Sent Events)

## 请求示例

```bash
curl -X GET "http://localhost:8000/api/v1/tts-flows/68590dd30889152680a21879/synthesize-all" \
  -H "Authorization: Bearer your_token_here"
```

## 响应格式

响应为 Server-Sent Events 格式，每个事件包含以下字段：

```json
{
  "data": {},      // 具体数据内容
  "code": 0,       // 状态码：0成功，其他失败
  "type": "start"  // 事件类型（英文）
}
```

### 事件类型常量

| 常量 | 值 | 说明 |
|------|----|----|
| `EventType.START` | `"start"` | 开始事件 |
| `EventType.NODE` | `"node"` | 节点事件 |
| `EventType.NODE_TASK` | `"node_task"` | 节点内生成任务 |
| `EventType.AUDIO_CONCAT` | `"audio_concat"` | 音频拼接 |
| `EventType.ZIP_PACKAGE` | `"zip_package"` | ZIP打包 |
| `EventType.END` | `"end"` | 结束事件 |

### 进度信息格式

每个事件都包含进度信息：

```json
{
  "progress": {
    "processed": 2,        // 已处理节点数
    "total": 5,           // 总节点数
    "percentage": 40.0,   // 完成百分比
    "currentNode": "TTS文本分段-01"  // 当前处理节点名称
  }
}
```

### 事件类型说明

#### 1. 开始事件 (start)
```json
{
  "data": {
    "totalNodes": 5,
    "progress": {
      "processed": 0,
      "total": 5,
      "percentage": 0.0,
      "currentNode": ""
    }
  },
  "code": 0,
  "type": "start"
}
```

#### 2. 节点事件 (node)
```json
{
  "data": {
    "nodeId": "logic_14agv6mk9gsg000",
    "nodeName": "TTS文本分段-01",
    "nodeType": "ttsTextChunk",
    "text": "这是最好的时代，这是最美的时代。",
    "audioUrl": "/tts_wav/68590dd30889152680a21879/logic_14agv6mk9gsg000.wav",
    "progress": {
      "processed": 1,
      "total": 5,
      "percentage": 20.0,
      "currentNode": "TTS文本分段-01"
    }
  },
  "code": 0,
  "type": "node"
}
```

#### 3. 节点内生成任务事件 (node_task)
```json
{
  "data": {
    "status": "开始生成音频",
    "progress": {
      "processed": 1,
      "total": 5,
      "percentage": 20.0,
      "currentNode": "TTS文本分段-01"
    }
  },
  "code": 0,
  "type": "node_task"
}
```

#### 4. 音频拼接事件 (audio_concat)
```json
{
  "data": {
    "status": "开始拼接音频文件",
    "progress": {
      "processed": 5,
      "total": 5,
      "percentage": 100.0,
      "currentNode": "音频拼接"
    }
  },
  "code": 0,
  "type": "audio_concat"
}
```

```json
{
  "data": {
    "status": "音频拼接完成",
    "combinedAudioPath": "/path/to/tts_all.wav",
    "audioCount": 3,
    "progress": {
      "processed": 5,
      "total": 5,
      "percentage": 100.0,
      "currentNode": "音频拼接完成"
    }
  },
  "code": 0,
  "type": "audio_concat"
}
```

#### 5. ZIP打包事件 (zip_package)
```json
{
  "data": {
    "status": "开始创建ZIP压缩包",
    "progress": {
      "processed": 5,
      "total": 5,
      "percentage": 100.0,
      "currentNode": "ZIP打包"
    }
  },
  "code": 0,
  "type": "zip_package"
}
```

```json
{
  "data": {
    "status": "ZIP压缩包创建完成",
    "zipPath": "/static/tts_wav/68590dd30889152680a21879.zip",
    "downloadUrl": "/static/tts_wav/68590dd30889152680a21879.zip",
    "progress": {
      "processed": 5,
      "total": 5,
      "percentage": 100.0,
      "currentNode": "ZIP打包完成"
    }
  },
  "code": 0,
  "type": "zip_package"
}
```

#### 6. 结束事件 (end)
```json
{
  "data": {
    "processedNodes": 5,
    "status": "合成完成",
    "audioFiles": 3,
    "zipDownloadPath": "/static/tts_wav/68590dd30889152680a21879.zip",
    "progress": {
      "processed": 5,
      "total": 5,
      "percentage": 100.0,
      "currentNode": "处理完成"
    }
  },
  "code": 0,
  "type": "end"
}
```

## 支持的节点类型

### 1. ttsTextChunk (TTS文本节点)
- 读取 `properties.nodeContentData.text` 进行语音合成
- 如果 `properties.nodeContentData.audioUrl` 已有值且文件存在，直接使用
- 否则调用 TTS 服务生成新音频

### 2. spaceVoid (留白节点)
- 读取 `properties.nodeContentData.duration` 作为留白时长（秒）
- 默认 3 秒
- 生成对应时长的空白音频

## 处理流程

1. **解析工作流配置**: 将 `flow_config.logicList` 解析为节点链表
2. **加载音色和平台**: 根据 `voiceId` 加载对应的音色和平台配置
3. **找到开始节点**: 定位 `event-node` 类型的开始节点
4. **顺序处理节点**: 按照链表顺序处理每个节点
5. **生成音频文件**: 将音频文件保存到 `static/tts_wav/{flow_id}/` 目录
6. **拼接音频文件**: 将所有节点的音频按顺序拼接成 `tts_all.wav`
7. **创建ZIP压缩包**: 将整个工作流目录打包成 `{flow_id}.zip`

## 文件结构

处理完成后，文件结构如下：

```
static/tts_wav/
├── {flow_id}/
│   ├── logic_14agv6mk9gsg000.wav    # 节点1音频
│   ├── logic_65o91hmnuac0000.wav    # 节点2音频（留白）
│   ├── logic_2jfjfzo3ksc0000.wav    # 节点3音频
│   └── tts_all.wav                  # 拼接后的完整音频
└── {flow_id}.zip                    # 压缩包（包含所有文件）
```

## 音频拼接说明

- 所有音频文件必须具有相同的采样率、声道数和采样宽度
- 按节点处理顺序进行拼接
- 拼接后的文件保存为 `tts_all.wav`
- 如果音频参数不匹配，会跳过该文件并输出警告

## 错误处理

### 常见错误

1. **工作流不存在**
```json
{
  "data": {
    "error": "工作流不存在",
    "progress": {
      "processed": 0,
      "total": 0,
      "percentage": 0.0,
      "currentNode": ""
    }
  },
  "code": 1,
  "type": "end"
}
```

2. **音色未配置**
```json
{
  "data": {
    "error": "工作流未配置音色",
    "progress": {
      "processed": 0,
      "total": 0,
      "percentage": 0.0,
      "currentNode": ""
    }
  },
  "code": 1,
  "type": "end"
}
```

## 前端使用示例

```javascript
// 使用 EventSource 接收流式响应
const eventSource = new EventSource('/api/v1/tts-flows/68590dd30889152680a21879/synthesize-all');

eventSource.onmessage = function(event) {
  const data = JSON.parse(event.data);
  
  // 更新进度条
  if (data.data.progress) {
    updateProgressBar(data.data.progress);
  }
  
  switch(data.type) {
    case 'start':
      console.log(`开始处理，共 ${data.data.totalNodes} 个节点`);
      break;
      
    case 'node':
      console.log(`处理节点: ${data.data.nodeName}`);
      break;
      
    case 'node_task':
      console.log(`生成任务: ${data.data.status}`);
      break;
      
    case 'audio_concat':
      if (data.data.status === '音频拼接完成') {
        console.log(`音频拼接完成，共 ${data.data.audioCount} 个音频文件`);
      }
      break;
      
    case 'zip_package':
      if (data.data.status === 'ZIP压缩包创建完成') {
        console.log(`ZIP打包完成，下载地址: ${data.data.downloadUrl}`);
        // 可以在这里提供下载链接
        const downloadLink = document.createElement('a');
        downloadLink.href = data.data.downloadUrl;
        downloadLink.download = `${flowId}.zip`;
        downloadLink.click();
      }
      break;
      
    case 'end':
      console.log(`处理完成，共处理 ${data.data.processedNodes} 个节点`);
      console.log(`ZIP下载路径: ${data.data.zipDownloadPath}`);
      eventSource.close();
      break;
  }
};

// 更新进度条函数
function updateProgressBar(progress) {
  const progressBar = document.getElementById('progress-bar');
  const progressText = document.getElementById('progress-text');
  
  if (progressBar) {
    progressBar.style.width = `${progress.percentage}%`;
  }
  
  if (progressText) {
    progressText.textContent = `${progress.currentNode} (${progress.processed}/${progress.total})`;
  }
}

eventSource.onerror = function(error) {
  console.error('连接错误:', error);
  eventSource.close();
};
```

## 注意事项

1. 接口需要认证，请在请求头中包含有效的 Authorization token
2. 音频文件会保存在 `static/tts_wav/{flow_id}/` 目录下
3. 如果节点已有音频文件且文件存在，会直接使用，不会重新生成
4. 留白节点会生成指定时长的空白音频文件
5. 处理过程中会实时返回状态，前端可以根据状态更新 UI
6. 最终会生成拼接后的完整音频文件 `tts_all.wav`
7. 整个工作流目录会打包成 ZIP 文件供下载
8. 音频拼接要求所有文件具有相同的音频参数（采样率、声道数等）
9. 所有事件都包含进度信息，便于前端显示处理进度
10. 事件类型使用英文常量，便于国际化处理 