# 架构设计

AIS 采用模块化架构设计，确保代码的可维护性、可扩展性和测试性。本文档详细介绍系统架构、核心组件和设计原则。

## 🏗️ 整体架构

### 架构图
```
┌─────────────────────────────────────────────────────────────┐
│                        用户界面层                             │
├─────────────────────────────────────────────────────────────┤
│  CLI Commands  │  Shell Integration  │  Rich UI Components  │
├─────────────────────────────────────────────────────────────┤
│                       应用服务层                             │
├─────────────────────────────────────────────────────────────┤
│  Ask Service  │  Analyze Service  │  Learn Service  │ Config │
├─────────────────────────────────────────────────────────────┤
│                        核心业务层                            │
├─────────────────────────────────────────────────────────────┤
│  AI Manager  │  Context Collector  │  Data Processor  │ Utils │
├─────────────────────────────────────────────────────────────┤
│                        数据访问层                            │
├─────────────────────────────────────────────────────────────┤
│  Database  │  File System  │  Network  │  External APIs     │
└─────────────────────────────────────────────────────────────┘
```

### 分层说明

#### 用户界面层
- **CLI Commands**: 命令行接口实现
- **Shell Integration**: Shell 钩子和集成
- **Rich UI Components**: 终端美化组件

#### 应用服务层
- **Ask Service**: AI 问答服务
- **Analyze Service**: 错误分析服务
- **Learn Service**: 学习系统服务
- **Config Service**: 配置管理服务

#### 核心业务层
- **AI Manager**: AI 提供商管理
- **Context Collector**: 上下文信息收集
- **Data Processor**: 数据处理和过滤
- **Utils**: 通用工具函数

#### 数据访问层
- **Database**: SQLite 数据库访问
- **File System**: 文件系统操作
- **Network**: 网络请求处理
- **External APIs**: 外部 API 集成

## 📁 目录结构

### 项目结构
```
src/ais/
├── __init__.py
├── main.py                 # 主入口
├── cli.py                  # CLI 主程序
├── commands/               # 命令实现
│   ├── __init__.py
│   ├── ask.py             # ais ask 命令
│   ├── analyze.py         # ais analyze 命令
│   ├── learn.py           # ais learn 命令
│   ├── config.py          # ais config 命令
│   └── providers.py       # 提供商管理命令
├── core/                  # 核心业务逻辑
│   ├── __init__.py
│   ├── config.py          # 配置管理
│   ├── database.py        # 数据库操作
│   ├── context.py         # 上下文收集
│   └── errors.py          # 错误处理
├── ai/                    # AI 相关模块
│   ├── __init__.py
│   ├── manager.py         # AI 管理器
│   ├── openai_client.py   # OpenAI 客户端
│   ├── claude_client.py   # Claude 客户端
│   └── ollama_client.py   # Ollama 客户端
├── shell/                 # Shell 集成
│   ├── __init__.py
│   ├── integration.py     # Shell 集成逻辑
│   ├── bash.py           # Bash 支持
│   ├── zsh.py            # Zsh 支持
│   └── fish.py           # Fish 支持
├── utils/                 # 工具函数
│   ├── __init__.py
│   ├── logger.py          # 日志系统
│   ├── text.py           # 文本处理
│   ├── network.py        # 网络工具
│   └── security.py       # 安全工具
└── ui/                   # 用户界面组件
    ├── __init__.py
    ├── console.py        # 控制台组件
    ├── panels.py         # 面板组件
    └── progress.py       # 进度显示
```

## 🔧 核心组件

### 配置管理 (Config)
```python
# src/ais/core/config.py
class Config:
    """配置管理器"""
    
    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or self.get_default_config_path()
        self._config = self._load_config()
    
    def get(self, key: str, default=None):
        """获取配置值"""
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any):
        """设置配置值"""
        self._config[key] = value
        self._save_config()
    
    def _load_config(self) -> dict:
        """加载配置文件"""
        if not self.config_path.exists():
            return self._get_default_config()
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
```

### AI 管理器 (AI Manager)
```python
# src/ais/ai/manager.py
class AIManager:
    """AI 提供商管理器"""
    
    def __init__(self, config: Config):
        self.config = config
        self.providers = self._load_providers()
    
    def get_provider(self, name: str) -> BaseAIClient:
        """获取 AI 提供商"""
        if name not in self.providers:
            raise ValueError(f"Unknown provider: {name}")
        
        provider_config = self.providers[name]
        return self._create_client(provider_config)
    
    def _create_client(self, config: dict) -> BaseAIClient:
        """创建 AI 客户端"""
        provider_type = config.get('type')
        
        if provider_type == 'openai':
            return OpenAIClient(config)
        elif provider_type == 'claude':
            return ClaudeClient(config)
        elif provider_type == 'ollama':
            return OllamaClient(config)
        else:
            raise ValueError(f"Unsupported provider type: {provider_type}")
```

### 上下文收集器 (Context Collector)
```python
# src/ais/core/context.py
class ContextCollector:
    """上下文信息收集器"""
    
    def __init__(self, config: Config):
        self.config = config
        self.level = config.get('context_level', 'standard')
    
    def collect(self, command: str, exit_code: int) -> dict:
        """收集上下文信息"""
        context = {
            'command': command,
            'exit_code': exit_code,
            'timestamp': datetime.now().isoformat()
        }
        
        if self.level in ['standard', 'detailed']:
            context.update(self._collect_system_info())
            context.update(self._collect_environment_info())
        
        if self.level == 'detailed':
            context.update(self._collect_detailed_info())
        
        return self._sanitize_context(context)
    
    def _collect_system_info(self) -> dict:
        """收集系统信息"""
        return {
            'os': platform.system(),
            'version': platform.version(),
            'architecture': platform.machine(),
            'python_version': platform.python_version()
        }
```

### 数据库管理 (Database)
```python
# src/ais/core/database.py
class Database:
    """数据库管理器"""
    
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.connection = None
        self._init_database()
    
    def _init_database(self):
        """初始化数据库"""
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        self._create_tables()
    
    def _create_tables(self):
        """创建数据表"""
        cursor = self.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                command TEXT NOT NULL,
                exit_code INTEGER NOT NULL,
                context TEXT,
                analysis TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.connection.commit()
    
    def insert_history(self, command: str, exit_code: int, 
                      context: str = None, analysis: str = None):
        """插入历史记录"""
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO history (command, exit_code, context, analysis)
            VALUES (?, ?, ?, ?)
        ''', (command, exit_code, context, analysis))
        self.connection.commit()
```

## 🔄 数据流

### 错误分析流程
```
命令执行失败
    ↓
Shell 钩子捕获
    ↓
上下文收集器收集信息
    ↓
数据清洗和过滤
    ↓
AI 管理器调用分析
    ↓
结果格式化和显示
    ↓
存储到数据库
```

### AI 问答流程
```
用户输入问题
    ↓
命令解析和验证
    ↓
上下文信息收集
    ↓
AI 管理器选择提供商
    ↓
发送请求到 AI 服务
    ↓
响应处理和格式化
    ↓
结果显示给用户
```

## 🔌 扩展机制

### 插件系统设计
```python
# src/ais/core/plugin.py
class BasePlugin:
    """插件基类"""
    
    def __init__(self, name: str):
        self.name = name
    
    def initialize(self, config: Config):
        """初始化插件"""
        pass
    
    def handle_command(self, command: str, args: list) -> bool:
        """处理命令"""
        return False
    
    def handle_error(self, error: dict) -> dict:
        """处理错误"""
        return error

class PluginManager:
    """插件管理器"""
    
    def __init__(self):
        self.plugins = {}
    
    def register_plugin(self, plugin: BasePlugin):
        """注册插件"""
        self.plugins[plugin.name] = plugin
    
    def handle_command(self, command: str, args: list) -> bool:
        """处理命令"""
        for plugin in self.plugins.values():
            if plugin.handle_command(command, args):
                return True
        return False
```

### AI 提供商扩展
```python
# src/ais/ai/base.py
class BaseAIClient:
    """AI 客户端基类"""
    
    def __init__(self, config: dict):
        self.config = config
    
    def chat(self, message: str, context: dict = None) -> str:
        """AI 对话"""
        raise NotImplementedError
    
    def analyze_error(self, error: dict) -> dict:
        """分析错误"""
        raise NotImplementedError
    
    def generate_learning_content(self, topic: str) -> str:
        """生成学习内容"""
        raise NotImplementedError

# 自定义提供商实现
class CustomAIClient(BaseAIClient):
    """自定义 AI 客户端"""
    
    def chat(self, message: str, context: dict = None) -> str:
        # 实现自定义的 AI 对话逻辑
        return self._call_custom_api(message, context)
```

## 🛡️ 安全设计

### 数据安全
- **本地存储**: 所有数据存储在本地 SQLite 数据库
- **敏感信息过滤**: 自动过滤密码、API 密钥等敏感信息
- **数据加密**: 支持数据库加密存储
- **访问控制**: 基于文件权限的访问控制

### 网络安全
- **HTTPS 强制**: 所有外部请求使用 HTTPS
- **证书验证**: 验证 SSL 证书有效性
- **代理支持**: 支持企业代理环境
- **超时控制**: 网络请求超时保护

### 代码安全
- **输入验证**: 严格的输入验证和清理
- **SQL 注入防护**: 使用参数化查询
- **命令注入防护**: 安全的命令执行
- **权限检查**: 最小权限原则

## 📊 性能优化

### 异步处理
```python
# src/ais/core/async_processor.py
class AsyncProcessor:
    """异步处理器"""
    
    def __init__(self, max_workers: int = 3):
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
    
    async def process_analysis(self, command: str, exit_code: int):
        """异步处理分析"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self.executor,
            self._analyze_error,
            command,
            exit_code
        )
```

### 缓存机制
```python
# src/ais/core/cache.py
class Cache:
    """缓存管理器"""
    
    def __init__(self, ttl: int = 3600):
        self.ttl = ttl
        self.cache = {}
    
    def get(self, key: str):
        """获取缓存"""
        if key in self.cache:
            item = self.cache[key]
            if time.time() - item['timestamp'] < self.ttl:
                return item['value']
            else:
                del self.cache[key]
        return None
    
    def set(self, key: str, value: Any):
        """设置缓存"""
        self.cache[key] = {
            'value': value,
            'timestamp': time.time()
        }
```

## 🧪 测试架构

### 测试分层
- **单元测试**: 测试单个组件功能
- **集成测试**: 测试组件间交互
- **端到端测试**: 测试完整用户场景
- **性能测试**: 测试系统性能

### 测试工具
- **pytest**: 测试框架
- **unittest.mock**: 模拟对象
- **pytest-asyncio**: 异步测试
- **pytest-cov**: 覆盖率测试

## 🔮 未来扩展

### 计划中的功能
- **图形化界面**: 基于 Web 的管理界面
- **云端同步**: 配置和数据云端同步
- **多语言支持**: 国际化和本地化
- **插件市场**: 第三方插件生态

### 架构演进
- **微服务化**: 核心功能服务化
- **容器化**: 完整的容器化支持
- **分布式**: 支持分布式部署
- **实时性**: 实时错误分析和反馈

---

## 下一步

- [贡献指南](./contributing) - 参与项目开发
- [测试指南](./testing) - 了解测试流程
- [配置指南](../configuration/) - 了解配置系统

---

::: tip 提示
架构设计注重模块化和可扩展性，新功能应该遵循现有的架构模式。
:::

::: info 设计原则
遵循 SOLID 原则，保持代码的高内聚和低耦合。
:::

::: warning 注意
在修改核心架构时，请确保向后兼容性和充分的测试覆盖。
:::