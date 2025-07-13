# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- 🎯 **pipx优先安装策略** - 将pipx作为官方首选安装方式，提供最佳安全性和可维护性
- 🧠 **智能安装检测** - 安装脚本自动检测环境（用户/管理员/容器）并选择最佳安装方式
- 🐳 **完整容器化支持** - 新增Docker镜像、docker-compose配置和专用安装脚本
- 🔍 **安装后健康检查** - 自动验证安装结果并提供诊断信息
- 📚 **按用户类型重构文档** - 文档按个人开发者、团队企业、容器部署、开发贡献等用户类型组织
- 🛠️ **新增专用命令** - 添加`ais-doctor`和`ais-setup`便捷命令
- 📖 **快速开始指南** - 新增5分钟快速上手文档
- 🐳 **Docker部署指南** - 详细的容器化部署文档
- 👨‍💻 **开发指南** - 完整的开发环境设置和贡献流程

### Changed

### Changed
- 🌍 **全局安装默认化** - 安装脚本现在默认进行全局安装，确保所有系统用户都可以使用 AIS
- 🔄 **简化安装选项** - 移除用户级安装选项，统一为全局安装模式
- 📚 **更新安装文档** - 重写 README 安装说明，突出全局安装的优势

### Fixed
- 🔧 **Shell集成脚本缺失问题** - 修复 `ais setup` 命令找不到集成脚本的问题
- 📦 **pipx安装命令兼容性** - 完全移除项目中所有`--global`参数引用，更新为使用PIPX_HOME和PIPX_BIN_DIR环境变量的系统级安装方法
- 🤖 **CI/CD自动化支持** - 安装脚本新增`--non-interactive`参数和CI环境自动检测，解决GitHub Actions等CI环境中的交互式安装问题
- 📁 **包安装路径错误** - 改进脚本路径查找逻辑，支持多种安装场景
- 🌐 **全局安装方案** - 新增 `install_global.sh` 脚本，实现真正的系统级全局安装
- 🔄 **自动错误分析触发** - 修复在某些环境下自动错误分析不工作的问题
- 🔑 **权限问题** - 解决虚拟环境限制导致的全局可用性问题
- 🤖 **AI分析结果显示** - 修复AI分析结果显示为JSON格式的问题，现在正确显示格式化内容和交互式菜单
- 📝 **JSON解析增强** - 改进AI返回内容的解析逻辑，支持各种格式的AI响应
- 🗂️ **交互式菜单 substitute 错误** - 彻底修复选择AI建议时的 'NoneType' object has no attribute 'substitute' 错误
  - 添加 `_safe_escape_for_questionary` 函数，安全转义特殊字符（{}、$）
  - 新增 `_safe_escape_for_rich` 函数，专门处理Rich库的标记语法转义
  - 增强 `show_command_details` 函数的错误处理，为每个Rich组件添加独立的异常捕获
  - 完善所有用户输入的验证和转义，确保None值安全处理
  - 添加全面的异常捕获和降级显示方案，即使部分组件失败也能正常显示基本信息
  - 修复命令选择格式化中的 None 值处理问题
  - 解决Rich Panel和Table组件内部模板处理导致的substitute错误
  - **优化用户体验**: 移除选择菜单选项后的重复命令详情显示，直接执行命令，避免信息冗余
  - **简化交互流程**: 移除多余的风险确认步骤，风险信息已在菜单选项中充分展示
  - **美化视觉效果**: 将命令执行分隔线从等号(=)改为更美观的横线(─)，提升视觉体验
  - **完善历史记录展示**: 为 `ais history` 命令添加索引列，便于用户查看详情
  - **统一历史命令接口**: 实现统一的 `ais history [索引]` 命令，完全替代原有的分离式命令
    - `ais history` 显示历史记录列表（带索引列）
    - `ais history <索引>` 直接查看指定记录的详细分析
    - 移除 `ais history-detail` 命令，统一为单一接口
    - 优化命令行界面的一致性和用户体验，简化命令结构
  - **简化Shell集成命令**: 将 `ais setup-shell` 简化为 `ais setup`，更简洁易记
    - 保持完全相同的功能和行为
    - 更新所有文档和帮助信息
    - 提升命令行界面的简洁性
  - **移除技能级别评估系统**: 完全删除用户技能级别检测功能，改为更智能的上下文驱动排序
    - 删除基于环境变量的简单技能级别判断逻辑（TERM、TMUX、VIM等）
    - 移除 `🧠 智能分析: 💻 intermediate级别` 显示，改为项目类型显示
    - 基于命令复杂度、项目类型、使用历史和环境特征进行智能评分
    - 提供更准确和个性化的命令建议排序
  - **重组Provider管理命令**: 统一provider相关命令的命名规范，提升一致性
    - `ais add-provider` → `ais provider-add`
    - `ais remove-provider` → `ais provider-remove`
    - `ais use-provider` → `ais provider-use`
    - `ais list-provider` → `ais provider-list`
    - 遵循现代CLI设计原则，相关功能命令统一前缀
  - **精简命令集合**: 移除使用率极低的命令，专注核心功能
    - 移除 `ais suggest` 命令 - 功能与 `ais ask` 重叠，使用率较低
    - 移除 `ais which` 命令 - 帮助功能已整合到主帮助系统
    - 简化用户选择，专注核心AI助手功能

### Added
- 📄 **内联集成脚本** - 当找不到外部脚本时自动创建内联版本
- 🚀 **改进的全局安装器** - 支持所有用户无权限问题的系统级安装
- 🔧 **健壮的路径处理** - 改进包文件查找和路径解析逻辑
- ✨ **自动配置功能** - 首次运行任何ais命令时自动设置shell集成和配置
- 🎯 **零配置体验** - 安装后无需手动配置，自动启用所有功能
- 🔄 **智能集成检测** - 自动检测并设置用户的shell配置文件
- 📋 **默认配置生成** - 自动创建带有最佳默认设置的配置文件
- 🎨 **交互式用户体验优化** - 全面重构交互式菜单，包含智能评分、风险评估和个性化建议
- 🧠 **智能建议排序** - 基于风险级别、命令复杂度和用户上下文的多维度评分算法
- 🔄 **上下文驱动的命令排序** - 完全移除技能级别评估，改为基于项目类型、命令复杂度、历史使用模式和环境特征的智能排序系统
- 🎨 **Panel美化输出系统** - 使用rich.Panel为AIS输出添加美观边框，提供清晰的视觉区分和专业的界面体验
  - 完善Panel覆盖范围，包括AI回答、配置信息、provider管理、错误提示等所有AIS输出
  - 统一视觉风格，创建AISPanels类管理所有Panel样式
  - 为不同类型的信息提供颜色编码：蓝色(AI分析)、绿色(成功/建议)、黄色(警告)、红色(错误)、青色(信息)、紫色(配置)

### Planned
- Windows support via WSL
- Plugin system for custom AI providers
- Command suggestion caching
- Web interface for configuration

## [0.1.0] - 2025-07-10

### Added
- 🤖 **自动错误分析** - 命令失败时自动分析原因并提供解决方案
- 💡 **智能建议菜单** - 交互式建议菜单，支持安全等级显示
- 📚 **学习功能** - `ais learn` 命令提供命令行知识教学
- 📖 **历史记录管理** - 完整的命令历史记录和分析查看
- 🎯 **多AI服务商支持** - 支持OpenAI、Ollama等多种AI服务
- 🔧 **Shell集成** - 支持Bash和Zsh的自动错误捕获
- ⚙️ **配置管理** - 灵活的配置系统，支持敏感信息过滤
- 🔒 **隐私保护** - 本地数据存储，敏感信息自动过滤

### Features
- `ais ask` - 向AI提问任何问题
- `ais analyze` - 手动分析命令错误
- `ais history` - 查看命令历史记录
- `ais learn` - 学习命令行知识和技巧
- `ais config` - 配置管理
- `ais on/off` - 开启/关闭自动错误分析
- `ais provider-add` - 添加自定义AI服务商
- `ais provider-remove` - 删除AI服务商
- `ais provider-use` - 切换默认AI服务商
- `ais provider-list` - 列出所有AI服务商
- `ais setup` - 配置shell集成

### Technical
- 基于Click构建的现代CLI界面
- 使用Rich提供美观的终端输出
- SQLModel + SQLite进行本地数据存储
- httpx支持异步HTTP请求和代理
- Questionary提供交互式菜单体验
- 支持Python 3.8+
- 跨平台支持（Linux、macOS）

### Installation
- 一键安装脚本
- pipx包管理器支持
- 自动shell集成配置
- 完整的卸载脚本

### Documentation
- 完整的README文档
- 故障排除指南
- 配置说明和示例
- 安全和隐私说明

[Unreleased]: https://github.com/kangvcar/ais/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/kangvcar/ais/releases/tag/v0.1.0