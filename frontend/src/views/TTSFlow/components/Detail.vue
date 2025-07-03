<script setup lang="ts">
import { PropType, computed } from 'vue'
import type { TTSFlow } from '@/api/tts-flow/types'
import { Descriptions, DescriptionsSchema } from '@/components/Descriptions'

const props = defineProps({
  currentRow: {
    type: Object as PropType<Nullable<TTSFlow>>,
    default: () => null
  },
  detailSchema: {
    type: Array as PropType<DescriptionsSchema[]>,
    default: () => []
  }
})

// 默认详情 schema
const defaultDetailSchema = computed<DescriptionsSchema[]>(() => [
  {
    field: 'name',
    label: '工作流名称'
  },
  {
    field: 'voiceName',
    label: '音色名称',
    render: (value: string) => value || '未选择音色'
  },
  {
    field: 'voiceId',
    label: '音色ID',
    render: (value: string) => value || '未选择音色'
  },
  {
    field: 'created_at',
    label: '创建时间',
    render: (value: string) => value ? new Date(value).toLocaleString('zh-CN') : '-'
  },
  {
    field: 'updated_at',
    label: '更新时间',
    render: (value: string) => value ? new Date(value).toLocaleString('zh-CN') : '-'
  }
])

// 使用传入的 schema 或默认 schema
const finalSchema = computed(() => {
  return props.detailSchema.length > 0 ? props.detailSchema : defaultDetailSchema.value
})
</script>

<template>
  <Descriptions :schema="finalSchema" :data="currentRow || {}" />
</template> 