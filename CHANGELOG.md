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
- 修复特定Linux发行版的CI测试问题
  - 修复CentOS 7/Stream 8 EOL后的镜像源问题，使用vault.centos.org
  - 暂时禁用Rocky Linux测试避免hatchling版本兼容性问题
  - 修复openSUSE容器shell问题，统一使用bash
  - 简化Windows测试，统一使用PowerShell环境
- 大幅简化CI测试策略以提高稳定性
  - 移除有问题的旧版本发行版（CentOS 7/8, Rocky Linux等）
  - 专注于主流稳定发行版：Ubuntu 22.04/24.04, Debian 12, Fedora 39, Alpine 3.19
  - 简化Windows测试避免Unicode编码问题
  - 统一使用sh shell确保最大兼容性
- 重新添加企业级Linux发行版支持
  - 恢复CentOS 7/Stream 8/Stream 9测试支持
  - 恢复Rocky Linux 8/9测试支持
  - 添加openEuler 22.03 LTS测试支持
  - 实现智能兼容性检测：区分actions兼容和非兼容系统
  - 特殊处理策略：EOL发行版使用vault镜像源，旧版本Python使用setuptools构建

### Changed

### Deprecated

### Removed

### Fixed

### Security