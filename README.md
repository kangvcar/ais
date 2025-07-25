# AIS - 上下文感知的错误分析学习助手

<div align="center">

![ais](https://socialify.git.ci/kangvcar/ais/image?custom_description=AI%E9%A9%B1%E5%8A%A8%E7%9A%84%E6%99%BA%E8%83%BD%E7%BB%88%E7%AB%AF%E5%8A%A9%E6%89%8B%EF%BC%8C%E8%87%AA%E5%8A%A8%E5%88%86%E6%9E%90%E5%91%BD%E4%BB%A4%E9%94%99%E8%AF%AF%E3%80%81%E6%8F%90%E4%BE%9B%E6%99%BA%E8%83%BD%E8%A7%A3%E5%86%B3%E6%96%B9%E6%A1%88%E3%80%82%0A%E8%AE%A9%E6%AF%8F%E6%AC%A1%E6%8A%A5%E9%94%99%E9%83%BD%E6%98%AF%E6%88%90%E9%95%BF%EF%BC%8C%E8%AE%A9%E6%AF%8F%E4%B8%AA%E9%94%99%E8%AF%AF%E9%83%BD%E6%98%AF%E5%AD%A6%E4%B9%A0&custom_language=Shell&description=1&font=Bitter&forks=1&issues=1&language=1&logo=https%3A%2F%2Fraw.githubusercontent.com%2Fkangvcar%2Fais%2Frefs%2Fheads%2Fmain%2Fdocs%2Fpublic%2Flogo-robot.svg&name=1&owner=1&pattern=Plus&stargazers=1&theme=Auto)

[📖 安装指南](#installation) · [🚀 快速开始](#quickstart) · [🤝 贡献](#contributing)

</div>

## 概述

AIS通过深度Shell集成架构，实现多维上下文感知和智能错误分析，自动收集执行环境信息并进行精准问题定位，在终端内直接提供基于上下文的解决方案和系统化学习指导，消除传统错误处理中的搜索跳转和盲目试错，显著提升问题解决效率和技能积累速度。

### 🌟 核心特性

#### 🔍 智能错误分析
- **自动检测** - 命令失败时自动分析错误原因
- **上下文感知** - 结合当前目录、Git状态、项目类型等环境信息  
- **个性化建议** - 基于用户技能水平提供针对性解决方案
- **安全等级** - 每个建议都标注风险等级，确保操作安全

#### 📚 智能学习系统
- **交互式教学** - 解释"为什么"而不只是"怎么做"
- **主题学习** - 深入学习Git、Docker、Vim等专题知识
- **渐进式内容** - 根据用户水平调整教学深度
- **实践导向** - 提供可执行的命令示例和最佳实践

#### 🎯 智能上下文感知
- **环境感知问答** - `ais ask` 基于当前系统环境提供精准回答
- **三级上下文收集** - minimal/standard/detailed可配置信息收集级别  
- **系统状态分析** - 自动检测硬件配置、网络状态、运行服务
- **项目类型识别** - 结合Git状态、项目文件智能识别技术栈

#### 🔌 强大的集成能力
- **Shell集成** - 支持Bash、Zsh自动错误捕获
- **多AI支持** - 兼容OpenAI、Ollama、Claude等多种AI服务
- **隐私保护** - 本地数据存储，敏感信息自动过滤
- **跨平台** - 支持Linux、macOS

---

## <a id="installation"></a>📦 安装

### 系统要求

- **Python**: 3.8+ （推荐 3.11+）
- **操作系统**: Linux, macOS
- **网络**: 需要网络连接以下载依赖和AI服务
- **空间**: 至少 100MB 可用空间

### ⚡ 一键安装（推荐）

```bash
# 智能安装 - 自动检测环境并选择最佳方式
curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.sh | bash

# 国内用户可使用Gitee镜像（更快更稳定）
curl -sSL https://gitee.com/kangvcar/ais/raw/main/scripts/install.sh | bash
```

**安装脚本会自动：**
- 🔍 检测当前环境（个人/团队/容器）
- 🎯 选择最佳安装方式（pipx用户级/系统级/容器化）
- 📦 安装pipx和AIS
- 🔧 配置shell集成
- ✓ 执行健康检查

### 🗑️ 一键卸载

```bash
# 智能卸载 - 自动检测安装方式并完全清理
curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/uninstall.sh | bash

# 国内用户可使用Gitee镜像
curl -sSL https://gitee.com/kangvcar/ais/raw/main/scripts/uninstall.sh | bash
```

**卸载脚本会自动：**
- 🔍 检测AIS安装方式（pipx用户级/系统级）
- 🗑️ 卸载AIS包和依赖
- 🧹 清理shell集成配置
- 📁 可选择保留或删除用户数据
- ✓ 验证卸载完成

### 🎯 分场景安装

<details>
<summary><b>🐳 Docker容器（推荐 - 零配置）</b></summary>

```bash
# 直接运行最新版本
docker run -it --rm kangvcar/ais:latest

# 或者交互式使用
docker run -it --rm -v $(pwd):/workspace kangvcar/ais:latest bash

# 使用Docker Compose（推荐用于持久化配置）
curl -O https://raw.githubusercontent.com/kangvcar/ais/main/docker-compose.yml
docker-compose up -d ais
docker-compose exec ais bash
```

**优势**: 零配置启动，环境隔离，跨平台一致性，支持ARM64架构

</details>

<details>
<summary><b>👨‍💻 个人开发者（Python环境）</b></summary>

```bash
# 用户级安装（最安全）
curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.sh | bash -s -- --user

# 国内用户可使用Gitee镜像
curl -sSL https://gitee.com/kangvcar/ais/raw/main/scripts/install.sh | bash -s -- --user

# 或手动安装
pipx install ais-terminal
ais setup

# 安装HTML报告可视化功能（可选）
pipx install "ais-terminal[html]"  # 包含plotly图表库
```

**优势**: 最高安全性，独立虚拟环境，无需sudo权限

</details>

<details>
<summary><b>🏢 团队/企业环境</b></summary>

```bash
# 系统级安装（所有用户可用）
curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.sh | bash -s -- --system

# 国内用户可使用Gitee镜像
curl -sSL https://gitee.com/kangvcar/ais/raw/main/scripts/install.sh | bash -s -- --system
```

**优势**: 所有用户可用，保持安全隔离，集中管理和更新

</details>

<details>
<summary><b>🐳 容器/云环境</b></summary>

```bash
# Docker容器化安装
curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/docker-install.sh | bash

# 或直接运行
docker run -it --rm ais-terminal:latest
```

**优势**: 环境一致性，快速部署，易于扩展，完全隔离

</details>

<details>
<summary><b>🔧 开发者/贡献者</b></summary>

```bash
# 源码安装
git clone https://github.com/kangvcar/ais.git
cd ais
pipx install -e .

# 或使用虚拟环境
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,html]"  # 包含开发和HTML可视化依赖
```

**优势**: 实时修改效果，完整开发工具链，易于调试

</details>

### ✓ 验证安装

```bash
# 检查版本
ais --version

# 测试基本功能
ais ask "你好，AIS！"

# 测试自动错误分析（故意输错命令）
mkdirr /tmp/test
```

---

## <a id="quickstart"></a>🚀 快速开始

### 基础配置

```bash
# 查看当前配置
ais config

# 设置上下文收集级别
ais config --set context_level=detailed
```

### 核心功能体验

#### 💬 智能环境感知问答
```bash
# 基于当前系统环境的智能问答
ais ask "我的系统配置如何？硬件性能怎么样？"
ais ask "我的网络连接正常吗？有什么安全建议？"
ais ask "基于我当前的项目类型，如何优化性能？"

# 传统技术问答（仍然支持）
ais ask "如何查看系统内存使用情况？"
ais ask "Docker容器如何挂载目录？"
ais ask "Git合并冲突如何解决？"

# 配置上下文收集级别
ais config --set context_level=minimal   # 基础信息
ais config --set context_level=standard  # 标准信息  
ais config --set context_level=detailed  # 完整信息
```

#### 📖 主题学习
```bash
ais learn git      # 学习Git版本控制
ais learn docker   # 学习容器化技术
ais learn vim      # 学习文本编辑器
ais learn ssh      # 学习远程连接
```

#### 🔍 智能错误分析
```bash
# 这些错误命令会自动触发AI分析
pytho --version        # 拼写错误
ls /not/exist         # 路径不存在
git statuss           # 命令错误
```

#### 📊 学习成长报告
```bash
ais report                     # 生成文本格式学习报告
ais report --html             # 生成HTML可视化报告
ais report --html -o my_report.html --open  # 生成并打开HTML报告

# 历史记录管理
ais history                    # 查看最近的命令记录
ais history --limit 20       # 显示20条命令记录
ais history 3                 # 查看第3条记录的详细分析
```

---

## 📚 详细功能

### 智能环境感知问答 - `ais ask`

基于当前系统环境的智能问答，自动感知硬件配置、网络状态、项目类型等信息：

```bash
# 🖥️ 系统环境感知问答
ais ask "我的系统性能如何？需要优化吗？"
ais ask "当前开放的端口安全吗？"
ais ask "我的网络连接状态如何？"

# 🚀 项目环境感知问答  
ais ask "这个项目是什么类型？如何安装依赖？"
ais ask "基于当前Git状态，我应该如何提交代码？"
ais ask "如何在当前环境下优化这个Python项目？"

# 📚 传统技术问答（仍然支持）
ais ask "Linux文件权限755表示什么？"
ais ask "如何优化Python脚本性能？"
ais ask "Nginx配置反向代理的步骤？"

# ⚙️ 上下文级别配置
ais config --set context_level=minimal   # 基础：系统信息、Git、项目类型
ais config --set context_level=standard  # 标准：+文件列表、命令历史
ais config --set context_level=detailed  # 详细：+网络状态、权限、服务信息

# 📋 查看详细帮助
ais ask --help-detail
```

**新特性亮点**：
- 🧠 **智能上下文收集**：自动检测CPU、内存、网络、服务状态
- 🎯 **环境感知回答**：基于实际系统配置提供针对性建议  
- ⚡ **三级可配置**：从轻量到详细，满足不同场景需求
- 🔒 **隐私保护**：敏感信息自动过滤，安全目录跳过收集

### 学习成长报告 - `ais report`

生成详细的个人化学习成长分析报告，支持文本和可视化HTML两种格式：

```bash
# 📊 文本格式报告（默认）
ais report

# 📈 HTML可视化报告（推荐）
ais report --html
ais report --html -o custom_report.html
ais report --html --open  # 生成后自动打开浏览器

# 📋 查看详细帮助
ais report --help
```

#### 🌟 HTML可视化报告特性

**6种专业图表类型**：
- 📈 **错误趋势图**：30天错误变化趋势，识别学习进步轨迹
- 🎯 **技能评估雷达图**：多维度技能水平可视化展示
- ⏰ **时间热力图**：错误发生时间分布，发现学习时间规律
- 📊 **命令频次图**：最常出错命令排序，重点学习优化
- 🔍 **错误类型分布**：饼图展示错误模式，针对性改进
- 📈 **学习进度趋势**：双轴图展示错误减少和技能提升

**现代化用户体验**：
- 🎨 **响应式设计**：完美适配桌面、平板、手机
- 🖱️ **交互式图表**：支持悬停提示、缩放、数据钻取
- 💡 **AI智能洞察**：个性化分析和改进建议
- 🌐 **浏览器友好**：支持所有现代浏览器，无需额外插件

**灵活配置选项**：
```bash
# 自定义输出文件名
ais report --html -o "2024-学习报告.html"

# 生成后自动打开浏览器查看
ais report --html --open

# 组合使用
ais report --html -o weekly_progress.html --open
```

**数据安全保证**：
- 📊 所有数据本地生成，无云端上传
- 🔒 敏感信息自动过滤
- 📁 支持离线查看和分享

### 知识学习 - `ais learn`

系统学习命令行工具和概念：

```bash
ais learn              # 查看所有可学习主题
ais learn git          # Git版本控制完整教程
ais learn docker       # 容器化技术深度学习
ais learn linux        # Linux系统管理基础
```

### AI服务商管理

支持多种AI服务商，灵活切换：

```bash
# 查看可用服务商
ais provider-list

# 添加本地Ollama服务
ais provider-add ollama \
  --url http://localhost:11434/v1/chat/completions \
  --model llama3

# 切换服务商
ais provider-use ollama
```

### Shell集成配置

AIS支持自动错误分析，需要配置Shell集成：

```bash
# 自动配置
ais setup

# 测试集成是否正常工作
ais test-integration
```

---

## ⚙️ 高级配置

### 智能上下文收集设置

分别控制错误分析和ask问答的上下文信息收集：

```bash
# 错误分析上下文级别（自动分析功能）
ais config --set context_level=minimal    # 基本信息
ais config --set context_level=standard   # 标准信息（默认）
ais config --set context_level=detailed   # 详细信息

# ask问答上下文级别（新增功能）
ais config --set ask.context_level=minimal   # 系统基础信息
ais config --set ask.context_level=standard  # +项目和Git信息
ais config --set ask.context_level=detailed  # +网络、权限、服务信息

# 控制自动分析
ais config --set auto_analysis=true       # 开启自动分析
ais config --set auto_analysis=false      # 关闭自动分析

# 查看当前配置
ais config
```

**上下文收集详情**：

| 级别 | 错误分析包含 | ask问答包含 |
|------|-------------|-------------|
| **minimal** | 命令、退出码、目录、用户 | 系统信息、CPU/内存、网络连通性、监听端口、运行服务 |
| **standard** | +文件列表、Git状态、命令历史 | +项目类型、Git详情、文件列表 |
| **detailed** | +系统信息、环境变量、完整目录 | +权限信息、详细网络状态、完整环境信息 |

### 隐私和安全

AIS重视用户隐私和数据安全：

- **本地存储** - 所有数据存储在本地SQLite数据库
- **敏感信息过滤** - 自动过滤密码、密钥等敏感信息
- **可配置的上下文级别** - 用户可控制信息收集范围
- **开源透明** - 完全开源，代码公开透明

---

## 🆕 最新功能亮点

### 📊 HTML可视化报告系统 (v2.5.2)

AIS现在支持生成专业的HTML可视化学习报告，将枯燥的数据转化为直观美观的图表：

#### 🎨 **现代化可视化设计**
```bash
$ ais report --html --open

# 自动生成包含以下图表的HTML报告：
📈 错误趋势分析 - 清晰展示30天学习进步轨迹
🎯 技能评估雷达图 - 多维度技能水平一目了然  
⏰ 时间分布热力图 - 发现最佳学习时间段
📊 命令频次统计 - 识别需要重点改进的命令
🔍 错误类型分析 - 针对性解决常见问题
📈 学习进度趋势 - 量化展示技能成长
```

#### 💻 **交互式用户体验**
- **响应式设计**: 完美支持桌面、平板、手机
- **交互式图表**: 悬停查看详情，缩放探索数据
- **AI智能洞察**: 个性化分析每个图表背后的含义
- **一键分享**: 生成静态HTML文件，轻松分享学习成果

#### 🔧 **灵活配置选项**
```bash
# 快速生成并查看
ais report --html --open

# 自定义文件名
ais report --html -o "我的技能成长报告.html"

# 适用场景
ais report --html -o weekly_report.html    # 周报
ais report --html -o monthly_review.html   # 月度回顾
ais report --html -o skill_assessment.html # 技能评估
```

### 🧠 智能上下文感知系统 (v2.4.0)

AIS现在能够智能感知你的系统环境，提供基于实际情况的精准建议：

#### 📊 **系统状态感知**
```bash
$ ais ask "我的系统配置如何？"

# AI会自动分析并回答：
✓ 操作系统: Ubuntu 24.04.2 LTS
✓ CPU: 4核 Intel Xeon Platinum  
✓ 内存: 7.1G 总内存，3.5G 已使用，3.6G 可用
✓ 磁盘: 40G 总空间，4.1G 已使用 (11%)
✓ 网络: 可连接 (ping 8.8.8.8)
```

#### 🔐 **安全状态分析**  
```bash
$ ais ask "我的系统开放了哪些端口？安全吗？"

# AI会分析端口安全性并提供建议：
✓ SSH (22): 安全，建议使用密钥认证
✓ DNS (53): 注意防范DNS放大攻击
✓ 其他端口: 提供具体的安全配置建议
```

#### 🚀 **项目优化建议**
```bash  
$ ais ask "基于我的系统环境，如何优化这个Python项目？"

# AI会结合系统配置和项目类型提供优化方案：
✓ 利用4核CPU进行并行处理 (multiprocessing)
✓ 基于内存情况优化数据处理策略
✓ 根据网络状态优化远程API调用
```

#### ⚙️ **灵活配置级别**
- **Minimal**: 系统基础信息 + 网络状态 + 运行服务
- **Standard**: + 项目类型 + Git状态 + 文件列表  
- **Detailed**: + 权限信息 + 详细网络 + 完整环境

---

## 🏗️ 项目架构

```
ais/
├── src/ais/              # 主要源代码
│   ├── cli/              # CLI界面模块
│   │   ├── main.py       # 主CLI入口
│   │   └── interactive.py # 交互式菜单
│   ├── core/             # 核心功能模块
│   │   ├── ai.py         # AI交互模块
│   │   ├── config.py     # 配置管理
│   │   ├── context.py    # 上下文收集
│   │   └── database.py   # 数据库操作
│   ├── ui/               # 用户界面
│   │   └── panels.py     # 显示面板
│   └── utils/            # 工具函数
├── scripts/              # 安装和部署脚本
├── tests/                # 测试文件
├── docs/                 # 文档目录
└── pyproject.toml        # 项目配置
```

### 核心模块

- **CLI模块** (`src/ais/cli/`): 命令行接口和交互式界面
- **Core模块** (`src/ais/core/`): AI服务集成、配置管理、上下文收集、数据库操作
- **UI模块** (`src/ais/ui/`): Rich库显示面板和格式化

---

---

## 🧪 开发和测试

### 开发环境设置

```bash
# 克隆仓库
git clone https://github.com/kangvcar/ais.git
cd ais

# 创建虚拟环境
python3 -m venv .venv
source .venv/bin/activate

# 安装开发版本和依赖
pip install -e ".[dev]"

# 设置pre-commit
pre-commit install
```

### 运行测试

```bash
# 运行所有测试
python -m pytest tests/ -v

# 运行覆盖率测试
python -m pytest --cov=ais tests/

# 代码质量检查
source .venv/bin/activate && black src/ tests/
source .venv/bin/activate && flake8 src/ tests/ --max-line-length=100
```

---

## <a id="contributing"></a>🤝 贡献指南

我们欢迎所有形式的贡献！

### 如何参与

1. **Fork** 这个仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 **Pull Request**

### 开发规范

- 遵循 [PEP 8](https://pep8.org/) 代码风格
- 为新功能添加测试用例
- 更新相关文档
- 提交信息使用清晰的描述

### 代码质量

确保代码符合项目标准：

```bash
# 自动代码格式化
source .venv/bin/activate && autopep8 --in-place --aggressive --aggressive --max-line-length=100 src/ tests/ -r

# 运行所有质量检查
python -m pytest tests/ -v
source .venv/bin/activate && black src/ tests/
source .venv/bin/activate && flake8 src/ tests/ --max-line-length=100
```

---

## 🆘 获取帮助

### 自助资源

```bash
# 测试系统集成
ais test-integration

# 查看版本信息
ais --version

# 查看所有帮助
ais help-all
```

### 社区支持

- 📚 [完整文档](docs/)
- 💬 [GitHub Discussions](https://github.com/kangvcar/ais/discussions) - 交流讨论
- 🐛 [GitHub Issues](https://github.com/kangvcar/ais/issues) - 问题反馈
- 📧 [邮件支持](mailto:ais@example.com) - 直接联系

### 报告问题

报告问题时请提供：
- 操作系统和版本
- Python版本 (`python3 --version`)
- AIS版本 (`ais --version`)
- 安装方式（pipx/Docker/源码）
- 完整错误信息
- 复现步骤

---

## 📝 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

## 🎉 鸣谢

感谢所有为这个项目做出贡献的开发者们！

### 技术栈

- **Python 3.8+** - 核心语言
- **Click** - 命令行界面框架
- **Rich** - 终端美化和格式化
- **SQLModel** - 数据库ORM
- **httpx** - HTTP客户端
- **Plotly** - 交互式图表可视化（HTML报告）
- **NumPy** - 数值计算支持（可视化依赖）
- **pytest** - 测试框架

---

<div align="center">

**🎉 让AI成为你的终端伙伴，让命令行学习变得简单而有趣！**

如果觉得有用，请给我们点个 ⭐️ 支持！

[![Stars](https://img.shields.io/github/stars/kangvcar/ais?style=social)](https://github.com/kangvcar/ais/stargazers)
[![Forks](https://img.shields.io/github/forks/kangvcar/ais?style=social)](https://github.com/kangvcar/ais/network/members)

[回到顶部](#ais---上下文感知的错误分析学习助手)

</div>