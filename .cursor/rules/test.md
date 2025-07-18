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
安装 Python 3.11.13
yum groupinstall -y "Development Tools"
yum install epel-release
yum install -y gcc make patch zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel  tk-devel libffi-devel xz-devel openssl11 openssl11-devel openssl11-libs ncurses-devel tk-devel gdbm-devel db4-devel libpcap-devel expat-devel
wget https://repo.huaweicloud.com/artifactory/python-local/3.10.9/Python-3.10.9.tgz
tar zxf Python-3.10.9.tgz && cd Python-3.10.9
export PKG_CONFIG_PATH="/usr/lib64/pkgconfig:$PKG_CONFIG_PATH"
export LDFLAGS="-L/usr/lib64"
export CPPFLAGS="-I/usr/include"
./configure --prefix=/usr/local/python3.12 --with-openssl=/usr --with-openssl-rpath=auto
make -j$(nproc) && make install
ln -s /usr/local/python3.10/bin/python3.10 /usr/local/bin/python3.10
ln -s /usr/local/python3.10/bin/pip3.10 /usr/local/bin/pip3.10
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
安装Python 3.11.13
yum install -y gcc make patch zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel openssl-devel tk-devel libffi-devel git
mkdir $HOME/.pyenv
git clone https://gitee.com/mirrors/pyenv.git ~/.pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
source ~/.bashrc
mkdir -p ~/.pyenv/cache
wget https://repo.huaweicloud.com/python/3.11.13/Python-3.11.13.tar.xz -O ~/.pyenv/cache/Python-3.11.13.tar.xz
pyenv install 3.11.13
mkdir -p ~/ais_project
cd ~/ais_project
pyenv local 3.11.13
$HOME/.pyenv/versions/3.11.13/bin/pip install ais-terminal
sudo ln -sf $HOME/.pyenv/versions/3.11.13/bin/ais /usr/local/bin/ais
ais setup
source ~/.bashrc