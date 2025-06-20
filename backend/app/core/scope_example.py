"""
Scope 示例和说明
"""

# 一个典型的HTTP请求的scope字典结构
example_scope = {
    # 基本信息
    "type": "http",                    # 请求类型：http, websocket, lifespan
    "asgi": {
        "version": "3.0",
        "spec_version": "2.0"
    },
    
    # HTTP请求信息
    "http_version": "1.1",             # HTTP版本
    "method": "GET",                   # HTTP方法：GET, POST, PUT, DELETE等
    "scheme": "https",                 # 协议：http, https
    "server": ("example.com", 443),    # 服务器地址和端口
    "client": ("192.168.1.1", 12345),  # 客户端地址和端口
    
    # URL信息
    "path": "/api/v1/users/me",        # 请求路径
    "raw_path": b"/api/v1/users/me",   # 原始路径（字节）
    "query_string": b"page=1&limit=10", # 查询字符串（字节）
    "root_path": "",                   # 根路径
    
    # 请求头
    "headers": [
        (b"host", b"example.com"),
        (b"user-agent", b"Mozilla/5.0..."),
        (b"authorization", b"Bearer token123"),
        (b"content-type", b"application/json"),
        (b"accept", b"application/json"),
    ],
    
    # 状态信息（中间件可以修改）
    "state": {},                       # 应用状态，可以存储自定义数据
    
    # 其他信息
    "extensions": {},                  # 扩展信息
    "app": None,                       # 应用实例
}


class ScopeExplainer:
    """Scope解释器"""
    
    @staticmethod
    def explain_scope(scope: dict):
        """解释scope的内容"""
        print("=== Scope 详细解释 ===\n")
        
        # 基本信息
        print(f"1. 请求类型: {scope.get('type', 'unknown')}")
        print(f"2. HTTP方法: {scope.get('method', 'unknown')}")
        print(f"3. 请求路径: {scope.get('path', 'unknown')}")
        print(f"4. HTTP版本: {scope.get('http_version', 'unknown')}")
        print(f"5. 协议: {scope.get('scheme', 'unknown')}")
        
        # 服务器和客户端信息
        server = scope.get('server', (None, None))
        client = scope.get('client', (None, None))
        print(f"6. 服务器地址: {server[0]}:{server[1] if server[1] else 'unknown'}")
        print(f"7. 客户端地址: {client[0]}:{client[1] if client[1] else 'unknown'}")
        
        # 查询字符串
        query_string = scope.get('query_string', b'')
        if query_string:
            print(f"8. 查询参数: {query_string.decode()}")
        
        # 请求头
        headers = scope.get('headers', [])
        print(f"\n9. 请求头 ({len(headers)} 个):")
        for name, value in headers:
            print(f"   {name.decode()}: {value.decode()}")
        
        # 状态信息
        state = scope.get('state', {})
        print(f"\n10. 状态信息: {state}")
        
        # 扩展信息
        extensions = scope.get('extensions', {})
        if extensions:
            print(f"\n11. 扩展信息: {extensions}")
    
    @staticmethod
    def show_scope_in_middleware():
        """展示在中间件中如何使用scope"""
        print("\n=== 中间件中的Scope使用 ===\n")
        
        middleware_code = '''
class AuthMiddleware:
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        # 1. 检查请求类型
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        
        # 2. 获取请求信息
        path = scope["path"]
        method = scope["method"]
        
        # 3. 获取请求头
        headers = dict(scope["headers"])
        auth_header = headers.get(b"authorization", b"").decode()
        
        # 4. 在scope中添加自定义数据
        scope["user"] = {"id": 123, "username": "test"}
        scope["auth_checked"] = True
        
        # 5. 继续处理请求
        await self.app(scope, receive, send)
        '''
        
        print(middleware_code)
    
    @staticmethod
    def show_scope_in_route():
        """展示在路由中如何访问scope"""
        print("\n=== 路由中的Scope访问 ===\n")
        
        route_code = '''
from fastapi import Request

@router.get("/me")
async def read_users_me(request: Request):
    # 通过Request对象访问scope
    scope = request.scope
    
    # 获取路径
    path = scope["path"]
    
    # 获取用户信息（由中间件添加）
    user = scope.get("user")
    
    # 获取请求头
    headers = dict(scope["headers"])
    user_agent = headers.get(b"user-agent", b"").decode()
    
    return {"user": user, "path": path, "user_agent": user_agent}
        '''
        
        print(route_code)


# 使用示例
if __name__ == "__main__":
    explainer = ScopeExplainer()
    explainer.explain_scope(example_scope)
    explainer.show_scope_in_middleware()
    explainer.show_scope_in_route() 