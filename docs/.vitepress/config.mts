import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'AIS 文档',
  description: 'AIS - 上下文感知的错误分析学习助手',
  lang: 'zh-CN',
  base: '/ais/',
  
  head: [
    ['link', { rel: 'icon', href: '/ais/logo-icon.ico' }],
    ['link', { rel: 'shortcut icon', href: '/ais/logo-icon.ico' }],
    ['link', { rel: 'apple-touch-icon', href: '/ais/logo-icon.ico' }]
  ],
  
  themeConfig: {
    logo: '/ais/logo.png',
    siteTitle: false,
    
    nav: [
      { text: '首页', link: '/' },
      { text: '快速开始', link: '/getting-started/installation' },
      { text: '功能特性', link: '/features/' },
      { text: '配置指南', link: '/configuration/' },
      { text: '开发者', link: '/development/' },
      { text: 'GitHub', link: 'https://github.com/kangvcar/ais' }
    ],

    sidebar: [
      {
        text: '快速开始',
        collapsed: false,
        items: [
          { text: '安装指南', link: '/getting-started/installation' },
          { text: '快速开始', link: '/getting-started/quick-start' },
          { text: '基本使用', link: '/getting-started/basic-usage' }
        ]
      },
      {
        text: '功能特性',
        collapsed: false,
        items: [
          { text: '功能概览', link: '/features/' },
          { text: '错误分析', link: '/features/error-analysis' },
          { text: 'AI 问答', link: '/features/ai-chat' },
          { text: '学习系统', link: '/features/learning-system' },
          { text: '学习报告', link: '/features/learning-reports' },
          { text: '提供商管理', link: '/features/provider-management' }
        ]
      },
      {
        text: '配置指南',
        collapsed: true,
        items: [
          { text: '基本配置', link: '/configuration/basic-config' },
          { text: 'Shell 集成', link: '/configuration/shell-integration' },
          { text: '隐私设置', link: '/configuration/privacy-settings' }
        ]
      },
      {
        text: '开发者指南',
        collapsed: true,
        items: [
          { text: '贡献指南', link: '/development/contributing' },
          { text: '测试指南', link: '/development/testing' },
          { text: '架构设计', link: '/development/architecture' }
        ]
      },
      {
        text: '故障排除',
        collapsed: true,
        items: [
          { text: '常见问题', link: '/troubleshooting/common-issues' },
          { text: '常见问答', link: '/troubleshooting/faq' }
        ]
      }
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/kangvcar/ais' }
    ],

    footer: {
      message: '基于 MIT 许可证发布',
      copyright: 'Copyright © 2024 AIS Team'
    },

    search: {
      provider: 'local'
    }
  }
})