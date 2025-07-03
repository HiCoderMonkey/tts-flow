<script lang="ts" setup>
import { ContentWrap } from '@/components/ContentWrap'
import { useI18n } from '@/hooks/web/useI18n'
import {
  ElTable,
  ElTableColumn,
  ElButton,
  ElInput,
  ElMessage,
  ElMessageBox,
  ElPagination
} from 'element-plus'
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Dialog } from '@/components/Dialog'
import { getTTSFlows, createTTSFlow, updateTTSFlow, deleteTTSFlow } from '@/api/tts-flow'
import type { TTSFlow, TTSFlowCreate } from '@/api/tts-flow/types'
import Write from './components/Write.vue'
import Detail from './components/Detail.vue'

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
const total = ref(0)
const pageIndex = ref(1)
const pageSize = ref(10)
const actionType = ref('') // 'create', 'edit', 'detail'

// 当前行数据
const currentRow = ref<TTSFlow | null>(null)

// 表单引用
const writeRef = ref()
const saveLoading = ref(false)



// 获取工作流列表
const getTTSFlowsList = async () => {
  loading.value = true
  try {
    const params: any = {
      pageIndex: pageIndex.value,
      pageSize: pageSize.value
    }
    if (searchName.value) {
      params.name = searchName.value
    }
    const res = await getTTSFlows(params)
    tableData.value = (res as any).data?.list || []
    total.value = (res as any).data?.total || 0
  } catch (error) {
    console.error('获取工作流列表失败:', error)
    ElMessage.error('获取工作流列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  pageIndex.value = 1
  getTTSFlowsList()
}

// 重置搜索
const resetSearch = () => {
  searchName.value = ''
  pageIndex.value = 1
  getTTSFlowsList()
}

// 打开创建对话框
const openCreateDialog = () => {
  dialogTitle.value = '创建工作流'
  actionType.value = 'create'
  isEdit.value = false
  currentId.value = ''
  currentRow.value = null
  dialogVisible.value = true
}

// 打开编辑对话框
const openEditDialog = (row: TTSFlow) => {
  dialogTitle.value = '编辑工作流'
  actionType.value = 'edit'
  isEdit.value = true
  currentId.value = row.id
  currentRow.value = row
  dialogVisible.value = true
}

// 打开详情对话框
const openDetailDialog = (row: TTSFlow) => {
  dialogTitle.value = '工作流详情'
  actionType.value = 'detail'
  currentRow.value = row
  dialogVisible.value = true
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

// 处理分页变化
const handlePageChange = (val: number) => {
  pageIndex.value = val
  getTTSFlowsList()
}

const handleSizeChange = (val: number) => {
  pageSize.value = val
  pageIndex.value = 1
  getTTSFlowsList()
}

// 提交表单
const handleSubmit = async (formData: any) => {
  try {
    saveLoading.value = true
    
    // 去掉 flow_config 参数
    const { flow_config, ...submitData } = formData
    
    if (actionType.value === 'edit') {
      // 编辑
      await updateTTSFlow(currentId.value, submitData)
      ElMessage.success('更新成功')
    } else {
      // 创建
      await createTTSFlow(submitData)
      ElMessage.success('创建成功')
    }

    dialogVisible.value = false
    getTTSFlowsList()
  } catch (error) {
    console.error('提交失败:', error)
    ElMessage.error(actionType.value === 'edit' ? '更新失败' : '创建失败')
  } finally {
    saveLoading.value = false
  }
}

// 保存操作
const save = async () => {
  if (writeRef.value) {
    const formData = await writeRef.value.submit()
    if (formData) {
      await handleSubmit(formData)
    }
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
      <ElTableColumn prop="voiceName" label="音色名称" min-width="150">
        <template #default="{ row }">
          <span v-if="row.voiceName">{{ row.voiceName }}</span>
          <span v-else style="color: #999;">未选择音色</span>
        </template>
      </ElTableColumn>
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
      <ElTableColumn label="操作" width="280" fixed="right">
        <template #default="{ row }">
          <ElButton type="primary" size="small" @click="openEditDialog(row)"> 编辑 </ElButton>
          <ElButton type="info" size="small" @click="openDetailDialog(row)"> 详情 </ElButton>
          <ElButton type="danger" size="small" @click="handleDelete(row)"> 删除 </ElButton>
          <ElButton type="warning" size="small" @click="goToCanvas(row)"> 配置 </ElButton>
        </template>
      </ElTableColumn>
    </ElTable>
    <el-pagination
      class="mt-4"
      background
      layout="total, sizes, prev, pager, next, jumper"
      :total="total"
      v-model:current-page="pageIndex"
      v-model:page-size="pageSize"
      :page-sizes="[10, 20, 50, 100]"
      @current-change="handlePageChange"
      @size-change="handleSizeChange"
    />

    <!-- 创建/编辑/详情对话框 -->
    <Dialog v-model="dialogVisible" :title="dialogTitle" width="800px">
      <Write
        v-if="actionType === 'create' || actionType === 'edit'"
        ref="writeRef"
        :current-row="currentRow"
        @submit="handleSubmit"
      />
      <Detail
        v-if="actionType === 'detail'"
        :current-row="currentRow"
        :detail-schema="[]"
      />

      <template #footer>
        <ElButton @click="dialogVisible = false">关闭</ElButton>
        <ElButton 
          v-if="actionType === 'create' || actionType === 'edit'"
          type="primary" 
          :loading="saveLoading"
          @click="save"
        >
          {{ actionType === 'edit' ? '更新' : '创建' }}
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
