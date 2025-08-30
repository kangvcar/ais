**语言 / Language:** [中文](./README-zh.md) | [English](./README.md)


# AIS – Context-Aware Error-Analysis Learning Assistant

<div align="center">

![ais](https://socialify.git.ci/kangvcar/ais/image?custom_description=AI%E9%A9%B1%E5%8A%A8%E7%9A%84%E6%99%BA%E8%83%BD%E7%BB%88%E7%AB%AF%E5%8A%A9%E6%89%8B%EF%BC%8C%E8%87%AA%E5%8A%A8%E5%88%86%E6%9E%90%E5%91%BD%E4%BB%A4%E9%94%99%E8%AF%AF%E3%80%81%E6%8F%90%E4%BE%9B%E6%99%BA%E8%83%BD%E8%A7%A3%E5%86%B3%E6%96%B9%E6%A1%88%E3%80%82%0A%E8%AE%A9%E6%AF%8F%E6%AC%A1%E6%8A%A5%E9%94%99%E9%83%BD%E6%98%AF%E6%88%90%E9%95%BF%EF%BC%8C%E8%AE%A9%E6%AF%8F%E4%B8%AA%E9%94%99%E8%AF%AF%E9%83%BD%E6%98%AF%E5%AD%A6%E4%B9%A0\&custom_language=Shell\&description=1\&font=Bitter\&forks=1\&issues=1\&language=1\&logo=https%3A%2F%2Fraw.githubusercontent.com%2Fkangvcar%2Fais%2Frefs%2Fheads%2Fmain%2Fdocs%2Fpublic%2Flogo-robot.svg\&name=1\&owner=1\&pattern=Plus\&stargazers=1\&theme=Auto)

[📖 Installation Guide](#installation) · [🌏 Official Docs](https://kangvcar.github.io/ais) · [🎞️ Feature Demo (Mainland China)](https://www.bilibili.com/video/BV1wDvwzDEEz) · [✨ Interactive Demo](https://app.arcade.software/share/hZWhYIC7dsD7Ed1GPv0G)

<a href="https://www.producthunt.com/products/ais?embed=true&utm_source=badge-featured&utm_medium=badge&utm_source=badge-ais" target="_blank"><img src="https://api.producthunt.com/widgets/embed-image/v1/featured.svg?post_id=1009557&theme=light&t=1756203101298" alt="AIS - Smart terminal AI assistant for instant error analysis | Product Hunt" style="width: 250px; height: 54px;" width="250" height="54" /></a>

[![AIS Demo](https://github.com/user-attachments/assets/f3b4fdd2-c76c-4e48-818d-1e0e4236820d)](https://www.youtube.com/watch?v=T8Q-y2BdFlw "This AI Terminal Assistant Just Changed How I Debug Code Forever | AIS Demo")

</div>

## Overview

Through a deep shell-integration architecture, AIS achieves multi-dimensional context awareness and intelligent error analysis. It automatically collects execution-environment information and pinpoints issues precisely; inside the terminal it provides context-based solutions and structured learning guidance. This eliminates the usual search hopping and blind trial-and-error in traditional error handling, significantly improving both problem-solving efficiency and the speed of skill accumulation.

### 🌟 Core Features

#### 🔍 Intelligent Error Analysis

* **Automatic detection** – Automatically analyzes the cause when a command fails
* **Context awareness** – Combines current directory, Git status, project type, and other environment info
* **Personalized suggestions** – Offers targeted solutions based on the user’s skill level
* **Safety levels** – Every suggestion is labeled with a risk level to keep operations safe

#### 📚 Intelligent Learning System

* **Interactive teaching** – Explains the “why,” not just the “how”
* **Topic learning** – Dive into focused topics like Git, Docker, and Vim
* **Progressive content** – Adjusts depth according to user level
* **Practice-oriented** – Provides runnable command examples and best practices

#### 🎯 Intelligent Context Awareness

* **Environment-aware Q\&A** – `ais ask` delivers precise answers based on the current system environment
* **Three-level context collection** – Configurable information-collection levels: minimal/standard/detailed
* **System status analysis** – Automatically detects hardware configuration, network status, and running services
* **Project-type recognition** – Intelligently identifies tech stacks using Git status and project files

#### 🔌 Strong Integrations

* **Shell integration** – Automatic error capture for Bash and Zsh
* **Multi-AI support** – Compatible with OpenAI, Ollama, Claude, and more
* **Privacy protection** – Local data storage; sensitive information is automatically filtered
* **Cross-platform** – Supports Linux and macOS

---

## <a id="installation"></a>📦 Installation

### System Requirements

* **Python**: 3.9+ (3.11+ recommended)
* **Operating Systems**: Linux, macOS
* **Network**: Required to download dependencies and access AI services
* **Disk Space**: At least 100 MB free space

### ⚡ One-Click Install (Recommended)

```bash
# Smart install – automatically detects the environment and chooses the best method
curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.sh | bash

# Mainland China users can use the Gitee mirror (faster and more stable)
curl -sSL https://gitee.com/kangvcar/ais/raw/main/scripts/install.sh | bash
```

**The install script will automatically:**

* 🔍 Detect the current environment (personal/team/container)
* 🎯 Choose the best installation method (pipx per-user/system-wide/containerized)
* 📦 Install pipx and AIS
* 🔧 Configure shell integration
* ✓ Run a health check

### 🗑️ One-Click Uninstall

```bash
# Smart uninstall – automatically detects how AIS was installed and cleans it completely
curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/uninstall.sh | bash

# Mainland China users can use the Gitee mirror
curl -sSL https://gitee.com/kangvcar/ais/raw/main/scripts/uninstall.sh | bash
```

**The uninstall script will automatically:**

* 🔍 Detect how AIS was installed (pipx per-user/system-wide)
* 🗑️ Uninstall the AIS package and dependencies
* 🧹 Clean shell-integration configuration
* 📁 Let you choose to keep or delete user data
* ✓ Verify that uninstallation is complete

### 🎯 Installation by Scenario

<details>
<summary><b>🐳 Docker Container (Recommended – zero configuration)</b></summary>

```bash
# Run the latest version directly
docker run -it --rm kangvcar/ais:latest

# Or use it interactively
docker run -it --rm -v $(pwd):/workspace kangvcar/ais:latest bash

# Use Docker Compose (recommended for persistent configuration)
curl -O https://raw.githubusercontent.com/kangvcar/ais/main/docker-compose.yml
docker-compose up -d ais
docker-compose exec ais bash
```

**Advantages**: Zero-config startup, environment isolation, cross-platform consistency, ARM64 supported

</details>

<details>
<summary><b>👨‍💻 Individual Developer (Python environment)</b></summary>

```bash
# Per-user install (safest)
curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.sh | bash -s -- --user

# Mainland China users can use the Gitee mirror
curl -sSL https://gitee.com/kangvcar/ais/raw/main/scripts/install.sh | bash -s -- --user

# Or install manually
pipx install ais-terminal
ais setup

# HTML report visualization is now included by default
```

**Advantages**: Maximum safety, isolated virtual environment, no sudo required

</details>

<details>
<summary><b>🏢 Team/Enterprise Environment</b></summary>

```bash
# System-wide installation (available to all users)
curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/install.sh | bash -s -- --system

# Mainland China users can use the Gitee mirror
curl -sSL https://gitee.com/kangvcar/ais/raw/main/scripts/install.sh | bash -s -- --system
```

**Advantages**: Available to all users, maintains safety isolation, centralized management and updates

</details>

<details>
<summary><b>🐳 Container/Cloud Environment</b></summary>

```bash
# Dockerized installation
curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/scripts/docker-install.sh | bash

# Or run directly
docker run -it --rm ais:latest
```

**Advantages**: Environment consistency, rapid deployment, easy scaling, full isolation

</details>

<details>
<summary><b>🔧 Developers/Contributors</b></summary>

```bash
# Install from source
git clone https://github.com/kangvcar/ais.git
cd ais
pipx install -e .

# Or use a virtual environment
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,html]"  # Includes dev and HTML visualization dependencies
```

**Advantages**: Live edits, complete dev toolchain, easy debugging

</details>

### ✓ Verify Installation

```bash
# Check version
ais --version

# Test basic functionality
ais ask "Hello, AIS!"

# Test automatic error analysis (enter a command with an intentional typo)
mkdirr /tmp/test
```

---

## <a id="quickstart"></a>🚀 Quick Start

### Basic Configuration

```bash
# View current configuration
ais config

# Set context-collection level
ais config --set context_level=detailed
```

### Core Feature Walkthrough

#### 💬 Environment-Aware Q\&A

```bash
# Environment-aware Q&A based on the current system
ais ask "What is my system configuration like? How is the hardware performance?"
ais ask "Is my network connection normal? Any security suggestions?"
ais ask "Given my current project type, how can I optimize performance?"

# Traditional technical Q&A (still supported)
ais ask "How do I check system memory usage?"
ais ask "How do Docker containers mount directories?"
ais ask "How do I resolve Git merge conflicts?"

# Configure context-collection level
ais config --set context_level=minimal   # Basic information
ais config --set context_level=standard  # Standard information  
ais config --set context_level=detailed  # Full information
```

#### 📖 Topic Learning

```bash
ais learn git      # Learn Git version control
ais learn docker   # Learn containerization
ais learn vim      # Learn the text editor
ais learn ssh      # Learn remote access
```

#### 🔍 Intelligent Error Analysis

```bash
# These erroneous commands will automatically trigger AI analysis
pytho --version        # Spelling error
ls /not/exist          # Path does not exist
git statuss            # Command error
```

#### 📊 Learning Growth Report

```bash
ais report                                 # Generate a text-format learning report
ais report --html                          # Generate an HTML visualization report
ais report --html -o my_report.html --open # Generate and open the HTML report

# History management
ais history                # View recent command history
ais history --limit 20     # Show 20 command records
ais history 3              # View detailed analysis of record #3
```

---

## 📚 Detailed Features

### Environment-Aware Q\&A – `ais ask`

Intelligent Q\&A based on the current system environment, automatically sensing hardware configuration, network status, project type, and more:

```bash
# 🖥️ System environment-aware Q&A
ais ask "How is my system performance? Do I need to optimize?"
ais ask "Are my currently open ports secure?"
ais ask "What is the status of my network connection?"

# 🚀 Project environment-aware Q&A  
ais ask "What type of project is this? How do I install dependencies?"
ais ask "Given the current Git status, how should I commit?"
ais ask "How do I optimize this Python project in my current environment?"

# 📚 Traditional technical Q&A (still supported)
ais ask "What does Linux file permission 755 mean?"
ais ask "How can I optimize Python script performance?"
ais ask "What are the steps to configure Nginx as a reverse proxy?"

# ⚙️ Context-level configuration
ais config --set context_level=minimal   # Basics: system info, Git, project type
ais config --set context_level=standard  # Standard: + file list, command history
ais config --set context_level=detailed  # Detailed: + network, permissions, services

# 📋 View detailed help
ais ask --help-detail
```

**New highlights**:

* 🧠 **Smart context collection**: Automatically detects CPU, memory, network, and service status
* 🎯 **Environment-aware answers**: Targeted advice based on actual system configuration
* ⚡ **Three configurable tiers**: From lightweight to detailed, fit for different scenarios
* 🔒 **Privacy**: Sensitive info is auto-filtered; protected directories are skipped

### Learning Growth Report – `ais report`

Generate a detailed, personalized learning-growth analysis report in text or visual HTML:

```bash
# 📊 Text report (default)
ais report

# 📈 HTML visualization report (recommended)
ais report --html
ais report --html -o custom_report.html
ais report --html --open  # Automatically open in the browser after generation

# 📋 View detailed help
ais report --help
```

#### 🌟 HTML Visualization Features

**6 professional chart types**:

* 📈 **Error trend chart**: 30-day error trend to show progress
* 🎯 **Skill assessment radar**: Visualize multi-dimensional skill levels
* ⏰ **Time heatmap**: Distribution over time to find learning patterns
* 📊 **Command frequency**: Rank most error-prone commands for focus
* 🔍 **Error-type distribution**: Pie chart of error patterns for targeted fixes
* 📈 **Learning-progress trend**: Dual-axis view of error reduction and skill growth

**Modern UX**:

* 🎨 **Responsive design**: Great on desktop, tablet, and mobile
* 🖱️ **Interactive charts**: Hover tooltips, zooming, and drill-down
* 💡 **AI insights**: Personalized analysis and improvement tips
* 🌐 **Browser-friendly**: Works in modern browsers; no plugins needed

**Flexible options**:

```bash
# Custom output filename
ais report --html -o "2024-Learning-Report.html"

# Open in a browser after generation
ais report --html --open

# Combine options
ais report --html -o weekly_progress.html --open
```

**Data security**:

* 📊 All data generated locally; nothing uploaded to the cloud
* 🔒 Sensitive information is auto-filtered
* 📁 Supports offline viewing and sharing

### Knowledge Learning – `ais learn`

Systematic learning for command-line tools and concepts:

```bash
ais learn              # List all available topics
ais learn git          # Complete Git tutorial
ais learn docker       # In-depth containerization
ais learn linux        # Linux system-administration basics
```

### Managing AI Providers

Supports multiple AI providers with easy switching:

```bash
# List available providers
ais provider-list

# Add a local Ollama provider
ais provider-add ollama \
  --url http://localhost:11434/v1/chat/completions \
  --model llama3

# Switch provider
ais provider-use ollama
```

### Shell-Integration Configuration

AIS supports automatic error analysis; shell integration is required:

```bash
# Automatic configuration
ais setup

# Test whether the integration works
ais test-integration
```

---

## ⚙️ Advanced Configuration

### Smart Context-Collection Settings

Independently control context collection for error analysis and for `ask` Q\&A:

```bash
# Context level for error analysis (automatic analysis feature)
ais config --set context_level=minimal    # Basic information
ais config --set context_level=standard   # Standard information (default)
ais config --set context_level=detailed   # Detailed information

# Context level for ask Q&A (new)
ais config --set ask.context_level=minimal   # System basics
ais config --set ask.context_level=standard  # + project and Git information
ais config --set ask.context_level=detailed  # + network, permissions, services

# Control automatic analysis
ais config --set auto_analysis=true       # Enable automatic analysis
ais config --set auto_analysis=false      # Disable automatic analysis

# View current configuration
ais config
```

**Context-collection details**:

| Level        | Included in error analysis                           | Included in ask Q\&A                                                             |
| ------------ | ---------------------------------------------------- | -------------------------------------------------------------------------------- |
| **minimal**  | Command, exit code, directory, user                  | System info, CPU/memory, network reachability, listening ports, running services |
| **standard** | + File list, Git status, command history             | + Project type, Git details, file list                                           |
| **detailed** | + System info, environment variables, full directory | + Permission info, detailed network status, full environment                     |

### Privacy and Security

AIS takes privacy and data security seriously:

* **Local storage** – All data stored in a local SQLite database
* **Sensitive-info filtering** – Passwords, keys, and similar are filtered automatically
* **Configurable context levels** – You control the scope of information collection
* **Open source and transparent** – Fully open source; code is publicly available

---

## 🆕 Latest Feature Highlights

### 📊 HTML Visualization Report System (v2.5.2)

AIS now supports professional HTML visualization reports, turning dry data into clear, attractive charts:

#### 🎨 **Modern visualization design**

```bash
$ ais report --html --open

# Automatically generates an HTML report containing:
📈 Error trend analysis – a clear 30-day learning-progress trajectory
🎯 Skill assessment radar – multi-dimensional skill levels at a glance  
⏰ Time-distribution heatmap – discover your best learning hours
📊 Command frequency statistics – identify where to focus
🔍 Error-type analysis – tackle common problems precisely
📈 Learning-progress trend – quantify skill growth
```

#### 💻 **Interactive user experience**

* **Responsive design**: Perfect on desktop, tablet, and phone
* **Interactive charts**: Hover details, zoom, explore data
* **AI insights**: Personalized meaning behind each chart
* **One-click sharing**: Generates a static HTML you can share easily

#### 🔧 **Flexible configuration options**

```bash
# Quick generate and view
ais report --html --open

# Custom filename
ais report --html -o "My-Skills-Growth-Report.html"

# Use cases
ais report --html -o weekly_report.html    # Weekly report
ais report --html -o monthly_review.html   # Monthly review
ais report --html -o skill_assessment.html # Skill assessment
```

### 🧠 Intelligent Context-Awareness System (v2.4.0)

AIS can now sense your system environment and provide precise, real-world advice:

#### 📊 **System-status awareness**

```bash
$ ais ask "How is my system configured?"

# AI will analyze and answer:
✓ OS: Ubuntu 24.04.2 LTS
✓ CPU: 4-core Intel Xeon Platinum  
✓ Memory: 7.1 G total, 3.5 G used, 3.6 G available
✓ Disk: 40 G total, 4.1 G used (11%)
✓ Network: Reachable (ping 8.8.8.8)
```

#### 🔐 **Security-status analysis**

```bash
$ ais ask "Which ports are open on my system? Are they secure?"

# AI will assess port security and provide suggestions:
✓ SSH (22): Secure; recommend key-based authentication
✓ DNS (53): Beware DNS amplification risk
✓ Other ports: Concrete hardening suggestions provided
```

#### 🚀 **Project optimization suggestions**

```bash
$ ais ask "Given my environment, how do I optimize this Python project?"

# AI will combine system configuration with project type to propose optimizations:
✓ Use 4 CPU cores for parallelism (multiprocessing)
✓ Tune data-processing strategy based on memory
✓ Adjust remote API calls according to network status
```

#### ⚙️ **Flexible levels**

* **Minimal**: System basics + network status + running services
* **Standard**: + Project type + Git status + file list
* **Detailed**: + Permission info + detailed network + full environment

---

## 🏗️ Project Structure

```
ais/
├── src/ais/              # Main source code
│   ├── cli/              # CLI modules
│   │   ├── main.py       # CLI entry point
│   │   └── interactive.py # Interactive menu
│   ├── core/             # Core modules
│   │   ├── ai.py         # AI interaction
│   │   ├── config.py     # Configuration management
│   │   ├── context.py    # Context collection
│   │   └── database.py   # Database operations
│   ├── ui/               # User interface
│   │   └── panels.py     # Display panels
│   └── utils/            # Utilities
├── scripts/              # Install and deployment scripts
├── tests/                # Tests
├── docs/                 # Documentation
└── pyproject.toml        # Project configuration
```

### Core Modules

* **CLI module** (`src/ais/cli/`): Command-line interface and interactive UI
* **Core module** (`src/ais/core/`): AI integration, configuration, context collection, database operations
* **UI module** (`src/ais/ui/`): Rich-based display panels and formatting

---

---

## 🧪 Development and Testing

### Development Environment Setup

```bash
# Clone the repository
git clone https://github.com/kangvcar/ais.git
cd ais

# Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dev build and dependencies
pip install -e ".[dev]"

# Set up pre-commit
pre-commit install
```

### Run Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Coverage
python -m pytest --cov=ais tests/

# Code quality checks
source .venv/bin/activate && black src/ tests/
source .venv/bin/activate && flake8 src/ tests/ --max-line-length=100
```

---

## <a id="contributing"></a>🤝 Contributing

We welcome all forms of contribution!

### How to Get Involved

1. **Fork** this repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a **Pull Request**

### Development Guidelines

* Follow the [PEP 8](https://pep8.org/) style guide
* Add tests for new features
* Update relevant documentation
* Write clear commit messages

### Code Quality

Ensure your code meets project standards:

```bash
# Auto-format code
source .venv/bin/activate && autopep8 --in-place --aggressive --aggressive --max-line-length=100 src/ tests/ -r

# Run all quality checks
python -m pytest tests/ -v
source .venv/bin/activate && black src/ tests/
source .venv/bin/activate && flake8 src/ tests/ --max-line-length=100
```

---

## 🆘 Getting Help

### Self-Serve Resources

```bash
# Test system integration
ais test-integration

# Show version
ais --version

# Show all help
ais help-all
```

### Community Support

* 📚 [Full Documentation](docs/)
* 💬 [GitHub Discussions](https://github.com/kangvcar/ais/discussions) – Q\&A and conversations
* 🐛 [GitHub Issues](https://github.com/kangvcar/ais/issues) – Bug reports
* 📧 [Email Support](mailto:ais@example.com) – Contact directly

### Reporting Issues

When reporting an issue, please provide:

* Your operating system and version
* Python version (`python3 --version`)
* AIS version (`ais --version`)
* Installation method (pipx/Docker/source)
* Full error message
* Reproduction steps

---

## 📝 License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

---

## 🎉 Acknowledgments

Thanks to all the developers who contributed to this project!

### Tech Stack

* **Python 3.9+** – Core language
* **Click** – CLI framework
* **Rich** – Terminal UI and formatting
* **SQLModel** – Database ORM
* **httpx** – HTTP client
* **Plotly** – Interactive charting (HTML reports)
* **NumPy** – Numerical computing support (for visualization)
* **pytest** – Testing framework

---

<div align="center">

**🎉 Let AI be your terminal companion and make command-line learning simple and fun!**

If you find AIS helpful, please give us a ⭐️!

[![Stars](https://img.shields.io/github/stars/kangvcar/ais?style=social)](https://github.com/kangvcar/ais/stargazers)
[![Forks](https://img.shields.io/github/forks/kangvcar/ais?style=social)](https://github.com/kangvcar/ais/network/members)

[Back to top](#ais-%E2%80%93-context%E2%80%91aware-error%E2%80%91analysis-learning-assistant)

</div>

---