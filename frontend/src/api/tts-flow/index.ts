import request from '@/axios'
import type { TTSFlow, TTSFlowCreate, TTSFlowUpdate } from './types'

// 获取TTS工作流列表
export const getTTSFlows = (params?: { name?: string; skip?: number; limit?: number }) => {
  return request.get<IResponse<TTSFlow[]>>({ url: '/api/v1/tts-flows', params })
}

// 获取单个TTS工作流
export const getTTSFlow = (id: string) => {
  return request.get<IResponse<TTSFlow>>({ url: `/api/v1/tts-flows/${id}` })
}

// 创建TTS工作流
export const createTTSFlow = (data: TTSFlowCreate) => {
  return request.post<IResponse<TTSFlow>>({ url: '/api/v1/tts-flows', data })
}

// 更新TTS工作流
export const updateTTSFlow = (id: string, data: TTSFlowUpdate) => {
  return request.put<IResponse<TTSFlow>>({ url: `/api/v1/tts-flows/${id}`, data })
}

// 删除TTS工作流
export const deleteTTSFlow = (id: string) => {
  return request.delete<IResponse>({ url: `/api/v1/tts-flows/${id}` })
}

// 根据名称搜索TTS工作流
export const searchTTSFlowByName = (name: string) => {
  return request.get<IResponse<TTSFlow>>({ url: `/api/v1/tts-flows/search/name/${name}` })
}
