# 登录对接完整流程

本文档详细说明了前端登录功能的完整实现流程。

## 功能概述

实现了完整的登录流程：
1. 调用登录接口
2. 获取access_token保存到cookie中
3. 请求拦截器自动添加token到请求头
4. 响应拦截器处理401错误，提示用户重新登录

## 文件结构

```
frontend/
├── src/
│   ├── api/login/
│   │   ├── index.ts          # 登录相关API
│   │   └── types.ts          # 类型定义
│   ├── axios/
│   │   ├── config.ts         # axios配置和拦截器
│   │   └── service.ts        # axios服务
│   ├── utils/
│   │   └── cookie.ts         # cookie工具类
│   ├── views/Login/
│   │   └── components/
│   │       └── LoginForm.vue # 登录表单组件
│   └── views/Test/
│       └── TestLogin.vue     # 登录测试页面
```

## 核心功能实现

### 1. Cookie工具类 (`utils/cookie.ts`)

```typescript
// 设置access_token
export function setAccessToken(token: string, days: number = 7): void

// 获取access_token
export function getAccessToken(): string | null

// 删除access_token
export function removeAccessToken(): void
```

### 2. 请求拦截器 (`axios/config.ts`)

```typescript
const defaultRequestInterceptors = (config: InternalAxiosRequestConfig) => {
  // 自动添加token到请求头
  const token = getAccessToken()
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  // ... 其他处理
}
```

### 3. 响应拦截器 (`axios/service.ts`)

```typescript
// 处理401未授权错误
if (response?.status === 401) {
  handleUnauthorized()
  return Promise.reject(error)
}
```

### 4. 401错误处理 (`axios/config.ts`)

```typescript
export const handleUnauthorized = async () => {
  // 清除token
  removeAccessToken()
  
  // 显示确认对话框
  try {
    await ElMessageBox.confirm(
      '登录已过期，请重新登录',
      '提示',
      {
        confirmButtonText: '重新登录',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    // 用户点击确认，跳转到登录页
    router.push('/login')
  } catch {
    // 用户点击取消，不做任何操作
  }
}
```

## 登录流程

### 1. 用户输入登录信息

用户在登录表单中输入用户名和密码。

### 2. 调用登录接口

```typescript
const res = await loginApi({
  username: 'admin',
  password: 'admin'
})
```

### 3. 保存Token

```typescript
if (res && res.data) {
  const { access_token } = res.data
  setAccessToken(access_token, remember.value ? 30 : 7)
}
```

### 4. 自动添加Token到请求头

每次API请求时，请求拦截器会自动从cookie中获取token并添加到请求头：

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 5. 处理401错误

当后端返回401错误时：
- 自动清除cookie中的token
- 显示确认对话框询问用户是否重新登录
- 用户确认后跳转到登录页面

## 使用示例

### 登录表单使用

```vue
<template>
  <LoginForm @to-register="toRegister" />
</template>

<script setup>
import { LoginForm } from '@/views/Login/components'
</script>
```

### API调用示例

```typescript
import request from '@/axios'

// 调用需要认证的API
const getUserInfo = async () => {
  try {
    const res = await request.get({ url: '/api/v1/users/me' })
    return res
  } catch (error) {
    // 401错误会自动处理
    console.error('获取用户信息失败:', error)
  }
}
```

### 测试登录功能

访问 `/test-login` 页面可以测试完整的登录流程：

1. **测试登录接口** - 验证登录API是否正常工作
2. **测试Token** - 检查token是否正确保存到cookie
3. **测试API请求** - 验证带token的API请求是否成功
4. **测试401处理** - 验证401错误处理是否正常

## 配置说明

### 环境变量

确保在 `.env` 文件中配置了正确的API地址：

```env
VITE_API_BASE_PATH=http://localhost:8000
```

### Token过期时间

- 记住我：30天
- 普通登录：7天

可以在 `LoginForm.vue` 中修改：

```typescript
setAccessToken(access_token, remember.value ? 30 : 7)
```

## 注意事项

1. **Token安全**：token存储在cookie中，确保在生产环境使用HTTPS
2. **错误处理**：401错误会自动处理，无需在每个API调用中手动处理
3. **路由保护**：建议配合路由守卫使用，未登录用户自动跳转到登录页
4. **用户体验**：401错误会显示确认对话框，用户可以选择是否重新登录

## 扩展功能

### 添加路由守卫

```typescript
// router/guard.ts
import { getAccessToken } from '@/utils/cookie'

router.beforeEach((to, from, next) => {
  const token = getAccessToken()
  
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else {
    next()
  }
})
```

### 添加用户状态管理

```typescript
// store/modules/user.ts
import { getAccessToken, removeAccessToken } from '@/utils/cookie'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: getAccessToken(),
    userInfo: null
  }),
  
  actions: {
    logout() {
      removeAccessToken()
      this.token = null
      this.userInfo = null
    }
  }
})
```

## 故障排除

### 常见问题

1. **Token未保存**：检查cookie是否被浏览器阻止
2. **401错误未处理**：检查响应拦截器是否正确配置
3. **API请求失败**：检查token是否正确添加到请求头

### 调试方法

1. 打开浏览器开发者工具
2. 查看Network标签页中的请求头
3. 查看Application标签页中的Cookies
4. 使用测试页面验证各个功能

## 总结

通过以上实现，我们完成了完整的登录流程：

✅ 登录接口调用  
✅ Token自动保存到cookie  
✅ 请求自动添加token  
✅ 401错误自动处理  
✅ 用户友好的错误提示  

整个流程对开发者透明，使用简单，用户体验良好。 