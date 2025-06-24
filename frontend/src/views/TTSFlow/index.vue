<script lang="ts" setup>
import { ContentWrap } from '@/components/ContentWrap'
import { useI18n } from '@/hooks/web/useI18n'
import {
  ElTable,
  ElTableColumn,
  ElButton,
  ElInput,
  ElDialog,
  ElForm,
  ElFormItem,
  ElMessage,
  ElMessageBox
} from 'element-plus'
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Dialog } from '@/components/Dialog'
import { getTTSFlows, createTTSFlow, updateTTSFlow, deleteTTSFlow } from '@/api/tts-flow'
import type { TTSFlow, TTSFlowCreate } from '@/api/tts-flow/types'

const { t } = useI18n()
const router = useRouter()

// 响应式数据
const tableData = ref<TTSFlow[]>([])
const loading = ref(false)
const searchName = ref('')
const dialogVisible = ref(false)
const dialogTitle = ref('')
const isEdit = ref(false)
const currentId = ref('')

// 表单数据
const formData = reactive<TTSFlowCreate>({
  name: '',
  flow_config: {
    logicList: [
      {
        id: 'text_input',
        type: 'input',
        name: '文本输入',
        config: {
          placeholder: '请输入要转换的文本'
        }
      },
      {
        id: 'tts_engine',
        type: 'tts',
        name: 'TTS引擎',
        config: {
          voice: 'zh-CN-XiaoxiaoNeural',
          speed: 1.0
        }
      }
    ]
  }
})

// 表单规则
const formRules = {
  name: [
    { required: true, message: '请输入工作流名称', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ]
}

const formRef = ref()

// 获取工作流列表
const getTTSFlowsList = async () => {
  loading.value = true
  try {
    const params: any = {}
    if (searchName.value) {
      params.name = searchName.value
    }
    const res = await getTTSFlows(params)
    tableData.value = (res as any).data || []
  } catch (error) {
    console.error('获取工作流列表失败:', error)
    ElMessage.error('获取工作流列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  getTTSFlowsList()
}

// 重置搜索
const resetSearch = () => {
  searchName.value = ''
  getTTSFlowsList()
}

// 打开创建对话框
const openCreateDialog = () => {
  dialogTitle.value = '创建工作流'
  isEdit.value = false
  currentId.value = ''
  resetForm()
  dialogVisible.value = true
}

// 打开编辑对话框
const openEditDialog = (row: TTSFlow) => {
  dialogTitle.value = '编辑工作流'
  isEdit.value = true
  currentId.value = row.id
  formData.name = row.name
  formData.flow_config = JSON.parse(JSON.stringify(row.flow_config))
  dialogVisible.value = true
}

// 重置表单
const resetForm = () => {
  formData.name = ''
  formData.flow_config = {
    logicList: [
      {
        id: 'text_input',
        type: 'input',
        name: '文本输入',
        config: {
          placeholder: '请输入要转换的文本'
        }
      },
      {
        id: 'tts_engine',
        type: 'tts',
        name: 'TTS引擎',
        config: {
          voice: 'zh-CN-XiaoxiaoNeural',
          speed: 1.0
        }
      }
    ]
  }
  formRef.value?.resetFields()
}

// 提交表单
const submitForm = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()

    if (isEdit.value) {
      // 编辑
      await updateTTSFlow(currentId.value, formData)
      ElMessage.success('更新成功')
    } else {
      // 创建
      await createTTSFlow(formData)
      ElMessage.success('创建成功')
    }

    dialogVisible.value = false
    getTTSFlowsList()
  } catch (error) {
    console.error('提交失败:', error)
    ElMessage.error(isEdit.value ? '更新失败' : '创建失败')
  }
}

// 删除工作流
const handleDelete = async (row: TTSFlow) => {
  try {
    await ElMessageBox.confirm(`确定要删除工作流 "${row.name}" 吗？`, '确认删除', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    await deleteTTSFlow(row.id)
    ElMessage.success('删除成功')
    getTTSFlowsList()
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
      ElMessage.error('删除失败')
    }
  }
}

// 格式化时间
const formatTime = (time: string) => {
  return new Date(time).toLocaleString('zh-CN')
}

// 格式化配置
const formatConfig = (config: any) => {
  try {
    return JSON.stringify(config, null, 2)
  } catch {
    return '配置格式错误'
  }
}

// 跳转到画布配置页面
const goToCanvas = (row: TTSFlow) => {
  router.push(`/tts-flow/canvas/${row.id}`)
}

// 获取节点数量
const getNodeCount = (config: any) => {
  try {
    if (config && config.logicList) {
      return config.logicList.length
    }
    return 0
  } catch {
    return 0
  }
}

// 页面加载时获取数据
onMounted(() => {
  getTTSFlowsList()
})
</script>

<template>
  <ContentWrap title="TTS工作流管理">
    <!-- 搜索区域 -->
    <div class="mb-4 flex items-center gap-4">
      <ElInput
        v-model="searchName"
        placeholder="请输入工作流名称搜索"
        style="width: 300px"
        clearable
        @keyup.enter="handleSearch"
      />
      <ElButton type="primary" @click="handleSearch">搜索</ElButton>
      <ElButton @click="resetSearch">重置</ElButton>
      <ElButton type="success" @click="openCreateDialog">创建工作流</ElButton>
    </div>

    <!-- 表格 -->
    <ElTable :data="tableData" :loading="loading" style="width: 100%" border>
      <ElTableColumn prop="name" label="工作流名称" min-width="150" />
      <ElTableColumn prop="flow_config" label="Flow配置" min-width="150">
        <template #default="{ row }">
          <div class="text-sm text-gray-600"> {{ getNodeCount(row.flow_config) }} 个节点 </div>
        </template>
      </ElTableColumn>
      <ElTableColumn prop="created_at" label="创建时间" min-width="150">
        <template #default="{ row }">
          {{ formatTime(row.created_at) }}
        </template>
      </ElTableColumn>
      <ElTableColumn prop="updated_at" label="更新时间" min-width="150">
        <template #default="{ row }">
          {{ formatTime(row.updated_at) }}
        </template>
      </ElTableColumn>
      <ElTableColumn label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <ElButton type="primary" size="small" @click="openEditDialog(row)"> 编辑 </ElButton>
          <ElButton type="danger" size="small" @click="handleDelete(row)"> 删除 </ElButton>
          <ElButton type="info" size="small" @click="goToCanvas(row)"> 配置 </ElButton>
        </template>
      </ElTableColumn>
    </ElTable>

    <!-- 创建/编辑对话框 -->
    <Dialog v-model="dialogVisible" :title="dialogTitle" width="800px" :max-height="600">
      <ElForm ref="formRef" :model="formData" :rules="formRules" label-width="100px">
        <ElFormItem label="工作流名称" prop="name">
          <ElInput
            v-model="formData.name"
            placeholder="请输入工作流名称"
            maxlength="50"
            show-word-limit
          />
        </ElFormItem>
      </ElForm>

      <template #footer>
        <ElButton @click="dialogVisible = false">取消</ElButton>
        <ElButton type="primary" @click="submitForm">
          {{ isEdit ? '更新' : '创建' }}
        </ElButton>
      </template>
    </Dialog>
  </ContentWrap>
</template>

<style scoped>
pre {
  white-space: pre-wrap;
  word-wrap: break-word;
}
</style>
