# AIS - 基于Ubuntu的丰富工具版本
# 适合学习和开发场景，包含大量常用命令行工具

# 构建参数
ARG VERSION=2.4.0
ARG BUILD_DATE
ARG VCS_REF
ARG PYTHON_VERSION=3.11

FROM ubuntu:22.04 as builder

# 设置环境变量避免交互式安装
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Shanghai

# 设置工作目录
WORKDIR /build

# 安装Python和构建依赖
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3.11-dev \
    python3.11-venv \
    python3-pip \
    git \
    curl \
    build-essential \
    && ln -sf /usr/bin/python3.11 /usr/bin/python \
    && ln -sf /usr/bin/python3.11 /usr/bin/python3 \
    && rm -rf /var/lib/apt/lists/*

# 复制项目文件
COPY pyproject.toml ./
COPY src/ src/
COPY README.md CHANGELOG.md ./

# 安装构建工具并构建包
RUN pip install --no-cache-dir build && \
    python -m build

# 运行时镜像
FROM ubuntu:22.04

# 设置环境变量
ENV DEBIAN_FRONTEND=noninteractive \
    TZ=Asia/Shanghai \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    AIS_CONTAINER=1 \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PATH="/usr/local/bin:$PATH"

# 安装Python运行环境和丰富的开发工具
RUN apt-get update && apt-get install -y \
    # Python环境
    python3.11 \
    python3.11-dev \
    python3-pip \
    # 基础工具
    curl \
    wget \
    git \
    vim \
    nano \
    tree \
    htop \
    less \
    # 虚拟包的具体实现
    gawk \
    iputils-ping \
    # 网络工具
    telnet \
    netcat-openbsd \
    traceroute \
    nmap \
    # 系统工具（procps包提供ps/top等命令）
    procps \
    lsof \
    strace \
    tcpdump \
    # 文本处理
    jq \
    xmlstarlet \
    # 压缩工具（系统内置，无需安装）
    zip \
    unzip \
    # 开发工具
    make \
    gcc \
    g++ \
    # 文件工具（findutils包提供find/xargs等）
    findutils \
    rsync \
    # Node.js生态系统
    nodejs \
    npm \
    # 数据库客户端
    sqlite3 \
    mysql-client \
    postgresql-client \
    && ln -sf /usr/bin/python3.11 /usr/bin/python \
    && ln -sf /usr/bin/python3.11 /usr/bin/python3 \
    && rm -rf /var/lib/apt/lists/*

# 从构建阶段复制构建好的包
COPY --from=builder /build/dist/*.whl /tmp/

# 安装AIS
RUN pip install --no-cache-dir /tmp/*.whl && \
    rm -rf /tmp/*.whl

# 创建非root用户
RUN useradd -m -s /bin/bash ais && \
    mkdir -p /home/ais/.config/ais && \
    # 给用户sudo权限（可选，用于某些学习场景）
    apt-get update && apt-get install -y sudo && \
    usermod -aG sudo ais && \
    echo "ais ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && \
    chown -R ais:ais /home/ais && \
    rm -rf /var/lib/apt/lists/*

# 切换到非root用户
USER ais
WORKDIR /home/ais

# 设置默认配置
RUN ais config init || true

# 创建工作目录
RUN mkdir -p /home/ais/workspace

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD ais --version || exit 1

# 默认命令
CMD ["bash"]

# 标签信息
LABEL maintainer="AIS Team <ais@example.com>" \
      org.opencontainers.image.title="AIS Ubuntu - 丰富工具版" \
      org.opencontainers.image.description="基于Ubuntu的AIS学习助手，包含丰富的开发和系统工具" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.created="${BUILD_DATE}" \
      org.opencontainers.image.revision="${VCS_REF}" \
      org.opencontainers.image.source="https://github.com/kangvcar/ais" \
      org.opencontainers.image.base.name="ubuntu:22.04" \
      org.opencontainers.image.vendor="AIS Team" \
      ais.variant="ubuntu-full"