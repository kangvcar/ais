# AIS - AI智能终端助手 Docker镜像
# 多阶段构建，优化镜像大小

# 构建参数
ARG VERSION=0.1.0
ARG BUILD_DATE
ARG VCS_REF

FROM python:3.11-slim as builder

# 设置工作目录
WORKDIR /build

# 安装构建依赖
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制项目文件（按照构建需要的优先级复制）
COPY pyproject.toml ./
COPY src/ src/
COPY README.md CHANGELOG.md ./

# 安装构建工具并构建包
RUN pip install --no-cache-dir build && \
    python -m build

# 运行时镜像
FROM python:3.11-slim

# 设置环境变量
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    AIS_CONTAINER=1 \
    PATH="/usr/local/bin:$PATH"

# 安装运行时依赖
RUN apt-get update && apt-get install -y \
    curl \
    bash \
    && rm -rf /var/lib/apt/lists/*

# 从构建阶段复制构建好的包
COPY --from=builder /build/dist/*.whl /tmp/

# 安装AIS
RUN pip install --no-cache-dir /tmp/*.whl && \
    rm -rf /tmp/*.whl

# 创建非root用户
RUN useradd -m -s /bin/bash ais && \
    mkdir -p /home/ais/.config/ais && \
    chown -R ais:ais /home/ais

# 切换到非root用户
USER ais
WORKDIR /home/ais

# 设置默认配置
RUN ais config init || true

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD ais --version || exit 1

# 默认命令
CMD ["ais", "--help"]

# 标签信息（符合OCI标准）
LABEL maintainer="AIS Team <ais@example.com>" \
      org.opencontainers.image.title="AIS - AI智能终端助手" \
      org.opencontainers.image.description="AI-powered terminal assistant for intelligent error analysis and learning" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.created="${BUILD_DATE}" \
      org.opencontainers.image.revision="${VCS_REF}" \
      org.opencontainers.image.source="https://github.com/kangvcar/ais" \
      org.opencontainers.image.url="https://github.com/kangvcar/ais" \
      org.opencontainers.image.documentation="https://github.com/kangvcar/ais/blob/main/README.md" \
      org.opencontainers.image.licenses="MIT" \
      org.opencontainers.image.vendor="AIS Team" \
      org.opencontainers.image.authors="kangvcar <kangvcar@gmail.com>"