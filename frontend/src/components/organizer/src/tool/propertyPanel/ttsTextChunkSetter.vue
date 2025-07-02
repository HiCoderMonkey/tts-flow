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
import { ref, watch } from 'vue'
import { ElInput, ElButton, ElForm, ElFormItem, ElMessage } from 'element-plus'

interface TtsTextChunkData {
  text: string
  audioUrl?: string
}

const props = defineProps<{ modelValue: TtsTextChunkData }>()
const emit = defineEmits(['update:modelValue'])

const localValue = ref<TtsTextChunkData>({ ...props.modelValue })
const loading = ref(false)

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
    // TODO: 替换为实际的音频生成API
    // 这里模拟生成音频
    await new Promise((resolve) => setTimeout(resolve, 1000))
    // 假设生成后返回音频URL
    localValue.value.audioUrl = 'https://www.w3schools.com/html/horse.mp3'
    ElMessage.success('音频生成成功')
  } catch (e) {
    ElMessage.error('音频生成失败')
  } finally {
    loading.value = false
  }
}

function handlePlayAudio() {
  if (localValue.value.audioUrl) {
    const audio = new Audio(localValue.value.audioUrl)
    audio.play()
  }
}
</script>

<style scoped lang="less">
.tts-chunk-setter {
  margin-top: 10px;
}
</style> 