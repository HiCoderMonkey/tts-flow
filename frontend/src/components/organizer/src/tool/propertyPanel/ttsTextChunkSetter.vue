<template>
  <div class="tts-chunk-setter">
    <el-form label-width="80px">
      <el-form-item label="文本内容">
        <el-input
          type="textarea"
          v-model="localValue.text"
          :rows="6"
          placeholder="请输入要合成的文本"
        />
      </el-form-item>
      <el-form-item label="音频路径" required>
        <el-input v-model="localValue.audioUrl" readonly placeholder="请先生成音频" />
      </el-form-item>
      <el-form-item v-if="localValue.audioUrl">
        <audio :src="audioUrlWithTs" controls style="width: 100%"></audio>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleGenerateAudio" :loading="loading">
          生成音频
        </el-button>
        <el-button @click="handlePlayAudio" :disabled="!localValue.audioUrl">
          试听播放
        </el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import { ElInput, ElButton, ElForm, ElFormItem, ElMessage } from 'element-plus'
import PCMPlayer from 'pcm-player'

interface TtsTextChunkData {
  text: string
  audioUrl?: string
}

const PATH_URL = import.meta.env.VITE_API_BASE_PATH

const static_path = PATH_URL + '/static'

const props = defineProps<{ modelValue: TtsTextChunkData; data_id: string; currentModel: any; node_name: string }>()
const emit = defineEmits(['update:modelValue'])

const localValue = ref<TtsTextChunkData>({ ...props.modelValue })
const loading = ref(false)

// 计算带时间戳的音频播放地址，避免缓存
const audioUrlWithTs = computed(() => {
  if (!localValue.value.audioUrl) return ''
  return static_path + localValue.value.audioUrl + '?t=' + Date.now()
})

// watch(
//   () => props.modelValue,
//   (val) => {
//     localValue.value = { ...val }
//   },
//   { immediate: true, deep: true }
// )

watch(
  () => localValue.value,
  (val) => {
    emit('update:modelValue', val)
  },
  { deep: true }
)

async function handleGenerateAudio() {
  if (!localValue.value.text?.trim()) {
    ElMessage.warning('请输入文本内容')
    return
  }
  loading.value = true
  try {
    // 1. 创建 pcm-player 实例
    const player = new PCMPlayer({
      inputCodec: 'Int16',
      channels: 1,
      sampleRate: 24000,
      flushTime: 200,
      fftSize: 2048
    })
    // 2. 发起 EventSource/SSE 请求
    const response = await fetch(PATH_URL + '/api/v1/tts-synthesize/synthesize', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        flow_id: props.data_id,
        text: localValue.value.text,
        node_id: props.currentModel.id,
        node_name: props.node_name
      })
    })
    if (!response.body) throw new Error('No stream body')

    const reader = response.body.getReader()
    let wavPath = ''
    let decoder = new TextDecoder('utf-8')
    let buffer = ''
    while (true) {
      const { value, done } = await reader.read()
      if (done) break
      buffer += decoder.decode(value, { stream: true })
      let lines = buffer.split('\n\n')
      buffer = lines.pop() || ''
      for (const line of lines) {
        if (!line.startsWith('data: ')) continue
        const jsonStr = line.replace('data: ', '').trim()
        if (!jsonStr) continue
        const data = JSON.parse(jsonStr)
        if (data.type === 'pcm' && data.data && !data.end) {
          // 播放pcm
          const pcmUint8 = Uint8Array.from(atob(data.data), c => c.charCodeAt(0))
          player.feed(pcmUint8.buffer)
        }
        if (data.type === 'wav_path' && data.end) {
          wavPath = data.data
        }
      }
    }
    if (wavPath) {
      localValue.value.audioUrl = '/' + wavPath.replace(/^static[\\/]+/, '')
      ElMessage.success('音频生成成功')
    } else {
      ElMessage.error('音频生成失败')
    }
  } catch (e) {
    ElMessage.error('音频生成失败')
  } finally {
    loading.value = false
  }
}

function handlePlayAudio() {
  if (localValue.value.audioUrl) {
    const audio = new Audio(audioUrlWithTs.value)
    audio.play()
  }
}
</script>

<style scoped lang="less">
.tts-chunk-setter {
  margin-top: 10px;
}
</style> 