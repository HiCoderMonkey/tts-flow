<template>
  <div class="flow-canvas-container">
    <div class="canvas-header">
      <div class="header-left">
        <el-button @click="goBack" icon="ArrowLeft">返回列表</el-button>
        <h2>{{ flowName }} - 流程配置</h2>
      </div>
      <div class="header-right">
        <el-button type="success" @click="startPackage" :loading="packaging" :disabled="packaging">
          <el-icon><Download /></el-icon>
          打包下载
        </el-button>
        <el-button type="primary" @click="saveFlow">保存配置</el-button>
      </div>
    </div>

    <div class="canvas-content">
      <div v-if="loading" class="loading-container">
        <div class="loading-spinner"></div>
        <p>加载中...</p>
      </div>
      <logic-panel
        v-else
        ref="logicPanelRef"
        class="logic-panel-wrapper"
        :context="context"
        :info="info"
        :data_id="flowId"
        @update-logic-list="context.logicList = $event"
      />
    </div>

    <!-- 打包进度对话框 -->
    <el-dialog
      v-model="packageDialogVisible"
      title="音频打包进度"
      width="500px"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :show-close="packageCompleted"
    >
      <div class="package-progress">
        <!-- 总体进度 -->
        <div class="progress-section">
          <div class="progress-header">
            <span class="progress-title">总体进度</span>
            <span class="progress-percentage">{{ overallProgress.percentage }}%</span>
          </div>
          <el-progress 
            :percentage="overallProgress.percentage" 
            :status="packageCompleted ? 'success' : ''"
            :stroke-width="8"
          />
          <div class="progress-info">
            {{ overallProgress.currentNode }} ({{ overallProgress.processed }}/{{ overallProgress.total }})
          </div>
        </div>

        <!-- 当前状态 -->
        <div class="current-status">
          <div class="status-header">
            <span class="status-title">当前状态</span>
          </div>
          <div class="status-content">
            <el-tag 
              :type="getStatusType(currentStatus.type)" 
              size="large"
              class="status-tag"
            >
              {{ getStatusText(currentStatus.type) }}
            </el-tag>
            <div class="status-message">{{ currentStatus.message }}</div>
          </div>
        </div>

        <!-- 处理日志 -->
        <div class="process-log">
          <div class="log-header">
            <span class="log-title">处理日志</span>
            <el-button size="small" @click="clearLog">清空</el-button>
          </div>
          <div class="log-content">
            <div 
              v-for="(log, index) in processLogs" 
              :key="index" 
              class="log-item"
              :class="getLogClass(log.type)"
            >
              <span class="log-time">{{ log.time }}</span>
              <span class="log-message">{{ log.message }}</span>
            </div>
          </div>
        </div>
      </div>

      <template #footer>
        <div class="dialog-footer">
          <el-button 
            v-if="packageCompleted" 
            type="primary" 
            @click="downloadZip"
            :disabled="!zipDownloadPath"
          >
            下载ZIP文件
          </el-button>
          <el-button @click="closePackageDialog">关闭</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElButton, ElDialog, ElProgress, ElTag, ElIcon } from 'element-plus'
import { Download } from '@element-plus/icons-vue'
import LogicPanel from '@/components/organizer/src/components/LogicPanel.vue'
import Context from '@/components/organizer/src/context'
import { getTTSFlow, updateTTSFlow } from '@/api/tts-flow'
import type { TTSFlow } from '@/api/tts-flow/types'

const route = useRoute()
const router = useRouter()

// 响应式数据
const flowId = ref(route.params.id as string)
const flowName = ref('')
const logicPanelRef = ref()
const loading = ref(true)

// 画布上下文
const context = reactive(new Context({ logicList: [] }))
const info = ref(undefined)

// 打包相关状态
const packaging = ref(false)
const packageDialogVisible = ref(false)
const packageCompleted = ref(false)
const zipDownloadPath = ref('')
const eventSource = ref<EventSource | null>(null)

// 进度信息
const overallProgress = reactive({
  processed: 0,
  total: 0,
  percentage: 0,
  currentNode: ''
})

// 当前状态
const currentStatus = reactive({
  type: '',
  message: ''
})

// 处理日志
const processLogs = ref<Array<{
  time: string,
  message: string,
  type: string
}>>([])

// 获取工作流详情
const getFlowDetail = async () => {
  try {
    const res = await getTTSFlow(flowId.value)
    const flowData = (res as any).data || {}
    flowName.value = flowData.name || ''

    // 如果有现有的flow_config，加载到画布
    if (flowData.flow_config && flowData.flow_config.logicList) {
      context.logicList = flowData.flow_config.logicList
    } else {
      // 默认配置
      context.logicList = []
    }
    
    // 数据加载完成，关闭 loading
    loading.value = false
  } catch (error) {
    console.error('获取工作流详情失败:', error)
    ElMessage.error('获取工作流详情失败')
    loading.value = false
  }
}

// 开始打包
const startPackage = async () => {
  if (packaging.value) return
  
  try {
    packaging.value = true
    packageDialogVisible.value = true
    packageCompleted.value = false
    zipDownloadPath.value = ''
    
    // 重置状态
    Object.assign(overallProgress, {
      processed: 0,
      total: 0,
      percentage: 0,
      currentNode: ''
    })
    
    Object.assign(currentStatus, {
      type: '',
      message: ''
    })
    
    processLogs.value = []
    
    // 添加开始日志
    addLog('开始音频打包处理', 'info')
    
    // 发起流式请求
    const apiBasePath = import.meta.env.VITE_API_BASE_PATH
    const url = `${apiBasePath}/api/v1/tts-flows/${flowId.value}/synthesize-all`
    
    eventSource.value = new EventSource(url)
    
    eventSource.value.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        handlePackageEvent(data)
      } catch (error) {
        console.error('解析事件数据失败:', error)
        addLog('解析事件数据失败', 'error')
      }
    }
    
    eventSource.value.onerror = (error) => {
      console.error('连接错误:', error)
      addLog('连接错误，请重试', 'error')
      packaging.value = false
      eventSource.value?.close()
    }
    
  } catch (error) {
    console.error('启动打包失败:', error)
    ElMessage.error('启动打包失败')
    packaging.value = false
  }
}

// 处理打包事件
const handlePackageEvent = (data: any) => {
  const { type, data: eventData, code } = data
  
  if (code !== 0) {
    addLog(`错误: ${eventData.error || '未知错误'}`, 'error')
    return
  }
  
  // 更新进度信息
  if (eventData.progress) {
    Object.assign(overallProgress, eventData.progress)
  }
  
  switch (type) {
    case 'start':
      addLog(`开始处理，共 ${eventData.totalNodes} 个节点`, 'info')
      break
      
    case 'node':
      addLog(`处理节点: ${eventData.nodeName}`, 'info')
      Object.assign(currentStatus, {
        type: 'node',
        message: `正在处理节点: ${eventData.nodeName}`
      })
      break
      
    case 'node_task':
      if (eventData.status) {
        addLog(`任务状态: ${eventData.status}`, 'info')
        Object.assign(currentStatus, {
          type: 'task',
          message: eventData.status
        })
      }
      break
      
    case 'audio_concat':
      if (eventData.status === '音频拼接完成') {
        addLog(`音频拼接完成，共 ${eventData.audioCount} 个音频文件`, 'success')
        Object.assign(currentStatus, {
          type: 'concat',
          message: '音频拼接完成'
        })
      } else {
        addLog(`音频拼接: ${eventData.status}`, 'info')
        Object.assign(currentStatus, {
          type: 'concat',
          message: eventData.status
        })
      }
      break
      
    case 'zip_package':
      if (eventData.status === 'ZIP压缩包创建完成') {
        addLog(`ZIP打包完成，下载地址: ${eventData.downloadUrl}`, 'success')
        zipDownloadPath.value = eventData.downloadUrl
        Object.assign(currentStatus, {
          type: 'zip',
          message: 'ZIP打包完成'
        })
      } else {
        addLog(`ZIP打包: ${eventData.status}`, 'info')
        Object.assign(currentStatus, {
          type: 'zip',
          message: eventData.status
        })
      }
      break
      
    case 'end':
      addLog(`处理完成，共处理 ${eventData.processedNodes} 个节点`, 'success')
      Object.assign(currentStatus, {
        type: 'complete',
        message: '处理完成'
      })
      packageCompleted.value = true
      packaging.value = false
      eventSource.value?.close()
      
      if (eventData.zipDownloadPath) {
        zipDownloadPath.value = eventData.zipDownloadPath
        ElMessage.success('音频打包完成，可以下载ZIP文件')
      }
      break
  }
}

// 添加日志
const addLog = (message: string, type: string = 'info') => {
  const time = new Date().toLocaleTimeString()
  processLogs.value.push({
    time,
    message,
    type
  })
  
  // 限制日志数量
  if (processLogs.value.length > 50) {
    processLogs.value.shift()
  }
}

// 清空日志
const clearLog = () => {
  processLogs.value = []
}

// 获取状态类型
const getStatusType = (type: string): 'primary' | 'warning' | 'info' | 'success' | 'danger' => {
  const typeMap: Record<string, 'primary' | 'warning' | 'info' | 'success' | 'danger'> = {
    'node': 'primary',
    'task': 'warning',
    'concat': 'info',
    'zip': 'success',
    'complete': 'success'
  }
  return typeMap[type] || 'info'
}

// 获取状态文本
const getStatusText = (type: string) => {
  const textMap: Record<string, string> = {
    'node': '节点处理',
    'task': '任务执行',
    'concat': '音频拼接',
    'zip': 'ZIP打包',
    'complete': '处理完成'
  }
  return textMap[type] || '处理中'
}

// 获取日志样式
const getLogClass = (type: string) => {
  return {
    'log-info': type === 'info',
    'log-success': type === 'success',
    'log-warning': type === 'warning',
    'log-error': type === 'error'
  }
}

// 下载ZIP文件
const downloadZip = async () => {
  if (!zipDownloadPath.value) {
    ElMessage.warning('下载路径不存在')
    return
  }

  const apiBasePath = import.meta.env.VITE_API_BASE_PATH
  const downloadUrl = `${apiBasePath}${zipDownloadPath.value}`

  try {
    // 1. 获取文件 blob
    const response = await fetch(downloadUrl)
    if (!response.ok) throw new Error('下载失败')
    const blob = await response.blob()

    // 2. 创建 a 标签下载
    const a = document.createElement('a')
    const url = window.URL.createObjectURL(blob)
    a.href = url
    // 使用 flowName 作为文件名，注意加 .zip 后缀，特殊字符替换
    a.download = `${(flowName.value || 'tts_flow').replace(/[\\/:*?"<>|]/g, '_')}.zip`
    document.body.appendChild(a)
    a.click()
    a.remove()
    window.URL.revokeObjectURL(url)
  } catch (e) {
    ElMessage.error('下载失败')
  }
}

// 关闭打包对话框
const closePackageDialog = () => {
  packageDialogVisible.value = false
  if (eventSource.value) {
    eventSource.value.close()
    eventSource.value = null
  }
  packaging.value = false
}

// 保存流程配置
const saveFlow = async () => {
  try {
    // 从画布获取当前配置
    const currentConfig = {
      logicList: context.logicList
    }

    // 更新工作流
    await updateTTSFlow(flowId.value, {
      name: flowName.value,
      flow_config: currentConfig
    })

    ElMessage.success('保存成功')
  } catch (error) {
    console.error('保存失败:', error)
    ElMessage.error('保存失败')
  }
}

// 返回列表
const goBack = () => {
  router.push('/tts-flow')
}

// 页面加载时获取数据
onMounted(() => {
  if (flowId.value) {
    getFlowDetail()
  }
})
</script>

<style scoped>
.flow-canvas-container {
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f5f5f5;
}

.canvas-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  background: white;
  border-bottom: 1px solid #e4e7ed;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.header-left h2 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.header-right {
  display: flex;
  gap: 12px;
}

.canvas-content {
  flex: 1;
  overflow: hidden;
  position: relative;
}

.logic-panel-wrapper {
  width: 100%;
  height: 100%;
  background: #eaecef;
  border: 1px solid #ccc;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #409eff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 打包进度对话框样式 */
.package-progress {
  max-height: 400px;
  overflow-y: auto;
}

.progress-section {
  margin-bottom: 24px;
}

.progress-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.progress-title {
  font-weight: 600;
  color: #303133;
}

.progress-percentage {
  font-weight: 600;
  color: #409eff;
}

.progress-info {
  margin-top: 8px;
  font-size: 14px;
  color: #606266;
}

.current-status {
  margin-bottom: 24px;
}

.status-header {
  margin-bottom: 12px;
}

.status-title {
  font-weight: 600;
  color: #303133;
}

.status-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.status-tag {
  align-self: flex-start;
}

.status-message {
  font-size: 14px;
  color: #606266;
  padding: 8px 12px;
  background: #f5f7fa;
  border-radius: 4px;
}

.process-log {
  border-top: 1px solid #e4e7ed;
  padding-top: 16px;
}

.log-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.log-title {
  font-weight: 600;
  color: #303133;
}

.log-content {
  max-height: 200px;
  overflow-y: auto;
  border: 1px solid #e4e7ed;
  border-radius: 4px;
  padding: 8px;
  background: #fafafa;
}

.log-item {
  display: flex;
  gap: 8px;
  margin-bottom: 4px;
  font-size: 12px;
  line-height: 1.4;
}

.log-time {
  color: #909399;
  min-width: 60px;
}

.log-message {
  flex: 1;
}

.log-info .log-message {
  color: #606266;
}

.log-success .log-message {
  color: #67c23a;
}

.log-warning .log-message {
  color: #e6a23c;
}

.log-error .log-message {
  color: #f56c6c;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style>
