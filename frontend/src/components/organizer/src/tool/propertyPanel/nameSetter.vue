<template>
  <div class="setter-wrap">
    <label class="label">节点名称:</label>
    <el-input
      class="input"
      v-model="localValue"
      placeholder="请输入值"
      size="small"
      @change="handleChange"
    />
    <div class="tip"><span>*</span> 建议为节点设置名称，以免后续出现同名节点</div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { ElInput } from 'element-plus'

const props = defineProps<{ modelValue: string }>()
const emit = defineEmits(['update:modelValue'])

const localValue = ref(props.modelValue)

watch(() => props.modelValue, (newVal) => {
  localValue.value = newVal
}, { immediate: true })

function handleChange(e: string) {
  localValue.value = e
  emit('update:modelValue', e)
}
</script>

<style scoped lang="less">
.setter-wrap {
  background: #f3f6fa;
  border-radius: 4px;
  font-family: PingFangSC-Regular;
  font-size: 12px;
  color: #303a51;
  line-height: 16px;
  font-weight: 400;
  padding: 9px 12px;
}
.label {
  margin-right: 10px;
}
.input {
  width: 200px;
}
.tip {
  color: #a0a1a5;
  margin-top: 8px;
}
</style>
