<template>
  <div class="flow-canvas-container">
    <div class="canvas-header">
      <div class="header-left">
        <el-button @click="goBack" icon="ArrowLeft">返回列表</el-button>
        <h2>{{ flowName }} - 流程配置</h2>
      </div>
      <div class="header-right">
        <el-button type="primary" @click="saveFlow">保存配置</el-button>
      </div>
    </div>
    
    <div class="canvas-content">
      <logic-panel
        ref="logicPanelRef"
        class="logic-panel-wrapper"
        :context="context"
        :info="info"
      ></logic-panel>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
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

// 画布上下文
const context = reactive(new Context({ logicList: [] }))
const info = ref(undefined)

// 获取工作流详情
const getFlowDetail = async () => {
  try {
    const res = await getTTSFlow(flowId.value)
    const flowData = res as any
    
    flowName.value = flowData.name
    
    // 如果有现有的flow_config，加载到画布
    if (flowData.flow_config && flowData.flow_config.logicList) {
      context.logicList = flowData.flow_config.logicList
    } else {
      // 默认配置
      context.logicList = [
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
  } catch (error) {
    console.error('获取工作流详情失败:', error)
    ElMessage.error('获取工作流详情失败')
  }
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
</style> 