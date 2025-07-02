// TTS平台类型
export interface TTSPlatform {
  id: string
  name: string
  type: string
  status: boolean
  description?: string
  created_at: string
  updated_at: string
  config?: Record<string, any>
}

// 新建TTS平台类型
export interface TTSPlatformCreate {
  name: string
  description?: string
}

// 更新TTS平台类型
export interface TTSPlatformUpdate {
  name?: string
  description?: string
}

// TTS音色类型
export interface TTSVoice {
  id: string
  name: string
  platform_id: string // 关联平台id
  language: string
  gender: string
  description?: string
  created_at: string
  updated_at: string
}

// 新建TTS音色类型
export interface TTSVoiceCreate {
  name: string
  platform_id: string
  language: string
  gender: string
  description?: string
}

// 更新TTS音色类型
export interface TTSVoiceUpdate {
  name?: string
  platform_id?: string
  language?: string
  gender?: string
  description?: string
} 