# AIS 文档

这是 AIS (AI Shell) 项目的官方文档站点，使用 VitePress 构建。

## 本地开发

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run docs:dev

# 构建文档
npm run docs:build

# 预览构建结果
npm run docs:preview
```

## 自动部署

文档会在每次推送到 main 分支时自动部署到 GitHub Pages。

### 启用 GitHub Pages

1. 进入 GitHub 仓库设置页面
2. 在左侧导航中选择 "Pages"
3. 在 "Source" 部分选择 "GitHub Actions"
4. 保存设置

部署完成后，文档将在 `https://kangvcar.github.io/ais/` 访问。

## 目录结构

```
docs/
├── .vitepress/
│   ├── config.mts          # VitePress 配置
│   └── theme/
│       ├── index.ts        # 主题配置
│       └── custom.css      # 自定义样式
├── public/                 # 静态资源
├── getting-started/        # 快速开始
├── features/              # 功能特性
├── configuration/         # 配置指南
├── development/           # 开发者指南
├── troubleshooting/       # 故障排除
└── index.md              # 首页
```

## 贡献

欢迎提交 Pull Request 来改进文档！请确保：

1. 文档内容准确且最新
2. 遵循现有的文档格式和风格
3. 在提交前本地测试构建结果