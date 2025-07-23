Run docker/build-push-action@v5
GitHub Actions runtime token ACs
Docker info
Proxy configuration
Buildx version
Builder info
/usr/bin/docker buildx build --build-arg VERSION=main --build-arg BUILD_DATE=2025-07-23T14:23:46+08:00 --build-arg VCS_REF=1cda6dea30c9a44f950358dd37b7b46a99639049 --cache-from type=gha --cache-to type=gha,mode=max --file ./Dockerfile --iidfile /home/runner/work/_temp/docker-actions-toolkit-mOeet7/build-iidfile-0d1e1e08eb.txt --label org.opencontainers.image.created=2025-07-23T06:24:22.059Z --label org.opencontainers.image.description=上下文感知的错误分析学习助手，让每次报错都是成长 --label org.opencontainers.image.licenses=MIT --label org.opencontainers.image.revision=1cda6dea30c9a44f950358dd37b7b46a99639049 --label org.opencontainers.image.source=https://github.com/***/ais --label org.opencontainers.image.title=AIS - 上下文感知的错误分析学习助手 --label org.opencontainers.image.url=https://github.com/***/ais --label org.opencontainers.image.vendor=AIS Team --label org.opencontainers.image.version=latest --platform linux/amd64,linux/arm64 --attest type=provenance,mode=max,builder-id=https://github.com/***/ais/actions/runs/16463176668 --tag docker.io/***/ais:latest --tag docker.io/***/ais:main-1cda6de --metadata-file /home/runner/work/_temp/docker-actions-toolkit-mOeet7/build-metadata-6c09b7b98c.json --push .
#0 building with "builder-78336a67-f60c-4d66-8b3a-dab5c16ba2ca" instance using docker-container driver

#1 [internal] load build definition from Dockerfile
#1 transferring dockerfile: 3.92kB done
#1 WARN: FromAsCasing: 'as' and 'FROM' keywords' casing do not match (line 10)
#1 DONE 0.0s

#2 [auth] library/ubuntu:pull token for registry-1.docker.io
#2 DONE 0.0s

#3 [linux/amd64 internal] load metadata for docker.io/library/ubuntu:22.04
#3 DONE 0.6s

#4 [linux/arm64 internal] load metadata for docker.io/library/ubuntu:22.04
#4 DONE 0.6s

#5 [internal] load .dockerignore
#5 transferring context: 911B done
#5 DONE 0.0s

#6 [internal] load build context
#6 DONE 0.0s

#7 [linux/arm64 builder 1/7] FROM docker.io/library/ubuntu:22.04@sha256:1ec65b2719518e27d4d25f104d93f9fac60dc437f81452302406825c46fcc9cb
#7 resolve docker.io/library/ubuntu:22.04@sha256:1ec65b2719518e27d4d25f104d93f9fac60dc437f81452302406825c46fcc9cb done
#7 DONE 0.0s

#8 importing cache manifest from gha:11440515367744974498
#8 DONE 0.2s

#6 [internal] load build context
#6 transferring context: 306.45kB 0.0s done
#6 DONE 0.0s

#9 [linux/amd64 builder 1/7] FROM docker.io/library/ubuntu:22.04@sha256:1ec65b2719518e27d4d25f104d93f9fac60dc437f81452302406825c46fcc9cb
#9 resolve docker.io/library/ubuntu:22.04@sha256:1ec65b2719518e27d4d25f104d93f9fac60dc437f81452302406825c46fcc9cb done
#9 sha256:1d387567261efec2a352c45b8d512a8db5c246122fb9f246ae9190252a0c3adb 0B / 29.54MB 0.2s
#9 sha256:1d387567261efec2a352c45b8d512a8db5c246122fb9f246ae9190252a0c3adb 29.54MB / 29.54MB 0.4s done
#9 extracting sha256:1d387567261efec2a352c45b8d512a8db5c246122fb9f246ae9190252a0c3adb
#9 ...

#7 [linux/arm64 builder 1/7] FROM docker.io/library/ubuntu:22.04@sha256:1ec65b2719518e27d4d25f104d93f9fac60dc437f81452302406825c46fcc9cb
#7 sha256:ef6d179edc98e93dc6073cb3ddec6f1a6ed1d68d04cd7836a82abfd397922a05 27.36MB / 27.36MB 0.3s done
#7 extracting sha256:ef6d179edc98e93dc6073cb3ddec6f1a6ed1d68d04cd7836a82abfd397922a05 0.8s done
#7 DONE 1.1s

#9 [linux/amd64 builder 1/7] FROM docker.io/library/ubuntu:22.04@sha256:1ec65b2719518e27d4d25f104d93f9fac60dc437f81452302406825c46fcc9cb
#9 extracting sha256:1d387567261efec2a352c45b8d512a8db5c246122fb9f246ae9190252a0c3adb 0.9s done
#9 DONE 1.3s

#10 [linux/arm64 stage-1 2/8] RUN apt-get update && apt-get install -y     python3.11     python3.11-dev     python3-pip     curl     wget     git     vim     nano     tree     htop     less     grep     sed     awk     ping     telnet     netcat     traceroute     nmap     ps     top     lsof     strace     tcpdump     jq     yq     xmlstarlet     zip     unzip     tar     gzip     make     gcc     g++     git     find     xargs     rsync     nodejs     npm     sqlite3     mysql-client     postgresql-client     && ln -sf /usr/bin/python3.11 /usr/bin/python     && ln -sf /usr/bin/python3.11 /usr/bin/python3     && rm -rf /var/lib/apt/lists/*
#10 ...

#11 [linux/arm64 builder 2/7] WORKDIR /build
#11 DONE 0.2s

#12 [linux/amd64 builder 2/7] WORKDIR /build
#12 DONE 0.1s

#13 [linux/amd64 stage-1 2/8] RUN apt-get update && apt-get install -y     python3.11     python3.11-dev     python3-pip     curl     wget     git     vim     nano     tree     htop     less     grep     sed     awk     ping     telnet     netcat     traceroute     nmap     ps     top     lsof     strace     tcpdump     jq     yq     xmlstarlet     zip     unzip     tar     gzip     make     gcc     g++     git     find     xargs     rsync     nodejs     npm     sqlite3     mysql-client     postgresql-client     && ln -sf /usr/bin/python3.11 /usr/bin/python     && ln -sf /usr/bin/python3.11 /usr/bin/python3     && rm -rf /var/lib/apt/lists/*
#13 0.188 Get:1 http://archive.ubuntu.com/ubuntu jammy InRelease [270 kB]
#13 0.345 Get:2 http://security.ubuntu.com/ubuntu jammy-security InRelease [129 kB]
#13 0.366 Get:3 http://archive.ubuntu.com/ubuntu jammy-updates InRelease [128 kB]
#13 0.409 Get:4 http://archive.ubuntu.com/ubuntu jammy-backports InRelease [127 kB]
#13 0.496 Get:5 http://archive.ubuntu.com/ubuntu jammy/restricted amd64 Packages [164 kB]
#13 0.549 Get:6 http://archive.ubuntu.com/ubuntu jammy/universe amd64 Packages [17.5 MB]
#13 0.791 Get:7 http://archive.ubuntu.com/ubuntu jammy/main amd64 Packages [1792 kB]
#13 0.801 Get:8 http://archive.ubuntu.com/ubuntu jammy/multiverse amd64 Packages [266 kB]
#13 0.830 Get:9 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 Packages [3470 kB]
#13 0.851 Get:10 http://archive.ubuntu.com/ubuntu jammy-updates/multiverse amd64 Packages [75.9 kB]
#13 0.852 Get:11 http://archive.ubuntu.com/ubuntu jammy-updates/universe amd64 Packages [1573 kB]
#13 0.871 Get:12 http://archive.ubuntu.com/ubuntu jammy-updates/restricted amd64 Packages [5163 kB]
#13 0.875 Get:13 http://security.ubuntu.com/ubuntu jammy-security/multiverse amd64 Packages [48.5 kB]
#13 0.930 Get:14 http://archive.ubuntu.com/ubuntu jammy-backports/main amd64 Packages [83.2 kB]
#13 0.932 Get:15 http://archive.ubuntu.com/ubuntu jammy-backports/universe amd64 Packages [35.2 kB]
#13 0.995 Get:16 http://security.ubuntu.com/ubuntu jammy-security/main amd64 Packages [3159 kB]
#13 1.460 Get:17 http://security.ubuntu.com/ubuntu jammy-security/restricted amd64 Packages [4976 kB]
#13 1.590 Get:18 http://security.ubuntu.com/ubuntu jammy-security/universe amd64 Packages [1268 kB]
#13 2.404 Fetched 40.2 MB in 2s (17.6 MB/s)
#13 2.404 Reading package lists...
#13 3.758 Reading package lists...
#13 5.347 Building dependency tree...
#13 5.683 Reading state information...
#13 5.701 Package awk is a virtual package provided by:
#13 5.701   gawk 1:5.1.0-1ubuntu0.1
#13 5.701   original-awk 2018-08-27-1
#13 5.702   mawk 1.3.4.20200120-3
#13 5.702 
#13 5.702 Package ping is a virtual package provided by:
#13 5.702   inetutils-ping 2:2.2-2ubuntu0.1
#13 5.702   iputils-ping 3:20211215-1
#13 5.702 
#13 5.706 E: Package 'awk' has no installation candidate
#13 5.708 E: Package 'ping' has no installation candidate
#13 5.709 E: Unable to locate package ps
#13 5.710 E: Unable to locate package top
#13 5.713 E: Unable to locate package yq
#13 5.714 E: Unable to locate package find
#13 5.715 E: Unable to locate package xargs
#13 ERROR: process "/bin/sh -c apt-get update && apt-get install -y     python3.11     python3.11-dev     python3-pip     curl     wget     git     vim     nano     tree     htop     less     grep     sed     awk     ping     telnet     netcat     traceroute     nmap     ps     top     lsof     strace     tcpdump     jq     yq     xmlstarlet     zip     unzip     tar     gzip     make     gcc     g++     git     find     xargs     rsync     nodejs     npm     sqlite3     mysql-client     postgresql-client     && ln -sf /usr/bin/python3.11 /usr/bin/python     && ln -sf /usr/bin/python3.11 /usr/bin/python3     && rm -rf /var/lib/apt/lists/*" did not complete successfully: exit code: 100

#14 [linux/amd64 builder 3/7] RUN apt-get update && apt-get install -y     python${PYTHON_VERSION}     python${PYTHON_VERSION}-dev     python${PYTHON_VERSION}-venv     python3-pip     git     curl     build-essential     && ln -sf /usr/bin/python${PYTHON_VERSION} /usr/bin/python     && ln -sf /usr/bin/python${PYTHON_VERSION} /usr/bin/python3     && rm -rf /var/lib/apt/lists/*
#14 0.164 Get:1 http://security.ubuntu.com/ubuntu jammy-security InRelease [129 kB]
#14 0.288 Get:2 http://archive.ubuntu.com/ubuntu jammy InRelease [270 kB]
#14 0.413 Get:3 http://security.ubuntu.com/ubuntu jammy-security/restricted amd64 Packages [4976 kB]
#14 0.643 Get:4 http://security.ubuntu.com/ubuntu jammy-security/main amd64 Packages [3159 kB]
#14 0.664 Get:5 http://security.ubuntu.com/ubuntu jammy-security/multiverse amd64 Packages [48.5 kB]
#14 0.664 Get:6 http://security.ubuntu.com/ubuntu jammy-security/universe amd64 Packages [1268 kB]
#14 0.821 Get:7 http://archive.ubuntu.com/ubuntu jammy-updates InRelease [128 kB]
#14 0.946 Get:8 http://archive.ubuntu.com/ubuntu jammy-backports InRelease [127 kB]
#14 1.075 Get:9 http://archive.ubuntu.com/ubuntu jammy/universe amd64 Packages [17.5 MB]
#14 1.774 Get:10 http://archive.ubuntu.com/ubuntu jammy/restricted amd64 Packages [164 kB]
#14 1.775 Get:11 http://archive.ubuntu.com/ubuntu jammy/main amd64 Packages [1792 kB]
#14 1.824 Get:12 http://archive.ubuntu.com/ubuntu jammy/multiverse amd64 Packages [266 kB]
#14 1.826 Get:13 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 Packages [3470 kB]
#14 1.904 Get:14 http://archive.ubuntu.com/ubuntu jammy-updates/universe amd64 Packages [1573 kB]
#14 1.935 Get:15 http://archive.ubuntu.com/ubuntu jammy-updates/restricted amd64 Packages [5163 kB]
#14 2.054 Get:16 http://archive.ubuntu.com/ubuntu jammy-updates/multiverse amd64 Packages [75.9 kB]
#14 2.055 Get:17 http://archive.ubuntu.com/ubuntu jammy-backports/universe amd64 Packages [35.2 kB]
#14 2.056 Get:18 http://archive.ubuntu.com/ubuntu jammy-backports/main amd64 Packages [83.2 kB]
#14 3.051 Fetched 40.2 MB in 3s (13.7 MB/s)
#14 3.051 Reading package lists...
#14 4.450 Reading package lists...
#14 CANCELED

#15 [linux/arm64 builder 3/7] RUN apt-get update && apt-get install -y     python${PYTHON_VERSION}     python${PYTHON_VERSION}-dev     python${PYTHON_VERSION}-venv     python3-pip     git     curl     build-essential     && ln -sf /usr/bin/python${PYTHON_VERSION} /usr/bin/python     && ln -sf /usr/bin/python${PYTHON_VERSION} /usr/bin/python3     && rm -rf /var/lib/apt/lists/*
#15 0.592 Get:1 http://ports.ubuntu.com/ubuntu-ports jammy InRelease [270 kB]
#15 0.896 Get:2 http://ports.ubuntu.com/ubuntu-ports jammy-updates InRelease [128 kB]
#15 0.898 Get:3 http://ports.ubuntu.com/ubuntu-ports jammy-backports InRelease [127 kB]
#15 0.899 Get:4 http://ports.ubuntu.com/ubuntu-ports jammy-security InRelease [129 kB]
#15 3.737 Get:5 http://ports.ubuntu.com/ubuntu-ports jammy/universe arm64 Packages [17.2 MB]
#15 5.284 Get:6 http://ports.ubuntu.com/ubuntu-ports jammy/main arm64 Packages [1758 kB]
#15 5.582 Get:7 http://ports.ubuntu.com/ubuntu-ports jammy/restricted arm64 Packages [24.2 kB]
#15 5.590 Get:8 http://ports.ubuntu.com/ubuntu-ports jammy/multiverse arm64 Packages [224 kB]
#15 CANCELED

#10 [linux/arm64 stage-1 2/8] RUN apt-get update && apt-get install -y     python3.11     python3.11-dev     python3-pip     curl     wget     git     vim     nano     tree     htop     less     grep     sed     awk     ping     telnet     netcat     traceroute     nmap     ps     top     lsof     strace     tcpdump     jq     yq     xmlstarlet     zip     unzip     tar     gzip     make     gcc     g++     git     find     xargs     rsync     nodejs     npm     sqlite3     mysql-client     postgresql-client     && ln -sf /usr/bin/python3.11 /usr/bin/python     && ln -sf /usr/bin/python3.11 /usr/bin/python3     && rm -rf /var/lib/apt/lists/*
#10 0.848 Get:1 http://ports.ubuntu.com/ubuntu-ports jammy InRelease [270 kB]
#10 1.407 Get:2 http://ports.ubuntu.com/ubuntu-ports jammy-updates InRelease [128 kB]
#10 1.491 Get:3 http://ports.ubuntu.com/ubuntu-ports jammy-backports InRelease [127 kB]
#10 1.623 Get:4 http://ports.ubuntu.com/ubuntu-ports jammy-security InRelease [129 kB]
#10 4.470 Get:5 http://ports.ubuntu.com/ubuntu-ports jammy/main arm64 Packages [1758 kB]
#10 5.596 Get:6 http://ports.ubuntu.com/ubuntu-ports jammy/restricted arm64 Packages [24.2 kB]
#10 5.708 Get:7 http://ports.ubuntu.com/ubuntu-ports jammy/universe arm64 Packages [17.2 MB]
#10 CANCELED
------
 > [linux/amd64 stage-1 2/8] RUN apt-get update && apt-get install -y     python3.11     python3.11-dev     python3-pip     curl     wget     git     vim     nano     tree     htop     less     grep     sed     awk     ping     telnet     netcat     traceroute     nmap     ps     top     lsof     strace     tcpdump     jq     yq     xmlstarlet     zip     unzip     tar     gzip     make     gcc     g++     git     find     xargs     rsync     nodejs     npm     sqlite3     mysql-client     postgresql-client     && ln -sf /usr/bin/python3.11 /usr/bin/python     && ln -sf /usr/bin/python3.11 /usr/bin/python3     && rm -rf /var/lib/apt/lists/*:
5.702   inetutils-ping 2:2.2-2ubuntu0.1
5.702   iputils-ping 3:20211215-1
5.702 
5.706 E: Package 'awk' has no installation candidate
5.708 E: Package 'ping' has no installation candidate
5.709 E: Unable to locate package ps
5.710 E: Unable to locate package top
5.713 E: Unable to locate package yq
5.714 E: Unable to locate package find
5.715 E: Unable to locate package xargs
------

 4 warnings found (use docker --debug to expand):
 - FromAsCasing: 'as' and 'FROM' keywords' casing do not match (line 10)
 - UndefinedVar: Usage of undefined variable '$VERSION' (line 155)
 - UndefinedVar: Usage of undefined variable '$BUILD_DATE' (line 155)
 - UndefinedVar: Usage of undefined variable '$VCS_REF' (line 155)
Dockerfile:55
--------------------
  54 |     # 安装Python运行环境和丰富的开发工具
  55 | >>> RUN apt-get update && apt-get install -y \
  56 | >>>     # Python环境
  57 | >>>     python3.11 \
  58 | >>>     python3.11-dev \
  59 | >>>     python3-pip \
  60 | >>>     # 基础工具
  61 | >>>     curl \
  62 | >>>     wget \
  63 | >>>     git \
  64 | >>>     vim \
  65 | >>>     nano \
  66 | >>>     tree \
  67 | >>>     htop \
  68 | >>>     less \
  69 | >>>     grep \
  70 | >>>     sed \
  71 | >>>     awk \
  72 | >>>     # 网络工具
  73 | >>>     ping \
  74 | >>>     telnet \
  75 | >>>     netcat \
  76 | >>>     traceroute \
  77 | >>>     nmap \
  78 | >>>     # 系统工具
  79 | >>>     ps \
  80 | >>>     top \
  81 | >>>     lsof \
  82 | >>>     strace \
  83 | >>>     tcpdump \
  84 | >>>     # 文本处理
  85 | >>>     jq \
  86 | >>>     yq \
  87 | >>>     xmlstarlet \
  88 | >>>     # 压缩工具
  89 | >>>     zip \
  90 | >>>     unzip \
  91 | >>>     tar \
  92 | >>>     gzip \
  93 | >>>     # 开发工具
  94 | >>>     make \
  95 | >>>     gcc \
  96 | >>>     g++ \
  97 | >>>     # 版本控制
  98 | >>>     git \
  99 | >>>     # 文件工具
 100 | >>>     find \
 101 | >>>     xargs \
 102 | >>>     rsync \
 103 | >>>     # Docker工具（如果需要Docker-in-Docker）
 104 | >>>     # docker.io \
 105 | >>>     # docker-compose \
 106 | >>>     # Node.js生态系统（常用于前端项目）
 107 | >>>     nodejs \
 108 | >>>     npm \
 109 | >>>     # 数据库客户端
 110 | >>>     sqlite3 \
 111 | >>>     mysql-client \
 112 | >>>     postgresql-client \
 113 | >>>     # 云工具（可选，根据需要启用）
 114 | >>>     # awscli \
 115 | >>>     # kubectl \
 116 | >>>     && ln -sf /usr/bin/python3.11 /usr/bin/python \
 117 | >>>     && ln -sf /usr/bin/python3.11 /usr/bin/python3 \
 118 | >>>     && rm -rf /var/lib/apt/lists/*
 119 |     
--------------------
ERROR: failed to build: failed to solve: process "/bin/sh -c apt-get update && apt-get install -y     python3.11     python3.11-dev     python3-pip     curl     wget     git     vim     nano     tree     htop     less     grep     sed     awk     ping     telnet     netcat     traceroute     nmap     ps     top     lsof     strace     tcpdump     jq     yq     xmlstarlet     zip     unzip     tar     gzip     make     gcc     g++     git     find     xargs     rsync     nodejs     npm     sqlite3     mysql-client     postgresql-client     && ln -sf /usr/bin/python3.11 /usr/bin/python     && ln -sf /usr/bin/python3.11 /usr/bin/python3     && rm -rf /var/lib/apt/lists/*" did not complete successfully: exit code: 100
Error: buildx failed with: ERROR: failed to build: failed to solve: process "/bin/sh -c apt-get update && apt-get install -y     python3.11     python3.11-dev     python3-pip     curl     wget     git     vim     nano     tree     htop     less     grep     sed     awk     ping     telnet     netcat     traceroute     nmap     ps     top     lsof     strace     tcpdump     jq     yq     xmlstarlet     zip     unzip     tar     gzip     make     gcc     g++     git     find     xargs     rsync     nodejs     npm     sqlite3     mysql-client     postgresql-client     && ln -sf /usr/bin/python3.11 /usr/bin/python     && ln -sf /usr/bin/python3.11 /usr/bin/python3     && rm -rf /var/lib/apt/lists/*" did not complete successfully: exit code: 100