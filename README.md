# tts-flow

## 项目简介

**tts-flow** 是一个面向文本转音频（TTS, Text-to-Speech）场景的工作流配置平台，支持灵活的音频合成流程设计与管理。平台支持多用户、权限管理、流程配置、任务调度等功能，适用于各类 TTS 业务需求。

**核心特色功能：**
- **文本块节点**：支持将长文本拆分为多个文本块（node），每个块可独立配置、合成与试听。
- **留白/特效节点**：可在流程中插入留白节点（如静音、停顿）或特效节点，实现更自然的音频拼接与表达。
- **单节点试听**：每个文本块或特效节点均可单独试听，便于调优与预览。
- **整体任务生成**：支持将整个流程配置为一次任务，自动串联所有节点进行批量音频合成。
- **音频打包导出**：支持将整体音频、各片段音频统一打包导出，便于后续分发与集成。
- **多用户与权限管理**：支持用户注册、登录、权限分级，适合团队协作。
- **流程可视化配置**：前端支持可视化拖拽、节点编辑，极大提升配置效率。

本项目采用前后端分离架构，后端负责 API、权限、数据存储与业务逻辑，前端提供现代化的管理界面。

---

## 技术栈

- **后端**：Python 3.10+、FastAPI、MongoDB、Beanie（MongoDB ORM）、Pydantic、JWT、Docker
- **前端**：Vue3、Vite、TypeScript、Element Plus、axios

---

## 主要目录结构

### 后端（backend）
```
backend/
├── app/
│   ├── api/                # 路由与接口
│   ├── core/               # 配置、异常、认证等核心代码
│   ├── models/             # ODM模型
│   ├── schemas/            # Pydantic数据校验
│   ├── services/           # 业务逻辑
│   ├── utils/              # 工具函数（如统一响应）
│   └── main.py             # FastAPI入口
├── requirements.txt
└── Dockerfile
```

### 前端（frontend）
```
frontend/
├── src/
│   ├── api/                # API接口封装
│   ├── axios/              # axios二次封装
│   ├── views/              # 页面组件
│   ├── components/         # 公共组件
│   └── App.vue, main.ts    # 入口
├── vite.config.ts
├── package.json
└── ...
```

---

## 接口规范与统一响应

- 所有后端接口返回如下结构：

```json
{
  "code": 200,                // 业务码，200为成功，其他为各种错误
  "data": {...} | null        // 成功时为数据，失败时为null或错误详情
}
```

- 失败时 `code` 为自定义业务码（如1001用户不存在、1002用户已存在等），`data` 中可包含 `msg` 字段描述错误。
- 后端所有异常自动映射为合适的 HTTP 状态码（如400、401、403、404、409、422、500等），响应体始终为统一格式。

---

## 前端请求封装与错误处理

- 所有API请求通过 `src/axios/service.ts` 封装，底层用 axios。
- 只要后端返回的 HTTP 状态码不是 200，且响应体有 `data.msg`，会自动用 `ElMessage.error(msg)` 弹出错误提示。
- 业务层无需手动处理错误提示，只需处理成功逻辑即可。

---

## 异常与错误码管理

- 后端所有异常都定义在 `app/core/exceptions.py`，包括业务异常、认证异常、参数异常等。
- 错误码集中管理，便于前后端协作和国际化。
- 详见 `backend/docs/exceptions.md`。

---

## 前后端协作建议

- 前端只需关注 `code` 和 `data`，无需关心 HTTP 状态码。
- 后端新增业务场景时，务必定义新的错误码和清晰的 `msg`。
- 前端如需特殊错误处理，可在 axios 封装中扩展。

---

## 示例

### 后端返回
```json
// 成功
{ "code": 200, "data": { "id": "xxx", "username": "test" } }

// 失败
{ "code": 1002, "data": { "msg": "用户名已存在" } }
```

### 前端处理
```typescript
try {
  await registerApi(form)
  // 注册成功逻辑
} catch (err) {
  // 不用再弹窗，axios已自动处理
}
```

---

## 适用场景

- TTS文本转音频流程配置、任务管理、用户权限、API集成等。
- 支持文本块拆分、留白特效、节点试听、批量合成、音频打包导出等复杂TTS工作流。
- 可扩展为多种文本处理/音频处理的工作流平台。

---

如需详细接口文档、错误码表或二次开发指导，请查阅 `backend/docs/exceptions.md` 或联系项目维护者。

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.
