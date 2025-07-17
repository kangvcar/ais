# 📦 多平台部署指南

本项目支持在多个平台上部署，包括 GitHub Pages、Vercel、Netlify 和 Cloudflare Pages。每个平台都有相应的配置文件和部署说明。

## 🌍 支持的平台

| 平台 | 配置文件 | 状态 | 访问方式 |
|------|----------|------|----------|
| **GitHub Pages** | `.github/workflows/deploy-docs-simple.yml` | ✅ 自动部署 | 推送到 main 分支 |
| **Vercel** | `vercel.json` | ✅ 自动部署 | 连接 GitHub 仓库 |
| **Netlify** | `netlify.toml` | ✅ 自动部署 | 连接 GitHub 仓库 |
| **Cloudflare Pages** | `wrangler.toml` | ✅ 自动部署 | 连接 GitHub 仓库 |

## 🔧 环境变量配置

为了确保样式和资源正确加载，需要在各平台设置以下环境变量：

### 所有平台通用设置
```bash
VITEPRESS_BASE=/
```

## 📋 各平台部署步骤

### 1. GitHub Pages（已配置）
- **自动部署**：推送到 `main` 分支自动触发
- **配置文件**：`.github/workflows/deploy-docs-simple.yml`
- **访问地址**：`https://yourusername.github.io/ais/`

### 2. Vercel 
#### 方法1：控制面板部署
1. 登录 [Vercel Dashboard](https://vercel.com/dashboard)
2. 点击 "New Project" → "Import Git Repository"
3. 选择你的 GitHub 仓库
4. 设置环境变量：
   - **Name**: `VITEPRESS_BASE`
   - **Value**: `/`
   - **Environment**: Production, Preview, Development
5. 点击 "Deploy"

#### 方法2：CLI部署
```bash
# 安装 Vercel CLI
npm i -g vercel

# 登录
vercel login

# 部署
vercel

# 设置环境变量
vercel env add VITEPRESS_BASE
# 输入值: /
```

### 3. Netlify
#### 方法1：控制面板部署
1. 登录 [Netlify Dashboard](https://app.netlify.com/)
2. 点击 "New site from Git"
3. 选择你的 GitHub 仓库
4. 构建设置会自动读取 `netlify.toml`
5. 如需手动设置环境变量：
   - Site settings → Environment variables
   - 添加 `VITEPRESS_BASE` = `/`

#### 方法2：CLI部署
```bash
# 安装 Netlify CLI
npm i -g netlify-cli

# 登录
netlify login

# 部署
netlify deploy

# 生产部署
netlify deploy --prod
```

### 4. Cloudflare Pages
#### 方法1：控制面板部署（推荐）
1. 登录 [Cloudflare Dashboard](https://dash.cloudflare.com/)
2. 进入 "Pages" → "Create a project"
3. 选择 "Connect to Git" → 选择你的仓库
4. 配置构建设置：
   - **Build command**: `npm run docs:build`
   - **Build output directory**: `docs/.vitepress/dist`
   - **Root directory**: `/`
5. 环境变量设置：
   - **Variable name**: `VITEPRESS_BASE`
   - **Value**: `/`
6. 点击 "Save and Deploy"

#### 方法2：Wrangler CLI部署
```bash
# 安装 Wrangler CLI
npm i -g wrangler

# 登录
wrangler login

# 构建项目
VITEPRESS_BASE=/ npm run docs:build

# 部署（直接上传构建结果）
wrangler pages deploy docs/.vitepress/dist --project-name=ais-docs
```

> **注意**：由于Cloudflare Pages的配置格式变化，推荐使用控制面板部署方式，更加稳定可靠。

## 🧪 本地测试

### 测试配置
```bash
# 检查配置
npm run check-vercel

# 测试构建
VITEPRESS_BASE=/ npm run docs:build

# 预览构建结果
npm run docs:preview
```

### 测试不同平台的构建
```bash
# 测试 GitHub Pages 构建（默认）
npm run docs:build

# 测试其他平台构建
VITEPRESS_BASE=/ npm run docs:build
```

## 🎯 最佳实践

1. **环境变量管理**：在所有平台上都设置 `VITEPRESS_BASE=/`
2. **缓存优化**：各平台的配置文件已包含缓存优化设置
3. **自动部署**：推荐使用 Git 连接实现自动部署
4. **监控部署**：定期检查各平台的部署状态

## 🔍 故障排除

### 常见问题
1. **样式不加载**：检查 `VITEPRESS_BASE` 环境变量是否正确设置
2. **资源路径错误**：确保构建输出目录配置正确
3. **构建失败**：检查 Node.js 版本是否为 20+

### 调试命令
```bash
# 检查环境变量
echo $VITEPRESS_BASE

# 检查构建输出
ls -la docs/.vitepress/dist/

# 检查配置
npm run check-vercel
```

## 📞 支持

如果在部署过程中遇到问题，请：
1. 检查对应平台的配置文件
2. 确认环境变量设置正确
3. 查看平台的部署日志
4. 提交 Issue 到项目仓库