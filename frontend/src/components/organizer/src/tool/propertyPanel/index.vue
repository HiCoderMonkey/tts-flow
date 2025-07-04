<template>
  <el-drawer
    :append-to-body="false"
    :wrapperClosable="true"
    :destroy-on-close="true"
    style="position: absolute"
    direction="rtl"
    class="properties-panel"
    width="100%"
    :size="500"
    @closeDrawer="closeDrawer"
    v-model="showDrawer"
  >
    <div v-if="panelType !== 'condition'">
      <div class="setter-title">节点名称</div>
      <name-setter v-model="name" :data_id="data_id" />
    </div>
    <div v-if="panelType === 'ttsTextChunk'">
      <div class="setter-title">文本块信息</div>
      <TtsTextChunkSetter v-model="ttsTextChunkData" :data_id="data_id" :currentModel="currentModel" :node_name="name" />
    </div>
    <div v-if="panelType === 'spaceVoid'">
     <div class="setter-title">留白设置</div>
     <SpaceVoidSetter v-model="spaceData" />
    </div>
    <el-button
      type="primary"
      size="small"
      @click="handleSubmit"
      class="properties-button"
      >确认</el-button
    >
    <el-button size="small" @click="handleCancel" class="properties-button"
      >取消</el-button
    >
  </el-drawer>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { map, filter } from 'lodash-es'
import { validateCode } from '../../util/validate'
import actionSetter from './actionSetter.vue'
import conditionSetter from './conditionSetter.vue'
import eventSetter from './eventSetter.vue'
import dsSetter from './dsSetter.vue'
import nameSetter from './nameSetter.vue'
import pageJumpSetter from './pageJumpSetter.vue'
import dcSetter from './dcSetter.vue'
import TtsTextChunkSetter from './ttsTextChunkSetter.vue'
import SpaceVoidSetter from './spaceVoidSetter.vue'
import { ElDrawer, ElButton } from 'element-plus'

const props = defineProps<{ lf: any; context: any; data_id: string }>()
const emit = defineEmits(['submit'])

const panelType = ref('')
const showDrawer = ref(false)
const currentModel = ref<any>({})
const currentNode = ref<any>({})
const currentEdge = ref<any>(null)
const actions = ref<any[]>([])
const condition = ref<any>({})
const event = ref<any>({})
const ds = ref<any>({})
const pageJump = ref<any>({})
const dc = ref<any>({})
const name = ref('')
const edgeProperties = ref()
const ttsTextChunkData = ref({ text: '', audioUrl: '' })
const spaceData = ref({ duration: 2 })

onMounted(() => {
  props.lf.on('node:click', ({ data }: any) => {
    console.log('data', data)
  })
  props.lf.on('blank:click', () => {
    showDrawer.value = false
    panelType.value = ''
    currentEdge.value = null
  })
  // 点击边处理
  props.lf.on('edge:option-click', (model: any) => {
    currentEdge.value = model
    const properties = model.getProperties()
    condition.value = properties.condition || {}
    showDrawer.value = true
    panelType.value = 'condition'
  })
  // 点击节点处理
  props.lf.on('node:select-click', (model: any) => {
    console.log('model ===>>>', model)
    currentModel.value = model
    const properties = model.getProperties()
    name.value = properties.name
    switch (model.type) {
      case 'event-node':
        event.value = (properties && properties.event) || {}
        panelType.value = 'event'
        if (model.properties && model.properties.componentName !== 'pageInit') {
          showDrawer.value = true
        }
        break
      case 'reaction-node':
        actions.value = (properties && properties.reactions) || []
        panelType.value = 'action'
        showDrawer.value = true
        break
      case 'common-node':
        panelType.value = properties.componentName
        ttsTextChunkData.value = properties.nodeContentData || {}
        showDrawer.value = true
        break
    }
  })
})

function handleSubmit() {
  console.log('name --->>>', name.value)
  console.log('ttsTextChunkData --->>>', ttsTextChunkData.value)
  const currentNodeVal = currentModel.value
  props.lf.setProperties(currentNodeVal.id, {
    name: name.value
  })
  console.log('panelType ...???', panelType.value)
  switch (panelType.value) {
    case 'ttsTextChunk':
      props.lf.setProperties(currentNodeVal.id, {
        nodeContentData: ttsTextChunkData.value
      })
      break
    case 'spaceVoid':
      props.lf.setProperties(currentNodeVal.id, {
        nodeContentData: spaceData.value
      })
      break
    case 'action':
      props.lf.setProperties(currentNodeVal.id, {
        reactions: actions.value
      })
      break
    case 'condition':
      if (currentEdge.value) {
        props.lf.setProperties(currentEdge.value.id, {
          condition: condition.value
        })
      }
      break
    case 'event':
      props.lf.setProperties(currentNodeVal.id, {
        event: event.value
      })
      break
    case 'ds':
      props.lf.setProperties(currentNodeVal.id, {
        ds: ds.value
      })
      break
    case 'pageJump':
      props.lf.setProperties(currentNodeVal.id, {
        pageJump: pageJump.value
      })
      break
    case 'dc': {
      const { convertList = [], convertCode } = dc.value
      if (!convertCode) {
        // @ts-ignore
        window?.$message?.error?.('数据转换函数不能为空')
        return false
      }
      try {
        const keyList = filter(
          map(convertList, (item) => item.key),
          (key) => key
        )
        const funcParams = keyList.join(', ')
        const fullFunc = `function main(${funcParams}) {\n${convertCode}\n}`
        const valid = validateCode(fullFunc)
        if (!valid) {
          throw new Error('代码校验未通过，请确认代码是否合规')
        }
      } catch (error: any) {
        console.error('ops, something error --->>>', error)
        // @ts-ignore
        window?.$message?.error?.(error?.message)
        return
      }
      props.lf.setProperties(currentNodeVal.id, {
        dc: dc.value
      })
      break
    }
  }
  showDrawer.value = false
  emit('submit', panelType.value)
}

function handleCancel() {
  showDrawer.value = false
}

function closeDrawer() {
  currentEdge.value = null
}
</script>

<style scoped lang="less">
/deep/.el-drawer {
  padding: 12px 12px;
  box-sizing: border-box;
  height: 100%;
  overflow-y: auto;
  &::-webkit-scrollbar {
    /*滚动条整体样式*/
    background: transparent;
    border-radius: 5px;
    width: 4px;
    z-index: -1;
  }

  &::-webkit-scrollbar-thumb {
    /*滚动条里面小方块*/
    border-radius: 4px;
    background: #dcdfe6;
    z-index: -1;
  }

  &::-webkit-scrollbar-track {
    /*滚动条里面轨道*/
    border-radius: 4px;
    background: transparent;
  }

  &::-webkit-scrollbar-corner {
    /*滚动条交汇处*/
    border-radius: 4px;
    background: transparent;
  }
}
/deep/.el-drawer__header {
  margin: 0;
  height: 0;
}

.setter-title {
  font-size: 16px;
  font-weight: bold;
  font-size: 16px;
  color: #303133;
  // background: #f2f3f7;
  height: 50px;
  line-height: 50px;
  margin-bottom: 10px;
  border-bottom: 1px solid #ebeef5;
}

.properties-button {
  float: right;
  margin-top: 20px;
  margin-left: 10px;
}
</style>
