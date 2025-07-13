# AIS Docker 部署指南

本指南详细介绍如何使用 Docker 部署和运行 AIS。

## 🐳 快速开始

### 一键安装
```bash
curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/docker-install.sh | bash
```

### 直接运行
```bash
# 拉取官方镜像
docker pull ais-terminal:latest

# 交互式运行
docker run -it --rm ais-terminal:latest
```

## 📋 部署方式

### 1. 交互式容器（推荐新手）
```bash
# 启动交互式容器
docker run -it --rm \
  --name ais-interactive \
  -v "$PWD:/workspace:ro" \
  ais-terminal:latest bash

# 在容器内使用AIS
ais --version
ais ask "Hello Docker"
```

### 2. 守护进程容器（推荐生产）
```bash
# 启动守护进程
docker run -d \
  --name ais-daemon \
  --restart unless-stopped \
  -v "$PWD:/workspace:ro" \
  -v ais-config:/home/ais/.config/ais \
  ais-terminal:latest tail -f /dev/null

# 进入容器执行命令
docker exec -it ais-daemon ais --version
docker exec -it ais-daemon bash
```

### 3. Docker Compose（推荐团队）
```yaml
# docker-compose.yml
version: '3.8'
services:
  ais:
    image: ais-terminal:latest
    container_name: ais-assistant
    restart: unless-stopped
    volumes:
      - ais-config:/home/ais/.config/ais
      - ./workspace:/workspace:ro
    command: ["tail", "-f", "/dev/null"]

volumes:
  ais-config:
```

```bash
# 启动服务
docker-compose up -d

# 使用AIS
docker-compose exec ais ais --version
```

## 🏗️ 自定义构建

### 从源码构建
```bash
# 克隆仓库
git clone https://github.com/kangvcar/ais.git
cd ais

# 构建镜像
docker build -t my-ais:latest .

# 多阶段构建（优化镜像大小）
docker build -t my-ais:latest --target builder .
```

### 自定义Dockerfile
```dockerfile
FROM ais-terminal:latest

# 添加自定义配置
COPY my-config.toml /home/ais/.config/ais/config.toml

# 安装额外工具
USER root
RUN apt-get update && apt-get install -y your-tools
USER ais

# 设置环境变量
ENV AIS_CUSTOM_SETTING=value
```

## 🔧 配置管理

### 环境变量
```bash
docker run -it --rm \
  -e AIS_PROVIDER=openai \
  -e AIS_API_KEY=your-key \
  -e AIS_DEBUG=true \
  ais-terminal:latest
```

### 配置文件挂载
```bash
# 挂载自定义配置
docker run -it --rm \
  -v /path/to/config.toml:/home/ais/.config/ais/config.toml:ro \
  ais-terminal:latest
```

### 持久化数据
```bash
# 创建数据卷
docker volume create ais-data

# 挂载数据卷
docker run -it --rm \
  -v ais-data:/home/ais/.config/ais \
  -v ais-data:/home/ais/.local/share/ais \
  ais-terminal:latest
```

## 🌐 网络和安全

### 网络配置
```bash
# 创建自定义网络
docker network create ais-network

# 在网络中运行
docker run -d \
  --name ais-service \
  --network ais-network \
  ais-terminal:latest
```

### 安全配置
```bash
# 非root用户运行
docker run -it --rm \
  --user $(id -u):$(id -g) \
  -v /etc/passwd:/etc/passwd:ro \
  ais-terminal:latest

# 只读根文件系统
docker run -it --rm \
  --read-only \
  --tmpfs /tmp \
  ais-terminal:latest
```

## 📊 监控和日志

### 健康检查
```bash
# 检查容器健康状态
docker ps --filter "name=ais"
docker inspect ais-daemon | grep Health

# 手动健康检查
docker exec ais-daemon ais --version
```

### 日志管理
```bash
# 查看日志
docker logs ais-daemon
docker logs -f ais-daemon  # 实时日志

# 配置日志轮转
docker run -d \
  --name ais-daemon \
  --log-driver json-file \
  --log-opt max-size=10m \
  --log-opt max-file=3 \
  ais-terminal:latest
```

## 🚀 生产部署

### Kubernetes 部署
```yaml
# ais-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ais-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ais
  template:
    metadata:
      labels:
        app: ais
    spec:
      containers:
      - name: ais
        image: ais-terminal:latest
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        volumeMounts:
        - name: config
          mountPath: /home/ais/.config/ais
      volumes:
      - name: config
        configMap:
          name: ais-config
```

### Docker Swarm 部署
```yaml
# docker-stack.yml
version: '3.8'
services:
  ais:
    image: ais-terminal:latest
    deploy:
      replicas: 3
      restart_policy:
        condition: on-failure
      resources:
        limits:
          memory: 512M
          cpus: '0.5'
    volumes:
      - ais-config:/home/ais/.config/ais
    networks:
      - ais-network

volumes:
  ais-config:

networks:
  ais-network:
    driver: overlay
```

## 🛠️ 故障排除

### 常见问题

#### 1. 容器无法启动
```bash
# 检查镜像
docker images | grep ais-terminal

# 检查容器日志
docker logs ais-daemon

# 调试模式运行
docker run -it --rm ais-terminal:latest bash
```

#### 2. 权限问题
```bash
# 检查用户映射
docker exec ais-daemon id

# 修复权限
docker exec --user root ais-daemon chown -R ais:ais /home/ais
```

#### 3. 网络连接问题
```bash
# 测试网络连接
docker exec ais-daemon ping -c 3 api.openai.com

# 检查DNS
docker exec ais-daemon nslookup api.openai.com
```

#### 4. 存储问题
```bash
# 检查卷挂载
docker inspect ais-daemon | grep Mounts

# 清理未使用的卷
docker volume prune
```

### 性能调优
```bash
# 限制资源使用
docker run -d \
  --name ais-optimized \
  --memory=256m \
  --cpus=0.5 \
  --restart unless-stopped \
  ais-terminal:latest

# 使用多阶段构建减小镜像大小
docker build --target production -t ais-terminal:slim .
```

## 📚 最佳实践

### 1. 镜像管理
- 使用特定版本标签而非`latest`
- 定期更新基础镜像
- 使用多阶段构建优化大小

### 2. 配置管理
- 使用环境变量传递配置
- 敏感信息使用secrets管理
- 配置文件使用卷挂载

### 3. 安全建议
- 非root用户运行容器
- 使用只读根文件系统
- 定期扫描镜像漏洞

### 4. 监控运维
- 配置健康检查
- 设置资源限制
- 收集日志和指标

## 🔗 相关资源

- [Docker 官方文档](https://docs.docker.com/)
- [Kubernetes 部署指南](https://kubernetes.io/docs/)
- [AIS 配置指南](CONFIGURATION.md)
- [性能优化指南](PERFORMANCE.md)

---

🐳 **享受 Docker 的便利性！** 有问题请查看 [故障排除](INSTALLATION.md#故障排除) 或提交 [Issue](https://github.com/kangvcar/ais/issues)。