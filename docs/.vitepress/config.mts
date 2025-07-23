import { defineConfig } from 'vitepress'
import { withMermaid } from 'vitepress-plugin-mermaid'

export default defineConfig(withMermaid({
  title: 'AIS 文档',
  description: 'AIS - 上下文感知的错误分析学习助手',
  lang: 'zh-CN',
  base: process.env.VITEPRESS_BASE || '/ais/',
  
  head: [
    ['link', { rel: 'icon', href: `${process.env.VITEPRESS_BASE || '/ais/'}logo.ico` }],
    ['link', { rel: 'shortcut icon', href: `${process.env.VITEPRESS_BASE || '/ais/'}logo.ico` }],
    ['link', { rel: 'apple-touch-icon', href: `${process.env.VITEPRESS_BASE || '/ais/'}logo.ico` }]
  ],
  
  themeConfig: {
    logo: '/logo-robot.png',
    siteTitle: 'AIS',
    
    nav: [
      { text: '首页', link: '/' },
      { 
        text: '快速开始', 
        link: '/getting-started/installation',
        activeMatch: '^/getting-started/'
      },
      { 
        text: '功能特性', 
        link: '/features/',
        activeMatch: '^/features/'
      },
      { 
        text: '配置指南', 
        link: '/configuration/',
        activeMatch: '^/configuration/'
      }
    ],

    sidebar: [
      {
        text: '快速开始',
        collapsed: false,
        items: [
          { text: '安装指南', link: '/getting-started/installation' },
          { text: '快速开始', link: '/getting-started/quick-start' },
          { text: 'Docker 使用', link: '/getting-started/docker-usage' },
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
        collapsed: false,
        items: [
          { text: '基本配置', link: '/configuration/basic-config' },
          { text: 'Shell 集成', link: '/configuration/shell-integration' },
          { text: '隐私设置', link: '/configuration/privacy-settings' }
        ]
      },
      {
        text: '开发者指南',
        collapsed: false,
        items: [
          { text: '贡献指南', link: '/development/contributing' },
          { text: '测试指南', link: '/development/testing' },
          { text: '架构设计', link: '/development/architecture' }
        ]
      },
      {
        text: '故障排除',
        collapsed: false,
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
      copyright: 'Copyright © 2025 AIS Team'
    },

    search: {
      provider: 'local'
    },

    // 移动端导航配置
    outline: {
      level: [2, 3]
    }
  },
  
  // Mermaid 配置
  mermaid: {
    theme: 'base',
    themeVariables: {
      // 主要颜色配置
      primaryColor: '#3b82f6',        // 主色调 - 蓝色
      primaryTextColor: '#1f2937',    // 主文本颜色 - 深灰
      primaryBorderColor: '#2563eb',  // 主边框颜色 - 深蓝
      lineColor: '#6b7280',          // 连接线颜色 - 中灰
      
      // 背景颜色
      background: '#ffffff',          // 图表背景 - 白色
      secondaryColor: '#f3f4f6',     // 次要颜色 - 浅灰
      
      // 节点样式
      tertiaryColor: '#e5e7eb',      // 第三级颜色
      
      // 文本样式
      fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
      fontSize: '14px',
      
      // 特定图表类型配置
      // 流程图
      cScale0: '#3b82f6',
      cScale1: '#10b981', 
      cScale2: '#f59e0b',
      cScale3: '#ef4444',
      cScale4: '#8b5cf6',
      cScale5: '#06b6d4',
      cScale6: '#84cc16',
      cScale7: '#f97316',
      
      // Git图表
      git0: '#3b82f6',
      git1: '#10b981',
      git2: '#f59e0b',
      git3: '#ef4444',
      git4: '#8b5cf6',
      git5: '#06b6d4',
      git6: '#84cc16',
      git7: '#f97316',
      
      // 序列图
      actorBkg: '#f8fafc',
      actorBorder: '#3b82f6',
      actorTextColor: '#1f2937',
      actorLineColor: '#6b7280',
      signalColor: '#1f2937',
      signalTextColor: '#1f2937',
      
      // 甘特图
      gridColor: '#e5e7eb',
      section0: '#3b82f6',
      section1: '#10b981',
      section2: '#f59e0b',
      section3: '#ef4444',
      
      // 状态图
      specialStateColor: '#f59e0b',
      
      // 类图
      classText: '#1f2937',
      
      // 用户旅程图
      fillType0: '#3b82f6',
      fillType1: '#10b981',
      fillType2: '#f59e0b',
      fillType3: '#ef4444',
      fillType4: '#8b5cf6',
      fillType5: '#06b6d4',
      fillType6: '#84cc16',
      fillType7: '#f97316'
    },
    
    // 流程图配置
    flowchart: {
      htmlLabels: true,
      curve: 'basis',
      padding: 15,
      nodeSpacing: 50,
      rankSpacing: 50,
      diagramPadding: 8,
      useMaxWidth: true,
    },
    
    // 序列图配置
    sequence: {
      diagramMarginX: 50,
      diagramMarginY: 10,
      actorMargin: 50,
      width: 150,
      height: 65,
      boxMargin: 10,
      boxTextMargin: 5,
      noteMargin: 10,
      messageMargin: 35,
      mirrorActors: true,
      bottomMarginAdj: 1,
      useMaxWidth: true,
      rightAngles: false,
      showSequenceNumbers: false,
    },
    
    // 甘特图配置  
    gantt: {
      titleTopMargin: 25,
      barHeight: 20,
      fontSize: 11,
      gridLineStartPadding: 35,
      topPadding: 50,
      rightPadding: 75,
    },
    
    // Git图配置
    gitGraph: {
      mainBranchName: 'main',
      showBranches: true,
      showCommitLabel: true,
      rotateCommitLabel: true,
    },
    
    // 全局配置
    startOnLoad: true,
    securityLevel: 'loose',
    maxTextSize: 50000,
    maxEdges: 500,
    htmlLabels: true,
    wrap: true,
    fontSize: 16,
  }
}))