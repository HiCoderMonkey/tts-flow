export interface TTSFlow {
  id: string
  name: string
  voiceId?: string
  voiceName?: string
  flow_config: any
  created_at: string
  updated_at: string
}

export interface TTSFlowCreate {
  name: string
  voiceId?: string
  voiceName?: string
  flow_config: any
}

export interface TTSFlowUpdate {
  name?: string
  voiceId?: string
  voiceName?: string
  flow_config?: any
}
