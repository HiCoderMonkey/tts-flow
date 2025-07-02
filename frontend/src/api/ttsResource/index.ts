import request from '@/axios'
// TODO: 后续引入类型定义，如：
// import type { TTSPlatform, TTSPlatformCreate, TTSPlatformUpdate, TTSVoice, TTSVoiceCreate, TTSVoiceUpdate } from './types'

// 平台管理接口
export const getPlatformList = (params?: { pageIndex?: number; pageSize?: number }) => {
  return request.get({ url: '/api/v1/tts/platforms', params })
}

export const createPlatform = (data: any) => {
  return request.post({ url: '/api/v1/tts/platforms', data })
}

export const updatePlatform = (data: any) => {
  return request.put({ url: `/api/v1/tts/platforms/${data.id}`, data })
}

export const deletePlatform = (id: string) => {
  return request.delete({ url: `/api/v1/tts/platforms/${id}` })
}

// 音色管理接口
export const getVoiceList = () => {
  return request.get({ url: '/api/v1/tts/voices' })
}

export const createVoice = (data: any) => {
  return request.post({ url: '/api/v1/tts/voices', data })
}

export const updateVoice = (data: any) => {
  return request.put({ url: `/api/v1/tts/voices/${data.id}`, data })
}

export const deleteVoice = (id: string) => {
  return request.delete({ url: `/api/v1/tts/voices/${id}` })
} 