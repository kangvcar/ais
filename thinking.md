
### **`ais`: 智能终端助手 - 最终技术设计规格书**

#### **一、 项目核心原则**

1.  **代码极简**: 始终选择能用最少、最直观代码实现功能的方案。优先使用高表达力的库来减少样板代码。
2.  **结构清晰**: 项目目录、模块划分和代码逻辑应清晰明了，易于新开发者理解和维护。
3.  **体验优先**: 所有技术决策最终都应服务于为用户提供一个流畅、直观、可靠的终端体验。
4.  **渐进式开发**: 采用 MVP 方式，分阶段实现功能，确保每个阶段都能独立工作。
5.  每个阶段性的修改都需要提交git 版本控制并写清楚详细的commit。
6.  使用最佳实践进行开发，使用最少的代码里。

#### **二、 项目结构设计**

...

#### **三、 开发阶段规划**

**阶段 1: 基础 CLI 框架 (MVP)**
- 实现 `ais` 命令行入口点
- 基础的 AI 对话功能 (`ais ask "问题"`)
- 配置文件管理 (`ais config`)
- 基础的开关控制 (`ais on/off`)

**阶段 2: 配置与持久化**
- 完善配置文件结构和管理
- 实现多 AI 服务提供商支持
- 基础的数据库存储

**阶段 3: 错误捕获机制**
- 实现 shell 集成脚本
- 优化的错误捕获策略（使用 PROMPT_COMMAND 而非 trap ERR）
- 上下文收集系统

**阶段 4: 智能分析与交互**
- AI 错误分析功能
- 交互式建议菜单
- 流式输出支持

**阶段 5: 安装与分发**
- 完善安装脚本
- 打包和分发机制

#### **四、 安装与初始化**

1.  **一键安装脚本**: 用户通过单一命令完成安装，无需手动干预。

    ```bash
    curl -sSL https://ais-cli.com/install.sh | bash
    ```

2.  **`install.sh` 脚本职责**:

      * **环境检查**: 验证系统是否已安装 `python` 和 `pip`。
      * **安装 `uv`**: 如果 `uv` 不存在，则尝试安装它。
      * **安装 `ais`**: 使用 `uv pip install ais-cli` 从PyPI（或其他源）安装`ais`包。
      * **Shell配置注入**:
          * 自动检测用户的Shell配置文件（`~/.bashrc`, `~/.zshrc`）。
          * 向配置文件中追加一段由明确标记包围的脚本，以便于未来更新或卸载。例如：
            ```bash
            # START AIS INTEGRATION
            # This block is managed by ais-cli. Do not edit manually.
            source "/path/to/ais/shell/integration.sh"
            # END AIS INTEGRATION
            ```
      * **提示用户**: 安装完成后，提示用户需执行 `source ~/.bashrc` 或重启终端以使配置生效。

3.  **零配置启动**: 程序内置默认API配置，确保开箱即用。

      * **默认端点**: `https://api.deepbricks.ai/v1/chat/completions`
      * **默认模型**: `gpt-4o-mini`
      * **默认密钥**: `sk-97RxyS9R2dsqFTUxcUZOpZwhnbjQCSOaFboooKDeTv5nHJgg`

#### **五、 功能模块详述**

1.  **Shell深度集成 (`integration.sh`)** - 优化版本:

      * **错误捕获机制**: 使用 `PROMPT_COMMAND` 而非 `trap ERR`，避免与其他工具冲突。
        ```bash
        # 在 integration.sh 中
        _ais_last_command=""
        _ais_last_exit_code=0
        
        _ais_preexec() {
          _ais_last_command="$1"
        }
        
        _ais_precmd() {
          _ais_last_exit_code=$?
          
          # 只处理非零退出码且非中断信号
          if [ $_ais_last_exit_code -ne 0 ] && [ $_ais_last_exit_code -ne 130 ]; then
            # 检查功能是否开启
            if grep -q "auto_analysis = true" ~/.config/ais/config.toml 2>/dev/null; then
              # 异步调用分析，避免阻塞用户操作
              ais _analyze --exit-code $_ais_last_exit_code --command "$_ais_last_command" &
            fi
          fi
        }
        
        # 根据不同 shell 设置钩子
        if [ -n "$ZSH_VERSION" ]; then
          autoload -U add-zsh-hook
          add-zsh-hook preexec _ais_preexec
          add-zsh-hook precmd _ais_precmd
        elif [ -n "$BASH_VERSION" ]; then
          trap '_ais_preexec "$BASH_COMMAND"' DEBUG
          PROMPT_COMMAND="_ais_precmd;$PROMPT_COMMAND"
        fi
        ```
      * **自动分析开关**:
          * 提供 `ais on` 和 `ais off` 命令。
          * 这两个命令会修改 `~/.config/ais/config.toml` 文件中的 `auto_analysis` 布尔值。
          * 集成脚本会检查配置文件状态来决定是否启用分析。

2.  **智能上下文收集** - 优化版本:
    `ais _analyze` 命令被触发后，采用分级收集策略：

      * **核心级别** (总是收集):
          * 错误命令和退出码
          * 标准错误输出
          * 当前工作目录
      
      * **标准级别** (默认收集):
          * 最近 10 条命令历史 (而非 20 条)
          * 当前目录文件列表 (仅文件名，不含详细信息)
          * Git 状态 (如果是 Git 仓库)
      
      * **详细级别** (可配置):
          * 系统信息 (`uname -a`)
          * 环境变量相关信息
          * 完整的 `ls -la` 输出
      
      * **安全过滤**:
          * 排除包含密码、密钥等敏感信息的上下文
          * 提供敏感目录黑名单配置 (如 ~/.ssh, ~/.config)
          * 对输出进行脱敏处理

3.  **AI交互协议** - 增强版本:

      * **请求**: System Prompt必须明确指示AI扮演一个Linux/macOS命令行专家，并且**必须**以指定的JSON格式返回响应。
      * **响应容错处理**: 
          * 主要解析标准 JSON 格式
          * 如果 JSON 解析失败，尝试从 Markdown 代码块中提取
          * 提供降级处理：纯文本解释 + 空建议列表
      * **响应 (JSON结构)**: AI的返回**必须**严格遵守以下结构：
        ```json
        {
          "explanation": "这里是对错误的详细分析、原因说明和背景知识普及。可以使用Markdown语法，例如 `代码块` 或 **加粗**。",
          "suggestions": [
            {
              "description": "修正该拼写错误，并检查仓库状态。",
              "command": "git status",
              "risk_level": "safe"  // 新增: safe, moderate, dangerous
            },
            {
              "description": "如果想暂存当前变更，使用此命令。",
              "command": "git stash",
              "risk_level": "safe"
            }
          ]
        }
        ```

4.  **用户交互流程** - 增强版本:

      * **流式渲染**: `explanation` 字段使用 `rich.markdown.Markdown` 进行流式渲染。
      * **增强交互菜单**: 使用 `questionary` 库生成，包含风险级别显示：
        ```
        🤖 AI Analysis Complete
        
        [错误分析内容以流式方式显示]
        
        ? Select an action: 
          ▸ 1. git status              ✅ (修正该拼写错误，并检查仓库状态。)
            2. git stash               ✅ (如果想暂存当前变更，使用此命令。)
            3. rm -rf /                ⚠️  (危险操作，请谨慎！)
            ---------------------------------------------------------------------------
            4. Edit a command...
            5. Ask follow-up question
            6. Exit
        ```
      * **命令执行确认**: 对于 `dangerous` 级别的命令，要求用户二次确认。
      * **执行反馈**: 命令执行后显示结果，并询问是否需要进一步帮助。

#### **六、 数据与配置持久化**

1.  **配置文件** - 增强版本:

      * **路径**: `~/.config/ais/config.toml`
      * **完整结构示例**:
        ```toml
        # 默认使用的AI服务提供商的名称
        default_provider = "default_free"

        # 自动错误分析功能的开关
        auto_analysis = true

        # 上下文收集级别: minimal, standard, detailed
        context_level = "standard"

        # 敏感目录黑名单
        sensitive_dirs = ["~/.ssh", "~/.config/ais", "~/.aws"]

        # UI 设置
        [ui]
        enable_colors = true
        enable_streaming = true
        max_history_display = 10

        # 预置的免费服务
        [providers.default_free]
        base_url = "https://api.deepbricks.ai/v1/chat/completions"
        model_name = "gpt-4o-mini"
        api_key = "sk-97RxyS9R2dsqFTUxcUZOpZwhnbjQCSOaFboooKDeTv5nHJgg"

        # 用户自定义的Ollama服务
        [providers.my_ollama]
        base_url = "http://localhost:11434/v1"
        model_name = "llama3"
        # api_key is not needed for local ollama

        # 用户自定义的OpenAI服务
        [providers.my_openai]
        # base_url is optional, defaults to official
        model_name = "gpt-4o"
        # api_key will be read from environment variable OPENAI_API_KEY
        
        # 高级设置
        [advanced]
        max_context_length = 4000  # 发送给AI的最大上下文长度
        async_analysis = true      # 异步分析以避免阻塞
        cache_analysis = true      # 缓存相似错误的分析结果
        ```

2.  **本地数据库**:

      * **路径**: `~/.local/share/ais/history.db`
      * **技术**: SQLite + `SQLModel`
      * **`CommandLog` 表结构字段**:
          * `id`: INTEGER, PRIMARY KEY
          * `timestamp`: DATETIME
          * `username`: TEXT
          * `original_command`: TEXT
          * `stderr_output`: TEXT
          * `context_json`: TEXT (存储收集到的所有上下文信息的JSON字符串)
          * `ai_explanation`: TEXT
          * `ai_suggestions_json`: TEXT (存储AI返回的suggestions列表的JSON字符串)
