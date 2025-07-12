# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed
- 🔧 **Shell集成脚本缺失问题** - 修复 `ais setup-shell` 命令找不到集成脚本的问题
- 📁 **包安装路径错误** - 改进脚本路径查找逻辑，支持多种安装场景
- 🌐 **全局安装方案** - 新增 `install_global.sh` 脚本，实现真正的系统级全局安装
- 🔄 **自动错误分析触发** - 修复在某些环境下自动错误分析不工作的问题
- 🔑 **权限问题** - 解决虚拟环境限制导致的全局可用性问题
- 🤖 **AI分析结果显示** - 修复AI分析结果显示为JSON格式的问题，现在正确显示格式化内容和交互式菜单
- 📝 **JSON解析增强** - 改进AI返回内容的解析逻辑，支持各种格式的AI响应

### Added
- 📄 **内联集成脚本** - 当找不到外部脚本时自动创建内联版本
- 🚀 **改进的全局安装器** - 支持所有用户无权限问题的系统级安装
- 🔧 **健壮的路径处理** - 改进包文件查找和路径解析逻辑
- ✨ **自动配置功能** - 首次运行任何ais命令时自动设置shell集成和配置
- 🎯 **零配置体验** - 安装后无需手动配置，自动启用所有功能
- 🔄 **智能集成检测** - 自动检测并设置用户的shell配置文件
- 📋 **默认配置生成** - 自动创建带有最佳默认设置的配置文件

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
- `ais history-detail` - 查看详细的历史分析
- `ais learn` - 学习命令行知识和技巧
- `ais suggest` - 根据任务描述获取命令建议
- `ais config` - 配置管理
- `ais on/off` - 开启/关闭自动错误分析
- `ais add-provider` - 添加自定义AI服务商
- `ais remove-provider` - 删除AI服务商
- `ais use-provider` - 切换默认AI服务商
- `ais list-provider` - 列出所有AI服务商
- `ais setup-shell` - 配置shell集成

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