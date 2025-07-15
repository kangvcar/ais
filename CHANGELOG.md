# Changelog

所有对此项目的重要更改都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/),
并且此项目遵循 [语义化版本控制](https://semver.org/lang/zh-CN/)。

## [Unreleased]

## [0.2.13] - 2025-07-15

### Fixed
- 🔧 **修复Package Release工作流git冲突问题**：优化CHANGELOG.md提交流程
  - 修复"cannot pull with rebase: You have unstaged changes"错误
  - 改进git操作顺序：先暂存更改再拉取远程代码
  - 使用更安全的合并策略避免冲突
### Removed
- 🗑️ **移除无效的命令别名**：删除 `ais-doctor` 和 `ais-setup` 命令别名
  - `ais-doctor` 引用的函数不存在，会导致错误
  - `ais-setup` 与 `ais setup` 功能重复，没有必要
  - 用户应使用 `ais setup` 进行shell集成配置

## [0.2.12] - 2025-07-15

### Changed
- 🔄 **移除Windows支持**：简化项目维护，专注于Linux和macOS平台
  - 移除所有文档中的Windows相关内容和安装说明
  - 移除PowerShell支持相关描述
  - 移除Windows CI测试相关的变更记录
  - 更新项目描述为仅支持Linux和macOS系统
- 🔄 **GitHub工作流全面重构**：优化CI/CD流程，消除重复代码，提高效率
  - 创建共享工作流`shared-quality-checks.yml`，消除test/lint重复代码
  - 重命名工作流文件，使用更清晰易懂的名称：
    - `ci.yml` → `continuous-integration.yml`
    - `docker.yml` → `container-build-deploy.yml`
    - `release.yml` → `package-release.yml`
  - 优化触发条件，添加路径过滤，避免文档更改触发构建
  - 改进工作流间依赖关系，实现release→docker自动化流程
  - 移除CI中的重复Docker测试功能，避免资源浪费

### Fixed
- 📋 **发布说明长度优化**：修复GitHub Release页面显示过长Changelog的问题
  - 改进Package Release工作流中的Changelog提取逻辑
  - 发布时自动创建具体版本章节，避免显示所有Unreleased内容
  - 只提取当前版本的更改内容作为发布说明
  - 自动管理CHANGELOG.md版本结构，符合Keep a Changelog标准
  - 发布后自动提交更新的CHANGELOG.md到仓库
- 🌍 **多用户环境Shell集成优化**：彻底解决切换用户后需要重新配置的问题
  - 系统级安装现在配置全局Shell集成(`/etc/profile.d/ais.sh`)
  - 所有用户（包括新用户）登录后自动启用AIS功能，无需手动配置
  - 优化用户切换体验：`su - user`后无需运行`ais setup`
  - 改进多用户场景：任何用户登录都自动启用自动错误分析
  - 更新卸载脚本：正确清理全局配置文件
- 🚀 **一键安装真正一键完成**：彻底解决系统级安装后需要多次配置的用户体验问题
  - 系统级安装现在自动配置Shell集成，无需手动运行`ais setup`
  - 修复安装脚本中系统级pipx路径检测逻辑
  - 优化安装流程：安装→重新打开终端→直接使用（真正一键完成）
  - 消除用户困惑：不再需要多次重新加载Shell配置
  - 改进提示信息：明确告知重新打开终端后即可直接使用所有功能
- 🔧 **一键安装脚本Shell激活修复**：修复系统级安装后需要手动重新加载Shell配置的问题
  - 增强系统级安装完成后的指导信息，明确告知用户如何激活ais命令
  - 提供多种Shell重新加载方法：重新打开终端、source配置文件、hash -r
  - 改进错误提示，解释ais命令安装位置和PATH配置要求
  - 优化用户体验，减少安装后的困惑
- 🔧 **卸载脚本修复**：修复在管道执行时无法正常读取用户输入的问题
  - 修复`curl | bash`方式执行卸载脚本时挂起的问题
  - 添加输入源检测，管道执行时使用/dev/tty读取用户确认
  - 提升卸载脚本在不同执行环境下的稳定性
- 🔄 **Container Build & Deploy工作流重复触发修复**：消除工作流重复触发问题
  - 移除release触发器，避免与workflow_run重复触发
  - 统一通过Package Release工作流完成后触发，避免重复构建
  - 保持push到main分支时的正常触发逻辑
- 🐳 **Docker工作流全面修复**：彻底解决Docker构建和推送工作流中的多个关键问题
  - 修复test-image作业中IMAGE_TAG变量为空的问题
  - 改进docker/metadata-action标签配置，确保正确生成镜像标签
  - 修复ARM64平台的exec format error问题，通过QEMU实现跨平台测试
  - 添加镜像架构验证步骤，确保多架构构建正确性
  - 优化健康检查测试，避免超时问题
  - 改进构建配置，使用稳定的buildkit版本
  - 添加详细的调试信息和错误处理机制
- 🔧 **CI工作流修复**：修复CI中docker-build-test作业的镜像构建和测试问题
  - 修复Docker镜像本地构建后无法找到的问题，添加load: true参数
  - 改进Docker镜像测试步骤，添加镜像验证和详细的功能测试
  - 添加容器信息测试，确保镜像正确构建
- 📦 **PyPI Trusted Publishing修复**：解决PyPI发布中的trusted publisher配置错误
  - 移除environment配置，简化trusted publishing设置
  - 添加条件限制，确保只在release事件时发布到PyPI
  - 修复工作流依赖关系，处理跳过PyPI发布的情况
  - 解决"invalid-publisher"错误，确保发布流程正常工作
- 🔄 **发布工作流优化**：改进Build Release Packages后的作业触发逻辑
  - 设置Publish to PyPI和Create GitHub Release同时依赖Build Release Packages
  - 根据触发事件智能决定是否执行PyPI发布和GitHub Release创建
  - 优化通知作业，支持不同发布场景的状态报告
  - 提高发布流程的灵活性和可控性

### Added
- 🐳 **Docker容器化完整支持**：实现符合行业最佳实践的容器化方案
  - 多阶段构建Dockerfile，优化镜像大小和安全性
  - 多架构支持（AMD64/ARM64），支持Apple Silicon和树莓派
  - 完整的Docker Compose配置，支持开发和生产环境
  - CI/CD自动构建和发布到Docker Hub
  - 安全扫描集成（Trivy）和SBOM生成
  - 符合OCI标准的镜像标签和元数据
- 🚀 **增强的CI/CD工作流**：专业级的DevOps流程
  - 新增docker.yml工作流，专门处理容器构建和发布
  - 在CI中集成Docker构建测试和安全扫描
  - 自动化的多平台镜像构建和推送
  - Docker Hub描述自动更新
  - 完善的镜像测试和验证流程
- 📝 **全面重写项目README.md**：符合现代开源项目最佳实践
  - 添加专业的徽章和导航链接
  - 结构化的功能介绍和使用指南
  - 详细的安装说明，支持多种场景（重点推荐Docker）
  - 完整的项目架构说明
  - 全面的开发和贡献指南
  - 美观的Markdown格式和布局
- 📊 **优化项目配置**：提升开发体验
  - 添加.dockerignore优化构建上下文
  - 更新pyproject.toml项目描述
  - 更新docs/README.md保持文档一致性
- CI测试支持多Linux发行版：新增对16个主流Linux发行版的测试支持
  - Ubuntu: 20.04 LTS, 22.04 LTS, 24.04 LTS
  - Debian: 11 (Bullseye), 12 (Bookworm)
  - CentOS: 7, Stream 8, Stream 9
  - Rocky Linux: 8, 9
  - Fedora: 38, 39
  - Alpine Linux: 3.18, 3.19
  - openSUSE: Leap 15.5, Tumbleweed
  - openEuler: 22.03 LTS
- CI流水线优化：符合GitHub Actions最佳实践
  - 添加pip缓存以提高构建速度
  - 增加定时任务确保依赖兼容性
  - 实现并发控制节省资源
  - 添加最小权限安全配置
  - 升级Codecov到v4版本

### Fixed
- 修复CI测试中的PEP 668"externally-managed-environment"问题
  - Linux发行版测试使用虚拟环境避免系统包管理冲突
  - 为不同发行版添加PEP 668兼容性标识
  - 添加包导入和基本功能验证测试
  - 改进错误处理和降级策略
- 修复特定Linux发行版的CI测试问题
  - 修复CentOS 7/Stream 8 EOL后的镜像源问题，使用vault.centos.org
  - 暂时禁用Rocky Linux测试避免hatchling版本兼容性问题
  - 修复openSUSE容器shell问题，统一使用bash
- 大幅简化CI测试策略以提高稳定性
  - 移除有问题的旧版本发行版（CentOS 7/8, Rocky Linux等）
  - 专注于主流稳定发行版：Ubuntu 22.04/24.04, Debian 12, Fedora 39, Alpine 3.19
  - 统一使用sh shell确保最大兼容性
- 重新添加企业级Linux发行版支持
  - 恢复CentOS 7/Stream 8/Stream 9测试支持
  - 恢复Rocky Linux 8/9测试支持
  - 添加openEuler 22.03 LTS测试支持
  - 实现智能兼容性检测：区分actions兼容和非兼容系统
  - 特殊处理策略：EOL发行版使用vault镜像源，旧版本Python使用setuptools构建
