#!/usr/bin/env node

console.log('🔍 检查Vercel部署配置...\n');

// 检查环境变量
console.log('环境变量检查:');
console.log('- VITEPRESS_BASE:', process.env.VITEPRESS_BASE || '未设置（将使用默认值 /ais/）');

// 检查base路径
const base = process.env.VITEPRESS_BASE || '/ais/';
console.log('- 实际使用的base路径:', base);

// 检查图标路径
const iconPath = `${base}logo-icon.ico`;
console.log('- 图标路径:', iconPath);

console.log('\n✅ 配置检查完成');

// 给出建议
if (!process.env.VITEPRESS_BASE) {
    console.log('\n💡 建议：');
    console.log('为了在Vercel上正常部署，请设置环境变量：');
    console.log('VITEPRESS_BASE = /');
} else {
    console.log('\n🎉 环境变量已正确设置！');
}