# AIS 开发指南

本指南帮助开发者快速搭建 AIS 开发环境并参与项目贡献。

## 🛠️ 开发环境设置

### 前置要求
- **Python**: 3.8+ （推荐 3.11+）
- **Git**: 最新版本
- **pipx**: 用于隔离安装（推荐）

### 1. 克隆项目
```bash
# 克隆主仓库
git clone https://github.com/kangvcar/ais.git
cd ais

# 或克隆你的fork
git clone https://github.com/your-username/ais.git
cd ais
```

### 2. 设置开发环境

#### 方式一：使用pipx（推荐）
```bash
# 开发模式安装
pipx install -e .

# 安装开发依赖
pipx install -e ".[dev]"

# 验证安装
ais --version
```

#### 方式二：使用虚拟环境
```bash
# 创建虚拟环境
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或 .venv\Scripts\activate  # Windows

# 安装项目和开发依赖
pip install -e ".[dev]"

# 验证安装
ais --version
```

### 3. 设置开发工具

#### Pre-commit钩子
```bash
# 安装pre-commit钩子
pre-commit install

# 手动运行检查
pre-commit run --all-files
```

#### IDE配置
推荐使用VSCode，项目包含以下配置：
- Python解释器设置
- 代码格式化配置
- 调试配置
- 测试配置

## 🧪 运行测试

### 基础测试
```bash
# 运行所有测试
python -m pytest tests/ -v

# 运行特定测试
python -m pytest tests/test_ai.py -v

# 运行测试并生成覆盖率报告
python -m pytest --cov=ais tests/ --cov-report=html
```

### 集成测试
```bash
# 测试安装功能
python -m pytest tests/test_installation.py -v

# 测试CLI功能
python -m pytest tests/test_cli_main.py -v
```

### 端到端测试
```bash
# 测试完整工作流
./scripts/test_installation.sh
```

## 🎨 代码质量

### 代码格式化
```bash
# 使用black格式化代码
source .venv/bin/activate && black src/ tests/

# 使用autopep8自动修复
source .venv/bin/activate && autopep8 --in-place --aggressive --aggressive --max-line-length=79 src/ tests/ -r
```

### 代码检查
```bash
# flake8语法检查
source .venv/bin/activate && flake8 src/ tests/ --max-line-length=79

# mypy类型检查
source .venv/bin/activate && mypy src/ais/ || echo "MyPy check completed with warnings"
```

### 一键质量检查
```bash
# 运行所有质量检查
./scripts/check_quality.sh
```

## 🏗️ 项目架构

### 目录结构
```
ais/
├── src/ais/              # 主要源代码
│   ├── __init__.py       # 包初始化
│   ├── cli/              # CLI界面模块
│   │   ├── __init__.py
│   │   ├── main.py       # 主CLI入口
│   │   └── interactive.py # 交互式界面
│   ├── core/             # 核心功能模块
│   │   ├── __init__.py
│   │   ├── ai.py         # AI交互
│   │   ├── config.py     # 配置管理
│   │   ├── context.py    # 上下文收集
│   │   └── database.py   # 数据库操作
│   ├── shell/            # Shell集成
│   │   └── integration.sh
│   ├── ui/               # 用户界面
│   │   ├── __init__.py
│   │   └── panels.py     # 显示面板
│   └── utils/            # 工具函数
│       └── __init__.py
├── tests/                # 测试文件
├── scripts/              # 安装和部署脚本
├── docs/                 # 文档目录
├── Dockerfile            # Docker配置
├── docker-compose.yml    # Docker Compose配置
└── pyproject.toml        # 项目配置
```

### 核心模块说明

#### 1. CLI模块 (`src/ais/cli/`)
- `main.py`: 主命令行接口，处理所有命令
- `interactive.py`: 交互式菜单和界面

#### 2. 核心模块 (`src/ais/core/`)
- `ai.py`: AI服务集成，支持多个提供商
- `config.py`: 配置文件管理
- `context.py`: 命令上下文和环境信息收集
- `database.py`: SQLite数据库操作

#### 3. UI模块 (`src/ais/ui/`)
- `panels.py`: Rich库显示面板和格式化

## 📝 开发规范

### 代码风格
- 遵循 [PEP 8](https://pep8.org/) 规范
- 使用 [Black](https://black.readthedocs.io/) 进行代码格式化
- 最大行长度：79字符
- 使用类型注解

### 提交规范
遵循 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```bash
# 功能添加
git commit -m "feat: 添加Docker支持"

# Bug修复
git commit -m "fix: 修复配置文件读取问题"

# 文档更新
git commit -m "docs: 更新安装指南"

# 重构
git commit -m "refactor: 重构AI模块"

# 测试
git commit -m "test: 添加CLI测试用例"
```

### 分支策略
- `main`: 主分支，稳定版本
- `develop`: 开发分支，最新功能
- `feature/*`: 功能分支
- `fix/*`: 修复分支
- `docs/*`: 文档分支

## 🔧 常见开发任务

### 添加新的AI提供商
1. 在 `src/ais/core/ai.py` 中添加新提供商类
2. 实现统一的接口方法
3. 添加配置支持
4. 编写测试用例
5. 更新文档

### 添加新的CLI命令
1. 在 `src/ais/cli/main.py` 中添加命令函数
2. 添加Click装饰器和参数
3. 实现命令逻辑
4. 添加帮助文档
5. 编写测试用例

### 修改配置系统
1. 更新 `src/ais/core/config.py`
2. 添加配置验证
3. 更新默认配置
4. 添加迁移逻辑（如需要）
5. 更新文档

## 🐛 调试技巧

### 启用调试模式
```bash
# 详细日志输出
ais --debug ask "test question"

# 环境变量调试
export AIS_DEBUG=1
ais ask "test"
```

### 常用调试工具
```bash
# 查看配置
ais config show

# 检查数据库
sqlite3 ~/.config/ais/ais.db ".tables"

# 查看shell集成状态
ais setup --check
```

### 问题排查
1. **导入错误**: 检查虚拟环境和依赖安装
2. **配置问题**: 检查配置文件权限和格式
3. **API调用失败**: 检查网络连接和API密钥
4. **Shell集成不工作**: 检查shell配置文件

## 🚀 发布流程

### 版本管理
1. 更新版本号（`src/ais/__init__.py`和`pyproject.toml`）
2. 更新 `docs/CHANGELOG.md`
3. 创建版本标签
4. 构建和测试

### 构建和发布
```bash
# 构建包
python -m build

# 检查包
twine check dist/*

# 发布到PyPI（需要权限）
twine upload dist/*
```

### Docker镜像
```bash
# 构建镜像
docker build -t ais-terminal:latest .

# 测试镜像
docker run -it --rm ais-terminal:latest ais --version

# 发布镜像（需要权限）
docker push ais-terminal:latest
```

## 🤝 贡献流程

### 1. 准备工作
- Fork项目到你的GitHub账号
- 克隆你的fork到本地
- 创建功能分支

### 2. 开发
- 编写代码和测试
- 遵循代码规范
- 运行所有测试
- 更新文档

### 3. 提交
- 提交代码到你的分支
- 推送到你的GitHub fork
- 创建Pull Request

### 4. 代码审查
- 响应审查意见
- 修改代码（如需要）
- 等待合并

## 📚 学习资源

### Python开发
- [Python官方文档](https://docs.python.org/)
- [Click库文档](https://click.palletsprojects.com/)
- [Rich库文档](https://rich.readthedocs.io/)

### 测试
- [pytest文档](https://pytest.org/)
- [unittest.mock](https://docs.python.org/3/library/unittest.mock.html)

### 工具
- [Black代码格式化](https://black.readthedocs.io/)
- [flake8代码检查](https://flake8.pycqa.org/)
- [pre-commit钩子](https://pre-commit.com/)

## 🆘 获取帮助

### 开发相关问题
- 查看 [GitHub Issues](https://github.com/kangvcar/ais/issues)
- 搜索 [GitHub Discussions](https://github.com/kangvcar/ais/discussions)
- 阅读现有代码和注释

### 联系方式
- 💬 [GitHub Discussions](https://github.com/kangvcar/ais/discussions)
- 📧 [邮件联系](mailto:ais@example.com)
- 🐛 [报告Bug](https://github.com/kangvcar/ais/issues/new)

---

🚀 **感谢你对AIS项目的贡献！** 每一个提交都让这个项目变得更好。