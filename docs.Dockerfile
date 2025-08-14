# 多阶段构建 - 构建AIS文档网站
# Stage 1: 构建阶段
FROM node:20-alpine AS builder

# 设置工作目录
WORKDIR /app

# 安装依赖
COPY package*.json ./
RUN npm install

# 复制文档相关文件
COPY docs/ ./docs/
COPY netlify.toml ./netlify.toml
COPY vercel.json ./vercel.json

# 构建文档（设置为根路径）
ENV VITEPRESS_BASE=/
RUN npm run docs:build

# Stage 2: 生产阶段
FROM nginx:alpine

# 安装ca-certificates以支持HTTPS
RUN apk add --no-cache ca-certificates

# 创建nginx配置
COPY <<EOF /etc/nginx/conf.d/default.conf
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;
    
    # 启用gzip压缩
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
    
    # 处理SPA路由
    location / {
        try_files \$uri \$uri/ /index.html;
    }
    
    # 静态资源缓存
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # 安全头
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
    
    # 健康检查端点
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
EOF

# 从构建阶段复制构建结果
COPY --from=builder /app/docs/.vitepress/dist /usr/share/nginx/html

# 设置权限
RUN chown -R nginx:nginx /usr/share/nginx/html && \
    chmod -R 755 /usr/share/nginx/html

# 添加元数据标签
LABEL org.opencontainers.image.title="AIS Documentation" \
      org.opencontainers.image.description="AIS项目文档网站 - 上下文感知的错误分析学习助手" \
      org.opencontainers.image.vendor="AIS Team" \
      org.opencontainers.image.url="https://github.com/kangvcar/ais" \
      org.opencontainers.image.source="https://github.com/kangvcar/ais" \
      org.opencontainers.image.documentation="https://github.com/kangvcar/ais/tree/main/docs"

# 健康检查 (使用wget，nginx镜像自带)
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost/health || exit 1

# 暴露端口
EXPOSE 80

# 启动nginx
CMD ["nginx", "-g", "daemon off;"]