# AIS - AI-powered terminal assistant

此项目已重构为标准的 **src-layout** 结构，以提供更好的代码组织和开发体验。

## 项目结构

```
ais/
├── src/                    # 源代码目录
│   └── ais/               # 主Python包
│       ├── __init__.py
│       ├── core/          # 核心功能模块
│       │   ├── __init__.py
│       │   ├── ai.py      # AI交互模块
│       │   ├── config.py  # 配置管理
│       │   ├── context.py # 上下文收集
│       │   └── database.py # 数据库存储
│       ├── cli/           # CLI相关模块
│       │   ├── __init__.py
│       │   ├── main.py    # 主CLI入口
│       │   └── interactive.py # 交互式菜单
│       └── utils/         # 工具函数
│           └── __init__.py
├── tests/                 # 测试目录
│   └── test_basic.py
├── scripts/               # 脚本目录
│   ├── install.sh
│   ├── uninstall.sh
│   └── shell/
│       └── integration.sh
├── docs/                  # 文档目录
│   ├── README.md         # 项目说明
│   ├── DEPLOYMENT_GUIDE.md
│   └── CHANGELOG.md
└── pyproject.toml        # 项目配置
```

## 重构内容

### 1. 目录结构调整

- 将所有源代码移动到 `src/ais/` 目录
- 按功能模块组织代码：
  - `core/` - 核心功能模块
  - `cli/` - CLI相关模块
  - `utils/` - 工具函数
- 将脚本移动到 `scripts/` 目录
- 将文档移动到 `docs/` 目录

### 2. 导入路径更新

- 更新了所有模块间的导入路径以适应新结构
- 修复了相对导入和绝对导入的问题

### 3. 配置文件更新

- 更新了 `pyproject.toml` 以支持 src-layout
- 修复了包路径配置
- 更新了脚本入口点

### 4. 测试更新

- 更新了测试文件以适应新的模块结构
- 所有测试都通过验证

## 安装和使用

### 开发环境安装

```bash
# 克隆项目
git clone https://github.com/kangvcar/ais.git
cd ais

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装开发版本
pip install -e .

# 运行测试
python -m pytest tests/ -v
```

### 使用

安装完成后，您可以直接使用 `ais` 命令：

```bash
# 查看帮助
ais --help

# 查看配置
ais config

# 向AI提问
ais ask "什么是Docker？"

# 学习命令行知识
ais learn git
```

## 功能验证

重构后的项目保持了所有原有功能：

- ✅ AI智能问答
- ✅ 配置管理  
- ✅ 历史记录
- ✅ 学习功能
- ✅ Shell集成
- ✅ 交互式菜单

## 优势

采用 src-layout 后的优势：

1. **更清晰的代码组织** - 源代码与配置文件分离
2. **更好的测试隔离** - 避免测试时导入问题
3. **更标准的Python项目结构** - 符合Python社区最佳实践
4. **更容易的CI/CD集成** - 标准结构便于自动化工具处理
5. **更清晰的依赖关系** - 模块划分更明确

## 向后兼容

重构保持了完全的向后兼容性：

- 所有CLI命令保持不变
- 所有配置文件格式保持不变
- 所有功能行为保持不变
- 安装脚本保持不变