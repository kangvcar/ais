import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'AIS 文档',
  description: 'AIS - 上下文感知的错误分析学习助手',
  lang: 'zh-CN',
  
  themeConfig: {
    nav: [
      { text: '首页', link: '/' },
      { text: '快速开始', link: '/getting-started/installation' },
      { text: '功能特性', link: '/features/' },
      { text: 'GitHub', link: 'https://github.com/kangvcar/ais' }
    ],

    sidebar: {
      '/getting-started/': [
        {
          text: '快速开始',
          items: [
            { text: '安装指南', link: '/getting-started/installation' },
            { text: '首次配置', link: '/getting-started/initial-setup' },
            { text: '基本使用', link: '/getting-started/basic-usage' },
            { text: '常见问题', link: '/getting-started/faq' }
          ]
        }
      ],
      '/features/': [
        {
          text: '功能特性',
          items: [
            { text: '功能概览', link: '/features/' }
          ]
        }
      ]
    },

    socialLinks: [
      { icon: 'github', link: 'https://github.com/kangvcar/ais' }
    ],

    footer: {
      message: '基于 MIT 许可证发布',
      copyright: 'Copyright © 2024 AIS Team'
    }
  }
})