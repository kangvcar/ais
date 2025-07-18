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
apt install -y python3.9 python3.9-venv python3.9-dev
python3.9 -m pip install ais-terminal
ais setup
source ~/.bashrc

# Ubuntu 22.04 (系统自带python3.10)
pip install ais-terminal
ais setup
source ~/.bashrc

# Ubuntu 24.04 (系统自带python3.12，要求externally-managed-environment）
apt update
apt install -y pipx
pipx install ais-terminal
pipx ensurepath
source ~/.bashrc
ais setup
source ~/.bashrc

# CentOS 7.x (系统自带Python 3.6)
安装 Python 3.10.9
yum install -y epel-release
yum install -y gcc make patch zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel  tk-devel libffi-devel xz-devel openssl11 openssl11-devel openssl11-libs ncurses-devel tk-devel gdbm-devel db4-devel libpcap-devel expat-devel
wget https://repo.huaweicloud.com/artifactory/python-local/3.10.9/Python-3.10.9.tgz
tar zxf Python-3.10.9.tgz && cd Python-3.10.9
sed -i 's/PKG_CONFIG openssl /PKG_CONFIG openssl11 /g' configure
./configure
make && make altinstall
python3.10 -m pip install ais-terminal
ais setup
source ~/.bashrc

# CentOS Stream 8 (系统自带python3.6)
dnf install python39 python39-pip
python3.9 -m pip install ais-terminal
ais setup
source ~/.bashrc

# CentOS Stream 9 (系统自带python3.9)
python3 -m pip install ais-terminal
ais setup
source ~/.bashrc

# Fedora 33-41（系统自带Python3.9+） 
python3 -m pip install ais-terminal
ais setup
source ~/.bashrc

# Debian 11.x（系统自带Python 3.9+）
python3 -m pip install ais-terminal
ais setup
source ~/.bashrc

# Debian 12.x（系统自带Python 3.11+，要求externally-managed-environment）
apt update
apt install -y pipx
pipx install ais-terminal
pipx ensurepath
source ~/.bashrc
ais setup
source ~/.bashrc

# openEuler 22.x （系统自带Python 3.9+）
python3 -m pip install ais-terminal
ais setup
source ~/.bashrc

# openEuler 24.x （系统自带Python 3.11+）
python3 -m pip install ais-terminal
ais setup
source ~/.bashrc

# Kylin Linux Advanced Server V10（系统自带Python 3.7）
安装 Python 3.10.9
yum install -y gcc make patch zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel libffi-devel
wget https://repo.huaweicloud.com/artifactory/python-local/3.10.9/Python-3.10.9.tgz
tar zxf Python-3.10.9.tgz && cd Python-3.10.9
./configure --enable-optimizations
make && make altinstall
python3.10 -m pip install ais-terminal
ais setup
source ~/.bashrc