<template>
  <div class="test-login">
    <h2>登录测试页面</h2>

    <div class="test-section">
      <h3>1. 测试登录接口</h3>
      <el-form :model="loginForm" label-width="100px">
        <el-form-item label="用户名">
          <el-input v-model="loginForm.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="loginForm.password" type="password" placeholder="请输入密码" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="testLogin" :loading="loading"> 测试登录 </el-button>
        </el-form-item>
      </el-form>
    </div>

    <div class="test-section">
      <h3>2. 测试Token</h3>
      <el-button @click="checkToken">检查Token</el-button>
      <el-button @click="clearToken">清除Token</el-button>
      <div v-if="tokenInfo" class="token-info">
        <p><strong>当前Token:</strong> {{ tokenInfo }}</p>
      </div>
    </div>

    <div class="test-section">
      <h3>3. 测试API请求</h3>
      <el-button @click="testApiCall">测试需要认证的API</el-button>
      <div v-if="apiResult" class="api-result">
        <p><strong>API结果:</strong></p>
        <pre>{{ JSON.stringify(apiResult, null, 2) }}</pre>
      </div>
    </div>

    <div class="test-section">
      <h3>4. 测试401处理</h3>
      <el-button @click="testUnauthorized">测试401错误处理</el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { loginApi } from '@/api/login'
import { getAccessToken, removeAccessToken } from '@/utils/cookie'
import request from '@/axios'

const loading = ref(false)
const tokenInfo = ref<string | null>(null)
const apiResult = ref<any>(null)

const loginForm = ref({
  username: 'admin',
  password: 'admin'
})

// 测试登录
const testLogin = async () => {
  if (!loginForm.value.username || !loginForm.value.password) {
    ElMessage.warning('请输入用户名和密码')
    return
  }

  loading.value = true
  try {
    const res = await loginApi(loginForm.value)
    if (res && res.data) {
      ElMessage.success('登录成功！')
      checkToken() // 检查token是否保存成功
    }
  } catch (error: any) {
    ElMessage.error(error?.message || '登录失败')
  } finally {
    loading.value = false
  }
}

// 检查Token
const checkToken = () => {
  const token = getAccessToken()
  tokenInfo.value = token
  if (token) {
    ElMessage.success('Token存在')
  } else {
    ElMessage.warning('Token不存在')
  }
}

// 清除Token
const clearToken = () => {
  removeAccessToken()
  tokenInfo.value = null
  ElMessage.success('Token已清除')
}

// 测试API请求
const testApiCall = async () => {
  try {
    const res = await request.get({ url: '/api/v1/users/me' })
    apiResult.value = res
    ElMessage.success('API调用成功')
  } catch (error: any) {
    apiResult.value = { error: error.message }
    ElMessage.error('API调用失败')
  }
}

// 测试401处理
const testUnauthorized = async () => {
  try {
    // 先清除token
    removeAccessToken()
    // 然后调用需要认证的API
    await request.get({ url: '/api/v1/users/me' })
  } catch (error: any) {
    ElMessage.info('401错误处理测试完成')
  }
}

// 页面加载时检查token
checkToken()
</script>

<style scoped>
.test-login {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.test-section {
  margin-bottom: 30px;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.test-section h3 {
  margin-top: 0;
  color: #333;
}

.token-info {
  margin-top: 10px;
  padding: 10px;
  background-color: #f5f5f5;
  border-radius: 4px;
}

.api-result {
  margin-top: 10px;
  padding: 10px;
  background-color: #f5f5f5;
  border-radius: 4px;
}

.api-result pre {
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
}
</style>
