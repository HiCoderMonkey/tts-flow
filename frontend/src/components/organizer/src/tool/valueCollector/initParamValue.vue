<template>
  <div>
    <el-input v-model="val" placeholder="请输入值" size="small" @change="handleChange" />
  </div>
</template>

<script>
import { ElInput } from 'element-plus'  

export default {
  components: {
    ElInput
  },
  props: {
    context: Object,
    value: Object
  },
  data() {
    return {
      val: ''
    }
  },
  watch: {
    value: {
      immediate: true,
      deep: true,
      handler(nv) {
        if (nv && nv.type === 'initParam') {
          this.val = nv.value
        }
      }
    }
  },
  methods: {
    handleChange(e) {
      this.val = e
      const data = {
        type: 'initParam',
        value: e,
        dataType: 'string' // 默认string类型
      }
      this.$emit('change', data)
    }
  }
}
</script>
