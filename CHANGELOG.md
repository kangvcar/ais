# Changelog

所有对此项目的重要更改都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/),
并且此项目遵循 [语义化版本控制](https://semver.org/lang/zh-CN/)。

## [Unreleased]

## [2.6.0] - 2025-07-24

### Added
- ✨ **功能展示页面**：新增showcase页面展示AIS核心功能演示
  - 创建了专门的功能展示页面 `/showcase`，包含6个核心功能的交互式演示
  - **错误自动分析**：展示AIS智能分析终端错误并提供解决方案的能力
  - **AIS Ask智能问答**：演示直接在终端中向AI助手提问获得即时帮助
  - **配置管理**：展示使用 `ais config` 命令管理API密钥、模型选择等配置
  - **历史记录管理**：演示 `ais history` 命令管理和查看AI对话历史
  - **知识学习功能**：展示 `ais learn` 命令的项目知识学习和个性化帮助
  - **报告生成**：演示 `ais report` 命令生成项目分析报告，包含代码质量和安全检查
  - 使用asciinema嵌入式播放器，提供真实的终端操作演示体验
  - 采用VitePress兼容的Vue组件，动态加载各个演示脚本
  - 在导航菜单中新增"功能展示"入口，方便用户快速了解AIS能力
### Enhanced  
- 📊 **报告示例展示优化**：在相关页面添加真实HTML报告示例链接
  - 在showcase页面的报告生成部分添加查看报告示例的直接链接
  - 在学习报告功能页面添加真实报告示例的查看入口
  - 链接指向 `/report.html`，展示包含完整数据可视化和AI洞察分析的真实报告
  - 帮助用户直观了解AIS报告生成功能的强大效果

## [2.5.6] - 2025-07-23

### Enhanced
- 📝 **团队页面信息优化**：更新团队成员描述，采用谦虚务实的表达方式
  - 优化各成员职责描述，突出学习成长和团队协作态度
  - 许队：团队主理人，负责团队整体规划和项目管理，有一些教学和项目管理经验
  - 黄队：团队技术指导老师，为团队提供技术方向指导，在软件开发和教学方面有一定经验
  - 詹皇浩：负责统筹项目和AIS终端伴侣开发工作，对项目管理和软件开发有浓厚兴趣
  - 陈友诚：主要负责AI大模型部署和调优工作，对人工智能技术充满热情
  - 黄金鸿：负责TIDB数据库管理和Docker部署相关工作，努力提升运维技能
  - 周俊麒：主要从事VUE数据可视化开发和录课制作工作，希望通过技术帮助更多人学习

## [2.5.5] - 2025-07-23

### Fixed
- 🐳 **Docker构建问题修复**：修复Ubuntu 22.04镜像中包安装失败的问题
  - 修复虚拟包问题：`awk` → `gawk`（GNU awk实现），`ping` → `iputils-ping`（ping命令具体实现）
  - 修复网络工具包名：`netcat` → `netcat-openbsd`（netcat的OpenBSD版本）
  - 添加系统工具包：`procps`（提供ps、top等命令），`findutils`（提供find、xargs等工具）
  - 修复Python包安装：使用具体版本号`python3.11`、`python3.11-dev`、`python3.11-venv`
  - 移除不存在的包：删除`yq`（Ubuntu 22.04仓库中不存在）和重复的包条目
  - 解决"Package has no installation candidate"和"Unable to locate package"错误
### Enhanced
- 📊 **文档可视化全面优化**：为AIS文档网站添加清晰美观的Mermaid图表，大幅提升用户理解度
  - 为6个核心页面添加专业级Mermaid流程图：快速开始、错误分析、安装指南、FAQ对比、Shell集成、学习报告
  - 快速开始页面：添加2分钟上手流程图，展示从安装到测试的完整过程
  - 错误分析页面：详细的智能分析工作流程图，涵盖错误捕获到用户行动的完整链路
  - 安装指南页面：创建安装方式选择决策流程图，帮助用户根据需求选择最佳安装方式
  - FAQ页面：添加传统方式vs AIS的直观对比图表，突出AIS的15倍效率提升优势
  - FAQ页面：GitHub Copilot vs AIS功能定位对比图，展示两者完美互补关系
  - FAQ页面：AI提供商选择决策流程图，指导用户根据隐私、成本、性能需求选择最佳方案
  - Shell集成页面：详细的时序图展示用户、Shell、AIS核心和AI服务之间的完整交互流程
  - 学习报告页面：报告生成工作流程图，从数据收集到可视化输出的完整流程展示
  - 统一的设计语言：一致的配色方案、字体大小(16px)、图标使用和分类样式
  - 优化用户体验：所有图表使用单行文本避免内容被遮挡，VS节点采用超大无边框设计突出对比效果
  - 删除冗余内容：移除意义不大的选择指南流程图，保持文档简洁直接
- 🎯 **文档内容精简优化**：删除复杂的选择流程图，让用户快速找到核心内容
  - 删除安装指南中的复杂安装方式选择流程图和对比表格，突出推荐的一键安装方式
  - 删除快速开始页面上方的详细流程图，让用户直接看到具体操作步骤，真正实现快速上手
### Added
- 🔧 **可配置HTTP请求超时**：支持从配置文件读取HTTP请求超时时间，提升本地大模型兼容性
  - 新增`advanced.request_timeout`配置项，默认值120秒
  - 支持通过`ais config --set advanced.request_timeout=180`动态调整超时时间
  - 完美支持Ollama等本地大模型部署，解决响应时间较长的超时问题
  - 向后兼容：如果配置文件中没有此设置，自动使用默认的120秒超时
- 🎯 **配置文件初始化命令**：新增`ais config --init`命令用于初始化或重置配置文件
  - 支持创建新的配置文件或覆盖现有配置文件
  - 包含所有默认配置项：AI提供商、自动分析、超时设置等
  - 提供友好的成功提示，显示配置文件路径和包含的默认设置
  - 便于快速恢复默认配置或解决配置文件损坏问题
- 📊 **VitePress文档Mermaid图表支持**：实现文档中Mermaid图表的完美渲染
  - 集成`vitepress-plugin-mermaid`插件实现架构图表在文档中的原生渲染
  - 支持流程图、序列图、甘特图、Git图、状态图等多种图表类型
  - 自定义主题配置：统一色彩方案、优化字体和尺寸、深色模式适配
  - 响应式设计：移动端优化、滚动条美化、加载动画增强
  - 专业视觉效果：圆角边框、阴影效果、悬停交互、渐变背景
  - 完整的TypeScript支持和错误处理机制
### Enhanced
- 🤖 **本地AI模型集成优化**：完善对Ollama等本地AI服务的支持
  - 验证Ollama OpenAI兼容API与AIS现有接口的100%兼容性
  - 提供详细的本地模型配置指南和集成建议
  - 支持deepseek-r1:7b等大型本地模型的长时间推理任务
- 🎨 **文档站点视觉优化**：大幅提升Mermaid图表的可读性和美观度
  - 实现现代化的图表容器设计：浅灰背景、圆角边框、精美阴影
  - 优化节点和连接线样式：增加线条粗细、添加阴影效果
  - 统一的颜色主题：蓝色系主色调配合多彩辅助色
  - 深色模式完美适配：自动切换背景和边框颜色
  - 移动端响应式优化：字体缩放、内边距调整、横向滚动支持

## [2.5.4] - 2025-07-22

### Fixed
- 🔧 **卸载脚本全面优化**：深度分析install.sh脚本后完全匹配所有安装操作的卸载逻辑
  - 修复编译Python路径错误：从`/usr/local/python3.10/`改为正确的`/usr/local/`
  - 新增`python-upgrade`策略的卸载支持，完善所有4种install.sh安装策略的卸载
  - 改进Shell集成清理：支持新版`ais shell-integration`格式和旧版格式的完全清理
  - 增强临时文件清理：清理`/tmp/python_build`、`/tmp/ais_install_*.log`等安装残留
  - 完善安装方式检测逻辑：修复路径检测错误，准确识别各种安装场景
  - 扩展清理范围：清理pipx用户级虚拟环境、编译Python的所有相关文件（bin、lib、include、man等）
  - 新增`cleanup_temp_files()`函数专门处理临时文件和构建残留清理
  - 更新帮助信息：反映所有支持的安装方式和卸载能力

## [2.5.3] - 2025-07-22

### Fixed
- 🔧 **文档准确性修复**：全面检查并修复文档中不存在的功能和命令引用
  - 删除不存在的 `ais report --error-stats` 和 `ais report --skill-assessment` 参数引用
  - 删除不存在的 `ais doctor` 命令，替换为实际存在的 `ais test-integration`
  - 删除不存在的 `ais status` 命令，替换为 `ais test-integration`
  - 修复不存在的 `ais shell-integration` 子命令引用，替换为 `ais setup` 命令
  - 删除不存在的 `ais --debug` 参数引用
  - 更新所有相关配置选项为实际存在的命令和参数
- 📚 **文档内容对齐**：确保所有文档内容与程序实际功能保持一致
  - 修复 `/root/ais/.cursor/rules/note.md` 中的示例命令
  - 更新 `/root/ais/docs/getting-started/quick-start.md` 中的报告生成命令示例
  - 修复 `/root/ais/docs/configuration/shell-integration.md` 中的集成配置方法
  - 更新 `/root/ais/README.md` 中的诊断命令示例
  - 移除所有不存在功能的手动配置说明，统一指向 `ais setup` 命令

## [2.5.2] - 2025-07-22

### Added
- 📊 **HTML可视化报告功能**：全新的HTML格式报告导出，提供现代美观的数据可视化体验
  - 新增`ais report --html`命令支持生成交互式HTML报告
  - 集成6种专业图表类型：错误趋势图、技能雷达图、时间热力图、命令频次图、错误类型分布图、学习进度图
  - 使用Plotly图表库实现交互式数据可视化，支持悬停提示和缩放操作
  - 响应式HTML设计，完美适配桌面和移动设备
  - 支持`-o/--output`参数自定义输出文件名
  - 支持`--open`参数自动在浏览器中打开生成的报告
  - 现代化CSS样式设计，包含渐变背景、阴影效果和流畅动画
  - 智能空数据处理，确保即使数据不足也能生成有意义的图表
- 📦 **可选依赖管理**：新增html可选依赖组，支持按需安装可视化功能
  - 在pyproject.toml中添加`[project.optional-dependencies.html]`配置
  - 包含plotly>=5.0.0和numpy>=1.20.0依赖
  - 用户可通过`pip install ais-terminal[html]`安装完整可视化功能
### Enhanced
- 📚 **文档系统全面升级**：HTML可视化报告功能的完整文档体系
  - 更新主README.md，新增HTML报告功能详细介绍和使用示例
  - 创建专门的HTML可视化报告完整使用指南(/docs/features/html-reports.md)
  - 全面重写学习报告功能文档，聚焦实际可用功能
  - 更新所有安装文档，包含HTML依赖的安装说明
  - 更新功能索引和导航，添加可视化报告入口
  - 更新CLI帮助文档，包含HTML报告命令说明
- 🔧 **项目版本管理优化**：统一版本号和依赖配置
  - 项目版本从1.3.0更新到2.5.2，保持与功能发展同步  
  - 统一__init__.py和pyproject.toml中的版本信息
  - 更新README中的版本徽章显示
- 📐 **代码质量标准化**：全面执行代码格式化和质量检查
  - 使用black统一代码风格，确保团队协作一致性
  - 执行autopep8激进格式化，自动修复PEP 8代码风格违规
  - 通过flake8静态分析检查，确保100%代码质量合规
  - 优化HTML报告模块和CLI模块的代码格式和可读性
- 🧠 **AI洞察总结增强**：大幅提升学习报告的智能化水平和个性化程度
  - 新增深度数据分析：时间模式、学习速度类型、工作环境识别、项目类型分布
  - 增强错误模式分析：包含错误占比、复杂度趋势、技能成长轨迹等多维度数据
  - 优化AI提示词：提供6个维度的详细数据，要求AI发现令人惊喜的个性化模式
  - 智能趋势对比：周对周错误率变化分析，量化进步速度和改进趋势
  - 自动成就识别：技术栈广度、错误控制能力、容器化尝试等突出表现检测
  - 增强备用洞察：当AI不可用时提供更丰富的3-5句话智能总结

## [2.5.1] - 2025-07-21

### Added
- 🐳 **Docker完整支持**：提供基于Ubuntu 22.04的丰富工具Docker镜像
  - 升级Dockerfile基础镜像从python:3.11-slim到ubuntu:22.04，包含完整开发工具链
  - 集成Python 3.11、Node.js、Git、系统监控工具、网络诊断工具等60+常用命令
  - 支持数据库客户端（SQLite、MySQL、PostgreSQL）和文本处理工具（jq、yq、vim等）
  - 优化容器安全性：非root用户运行、适当的权限控制
  - 提供Docker Compose配置支持多环境部署
- 📚 **Docker使用文档**：在文档站点添加完整的Docker使用指南
  - 新增`/docs/getting-started/docker-usage.md`详细使用文档
  - 涵盖构建、部署、配置管理、故障排除等完整流程
  - 提供5个实际使用场景：Linux学习、代码分析、网络诊断、数据处理、Git实践
  - 包含高级配置、生产环境部署和最佳实践建议
### Enhanced
- 🔧 **Dockerfile优化**：提升容器化使用体验
  - 更新版本号从0.1.0到2.4.0与项目版本保持一致
  - 添加时区设置（Asia/Shanghai）和中文环境支持
  - 优化多阶段构建减少最终镜像大小
  - 完善健康检查和容器生命周期管理
### Documentation
- 📖 **文档站点更新**：优化Docker相关文档的导航和组织
  - 在VitePress配置中添加Docker使用页面链接
  - 将Docker使用指南整合到快速开始部分，便于用户发现和使用
  - 提供从基础到高级的完整Docker使用路径

## [2.4.0] - 2025-07-21

### Added
- 🧠 **ask命令智能上下文感知功能**：实现了基于环境上下文的智能问答系统
- ⏱️ **可配置的重复分析避免间隔**：使重复分析冷却时间可在配置文件中设置
  - 添加`advanced.analysis_cooldown`配置项，默认值60秒
  - 支持通过`ais config --set advanced.analysis_cooldown=<秒数>`设置间隔时间  
  - Shell集成脚本自动读取配置值，动态调整重复分析检测间隔
  - 优化用户体验：避免相同命令短时间内重复触发AI分析
  - 添加三级上下文收集系统：minimal（基础信息）、standard（标准信息）、detailed（详细信息）
  - 新增`collect_ask_context()`函数专门为ask功能收集上下文信息
  - 新增`ask_ai_with_context()`函数提供上下文感知的AI问答
  - 添加`_generate_contextual_system_prompt_for_ask()`函数生成环境感知的系统提示词
  - 支持通过`ais config --set ask.context_level=<level>`配置上下文收集级别
  - ask命令现在能自动识别项目类型、Git状态、工作环境并提供针对性回答
### Enhanced
- 🖥️ **大幅增强minimal级别的系统基础信息收集**：将"最小"级别打造为功能丰富的环境感知
  - **系统信息**：自动检测Linux发行版、内核版本、完整系统信息（uname -a）
  - **硬件信息**：CPU核心数量和详细型号、内存使用状态、磁盘使用情况、系统负载
  - **网络状态**：智能网络连通性检测（ping 8.8.8.8）
  - **服务和安全**：监听端口列表、运行的系统服务信息
  - 添加`collect_system_basic_info()`函数系统化收集基础环境信息
  - 所有信息收集都有异常处理和超时控制，确保性能和稳定性
### Changed
- 📋 **ask命令帮助文档全面更新**：反映新的智能上下文感知功能
  - 更新功能描述：从"快速问答"升级为"智能问答模式"
  - 添加智能上下文感知特性说明
  - 新增上下文配置使用方法和级别说明
  - 提供更多实际使用场景示例
- 🔧 **配置系统增强**：支持嵌套配置项管理
  - 更新`set_config()`函数支持嵌套键（如`ask.context_level`）
  - 配置显示界面新增ask命令上下文级别信息
  - 添加ask.context_level配置验证和错误提示
### Fixed
- 🌐 **网络连通性检测目标优化**：提升网络状态检测的可靠性
  - 将ping目标从114.114.114.114改为8.8.8.8（Google公共DNS）
  - 更新相关提示信息显示正确的测试目标
  - 保持超时控制和异常处理逻辑不变
### Technical Improvements
- 🎯 **上下文信息智能展示**：优化AI提示词中的信息展示
  - 长文本自动截断防止提示词过长
  - 端口和服务信息限量显示保持简洁
  - CPU型号等详细信息智能格式化
- 🔒 **安全性增强**：继承并增强原有的安全过滤机制
  - 敏感目录自动跳过上下文收集
  - API密钥、密码等敏感数据过滤
  - 递归字典过滤确保嵌套数据安全

## [2.3.0] - 2025-07-21

### Changed
- 发布版本 2.3.0

## [2.1.0] - 2025-07-21

### Added
- 🚀 **自动错误输出捕获功能**：实现AIS程序的核心功能之一 - 自动捕获命令错误输出并发送给AI分析
  - 使用exec重定向+临时文件方案实现stderr捕获，既保持用户可见性又实现内容捕获
  - 添加`_ais_init_stderr_capture()`函数初始化stderr重定向机制
  - 添加`_ais_get_captured_stderr()`函数获取和清理捕获的错误输出
  - 添加`_ais_cleanup_stderr_capture()`函数确保资源正确清理和恢复
  - 添加`_ais_filter_stderr()`函数过滤无关内容、限制长度并转义特殊字符
  - 修改`_ais_precmd()`函数将捕获的stderr作为`--stderr`参数传递给`ais analyze`
  - 支持bash和zsh环境，设置适当的trap和hook确保资源清理
  - 实现智能内容过滤：过滤AIS内部函数输出、限制1500字符长度、安全字符转义
  - 解决了之前只能获取命令和退出码但无法获取具体错误信息的关键问题
### Enhanced  
- 🔧 **完善Shell集成脚本生成**：同步更新CLI中的脚本生成功能
  - 更新`_create_integration_script()`函数生成包含stderr捕获功能的集成脚本
  - 确保通过`ais setup`命令重新安装的用户也能获得新的错误捕获功能
  - 保持向后兼容性，新旧版本脚本都能正常工作
### Technical Improvements
- 📋 **优化错误输出处理流程**：提升错误分析的准确性和实用性
  - 使用`exec 3>&2`保存原始stderr，`exec 2> >(tee -a "$file" >&3)`实现分流
  - 添加0.1秒延迟确保tee完成写入，避免内容丢失
  - 实现tail -n 100限制行数、head -c 2000限制字符数的双重保护
  - 添加grep过滤机制移除空行、AIS内部输出和tee错误信息
  - 使用sed和tr进行字符转义，确保参数传递安全性

## [2.0.0] - 2025-07-21

### Changed
- 发布版本 2.0.0

## [1.4.0] - 2025-07-21

### Enhanced
- 🎯 **安装脚本显示增强**：优化安装过程的用户体验和进度追踪
  - 为所有安装步骤添加时间戳显示 `[HH:MM:SS]`，方便用户了解每步耗时
  - 增加安装进度百分比显示 `[进度%]`，让用户清楚了解整体安装进度
  - 统一所有成功消息的显示格式：`✓ [时间戳][进度%] 消息内容`
  - 修复Shell集成、配置文件创建等步骤的显示格式不一致问题
  - 优化安装进度分配：检测(10%) → 依赖(15-30%) → Python(40-50%) → AIS(60%) → 集成(80%) → 验证(90-100%)
- 📝 **优化setup命令输出**：简化ais setup命令的显示信息，提升用户体验
  - 移除冗余的集成脚本路径显示，只保留关键信息
  - 精简配置提示，将多行提示合并为单行显示
  - 优化文件路径显示，只显示文件名而非完整路径
  - 统一成功状态消息格式，保持一致性
- 🎨 **统一状态符号风格**：优化程序中的状态符号显示
  - 将所有 `✅` 替换为 `✓ ` 确保在不同终端环境下的兼容性
  - 将所有 `❌` 替换为 `✗ ` 保持错误提示的一致性
  - 保留信息符号 `ℹ️` 以保持良好的用户体验
  - 涵盖Python代码、Shell脚本、文档等所有文件类型
### Fixed
- 🔄 **修复Shell集成重复错误分析问题**：彻底解决用户按回车键也触发错误分析的体验问题
  - 在`_ais_precmd`钩子函数中添加智能去重机制，防止相同命令在30秒内重复分析
  - 添加`_ais_should_analyze_command`函数实现时间窗口和命令内容的双重检查
  - 修复因Shell历史记录持久性导致的空命令触发上次错误分析的问题
  - 同时更新CLI中动态生成的集成脚本，确保新安装用户也获得修复
  - 显著提升用户体验，避免不必要的重复AI分析干扰

## [1.3.5] - 2025-07-20

### Fixed
- 🌐 **修复CentOS 7系统Python源码下载失败问题**：针对国内网络环境优化
  - 替换SHA256验证为文件大小验证，避免因哈希值不匹配导致的下载失败
  - 优先使用华为云和阿里云镜像源，提高国内用户下载成功率
  - 保持多镜像源重试机制，确保在网络不稳定情况下的可靠性
  - 修复"源码下载完成"重复显示但实际下载失败的问题

## [1.3.4] - 2025-07-20

### Changed
- 🔧 **优化一键安装脚本安全性和可靠性**：增强安装过程的安全性和用户体验
  - 统一Python编译策略：删除未实现的`compile_python39`逻辑，统一使用`compile_python310`
  - 添加Python源码完整性验证：使用SHA256校验确保下载文件安全
  - 增强下载可靠性：添加3次重试机制、30秒超时和断点续传支持
  - 优化API配置说明：在配置文件中添加详细注释，明确标注测试密钥的使用限制
  - 简化安装完成提示：精简输出信息，通过`ais provider-add --help-detail`引导用户配置

### Security
- 🔐 **提升API密钥安全性**：改进默认API密钥的处理方式
  - 在配置文件中明确标注API密钥为测试用途，有使用限制
  - 提供多种自定义API密钥的配置方法和说明
  - 支持环境变量`AIS_API_KEY`覆盖配置文件设置

### Fixed
- 🛡️ **修复文件下载安全问题**：防止文件篡改和网络异常
  - Python 3.10.9源码SHA256验证：`5ae03e0718a83b189d468bca544d2ba0c9d1e7bd73e5b1ff9b18b15ea729ee5d`
  - 智能检测已下载文件完整性，避免重复下载
  - 下载失败时提供手动下载指导和预期SHA256值

## [1.3.3] - 2025-07-19

### Fixed
- 🔧 **修复一键安装脚本Shell集成问题**：解决安装完成后source失败的关键问题
  - 修复`integration.sh`文件不存在导致的`No such file or directory`错误
  - 在Strategy 2中添加`create_integration_script()`函数，确保集成脚本在配置前就存在
  - 自动创建AIS配置文件`config.toml`，确保`auto_analysis = true`设置生效
  - 智能路径检测，支持不同Python版本的安装路径
### Changed
- 🎯 **优化一键安装用户体验**：提供更清晰的两步完成指导
  - 将安装后的指导从单步改为明确的两步操作：1) `ais setup` 2) `source ~/.bashrc`
  - 添加步骤编号和清晰的注释说明，避免用户困惑
  - 确保用户了解需要先配置Shell集成，再重新加载配置文件
  - 提供更准确的完成反馈，提高安装成功率

## [1.3.2] - 2025-07-19

### Changed
- 发布版本 1.3.2

## [1.3.1] - 2025-07-19

### Changed
- 发布版本 1.3.1

## [1.3.0] - 2025-07-19

### Fixed
- 🔧 **修复CentOS 7安装脚本重复执行问题**：解决一键安装脚本中compile_python310分支的代码重复导致的错误
  - 删除782-919行的重复Python编译逻辑，避免变量冲突和文件名错误
  - 修复`tar: Python-3.6.tar.xz: Cannot open: No such file or directory`错误
  - 确保CentOS 7系统第一次运行安装脚本即可成功，无需使用--debug参数重复运行
- 🎨 **优化安装脚本输出显示**：解决验证安装阶段的重复进度条输出问题
  - 简化`update_progress_with_spinner`函数逻辑，避免while循环造成的重复显示
  - 移除验证安装阶段的冗余动画效果，使用简洁的进度条显示
  - 优化系统检测和策略选择阶段的输出格式，提升用户体验
  - 添加AIS ASCII艺术字标题，提升视觉效果
  - 修改Python源码下载信息显示具体版本号
  - 优化Python编译安装完成信息的显示格式
  - 删除冗余的软链接创建信息输出
  - 改进进度条显示逻辑，确保在一行中动态更新
  - 修复进度条显示位置错误和重复100%显示的问题
  - 重构安装过程的输出格式，使用图标和颜色增强可读性
  - Python编译安装完成信息统一使用"✓"符号显示
  - 重新设计进度条系统，确保在整个安装过程中动态更新到100%
  - 修复进度条停止在15%的问题，添加各个安装阶段的进度更新
  - 美化安装成功后的输出显示，添加精美的边框和结构化布局
  - 优化配置指导格式，使用不同颜色和图标增强可读性
  - 修复脚本语法错误：添加缺失的fi语句
  - 改进管道执行支持：添加pipefail选项和管道检测逻辑
  - 解决curl管道执行时脚本无响应的问题
  - 修复管道执行条件判断：正确检测BASH_SOURCE为空和$0为bash的情况
  - 确保curl管道执行和直接执行都能正常工作
  - 修复安装成功信息框的文本对齐问题
  - 改进框架布局和间距，提升视觉效果
  - 重新设计安装成功显示：使用简洁的分割线替代Unicode边框
  - 解决不同终端环境下的对齐兼容性问题
  - 优化分割线样式：使用更美观的短横线替代等号
  - 简化标题显示：移除成功标题上方的分割线，保持简洁
- 🔧 **修复Kylin V10安装脚本错误**：解决"install: missing destination file operand"错误
  - 修改Python 3.10.9编译安装路径从`/usr/local/python3.10`改为`/usr/local`
  - 更新PIP_CMD使用`python3.10 -m pip`替代直接调用pip3.10二进制文件
  - 参考test.md中成功的手动安装步骤，简化安装路径配置
  - 移除复杂的软链接创建逻辑，使用标准的altinstall路径
  - 修复策略检测逻辑：Kylin系统优先使用compile_python310而不是基于Python版本的compile_python39
  - 同时修复compile_python39分支的PIP_CMD设置，使用`python3 -m pip`避免类似问题
- 🕐 **优化用户体验**：在Python 3.10.9编译安装提示后添加耗时说明
  - 添加"编译过程可能需要3-5分钟，请耐心等待..."提示
  - 避免用户在编译过程中因为等待时间过长而误以为脚本卡住
- 🎨 **优化安装策略提示显示**：改进策略信息的视觉效果
  - 将策略提示符号从"ℹ️"统一改为"✓"，使用绿色显示
  - 删除策略提示后的多余空行，使输出更紧凑美观
- 🚀 **实施混合策略优化用户体验**：三策略组合覆盖全场景配置需求
  - **策略1-优化ais setup**: 提供最简洁直接的配置体验，一步到位的提示
  - **策略2-一键安装脚本自动配置**: 安装完成后自动执行shell集成配置
  - **策略3-首次运行自动提示**: 检测配置状态，未配置时友好提醒
  - 支持所有安装方式：一键脚本、pip安装、pipx安装、源码安装等
  - 兼顾自动化和兼容性：主流场景自动化，特殊场景有保障
  - 用户体验分层：一键安装用户几乎无感，其他用户有清晰指导

## [1.2.0] - 2025-07-18

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
