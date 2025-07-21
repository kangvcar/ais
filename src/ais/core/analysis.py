"""错误分析和学习建议模块。"""

from collections import Counter, defaultdict
from datetime import datetime, timedelta
from typing import Dict, List, Any

from .database import get_recent_logs, CommandLog


class ErrorAnalyzer:
    """错误分析器，用于分析用户的错误历史。"""

    def __init__(self, days_back: int = 30):
        """初始化错误分析器。

        Args:
            days_back: 分析最近多少天的数据
        """
        self.days_back = days_back
        self.cutoff_date = datetime.now() - timedelta(days=days_back)

    def get_error_logs(self) -> List[CommandLog]:
        """获取错误日志（非零退出码）。"""
        all_logs = get_recent_logs(limit=1000)  # 获取大量日志

        # 过滤错误日志和时间范围
        error_logs = []
        for log in all_logs:
            if log.exit_code != 0 and log.timestamp >= self.cutoff_date:
                error_logs.append(log)

        return error_logs

    def analyze_error_patterns(self) -> Dict[str, Any]:
        """分析错误模式。"""
        error_logs = self.get_error_logs()

        if not error_logs:
            return {
                "total_errors": 0,
                "common_commands": [],
                "error_types": [],
                "time_distribution": {},
                "improvement_trend": [],
                "analysis_period": f"{self.days_back}天",
            }

        # 统计常见错误命令
        command_counter = Counter()
        error_type_counter = Counter()
        daily_errors = defaultdict(int)

        for log in error_logs:
            # 提取命令的主要部分
            cmd_parts = log.original_command.split()
            if cmd_parts:
                main_command = cmd_parts[0]
                command_counter[main_command] += 1

            # 分析错误类型
            error_type = self._classify_error(log)
            error_type_counter[error_type] += 1

            # 按天统计
            day_key = log.timestamp.strftime("%Y-%m-%d")
            daily_errors[day_key] += 1

        # 分析改进趋势
        improvement_trend = self._analyze_improvement_trend(error_logs)

        return {
            "total_errors": len(error_logs),
            "common_commands": command_counter.most_common(10),
            "error_types": error_type_counter.most_common(10),
            "time_distribution": dict(daily_errors),
            "improvement_trend": improvement_trend,
            "analysis_period": f"{self.days_back}天",
        }

    def _classify_error(self, log: CommandLog) -> str:
        """分类错误类型。"""
        command = log.original_command.lower()
        stderr = (log.stderr_output or "").lower()

        # 命令不存在
        if "command not found" in stderr or "not found" in stderr:
            return "命令不存在"

        # 权限问题
        if "permission denied" in stderr or "access denied" in stderr:
            return "权限不足"

        # 文件/目录不存在
        if "no such file or directory" in stderr:
            return "文件/目录不存在"

        # 语法错误
        if "syntax error" in stderr or "invalid option" in stderr:
            return "语法错误"

        # Git相关错误
        if command.startswith("git"):
            return "Git操作错误"

        # Docker相关错误
        if command.startswith("docker"):
            return "Docker操作错误"

        # 网络相关错误
        if any(net_cmd in command for net_cmd in ["curl", "wget", "ping"]):
            return "网络操作错误"

        # 包管理错误
        if any(pkg_cmd in command for pkg_cmd in ["pip", "npm", "apt", "yum"]):
            return "包管理错误"

        return "其他错误"

    def _analyze_improvement_trend(self, error_logs: List[CommandLog]) -> List[Dict[str, Any]]:
        """分析改进趋势。"""
        if len(error_logs) < 7:  # 数据不足
            return []

        # 按周分组
        weekly_errors = defaultdict(list)
        for log in error_logs:
            week_key = log.timestamp.strftime("%Y-W%U")
            weekly_errors[week_key].append(log)

        # 计算每周的错误数量和重复错误
        trend_data = []
        for week, logs in sorted(weekly_errors.items()):
            command_types = [
                (log.original_command.split()[0] if log.original_command.split() else "")
                for log in logs
            ]
            repeated_commands = len(command_types) - len(set(command_types))

            trend_data.append(
                {
                    "week": week,
                    "total_errors": len(logs),
                    "repeated_errors": repeated_commands,
                    "unique_commands": len(set(command_types)),
                }
            )

        return trend_data[-4:]  # 返回最近4周的数据

    def generate_skill_assessment(self) -> Dict[str, Any]:
        """生成技能评估。"""
        error_logs = self.get_error_logs()

        if not error_logs:
            return {
                "skill_level": "初学者",
                "strengths": [],
                "weaknesses": [],
                "knowledge_gaps": [],
            }

        # 分析技能领域
        skill_areas = {
            "基础命令": ["ls", "cd", "pwd", "cat", "mkdir", "rm", "cp", "mv"],
            "文件操作": ["find", "grep", "sed", "awk", "sort", "uniq"],
            "系统管理": ["ps", "top", "kill", "chmod", "chown", "sudo"],
            "网络工具": ["curl", "wget", "ping", "ssh", "scp"],
            "Git版本控制": ["git"],
            "Docker容器": ["docker"],
            "包管理": ["pip", "npm", "apt", "yum", "brew"],
        }

        # 统计每个技能领域的错误
        skill_errors = defaultdict(int)
        total_commands = defaultdict(int)

        for log in error_logs:
            cmd_parts = log.original_command.split()
            if cmd_parts:
                main_cmd = cmd_parts[0]

                for skill_area, commands in skill_areas.items():
                    if main_cmd in commands or any(cmd in main_cmd for cmd in commands):
                        skill_errors[skill_area] += 1
                        total_commands[skill_area] += 1

        # 计算技能水平
        strengths = []
        weaknesses = []
        knowledge_gaps = []

        for skill_area, error_count in skill_errors.items():
            if error_count == 0:
                strengths.append(skill_area)
            elif error_count >= 3:
                weaknesses.append(skill_area)
            elif error_count >= 1:
                knowledge_gaps.append(skill_area)

        # 评估整体技能水平
        total_errors = len(error_logs)
        unique_commands = len(
            set(
                (log.original_command.split()[0] if log.original_command.split() else "")
                for log in error_logs
            )
        )

        if total_errors < 5:
            skill_level = "熟练者"
        elif total_errors < 15:
            skill_level = "中级用户"
        elif unique_commands > 10:
            skill_level = "探索者"
        else:
            skill_level = "初学者"

        return {
            "skill_level": skill_level,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "knowledge_gaps": knowledge_gaps,
            "total_errors": total_errors,
            "unique_commands": unique_commands,
        }

    def generate_learning_recommendations(self) -> List[Dict[str, Any]]:
        """生成学习建议。"""
        error_patterns = self.analyze_error_patterns()
        skill_assessment = self.generate_skill_assessment()

        recommendations = []

        # 基于常见错误的建议
        common_commands = error_patterns["common_commands"][:5]
        for cmd, count in common_commands:
            recommendations.append(
                {
                    "type": "命令掌握",
                    "title": f"深入学习 {cmd} 命令",
                    "description": f"你在 {cmd} 命令上出现了 {count} 次错误，"
                    f"建议系统学习这个命令的用法。",
                    "priority": "高" if count >= 3 else "中",
                    "learning_path": self._get_learning_path(cmd),
                }
            )

        # 基于错误类型的建议
        error_types = error_patterns["error_types"][:3]
        for error_type, count in error_types:
            recommendations.append(
                {
                    "type": "错误预防",
                    "title": f"减少{error_type}",
                    "description": f"你遇到了 {count} 次{error_type}，建议学习相关的预防技巧。",
                    "priority": "高" if count >= 5 else "中",
                    "learning_path": self._get_error_prevention_tips(error_type),
                }
            )

        # 基于技能弱点的建议
        weaknesses = skill_assessment["weaknesses"][:3]
        for weakness in weaknesses:
            recommendations.append(
                {
                    "type": "技能提升",
                    "title": f"加强{weakness}技能",
                    "description": f"在{weakness}方面出现较多错误，建议重点学习。",
                    "priority": "高",
                    "learning_path": self._get_skill_learning_path(weakness),
                }
            )

        # 基于知识盲点的建议
        knowledge_gaps = skill_assessment["knowledge_gaps"][:2]
        for gap in knowledge_gaps:
            recommendations.append(
                {
                    "type": "知识补充",
                    "title": f"了解{gap}基础",
                    "description": f"建议补充{gap}的基础知识，避免常见错误。",
                    "priority": "中",
                    "learning_path": self._get_skill_learning_path(gap),
                }
            )

        # 按优先级排序
        priority_order = {"高": 0, "中": 1, "低": 2}
        recommendations.sort(key=lambda x: priority_order.get(x["priority"], 2))

        return recommendations[:8]  # 返回最多8个建议

    def _get_learning_path(self, command: str) -> List[str]:
        """获取命令的学习路径。"""
        learning_paths = {
            "git": [
                "学习Git基础概念（工作区、暂存区、仓库）",
                "掌握常用Git命令（add, commit, push, pull）",
                "了解分支操作（branch, checkout, merge）",
                "学习解决合并冲突的方法",
            ],
            "docker": [
                "了解Docker基本概念（镜像、容器）",
                "学习Docker基础命令（run, build, ps, stop）",
                "掌握Dockerfile编写",
                "了解Docker网络和存储",
            ],
            "ssh": [
                "学习SSH基础概念和用法",
                "掌握SSH密钥配置",
                "了解SSH隧道和端口转发",
                "学习SSH安全最佳实践",
            ],
            "vim": [
                "学习Vim基本模式（普通、插入、命令）",
                "掌握基本移动和编辑操作",
                "了解Vim配置文件",
                "学习高级编辑技巧",
            ],
        }

        return learning_paths.get(
            command,
            [
                f"查看 {command} 的帮助文档（{command} --help）",
                f"学习 {command} 的常用参数和选项",
                f"练习 {command} 的实际应用场景",
                f"了解 {command} 的最佳实践",
            ],
        )

    def _get_error_prevention_tips(self, error_type: str) -> List[str]:
        """获取错误预防技巧。"""
        prevention_tips = {
            "命令不存在": [
                "使用 which 命令检查程序是否已安装",
                "学习使用包管理器安装缺失的程序",
                "配置正确的PATH环境变量",
                "使用Tab键自动补全命令",
            ],
            "权限不足": [
                "了解Linux文件权限系统",
                "学习正确使用sudo命令",
                "掌握chmod和chown命令",
                "理解用户和组的概念",
            ],
            "文件/目录不存在": [
                "使用ls命令确认文件/目录存在",
                "学习使用相对路径和绝对路径",
                "使用Tab键自动补全路径",
                "掌握find命令查找文件",
            ],
            "语法错误": [
                "仔细阅读命令的帮助文档",
                "学习命令的正确语法格式",
                "使用命令的示例进行练习",
                "学习常用的命令选项组合",
            ],
        }

        return prevention_tips.get(
            error_type,
            [
                "仔细阅读错误信息",
                "查看相关文档和教程",
                "在测试环境中练习",
                "向社区寻求帮助",
            ],
        )

    def _get_skill_learning_path(self, skill_area: str) -> List[str]:
        """获取技能领域的学习路径。"""
        skill_paths = {
            "基础命令": [
                "学习文件和目录操作命令",
                "掌握文件查看和编辑命令",
                "了解文件权限和所有权",
                "练习命令行导航技巧",
            ],
            "文件操作": [
                "学习文本处理命令（grep, sed, awk）",
                "掌握文件查找和过滤技巧",
                "了解正则表达式基础",
                "练习复杂的文件操作组合",
            ],
            "系统管理": [
                "学习进程管理命令",
                "掌握系统监控工具",
                "了解用户和权限管理",
                "学习系统服务管理",
            ],
            "网络工具": [
                "学习网络诊断命令",
                "掌握远程连接工具",
                "了解网络配置基础",
                "练习网络故障排查",
            ],
            "Git版本控制": [
                "学习Git基础概念",
                "掌握版本控制工作流",
                "了解分支管理策略",
                "练习团队协作技巧",
            ],
            "Docker容器": [
                "学习容器化基础概念",
                "掌握Docker常用命令",
                "了解容器编排基础",
                "练习容器化应用部署",
            ],
        }

        return skill_paths.get(
            skill_area,
            [
                f"学习{skill_area}的基础知识",
                f"掌握{skill_area}的常用工具",
                f"了解{skill_area}的最佳实践",
                f"练习{skill_area}的实际应用",
            ],
        )
