<template>
  <div class="space-void-setter">
    <el-form label-width="80px">
      <el-form-item label="留白时间">
        <el-input
          v-model.number="localValue.duration"
          type="number"
          min="0"
          :step="1"
          placeholder="请输入留白时间"
          style="width: 120px"
        >
          <template #append>秒</template>
        </el-input>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { ElInput, ElForm, ElFormItem } from 'element-plus'

interface SpaceVoidData {
  duration: number
}

const props = defineProps<{ modelValue: SpaceVoidData }>()
const emit = defineEmits(['update:modelValue'])

const localValue = ref<SpaceVoidData>({
  duration: props.modelValue?.duration ?? 2
})

watch(
  () => props.modelValue,
  (val) => {
    if (val && typeof val.duration === 'number') {
      localValue.value.duration = val.duration
    }
  },
  { immediate: true, deep: true }
)

watch(
  () => localValue.value,
  (val) => {
    emit('update:modelValue', val)
  },
  { deep: true }
)
</script>

<style scoped lang="less">
.space-void-setter {
  margin-top: 10px;
}
</style> 