#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

console.log('🔍 检查多平台部署配置...\n');

// 检查环境变量
console.log('📋 环境变量检查:');
console.log('- VITEPRESS_BASE:', process.env.VITEPRESS_BASE || '未设置（将使用默认值 /ais/）');

// 检查base路径
const base = process.env.VITEPRESS_BASE || '/ais/';
console.log('- 实际使用的base路径:', base);

// 检查图标路径
const iconPath = `${base}logo-icon.ico`;
console.log('- 图标路径:', iconPath);

console.log('\n📁 配置文件检查:');

// 检查各平台配置文件
const configs = [
    { name: 'GitHub Pages', file: '.github/workflows/deploy-docs-simple.yml' },
    { name: 'Vercel', file: 'vercel.json' },
    { name: 'Netlify', file: 'netlify.toml' },
    { name: 'Cloudflare Pages', file: 'wrangler.toml' },
    { name: 'VitePress', file: 'docs/.vitepress/config.mts' }
];

configs.forEach(config => {
    const exists = fs.existsSync(config.file);
    const status = exists ? '✅' : '❌';
    console.log(`- ${status} ${config.name}: ${config.file}`);
});

console.log('\n📦 构建测试:');
console.log('- 输出目录:', 'docs/.vitepress/dist');
console.log('- 构建命令:', 'npm run docs:build');

// 检查构建输出目录
const distPath = 'docs/.vitepress/dist';
if (fs.existsSync(distPath)) {
    console.log('- 构建输出: ✅ 存在');
    const files = fs.readdirSync(distPath);
    console.log(`- 文件数量: ${files.length}`);
    
    // 检查关键文件
    const keyFiles = ['index.html', 'assets', 'logo.png', 'logo-icon.ico'];
    keyFiles.forEach(file => {
        const exists = files.includes(file);
        const status = exists ? '✅' : '❌';
        console.log(`  - ${status} ${file}`);
    });
} else {
    console.log('- 构建输出: ❌ 不存在（运行 npm run docs:build 生成）');
}

console.log('\n🌍 平台部署建议:');

// 给出建议
if (!process.env.VITEPRESS_BASE) {
    console.log('💡 为了在 Vercel、Netlify、Cloudflare Pages 上正常部署，请设置环境变量：');
    console.log('   VITEPRESS_BASE = /');
    console.log('');
    console.log('📝 各平台设置方法：');
    console.log('- Vercel: Dashboard → Settings → Environment Variables');
    console.log('- Netlify: Site settings → Environment variables');
    console.log('- Cloudflare Pages: Workers & Pages → Settings → Environment variables');
} else {
    console.log('🎉 环境变量已正确设置！');
}

console.log('\n📚 查看详细部署指南：');
console.log('cat DEPLOYMENT.md');

console.log('\n✅ 配置检查完成');