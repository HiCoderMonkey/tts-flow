<script setup lang="ts">
import { ref, watch, defineProps, defineEmits } from 'vue'
import { ElForm, ElFormItem, ElInput, ElSelect, ElOption, ElButton, ElMessage } from 'element-plus'
import type { TTSFlow } from '@/api/tts-flow/types'
import { getVoiceList } from '@/api/ttsResource'

const props = defineProps<{ currentRow: Partial<TTSFlow> | null }>()
const emit = defineEmits(['submit'])

const formRef = ref()
const formData = ref({
  id: '',
  name: '',
  voiceId: '',
  voiceName: '',
  flow_config: {
    logicList: []
  }
})

// 音色列表
const voiceList = ref<any[]>([])
const loading = ref(false)

// 获取音色列表
const getVoiceOptions = async () => {
  try {
    loading.value = true
    const res = await getVoiceList()
    voiceList.value = (res as any).data?.list || []
  } catch (error) {
    console.error('获取音色列表失败:', error)
    ElMessage.error('获取音色列表失败')
  } finally {
    loading.value = false
  }
}

// 处理音色选择变化
const handleVoiceChange = (voiceId: string) => {
  const selectedVoice = voiceList.value.find(voice => voice.id === voiceId)
  if (selectedVoice) {
    formData.value.voiceId = selectedVoice.id
    formData.value.voiceName = selectedVoice.name
  } else {
    formData.value.voiceId = ''
    formData.value.voiceName = ''
  }
}

// 编辑时回填
watch(
  () => props.currentRow,
  (row) => {
    if (row) {
      formData.value = {
        id: row.id || '',
        name: row.name || '',
        voiceId: row.voiceId || '',
        voiceName: row.voiceName || '',
        flow_config: row.flow_config || { logicList: [] }
      }
    } else {
      formData.value = {
        id: '',
        name: '',
        voiceId: '',
        voiceName: '',
        flow_config: { logicList: [] }
      }
    }
  },
  { immediate: true, deep: true }
)

const rules = {
  name: [
    { required: true, message: '请输入工作流名称', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  voiceId: [
    { required: true, message: '请选择音色', trigger: 'change' }
  ]
}

const submit = async () => {
  await formRef.value.validate()
  emit('submit', { ...formData.value })
}

const initialForm = {
  name: '',
  voiceId: '',
  voiceName: '',
  flow_config: { logicList: [] }
}

const resetForm = () => {
  formData.value = JSON.parse(JSON.stringify(initialForm))
  formRef.value?.resetFields()
}

// 组件挂载时获取音色列表
getVoiceOptions()

defineExpose({ submit })
</script>

<template>
  <el-form ref="formRef" :model="formData" :rules="rules" label-width="150px">
    <el-form-item label="工作流名称" prop="name">
      <el-input v-model="formData.name" placeholder="请输入工作流名称" maxlength="50" show-word-limit />
    </el-form-item>
    <el-form-item label="选择音色" prop="voiceId">
      <el-select 
        v-model="formData.voiceId" 
        placeholder="请选择音色" 
        :loading="loading"
        clearable
        style="width: 100%"
        @change="handleVoiceChange"
      >
        <el-option 
          v-for="voice in voiceList" 
          :key="voice.id" 
          :label="`${voice.name} (${voice.platformName || '未知平台'})`" 
          :value="voice.id"
        >
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <span>{{ voice.name }}</span>
            <span style="color: #999; font-size: 12px;">{{ voice.platformName || '未知平台' }}</span>
          </div>
        </el-option>
      </el-select>
    </el-form-item>
  </el-form>
</template> 