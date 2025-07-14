# Changelog

所有对此项目的重要更改都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/),
并且此项目遵循 [语义化版本控制](https://semver.org/lang/zh-CN/)。

## [Unreleased]

### Added
- CI测试支持多Linux发行版：新增对16个主流Linux发行版的测试支持
  - Ubuntu: 20.04 LTS, 22.04 LTS, 24.04 LTS
  - Debian: 11 (Bullseye), 12 (Bookworm)
  - CentOS: 7, Stream 8, Stream 9
  - Rocky Linux: 8, 9
  - Fedora: 38, 39
  - Alpine Linux: 3.18, 3.19
  - openSUSE: Leap 15.5, Tumbleweed
  - openEuler: 22.03 LTS
- CI测试支持Windows系统：新增对Windows平台的全面测试支持
  - Windows Server 2019 (Python 3.8, 3.9)
  - Windows Server 2022 (Python 3.10, 3.11, 3.12)
  - Windows Latest (Python 3.11)
  - 支持CMD和PowerShell环境测试
  - Windows特定路径和编码处理测试
- CI流水线优化：符合GitHub Actions最佳实践
  - 添加pip缓存以提高构建速度
  - 增加定时任务确保依赖兼容性
  - 实现并发控制节省资源
  - 添加最小权限安全配置
  - 升级Codecov到v4版本

### Fixed
- 修复CI测试中的PEP 668"externally-managed-environment"问题
  - Linux发行版测试使用虚拟环境避免系统包管理冲突
  - 为不同发行版添加PEP 668兼容性标识
  - 增强Windows测试覆盖CMD和PowerShell环境
  - 添加包导入和基本功能验证测试
  - 改进错误处理和降级策略

### Changed

### Deprecated

### Removed

### Fixed

### Security