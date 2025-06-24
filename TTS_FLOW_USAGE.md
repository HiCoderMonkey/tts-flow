# TTS工作流管理功能使用说明

## 功能概述

TTS工作流管理功能提供了完整的TTS（文本转语音）工作流CRUD操作，包括创建、查询、更新和删除工作流配置。

## 后端API接口

### 1. 创建TTS工作流
- **接口**: `POST /api/v1/tts-flows`
- **权限**: 需要登录用户
- **请求体**:
```json
{
  "name": "工作流名称",
  "flow_config": {
    "steps": [
      {
        "id": "text_input",
        "type": "input",
        "config": {
          "placeholder": "请输入要转换的文本"
        }
      },
      {
        "id": "tts_engine",
        "type": "tts",
        "config": {
          "voice": "zh-CN-XiaoxiaoNeural",
          "speed": 1.0
        }
      }
    ]
  }
}
```

### 2. 获取TTS工作流列表
- **接口**: `GET /api/v1/tts-flows`
- **权限**: 需要登录用户
- **查询参数**:
  - `name`: 按名称搜索（可选）
  - `skip`: 跳过记录数（默认0）
  - `limit`: 限制记录数（默认100，最大1000）

### 3. 获取单个TTS工作流
- **接口**: `GET /api/v1/tts-flows/{flow_id}`
- **权限**: 需要登录用户

### 4. 更新TTS工作流
- **接口**: `PUT /api/v1/tts-flows/{flow_id}`
- **权限**: 需要登录用户
- **请求体**: 同创建接口，字段可选

### 5. 删除TTS工作流
- **接口**: `DELETE /api/v1/tts-flows/{flow_id}`
- **权限**: 需要登录用户

### 6. 按名称搜索TTS工作流
- **接口**: `GET /api/v1/tts-flows/search/name/{name}`
- **权限**: 需要登录用户

## 前端页面功能

### 页面路径
- 访问路径: `/function/tts-flow`
- 菜单位置: 功能 → TTS工作流管理

### 主要功能

1. **工作流列表展示**
   - 表格形式展示所有工作流
   - 显示工作流名称、配置、创建时间、更新时间
   - 支持分页和搜索

2. **搜索功能**
   - 按工作流名称搜索
   - 支持实时搜索和重置

3. **创建工作流**
   - 点击"创建工作流"按钮
   - 填写工作流名称（必填，2-50字符）
   - 编辑JSON格式的flow配置
   - 支持JSON格式验证

4. **编辑工作流**
   - 点击表格中的"编辑"按钮
   - 修改工作流名称和配置
   - 保持原有配置结构

5. **删除工作流**
   - 点击表格中的"删除"按钮
   - 确认删除操作
   - 删除后自动刷新列表

### 界面特性

1. **响应式设计**
   - 适配不同屏幕尺寸
   - 表格支持横向滚动

2. **用户体验**
   - 加载状态提示
   - 操作成功/失败消息提示
   - 删除确认对话框

3. **JSON编辑器**
   - 支持JSON格式的flow配置编辑
   - 实时格式验证
   - 语法高亮显示

## 数据模型

### TTSFlow模型
```python
class TTSFlow(Document):
    name: Indexed(str)  # 工作流名称
    flow_config: Dict[str, Any]  # flow配置（JSON）
    created_at: datetime  # 创建时间
    updated_at: datetime  # 更新时间
```

### 字段说明
- `name`: 工作流名称，唯一索引，必填
- `flow_config`: JSON格式的工作流配置，支持复杂的嵌套结构
- `created_at`: 创建时间，自动生成
- `updated_at`: 更新时间，自动更新

## 权限控制

- 所有接口都需要用户登录认证
- 使用统一的认证中间件进行权限验证
- 支持JWT token认证

## 错误处理

### 常见错误码
- `400`: 请求参数错误
- `401`: 未认证
- `404`: 资源不存在
- `409`: 资源冲突（如名称重复）
- `500`: 服务器内部错误

### 错误响应格式
```json
{
  "code": 400,
  "message": "错误描述",
  "data": null
}
```

## 部署说明

### 后端部署
1. 确保MongoDB数据库已启动
2. 安装Python依赖: `pip install -r requirements.txt`
3. 配置环境变量（参考env.example）
4. 启动服务: `python run.py`

### 前端部署
1. 安装Node.js依赖: `npm install`
2. 启动开发服务器: `npm run dev`
3. 构建生产版本: `npm run build`

## 使用示例

### 创建简单工作流
```json
{
  "name": "简单TTS工作流",
  "flow_config": {
    "steps": [
      {
        "id": "text_input",
        "type": "input",
        "config": {
          "placeholder": "请输入要转换的文本"
        }
      },
      {
        "id": "tts_engine",
        "type": "tts",
        "config": {
          "voice": "zh-CN-XiaoxiaoNeural",
          "speed": 1.0
        }
      }
    ]
  }
}
```

### 创建复杂工作流
```json
{
  "name": "高级TTS工作流",
  "flow_config": {
    "steps": [
      {
        "id": "text_preprocess",
        "type": "preprocess",
        "config": {
          "remove_punctuation": true,
          "normalize_text": true
        }
      },
      {
        "id": "text_input",
        "type": "input",
        "config": {
          "placeholder": "请输入要转换的文本",
          "max_length": 1000
        }
      },
      {
        "id": "tts_engine",
        "type": "tts",
        "config": {
          "voice": "zh-CN-XiaoxiaoNeural",
          "speed": 1.0,
          "pitch": 0,
          "volume": 100
        }
      },
      {
        "id": "audio_postprocess",
        "type": "postprocess",
        "config": {
          "format": "mp3",
          "quality": "high"
        }
      }
    ]
  }
}
```

## 注意事项

1. **数据备份**: 定期备份MongoDB数据库
2. **性能优化**: 大量数据时考虑分页和索引优化
3. **安全考虑**: 确保API接口的安全性，避免未授权访问
4. **配置验证**: 前端会对JSON配置进行格式验证，但建议后端也进行验证
5. **错误日志**: 建议记录详细的错误日志便于问题排查 