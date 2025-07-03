<script setup lang="ts">
import { ref, watch, defineProps, defineEmits, onMounted } from 'vue'
import { ElForm, ElFormItem, ElInput, ElSelect, ElOption, ElButton, ElMessage } from 'element-plus'
import type { TTSVoice, TTSPlatform } from '@/api/ttsResource/types'
import { getPlatformList } from '@/api/ttsResource'

const props = defineProps<{ currentRow: Partial<TTSVoice> | null }>()
const emit = defineEmits(['submit'])

const formRef = ref()
const formData = ref({
  id: '',
  name: '',
  platformId: '',
  roleId: '',
  extensionJson: '',
})

const platformList = ref<TTSPlatform[]>([])

// 记录上次平台前缀，便于切换平台时替换前缀
let lastPlatformPrefix = ''

const handlePlatformChange = (val: string) => {
  const selectedPlatform = platformList.value.find(p => p.id === val)
  const prefix = selectedPlatform ? selectedPlatform.name + '-' : ''
  // 如果原来有前缀，去掉再加新前缀
  if (lastPlatformPrefix && formData.value.name.startsWith(lastPlatformPrefix)) {
    formData.value.name = formData.value.name.slice(lastPlatformPrefix.length)
  }
  // 新前缀加上
  formData.value.name = prefix + formData.value.name.replace(/^[-]+/, '')
  lastPlatformPrefix = prefix
}

const handlePlatformClear = () => {
  // 清除平台时去掉前缀
  if (lastPlatformPrefix && formData.value.name.startsWith(lastPlatformPrefix)) {
    formData.value.name = formData.value.name.slice(lastPlatformPrefix.length)
  }
  lastPlatformPrefix = ''
}

const loadPlatformList = async () => {
  try {
    const res = await getPlatformList()
    platformList.value = res.data?.list || res.data || []
  } catch (e) {
    ElMessage.error('加载平台列表失败')
  }
}

onMounted(() => {
  loadPlatformList()
})

// 编辑时回填
watch(
  () => props.currentRow,
  (row) => {
    if (row) {
      formData.value = {
        id: row.id || '',
        name: row.name || '',
        platformId: (row as any).platformId || '',
        roleId: (row as any).roleId || '',
        extensionJson: (row as any).extensionJson || '',
      }
      // 回填角色ID（如果 extensionJson 里有 roleId 也同步到表单）
      try {
        const ext = JSON.parse(formData.value.extensionJson || '{}')
        if (ext.roleId) formData.value.roleId = ext.roleId
      } catch {}
      // 记录前缀
      const selectedPlatform = platformList.value.find(p => p.id === formData.value.platformId)
      lastPlatformPrefix = selectedPlatform ? selectedPlatform.name + '-' : ''
    } else {
      formData.value = {
        id: '',
        name: '',
        platformId: '',
        roleId: '',
        extensionJson: '',
      }
      lastPlatformPrefix = ''
    }
  },
  { immediate: true, deep: true }
)

const rules = {
  name: [
    { required: true, message: '请输入音色名称', trigger: 'blur' }
  ],
  platformId: [
    { required: true, message: '请选择TTS平台', trigger: 'change' }
  ],
  roleId: [
    { required: true, message: '请输入角色ID', trigger: 'blur' }
  ]
}

const submit = async () => {
  await formRef.value.validate()
  // 合并角色ID到 extensionJson
  const ext = formData.value.extensionJson ? JSON.parse(formData.value.extensionJson) : {}
  ext.roleId = formData.value.roleId
  emit('submit', {
    id: formData.value.id,
    name: formData.value.name,
    platformId: formData.value.platformId,
    roleId: formData.value.roleId,
    extensionJson: JSON.stringify(ext)
  })
}

defineExpose({ submit })
</script>

<template>
  <el-form ref="formRef" :model="formData" :rules="rules" label-width="150px">
    <el-form-item label="TTS平台" prop="platformId">
      <el-select v-model="formData.platformId" placeholder="请选择TTS平台" clearable @change="handlePlatformChange" @clear="handlePlatformClear">
        <el-option v-for="platform in platformList" :key="platform.id" :label="platform.name" :value="platform.id" />
      </el-select>
    </el-form-item>
    <el-form-item label="音色名称" prop="name">
      <el-input v-model="formData.name" placeholder="请输入音色名称" />
    </el-form-item>
    <el-form-item label="角色ID" prop="roleId">
      <el-input v-model="formData.roleId" placeholder="请输入角色ID" />
    </el-form-item>
  </el-form>
</template> 