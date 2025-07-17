# Todo
由于国内部分用户网络无法访问GitHub，导致无法使用一键安装脚本，请在文档中一键脚本的地方提供多一个国内的脚本地址：`curl -sSL https://gitee.com/kangvcar/ais/raw/main/scripts/install.sh | bash`

在centos 7.9 中使用一键安装脚本提示pipx安装失败

程序只能捕获错误码，无法捕获错误输出。

# 系统适配测试
# Rocky Linux 8.x (系统自带python3.6)
dnf install -y python39
python3.9 -m pip install pipx
pipx ensurepath
pipx install ais-terminal
source ~/.bashrc
ais setup
source ~/.bashrc

# Rocky Linux 9.x (系统自带python3.9)
pip install pipx
pipx install ais-terminal
source ~/.bashrc
ais setup
source ~/.bashrc

# Ubuntu 20.04 (系统自带python3.8)
apt install -y software-properties-common
add-apt-repository ppa:deadsnakes/ppa
apt install -y python3.9 python3.9-venv python3.9-dev python3.9-pipx
python3.9 -m pip install ais-terminal
ais setup
source ~/.bashrc

# Ubuntu 22.04 (系统自带python3.10)
pip install ais-terminal
ais setup
source ~/.bashrc

# Ubuntu 24.04 (系统自带python3.12)
apt update
apt install -y pipx
pipx install ais-terminal
pipx ensurepath
source ~/.bashrc
ais setup
source ~/.bashrc

# CentOS 8


# CentOS Stream 8 (系统自带python3.6)
dnf install python39 python39-pip
python3.9 -m pip install ais-terminal
ais setup
source ~/.bashrc

# CentOS Stream 9 (系统自带python3.9)
python3 -m pip install ais-terminal
ais setup
source ~/.bashrc

# Fedora 33-41（系统自带python3.9+） 
python3 -m pip install ais-terminal
ais setup
source ~/.bashrc



