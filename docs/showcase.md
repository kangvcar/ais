# AIS 功能展示

欢迎来到 AIS (AI Shell) 功能展示页面！在这里您可以直观地了解 AIS 的各项强大功能，通过实际的终端演示来体验它是如何提升您的开发效率的。

::: info 关于演示
以下演示展示了 AIS 的核心功能，包括智能错误分析、问答助手、配置管理、历史记录、知识学习和报告生成等。
:::

## 🔍 错误自动分析

AIS 能够智能分析终端中的错误信息，并提供解决方案建议。

<div id="asciicast-729620-container"></div>

::: tip 智能分析
AIS 会自动检测命令执行失败时的错误信息，并基于上下文提供针对性的解决方案。
:::

## 💬 AIS Ask - 智能问答

通过 `ais ask` 命令，您可以直接在终端中向 AI 助手提问，获得即时的帮助和建议。

<div id="asciicast-729619-container"></div>

::: info Ask 命令特性
- 支持自然语言提问
- 上下文感知的回答
- 多种问题类型支持
- 即时响应
:::

## ⚙️ 配置管理

使用 `ais config` 命令轻松管理 AIS 的各项配置，包括 API 密钥、模型选择等。

<div id="asciicast-729621-container"></div>

::: warning 配置安全
配置包含敏感信息如 API 密钥，请妥善保管您的配置文件。
:::

## 📚 历史记录管理

`ais history` 命令帮助您管理和查看与 AI 的对话历史，方便回顾和复用之前的交互内容。

<div id="asciicast-729622-container"></div>

## 🎓 知识学习功能

通过 `ais learn` 命令，AIS 可以学习和记住项目相关的知识，为您提供更加个性化和精准的帮助。

<div id="asciicast-729623-container"></div>

::: tip 学习能力
AIS 可以学习您的项目结构、编码习惯和常用模式，提供更加智能化的建议。
:::

## 📊 报告生成

`ais report` 命令可以生成详细的项目分析报告，包括代码质量、依赖分析、安全检查等多个维度。

<div id="asciicast-729624-container"></div>

::: info 报告功能
生成的报告包含项目的全面分析，帮助您了解项目状态并发现潜在问题。
:::

::: tip 查看报告示例
想要查看 AIS 生成的详细 HTML 报告效果吗？  
👉 [点击查看报告示例](/report.html) - 这是一个真实的 AIS 学习成长报告，包含了数据可视化图表和详细分析内容。
:::

## 🚀 开始使用

想要开始使用这些强大的功能吗？

<div class="tip custom-block" style="padding-top: 8px">

查看我们的 [快速开始指南](/getting-started/installation) 来安装和配置 AIS。

</div>

## 🔗 相关链接

| 链接 | 描述 |
|------|------|
| [功能特性](/features/) | 详细了解 AIS 的所有功能 |
| [配置指南](/configuration/) | 学习如何配置和优化 AIS |
| [故障排除](/troubleshooting/common-issues) | 常见问题和解决方案 |
| [开发者指南](/development/) | 为 AIS 贡献代码 |

---

<div style="text-align: center; margin-top: 2rem; padding: 1rem; background: var(--vp-c-bg-soft); border-radius: 8px;">

**体验过这些功能展示后，您是否对 AIS 的能力感到惊喜？**  
[立即开始使用 AIS](/getting-started/installation) 来提升您的开发效率！

</div>

<script setup>
import { onMounted } from 'vue'

onMounted(() => {
  // 为每个容器嵌入对应的 asciinema 播放器
  const casts = [
    { containerId: 'asciicast-729620-container', src: 'https://asciinema.org/a/729620.js', id: 'asciicast-729620' },
    { containerId: 'asciicast-729619-container', src: 'https://asciinema.org/a/729619.js', id: 'asciicast-729619' },
    { containerId: 'asciicast-729621-container', src: 'https://asciinema.org/a/729621.js', id: 'asciicast-729621' },
    { containerId: 'asciicast-729622-container', src: 'https://asciinema.org/a/729622.js', id: 'asciicast-729622' },
    { containerId: 'asciicast-729623-container', src: 'https://asciinema.org/a/729623.js', id: 'asciicast-729623' },
    { containerId: 'asciicast-729624-container', src: 'https://asciinema.org/a/729624.js', id: 'asciicast-729624' }
  ]
  
  casts.forEach(cast => {
    const container = document.getElementById(cast.containerId)
    if (container) {
      // 创建 script 标签并插入到对应容器中
      const script = document.createElement('script')
      script.src = cast.src
      script.id = cast.id
      script.async = true
      container.appendChild(script)
    }
  })
})
</script>