# Docker 使用指南

AIS 提供了基于 Ubuntu 22.04 的 Docker 镜像，包含丰富的开发工具和完整的 Python 环境，非常适合学习和实践各种命令行技能。

## 快速开始

### 构建镜像

```bash
# 克隆项目
git clone https://github.com/kangvcar/ais.git
cd ais

# 构建 Docker 镜像
docker build -t ais-terminal:latest .
```

### 基础使用

```bash
# 直接运行 AIS 命令
docker run --rm -it ais-terminal:latest ais ask "如何使用 Docker？"

# 进入交互式容器环境
docker run --rm -it ais-terminal:latest bash

# 在容器内使用 AIS
# ais config init  # 初始化配置
# ais ask "什么是容器化？"
# ais learn docker  # 学习 Docker 知识
```

## Docker Compose 使用

### 基础配置

创建 `docker-compose.yml` 文件：

```yaml
version: '3.8'

services:
  ais:
    build:
      context: .
      dockerfile: Dockerfile
    image: ais-terminal:latest
    container_name: ais-assistant
    restart: unless-stopped
    environment:
      - AIS_CONTAINER=1
      - TERM=xterm-256color
    volumes:
      # 配置持久化
      - ais-config:/home/ais/.config/ais
      # 工作空间挂载
      - ./workspace:/home/ais/workspace
      # Docker socket 访问（如果需要）
      - /var/run/docker.sock:/var/run/docker.sock:ro
    working_dir: /home/ais
    command: ["bash"]
    stdin_open: true
    tty: true

volumes:
  ais-config:
    driver: local
```

### 启动和使用

```bash
# 启动容器
docker-compose up -d

# 进入容器
docker-compose exec ais bash

# 查看日志
docker-compose logs -f ais

# 停止容器
docker-compose down
```

## 包含的工具和环境

AIS Docker 镜像基于 Ubuntu 22.04，包含以下丰富的工具集：

### 开发工具
- **Python 3.11** - 完整的 Python 开发环境
- **Node.js & npm** - JavaScript/TypeScript 开发
- **Git** - 版本控制系统
- **编译器** - gcc, g++, make, cmake

### 系统和网络工具
- **系统监控** - htop, ps, lsof, strace
- **网络工具** - ping, telnet, netcat, nmap, traceroute  
- **文本处理** - vim, nano, grep, sed, awk, jq, yq
- **文件工具** - tree, find, xargs, rsync

### 数据库客户端
- **SQLite** - sqlite3 命令行工具
- **MySQL** - mysql 客户端
- **PostgreSQL** - psql 客户端

## 实际使用示例

### 1. 学习 Linux 命令

```bash
# 进入容器
docker run --rm -it ais-terminal:latest bash

# 使用 AIS 学习系统命令
ais ask "如何查看系统进程？"
# AIS 会解释 ps, top, htop 等命令的使用

# 实际练习
ps aux | grep python
htop  # 交互式进程查看器
```

### 2. 项目代码分析

```bash
# 挂载项目目录到容器
docker run --rm -it \
  -v $(pwd):/workspace \
  -v ais-config:/home/ais/.config/ais \
  ais-terminal:latest bash

# 在容器内分析项目
cd /workspace
ais ask "分析这个项目的架构"
ais ask "如何优化这个 Python 项目？"

# 使用工具分析代码
tree .  # 查看目录结构
find . -name "*.py" | head -10  # 查找 Python 文件
grep -r "TODO" . --include="*.py"  # 查找待办事项
```

### 3. 网络问题诊断

```bash
# 容器内网络诊断
docker run --rm -it ais-terminal:latest bash

# 使用 AIS 学习网络命令
ais ask "如何诊断网络连接问题？"

# 实际使用网络工具
ping google.com
nmap -p 80,443 google.com
netstat -tuln  # 查看监听端口
lsof -i :80    # 查看端口占用
```

### 4. 数据处理和分析

```bash
# 创建测试数据并分析
docker run --rm -it ais-terminal:latest bash

# 生成测试数据
echo -e "name,age,city\\nAlice,25,Beijing\\nBob,30,Shanghai\\nCharlie,35,Guangzhou" > /tmp/data.csv

# 使用 AIS 学习数据处理
ais ask "如何用命令行处理 CSV 数据？"

# 实际处理数据
cat /tmp/data.csv | column -t -s ','  # 格式化显示
jq -r '.[] | "\(.name): \(.age)"' <<< '[]'  # JSON 处理示例
awk -F',' 'NR>1 {sum+=$2} END {print "平均年龄:", sum/(NR-1)}' /tmp/data.csv
```

### 5. Git 和版本控制学习

```bash
# 在容器内学习 Git
docker run --rm -it \
  -v ais-config:/home/ais/.config/ais \
  ais-terminal:latest bash

# 创建测试仓库
mkdir /tmp/git-practice && cd /tmp/git-practice
git init

# 使用 AIS 学习 Git 命令
ais ask "Git 的基本工作流程是什么？"
ais learn git  # 系统学习 Git 知识

# 实际练习 Git 命令
echo "Hello World" > README.md
git add README.md
git commit -m "Initial commit"
git log --oneline
git status
```

## 高级配置

### 多项目环境

```yaml
# docker-compose.advanced.yml
version: '3.8'

services:
  ais-dev:
    build: .
    image: ais-terminal:latest
    container_name: ais-development
    volumes:
      - ais-config:/home/ais/.config/ais
      - ./projects:/home/ais/projects
      - ./scripts:/home/ais/scripts
    environment:
      - AIS_CONTAINER=1
      - AIS_WORKSPACE=/home/ais/projects
    working_dir: /home/ais/projects
    command: ["bash"]
    stdin_open: true
    tty: true
    networks:
      - ais-network

  # 可选：数据库服务用于练习
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: testdb
      POSTGRES_USER: testuser  
      POSTGRES_PASSWORD: testpass
    ports:
      - "5432:5432"
    networks:
      - ais-network

  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: rootpass
      MYSQL_DATABASE: testdb
      MYSQL_USER: testuser
      MYSQL_PASSWORD: testpass
    ports:
      - "3306:3306"
    networks:
      - ais-network

networks:
  ais-network:
    driver: bridge

volumes:
  ais-config:
```

### 生产环境部署

```bash
# 创建专用网络和数据卷
docker network create ais-network
docker volume create ais-config

# 后台运行 AIS 服务
docker run -d \
  --name ais-assistant \
  --network ais-network \
  --restart unless-stopped \
  -v ais-config:/home/ais/.config/ais \
  -v /host/projects:/home/ais/projects:ro \
  -e AIS_CONTAINER=1 \
  ais-terminal:latest \
  tail -f /dev/null

# 执行 AIS 命令
docker exec -it ais-assistant ais ask "分析这个系统的性能"
docker exec -it ais-assistant bash
```

## 配置管理

### 持久化配置

```bash
# 初始化配置
docker run --rm -it \
  -v ais-config:/home/ais/.config/ais \
  ais-terminal:latest \
  ais config init

# 设置 AI 服务提供商
docker exec -it ais-assistant ais config --set default_provider=openai

# 查看配置
docker exec -it ais-assistant ais config --show
```

### 环境变量配置

```bash
# 通过环境变量配置
docker run --rm -it \
  -e AIS_CONTAINER=1 \
  -e AIS_AUTO_ANALYSIS=true \
  -e AIS_CONTEXT_LEVEL=detailed \
  ais-terminal:latest bash
```

## 故障排除

### 常见问题

**1. 容器无法启动**
```bash
# 检查镜像是否构建成功
docker images | grep ais-terminal

# 查看容器日志
docker logs ais-assistant

# 检查端口占用
docker port ais-assistant
```

**2. 权限问题**
```bash
# 以 root 用户运行（仅调试用）
docker run --rm -it --user root ais-terminal:latest bash

# 检查文件权限
docker exec -it ais-assistant ls -la /home/ais/.config
```

**3. 网络连接问题**
```bash
# 测试网络连通性
docker exec -it ais-assistant ping google.com

# 检查 DNS 设置
docker exec -it ais-assistant cat /etc/resolv.conf
```

## 最佳实践

1. **配置持久化** - 始终使用数据卷保存配置
2. **资源限制** - 在生产环境中设置内存和 CPU 限制
3. **安全考虑** - 避免以 root 用户运行，限制容器权限
4. **日志管理** - 配置适当的日志轮转和存储
5. **备份策略** - 定期备份配置和学习数据

```bash
# 资源限制示例
docker run --rm -it \
  --memory="512m" \
  --cpus="1.0" \
  ais-terminal:latest bash

# 安全配置示例
docker run --rm -it \
  --read-only \
  --tmpfs /tmp \
  --security-opt no-new-privileges \
  ais-terminal:latest bash
```

通过 Docker 使用 AIS，您可以在隔离的环境中安全地学习和实践各种命令行技能，同时享受完整的工具链和 AI 辅助学习体验。