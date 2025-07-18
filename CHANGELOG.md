# Changelog

所有对此项目的重要更改都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/),
并且此项目遵循 [语义化版本控制](https://semver.org/lang/zh-CN/)。

## [Unreleased]

### Added
- 📋 **系统适配测试文档**：新增完整的多发行版测试验证文档
  - 添加 `.cursor/rules/test.md` 测试文档，涵盖Rocky Linux、Ubuntu、CentOS、Fedora、Debian、openEuler和Kylin Linux等多个版本
  - 提供详细的Python环境安装和配置步骤，确保用户能够顺利安装ais-terminal
  - 统一文档格式，提升可读性和易用性

### Changed
- 🎯 **安装脚本架构全面优化**：基于实际测试验证，重构一键安装脚本
  - **脚本整合**：将 `install_optimized.sh` 合并为主安装脚本 `install.sh`，简化维护
  - **CentOS 7.x 支持增强**：
    - 添加 EPEL 源安装和 OpenSSL 1.1 完整支持
    - 智能修改 configure 文件以兼容 OpenSSL 1.1
    - 编译安装 Python 3.10.9，严格按照手动测试流程实现
  - **Kylin Linux 支持**：
    - 新增 Kylin Linux 系统检测和适配
    - 编译安装 Python 3.10.9 并启用 `--enable-optimizations` 优化选项
    - 完整的依赖包安装流程，确保编译成功
  - **脚本清理**：删除所有测试脚本（test_*.sh）、演示脚本（demo_*.sh）和临时文档文件，保留核心功能脚本
- 🔧 **卸载脚本增强**：完善对编译安装Python环境的支持
  - 新增编译安装 Python 3.10.9 和 Python 3.9 环境的检测和卸载功能
  - 智能询问用户是否删除编译安装的 Python 环境，保护用户数据
  - 完善残留文件清理逻辑，确保完全卸载
- 📖 **全面更新项目文档**：基于实际功能深度重构文档体系，提升用户体验和开发者友好度
  - **主页优化**：更准确地体现项目核心价值 - "上下文感知的错误分析学习助手"
  - **安装指南全面重写**：突出一键安装脚本的自动化能力
    - 强调支持20+种Linux发行版的自动检测和适配
    - 突出CentOS 7.x/Kylin Linux的Python 3.10.9自动编译能力
    - 体现内置免费AI服务，安装后即可使用的便利性
  - **快速开始指南优化**：从5分钟简化为2分钟快速上手
    - 突出自动配置完成：Shell集成、AI服务、配置文件和数据库
    - 更新命令示例为实际可用的CLI命令语法
    - 添加实际功能的验证步骤
  - **功能特性文档更新**：基于源代码分析确保描述准确性
    - 更新安装方式说明，突出一键安装脚本
    - 强调内置免费AI服务，无需配置API密钥
    - 更新多平台支持说明，体现20+发行版自动适配能力
  - **配置文档重构**：基于实际配置文件结构更新
    - 使用真实的TOML配置文件示例
    - 更新为正确的CLI命令语法（`ais config --set key=value`）
    - 添加实际可用的配置选项和AI提供商管理说明
  - **开发贡献指南更新**：符合项目实际开发流程
    - 更新开发环境设置为实际的虚拟环境配置方式
    - 修正代码示例为实际项目结构的导入路径
    - 更新代码质量检查命令为项目实际使用的工具链
    - 强调Keep a Changelog最佳实践和详细的git commit要求

### Fixed
- 🐛 **CentOS 7 Python编译错误修复**：智能版本适配解决老系统兼容性问题
  - 新增 GCC 版本自动检测，GCC < 5.0 或 CentOS ≤ 7 自动使用 Python 3.9.18
  - 修复 profile-opt 编译错误（SystemError: compile returned NULL）
  - 禁用老编译器不支持的 `--enable-optimizations` 选项
  - 使用华为云镜像下载 Python 3.9.18 源码，提升下载稳定性
  - 完善调试模式，显示详细的编译环境信息
  - 解决 runpy 模块导入失败和 SystemError 错误
  - 保持向后兼容，新系统继续使用 Python 3.9.23

## [1.1.0] - 2025-07-18

### Added
- 🚀 **多平台部署支持**：新增对Vercel、Netlify、Cloudflare Pages的完整部署配置
  - 添加`vercel.json`配置文件，支持Vercel自动部署
  - 添加`netlify.toml`配置文件，支持Netlify自动部署并优化缓存
  - 添加`wrangler.toml`配置文件，支持Cloudflare Pages部署
  - 创建`DEPLOYMENT.md`部署指南，详细说明各平台的部署步骤
  - 通过环境变量`VITEPRESS_BASE`实现多平台兼容的路径配置
  - 增强配置检查脚本，支持检查所有平台的部署配置状态
  - 确保GitHub Pages、Vercel、Netlify、Cloudflare Pages四个平台都能正常部署
- 🇨🇳 **国内用户友好支持**：为网络受限用户提供Gitee镜像安装脚本
  - 在所有文档中添加Gitee镜像安装脚本地址
  - 提供更快更稳定的国内访问体验
  - 覆盖README.md、文档首页、FAQ等所有安装相关位置
### Changed
- 🔧 **VitePress配置优化**：支持动态base路径配置
  - 修改`config.mts`支持通过环境变量动态设置base路径
  - 优化图标路径配置，确保在不同平台上正确显示
  - 保持GitHub Pages部署的向后兼容性
### Fixed
- 🎨 **Vercel样式加载问题修复**：解决Vercel部署时样式和资源无法正常加载的问题
  - 通过环境变量配置解决base路径冲突
  - 确保CSS和静态资源在所有平台上正确加载
  - 优化资源缓存策略，提升网站性能

## [1.0.0] - 2025-07-16

### Added
- 🚀 **完整的GitHub Pages文档站点**：基于VitePress构建的现代化文档系统
  - 自动部署工作流，推送代码后自动更新在线文档
  - 响应式设计，支持桌面和移动设备
  - 完整的项目文档结构：快速开始、功能特性、配置指南、开发者指南等
  - 在线访问：https://kangvcar.github.io/ais/
- 🎨 **首页Hero区域图标化按钮**：提升用户体验
  - 🚀 立即体验 - 快速开始使用AIS
  - 📖 了解更多 - 深入了解功能特性  
  - 💻 GitHub - 直接访问源码仓库
- 🖼️ **完整的品牌视觉系统**：统一的logo和图标设计
  - 高质量PNG logo用于网站展示
  - ICO favicon用于浏览器标签页显示
  - 自适应的图标在不同设备上完美显示

### Changed
- 🎨 **现代化首页设计**：重新设计的文档首页界面
  - 简洁大气的Hero区域设计
  - 三个核心功能的终端风格演示
  - 智能错误分析、AI问答、学习报告的真实案例展示
  - 6个用户评价卡片，展示真实用户反馈
- 📱 **优化移动端体验**：确保在所有设备上的良好显示
  - 响应式布局适配不同屏幕尺寸
  - 移动端优化的导航和内容展示
  - 触摸友好的交互设计
- 📋 **更新版权信息**：版权年份更新为2025年

### Fixed  
- 🔧 **GitHub Pages部署问题修复**：解决样式和静态资源加载问题
  - 配置正确的base路径以匹配GitHub Pages URL结构
  - 修复CSS样式404错误，确保网站完整显示
  - 修复logo和favicon路径问题，确保图标正确显示
- 🎯 **导航栏边距修复**：解决导航栏显示异常问题
  - 修复导航栏上边距缺失问题
  - 统一导航栏高度和内边距设置
  - 确保logo与菜单项正确对齐

### Removed
- 📚 **清理无效文档链接**：删除README中指向不存在文件的链接
  - 移除"📚 文档"章节及其死链接
  - 清理指向docs/INSTALLATION.md等不存在文件的引用
  - 保持README简洁准确，避免用户困惑

## [0.3.3] - 2025-07-16

### Changed
- 发布版本 0.3.3

## [0.3.2] - 2025-07-15

### Added
- ✨ **流式输出功能**：优化AI分析用户体验
  - 新增流式显示组件，提供实时进度反馈
  - 支持三种显示模式：progressive（步骤化）、realtime（实时进度条）、spinner（简单转圈）
  - 可通过配置开启/关闭流式输出：`ais config --set enable_streaming=true/false`
  - 可切换输出模式：`ais config --set stream_mode=progressive/realtime/spinner`
  - 改进错误处理，在AI分析失败时显示清晰的错误信息
  - 保持同步处理，避免中断用户操作
- 🎓 **学习功能流式输出**：为 `ais learn` 命令添加流式输出支持
  - 学习过程显示：分析学习需求、收集知识点、生成内容、优化格式、验证质量
  - 支持所有三种显示模式，与错误分析功能保持一致
  - 提供个性化的学习进度提示
- 🤔 **问答功能流式输出**：为 `ais ask` 命令添加流式输出支持
  - 问答过程显示：理解问题、搜索知识、组织答案、生成回答、检查质量
  - 同样支持三种显示模式
  - 优化用户等待体验
### Changed
- 🔧 **优化AI交互流程**：为所有主要AI功能集成流式输出
  - `ais analyze` 命令：显示错误分析实时进度（收集环境上下文、诊断问题根因、生成解决方案等步骤）
  - `ais learn` 命令：显示学习内容生成进度（分析学习需求、收集知识点、生成内容等步骤）
  - `ais ask` 命令：显示问答处理进度（理解问题、搜索知识、组织答案等步骤）
  - 用户可以看到AI处理进度，而不是等待黑屏
  - 统一的用户体验，所有AI功能都支持相同的流式输出配置
- 🎨 **统一learn命令输出格式使用rich Panel**
  - 修改learn命令使用panels.learning_content()方法
  - 保持与ask命令一致的Panel框架式输出风格
  - 提升用户界面的视觉一致性
### Fixed
- 🐛 **修复代码格式问题**：通过autopep8和flake8检查
  - 修正所有代码格式违规问题
  - 确保代码符合PEP8标准

## [0.3.1] - 2025-07-15

### Changed
- 发布版本 0.3.1

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
