# 基本配置

AIS 的基本配置包括语言、主题、输出格式等核心设置，这些设置影响 AIS 的整体行为和用户体验。

## 🌍 语言设置

### 支持的语言
```bash
# 中文（默认）
ais config set language zh-CN

# 英文
ais config set language en-US

# 查看当前语言
ais config show language
```

### 语言影响范围
- **命令输出**：所有命令的输出信息
- **错误分析**：错误分析结果和建议
- **AI 问答**：AI 回答的语言
- **学习内容**：学习材料的语言

## 🎨 主题和输出

### 主题设置
```bash
# 自动主题（跟随系统）
ais config set theme auto

# 深色主题
ais config set theme dark

# 浅色主题
ais config set theme light
```

### 输出格式
```bash
# Rich 格式（推荐）
ais config set output-format rich

# 简单文本格式
ais config set output-format plain

# JSON 格式（适合脚本）
ais config set output-format json
```

### 输出详细程度
```bash
# 详细输出
ais config set verbosity verbose

# 标准输出（默认）
ais config set verbosity normal

# 简洁输出
ais config set verbosity quiet
```

## 🔄 自动分析设置

### 全局开关
```bash
# 开启自动分析
ais on

# 关闭自动分析
ais off

# 查看状态
ais status
```

### 分析触发条件
```bash
# 设置触发的最小退出码
ais config set min-exit-code 1

# 设置分析延迟（秒）
ais config set analysis-delay 1

# 设置最大分析时间（秒）
ais config set max-analysis-time 30
```

## 🧠 上下文收集

### 收集级别
```bash
# 最小收集
ais config set context-level minimal

# 标准收集（推荐）
ais config set context-level standard

# 详细收集
ais config set context-level detailed
```

### 收集级别说明

#### minimal（最小）
- 基本系统信息
- 命令和退出码
- 最小环境变量

#### standard（标准）
- 完整系统信息
- 网络状态检查
- 项目类型检测
- 常用环境变量

#### detailed（详细）
- 完整环境快照
- 详细网络诊断
- 完整权限检查
- 所有相关环境变量

## 📊 性能设置

### 缓存配置
```bash
# 设置缓存大小（MB）
ais config set cache-size 100

# 设置缓存过期时间（小时）
ais config set cache-ttl 24

# 清空缓存
ais config clear-cache
```

### 并发设置
```bash
# 设置最大并发数
ais config set max-concurrent 3

# 设置超时时间（秒）
ais config set timeout 30
```

## 🔔 通知设置

### 通知类型
```bash
# 开启桌面通知
ais config set desktop-notifications true

# 开启声音通知
ais config set sound-notifications true

# 开启完成通知
ais config set completion-notifications true
```

### 通知级别
```bash
# 只通知错误
ais config set notification-level error

# 通知警告和错误
ais config set notification-level warning

# 通知所有信息
ais config set notification-level info
```

## 💾 数据存储

### 存储位置
```bash
# 查看数据目录
ais config show data-dir

# 设置自定义数据目录
ais config set data-dir /custom/path

# 重置为默认位置
ais config reset data-dir
```

### 历史记录
```bash
# 设置历史记录保留天数
ais config set history-retention 30

# 设置最大历史记录数
ais config set max-history 1000

# 清空历史记录
ais history clear
```

## 🛡️ 安全设置

### 安全级别
```bash
# 严格模式（推荐）
ais config set security-level strict

# 标准模式
ais config set security-level standard

# 宽松模式
ais config set security-level relaxed
```

### 安全选项
```bash
# 启用命令确认
ais config set require-confirmation true

# 启用危险命令警告
ais config set dangerous-command-warning true

# 启用网络请求确认
ais config set network-request-confirmation true
```

## 🔧 高级设置

### 调试模式
```bash
# 开启调试模式
ais config set debug true

# 设置日志级别
ais config set log-level debug

# 查看日志文件
ais config show log-file
```

### 实验性功能
```bash
# 开启实验性功能
ais config set experimental true

# 查看可用的实验性功能
ais config list-experimental
```

## 📋 配置模板

### 开发者配置
```bash
# 适合开发者的配置
ais config set context-level detailed
ais config set verbosity verbose
ais config set debug true
ais config set experimental true
```

### 生产环境配置
```bash
# 适合生产环境的配置
ais config set context-level minimal
ais config set verbosity quiet
ais config set security-level strict
ais config set auto-analysis false
```

### 学习者配置
```bash
# 适合学习者的配置
ais config set context-level standard
ais config set verbosity verbose
ais config set completion-notifications true
ais config set require-confirmation true
```

## 🔍 配置验证

### 验证配置
```bash
# 验证所有配置
ais config validate

# 验证特定配置
ais config validate auto-analysis

# 检查配置冲突
ais config check-conflicts
```

### 配置诊断
```bash
# 诊断配置问题
ais config diagnose

# 修复配置问题
ais config repair

# 生成配置报告
ais config report
```

## 📤 配置导入导出

### 导出配置
```bash
# 导出所有配置
ais config export config.yaml

# 导出特定配置
ais config export --section basic config.yaml
```

### 导入配置
```bash
# 导入配置
ais config import config.yaml

# 合并配置
ais config import --merge config.yaml
```

---

## 下一步

- [Shell 集成](./shell-integration) - 配置 Shell 集成
- [隐私设置](./privacy-settings) - 配置隐私保护
- [提供商管理](../features/provider-management) - 管理 AI 提供商
- [故障排除](../troubleshooting/common-issues) - 解决常见问题

---

::: tip 提示
建议定期备份配置文件，特别是在进行大量定制化配置后。
:::

::: info 配置优先级
命令行参数 > 环境变量 > 配置文件 > 默认值
:::

::: warning 注意
某些配置修改后需要重启 AIS 或重新加载 Shell 配置才能生效。
:::