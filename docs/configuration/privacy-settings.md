# 隐私设置

AIS 非常重视用户隐私，提供了全面的隐私保护机制。所有数据都存储在本地，您可以完全控制数据的收集和使用。

## 🔒 隐私原则

### 数据本地化
- 所有数据存储在本地 SQLite 数据库
- 不向外部服务器发送敏感信息
- 用户完全控制数据的收集和删除

### 敏感信息过滤
- 自动过滤密码、API 密钥等敏感信息
- 支持自定义敏感信息模式
- 在发送给 AI 之前进行数据清洗

## 🛡️ 敏感信息过滤

### 默认过滤规则
AIS 默认过滤以下类型的敏感信息：
- 密码和密钥
- API 令牌
- 数据库连接字符串
- 私钥文件内容
- 环境变量中的敏感信息

### 查看过滤规则
```bash
# 查看所有过滤规则
ais config show privacy

# 查看敏感模式
ais config show sensitive-patterns

# 查看排除目录
ais config show excluded-dirs
```

### 自定义过滤规则
```bash
# 添加敏感信息模式
ais config add-sensitive-pattern "*password*"
ais config add-sensitive-pattern "*token*"
ais config add-sensitive-pattern "*secret*"
ais config add-sensitive-pattern "*key*"

# 添加敏感命令
ais config add-sensitive-command "mysql"
ais config add-sensitive-command "ssh"
ais config add-sensitive-command "curl"

# 添加敏感环境变量
ais config add-sensitive-env "AWS_SECRET_ACCESS_KEY"
ais config add-sensitive-env "GITHUB_TOKEN"
```

## 📁 目录和文件排除

### 默认排除目录
```bash
# 查看默认排除目录
ais config show excluded-dirs

# 默认排除的目录包括：
# ~/.ssh/
# ~/.gnupg/
# ~/.aws/
# ~/.config/gcloud/
# /etc/ssl/private/
```

### 自定义排除规则
```bash
# 添加排除目录
ais config add-excluded-dir ~/.secrets
ais config add-excluded-dir /opt/company/secrets
ais config add-excluded-dir ~/.config/sensitive-app

# 添加排除文件模式
ais config add-excluded-pattern "*.key"
ais config add-excluded-pattern "*.pem"
ais config add-excluded-pattern "*.p12"
ais config add-excluded-pattern "*secret*"
ais config add-excluded-pattern "*password*"

# 移除排除规则
ais config remove-excluded-dir ~/.secrets
ais config remove-excluded-pattern "*.key"
```

## 🔍 上下文收集控制

### 收集级别
```bash
# 最小收集（推荐隐私敏感用户）
ais config set context-level minimal

# 标准收集（默认）
ais config set context-level standard

# 详细收集（开发调试用）
ais config set context-level detailed
```

### 收集级别详情

#### minimal（最小）
```bash
收集内容：
- 基本系统信息（OS、架构）
- 命令和退出码
- 最小环境变量（PATH、HOME）
- 不收集网络信息
- 不收集文件内容
```

#### standard（标准）
```bash
收集内容：
- 完整系统信息
- 网络连接状态（不含详细信息）
- 项目类型检测
- 常用环境变量
- 基本权限信息
```

#### detailed（详细）
```bash
收集内容：
- 所有系统信息
- 详细网络诊断
- 完整环境变量
- 详细权限检查
- 相关文件内容（经过过滤）
```

## 🌐 网络隐私

### 网络信息收集
```bash
# 禁用网络状态收集
ais config set collect-network-info false

# 禁用 DNS 检查
ais config set collect-dns-info false

# 禁用外部 IP 检查
ais config set collect-external-ip false
```

### AI 服务隐私
```bash
# 使用本地 AI 模型（推荐）
ais provider-add ollama \
  --url http://localhost:11434/v1/chat/completions \
  --model llama2

# 设置为默认提供商
ais provider-use ollama

# 验证本地模型
ais provider-test ollama
```

## 📊 数据管理

### 数据存储位置
```bash
# 查看数据存储位置
ais config show data-dir

# 自定义数据存储位置
ais config set data-dir /secure/location/ais-data
```

### 数据清理
```bash
# 清理历史记录
ais history clear

# 清理分析缓存
ais config clear-cache

# 清理所有数据
ais data clear --all

# 安全删除数据
ais data secure-delete
```

### 数据备份
```bash
# 备份数据
ais data backup backup.tar.gz

# 恢复数据
ais data restore backup.tar.gz

# 导出数据（去敏感化）
ais data export --anonymize export.json
```

## 🔐 加密设置

### 数据库加密
```bash
# 启用数据库加密
ais config set database-encryption true

# 设置加密密钥
ais config set-encryption-key

# 验证加密状态
ais config show encryption-status
```

### 传输加密
```bash
# 强制使用 HTTPS
ais config set force-https true

# 验证 SSL 证书
ais config set verify-ssl true

# 使用自定义 CA 证书
ais config set ca-cert-path /path/to/ca.pem
```

## 🚫 禁用功能

### 禁用特定功能
```bash
# 禁用自动分析
ais off

# 禁用学习功能
ais config set learning-enabled false

# 禁用历史记录
ais config set history-enabled false

# 禁用统计收集
ais config set stats-enabled false
```

### 禁用网络功能
```bash
# 禁用所有网络功能
ais config set network-enabled false

# 禁用更新检查
ais config set update-check false

# 禁用遥测
ais config set telemetry false
```

## 🔍 隐私审计

### 审计数据收集
```bash
# 查看将要收集的数据
ais audit --dry-run

# 查看历史数据收集
ais audit --history

# 生成隐私报告
ais audit --report
```

### 数据清单
```bash
# 查看存储的数据类型
ais data inventory

# 查看数据统计
ais data stats

# 查看敏感数据检测结果
ais data scan-sensitive
```

## 📋 隐私配置模板

### 高隐私模式
```bash
# 适合隐私敏感用户的配置
ais config set context-level minimal
ais config set collect-network-info false
ais config set collect-dns-info false
ais config set history-enabled false
ais config set stats-enabled false
ais config set telemetry false
ais config set database-encryption true

# 使用本地 AI 模型
ais provider-add ollama --url http://localhost:11434/v1/chat/completions --model llama2
ais provider-use ollama
```

### 企业安全模式
```bash
# 适合企业环境的配置
ais config set context-level standard
ais config set force-https true
ais config set verify-ssl true
ais config set database-encryption true
ais config add-excluded-dir /opt/company
ais config add-sensitive-pattern "*company*"
ais config add-sensitive-pattern "*internal*"
```

### 开发者模式
```bash
# 适合开发者的配置（平衡隐私和功能）
ais config set context-level standard
ais config set collect-network-info true
ais config set history-enabled true
ais config set stats-enabled true
ais config add-excluded-dir ~/.ssh
ais config add-excluded-dir ~/.aws
ais config add-sensitive-pattern "*password*"
ais config add-sensitive-pattern "*token*"
```

## 🔒 隐私最佳实践

### 定期检查
```bash
# 定期审计隐私设置
ais audit --comprehensive

# 检查数据收集状态
ais privacy status

# 更新敏感信息过滤规则
ais config update-sensitive-patterns
```

### 安全提醒
```bash
# 启用隐私提醒
ais config set privacy-reminders true

# 设置数据清理提醒
ais config set cleanup-reminders true

# 设置审计提醒
ais config set audit-reminders true
```

---

## 下一步

- [提供商管理](../features/provider-management) - 配置本地 AI 提供商
- [故障排除](../troubleshooting/common-issues) - 解决隐私相关问题
- [基本配置](./basic-config) - 了解其他配置选项

---

::: tip 提示
推荐使用本地 AI 模型（如 Ollama）来最大化隐私保护，避免向外部服务发送数据。
:::

::: info 透明度
AIS 的所有数据收集和处理都是透明的，您可以随时查看存储的数据和隐私设置。
:::

::: warning 注意
修改隐私设置后，建议运行 `ais audit` 命令验证配置是否正确。
:::