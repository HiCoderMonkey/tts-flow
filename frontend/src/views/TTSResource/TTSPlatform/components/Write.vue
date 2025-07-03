<script setup lang="ts">
import { ref, watch, defineProps, defineEmits } from 'vue'
import { ElForm, ElFormItem, ElInput, ElSelect, ElOption, ElButton, ElMessage } from 'element-plus'
import type { TTSPlatform } from '@/api/ttsResource/types'

const props = defineProps<{ currentRow: Partial<TTSPlatform> | null }>()
const emit = defineEmits(['submit'])

const formRef = ref()
const formData = ref({
  id: '',
  name: '',
  type: 'volcano',
  config: {
    appid: '',
    access_token: '',
    resource_id: ''
  }
})

const typeLabelMap: Record<string, string> = {
  volcano: '火山引擎'
  // 可扩展其它类型
}

// 记录上次类型前缀，便于切换类型时替换前缀
let lastTypePrefix = ''

const handleTypeChange = (val: string) => {
  const prefix = typeLabelMap[val] ? typeLabelMap[val] + '-' : ''
  // 如果原来有前缀，去掉再加新前缀
  if (lastTypePrefix && formData.value.name.startsWith(lastTypePrefix)) {
    formData.value.name = formData.value.name.slice(lastTypePrefix.length)
  }
  // 新前缀加上
  formData.value.name = prefix + formData.value.name.replace(/^[-]+/, '')
  lastTypePrefix = prefix
}

const handleTypeClear = () => {
  // 清除类型时去掉前缀
  if (lastTypePrefix && formData.value.name.startsWith(lastTypePrefix)) {
    formData.value.name = formData.value.name.slice(lastTypePrefix.length)
  }
  lastTypePrefix = ''
}

// 编辑时回填
watch(
  () => props.currentRow,
  (row) => {
    if (row) {
      formData.value = {
        id: row.id || '',
        name: row.name || '',
        type: row.type || '',
        config: {
          appid: row.config?.appid || '',
          access_token: row.config?.access_token || '',
          resource_id: row.config?.resource_id || ''
        }
      }
      // 记录前缀
      lastTypePrefix = row.type && typeLabelMap[row.type] ? typeLabelMap[row.type] + '-' : ''
    } else {
      formData.value = {
        id: '',
        name: '',
        type: 'volcano',
        config: { appid: '', access_token: '', resource_id: '' }
      }
      lastTypePrefix = typeLabelMap['volcano'] + '-'
    }
  },
  { immediate: true, deep: true }
)

const rules = {
  name: [
    { required: true, message: '请输入平台名称', trigger: 'blur' }
  ],
  type: [
    { required: true, message: '请选择平台类型', trigger: 'change' }
  ],
  'config.appid': [
    { required: true, message: '请输入AppID', trigger: 'blur' }
  ],
  'config.access_token': [
    { required: true, message: '请输入Access Token', trigger: 'blur' }
  ],
  'config.resource_id': [
    { required: true, message: '请选择Resource Id', trigger: 'change' }
  ]
}

const submit = async () => {
  await formRef.value.validate()
  // volcano类型校验
  if (formData.value.type === 'volcano') {
    if (!formData.value.config.appid || !formData.value.config.access_token || !formData.value.config.resource_id) {
      ElMessage.error('请填写AppID、Access Token 和 Resource Id')
      return
    }
  }
  emit('submit', { ...formData.value })
}

const initialForm = {
  name: '',
  type: 'volcano',
  config: { appid: '', access_token: '', resource_id: '' }
}

const resetForm = () => {
  formData.value = JSON.parse(JSON.stringify(initialForm))
  formRef.value?.resetFields()
  lastTypePrefix = typeLabelMap['volcano'] + '-'
}

defineExpose({ submit })
</script>

<template>
  <el-form ref="formRef" :model="formData" :rules="rules" label-width="150px">
    <el-form-item label="平台类型" prop="type">
      <el-select v-model="formData.type" placeholder="请选择平台类型" clearable @change="handleTypeChange" @clear="handleTypeClear">
        <el-option label="火山引擎" value="volcano" />
        <!-- 可扩展其它平台类型 -->
      </el-select>
    </el-form-item>
    <el-form-item label="平台名称" prop="name">
      <el-input v-model="formData.name" placeholder="请输入平台名称" />
    </el-form-item>
    <template v-if="formData.type === 'volcano'">
      <el-form-item label="AppID" prop="config.appid">
        <el-input v-model="formData.config.appid" placeholder="请输入火山引擎AppID" />
      </el-form-item>
      <el-form-item label="Access Token" prop="config.access_token">
        <el-input v-model="formData.config.access_token" type="password" placeholder="请输入火山引擎Access Token" show-password />
      </el-form-item>
      <el-form-item label="Resource Id" prop="config.resource_id">
        <el-select v-model="formData.config.resource_id" placeholder="请选择Resource Id">
          <el-option label="大模型语音合成及混音" value="volc.service_type.10029" />
          <el-option label="声音复刻2.0" value="volc.megatts.default" />
        </el-select>
      </el-form-item>
    </template>
  </el-form>
</template> 