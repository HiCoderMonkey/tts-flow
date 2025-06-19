# TTS Flow Backend 使用示例

## 🚀 快速开始

### 1. 启动服务

```bash
# 使用启动脚本（推荐）
./start.sh

# 或使用 docker-compose
docker-compose up -d
```

### 2. 访问API文档

打开浏览器访问：http://localhost:8000/docs

## 📝 API 使用示例

### 用户注册

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "testuser",
    "password": "password123",
    "full_name": "Test User"
  }'
```

响应：
```json
{
  "id": "507f1f77bcf86cd799439011",
  "email": "user@example.com",
  "username": "testuser",
  "full_name": "Test User",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

### 用户登录

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=password123"
```

响应：
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 获取当前用户信息

```bash
curl -X GET "http://localhost:8000/api/v1/users/me" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

响应：
```json
{
  "id": "507f1f77bcf86cd799439011",
  "email": "user@example.com",
  "username": "testuser",
  "full_name": "Test User",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

### 更新用户信息

```bash
curl -X PUT "http://localhost:8000/api/v1/users/me" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Updated User Name"
  }'
```

### 获取用户列表（超级用户）

```bash
curl -X GET "http://localhost:8000/api/v1/users/" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

## 🔧 使用 JavaScript/Fetch

### 用户注册

```javascript
const registerUser = async (userData) => {
  const response = await fetch('http://localhost:8000/api/v1/auth/register', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(userData)
  });
  
  return await response.json();
};

// 使用示例
const user = await registerUser({
  email: 'user@example.com',
  username: 'testuser',
  password: 'password123',
  full_name: 'Test User'
});
```

### 用户登录

```javascript
const loginUser = async (username, password) => {
  const formData = new FormData();
  formData.append('username', username);
  formData.append('password', password);
  
  const response = await fetch('http://localhost:8000/api/v1/auth/login', {
    method: 'POST',
    body: formData
  });
  
  return await response.json();
};

// 使用示例
const token = await loginUser('testuser', 'password123');
localStorage.setItem('token', token.access_token);
```

### 获取用户信息

```javascript
const getUserInfo = async () => {
  const token = localStorage.getItem('token');
  
  const response = await fetch('http://localhost:8000/api/v1/users/me', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  return await response.json();
};

// 使用示例
const userInfo = await getUserInfo();
console.log(userInfo);
```

## 🐍 使用 Python/Requests

### 用户注册

```python
import requests

def register_user(user_data):
    response = requests.post(
        'http://localhost:8000/api/v1/auth/register',
        json=user_data
    )
    return response.json()

# 使用示例
user = register_user({
    'email': 'user@example.com',
    'username': 'testuser',
    'password': 'password123',
    'full_name': 'Test User'
})
print(user)
```

### 用户登录

```python
def login_user(username, password):
    response = requests.post(
        'http://localhost:8000/api/v1/auth/login',
        data={'username': username, 'password': password}
    )
    return response.json()

# 使用示例
token_data = login_user('testuser', 'password123')
token = token_data['access_token']
print(f"Token: {token}")
```

### 获取用户信息

```python
def get_user_info(token):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(
        'http://localhost:8000/api/v1/users/me',
        headers=headers
    )
    return response.json()

# 使用示例
user_info = get_user_info(token)
print(user_info)
```

## 🔍 错误处理

### 常见错误响应

#### 401 Unauthorized
```json
{
  "detail": "无法验证凭据"
}
```

#### 400 Bad Request
```json
{
  "detail": "用户名已存在"
}
```

#### 403 Forbidden
```json
{
  "detail": "权限不足"
}
```

#### 404 Not Found
```json
{
  "detail": "用户不存在"
}
```

### 错误处理示例

```javascript
const handleApiError = async (response) => {
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || '请求失败');
  }
  return response.json();
};

// 使用示例
try {
  const user = await fetch('http://localhost:8000/api/v1/users/me', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  }).then(handleApiError);
  
  console.log('用户信息:', user);
} catch (error) {
  console.error('错误:', error.message);
}
```

## 📊 健康检查

```bash
curl -X GET "http://localhost:8000/health"
```

响应：
```json
{
  "status": "healthy"
}
```

## 🔐 安全注意事项

1. **Token 安全**
   - 不要在客户端代码中硬编码 Token
   - 使用 HTTPS 传输 Token
   - 定期刷新 Token

2. **密码安全**
   - 使用强密码
   - 不要在日志中记录密码
   - 定期更换密码

3. **API 安全**
   - 限制 API 调用频率
   - 监控异常访问
   - 记录安全事件

## 📚 更多信息

- [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- [JWT 认证](https://jwt.io/)
- [MongoDB 文档](https://docs.mongodb.com/)
- [Beanie ODM 文档](https://roman-right.github.io/beanie/) 