"""学习报告生成器。"""

from datetime import datetime
from typing import Dict, Any, List

from .analysis import ErrorAnalyzer


class LearningReportGenerator:
    """学习报告生成器。"""

    def __init__(self, days_back: int = 30):
        """初始化报告生成器。

        Args:
            days_back: 分析最近多少天的数据
        """
        self.analyzer = ErrorAnalyzer(days_back)
        self.days_back = days_back

    def generate_report(self) -> Dict[str, Any]:
        """生成完整的学习报告。"""
        # 获取分析数据
        error_patterns = self.analyzer.analyze_error_patterns()
        skill_assessment = self.analyzer.generate_skill_assessment()
        learning_recommendations = self.analyzer.generate_learning_recommendations()

        # 构建报告
        report = {
            "report_info": {
                "generated_at": datetime.now().isoformat(),
                "analysis_period": f"最近{self.days_back}天",
                "report_type": "学习成长报告",
            },
            "error_summary": {
                "total_errors": error_patterns["total_errors"],
                "analysis_period": error_patterns["analysis_period"],
                "most_common_commands": error_patterns["common_commands"][:5],
                "most_common_error_types": error_patterns["error_types"][:5],
            },
            "skill_assessment": skill_assessment,
            "learning_recommendations": learning_recommendations,
            "improvement_insights": self._generate_improvement_insights(error_patterns),
            "next_steps": self._generate_next_steps(learning_recommendations),
        }

        # 生成AI洞察总结
        try:
            ai_insights = self._generate_ai_insights(report)
            report["ai_insights"] = ai_insights
        except Exception:
            # 如果AI洞察生成失败，使用默认总结
            report["ai_insights"] = self._generate_fallback_insights(report)

        return report

    def _generate_improvement_insights(
        self, error_patterns: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """生成改进洞察。"""
        insights = []

        total_errors = error_patterns["total_errors"]
        common_commands = error_patterns["common_commands"]
        error_types = error_patterns["error_types"]
        improvement_trend = error_patterns["improvement_trend"]

        # 错误频率洞察
        if total_errors > 20:
            insights.append(
                {
                    "type": "频率警告",
                    "title": "错误频率较高",
                    "description": (
                        f"在过去{self.days_back}天里发生了{total_errors}次错误，"
                        "建议重点关注常见错误的预防。"
                    ),
                    "severity": "高",
                }
            )
        elif total_errors > 10:
            insights.append(
                {
                    "type": "频率提醒",
                    "title": "错误频率适中",
                    "description": (
                        f"在过去{self.days_back}天里发生了{total_errors}次错误，"
                        "整体表现良好，可以进一步优化。"
                    ),
                    "severity": "中",
                }
            )
        elif total_errors > 0:
            insights.append(
                {
                    "type": "频率良好",
                    "title": "错误频率较低",
                    "description": (
                        f"在过去{self.days_back}天里仅发生了{total_errors}次错误，" "表现优秀！"
                    ),
                    "severity": "低",
                }
            )

        # 命令集中度洞察
        if common_commands:
            top_command, top_count = common_commands[0]
            if top_count >= 5:
                insights.append(
                    {
                        "type": "命令集中",
                        "title": f"{top_command} 命令需要重点关注",
                        "description": (
                            f"你在 {top_command} 命令上出现了 {top_count} 次错误，"
                            f"占总错误的 {top_count / total_errors * 100:.1f}%。"
                        ),
                        "severity": "高",
                    }
                )

        # 错误类型分布洞察
        if error_types:
            top_error_type, top_error_count = error_types[0]
            if top_error_count >= 3:
                insights.append(
                    {
                        "type": "错误类型",
                        "title": f"{top_error_type}是主要问题",
                        "description": (
                            f"你遇到了 {top_error_count} 次{top_error_type}，"
                            "建议学习相关的预防技巧。"
                        ),
                        "severity": "中",
                    }
                )

        # 趋势洞察
        if len(improvement_trend) >= 2:
            recent_errors = improvement_trend[-1]["total_errors"]
            previous_errors = improvement_trend[-2]["total_errors"]

            if recent_errors < previous_errors:
                insights.append(
                    {
                        "type": "趋势改善",
                        "title": "错误趋势正在改善",
                        "description": (
                            f"最近一周的错误数量({recent_errors})比前一周"
                            f"({previous_errors})有所减少，继续保持！"
                        ),
                        "severity": "低",
                    }
                )
            elif recent_errors > previous_errors:
                insights.append(
                    {
                        "type": "趋势警告",
                        "title": "错误趋势需要注意",
                        "description": (
                            f"最近一周的错误数量({recent_errors})比前一周"
                            f"({previous_errors})有所增加，需要关注。"
                        ),
                        "severity": "中",
                    }
                )

        return insights

    def _generate_next_steps(self, recommendations: List[Dict[str, Any]]) -> List[str]:
        """生成下一步行动建议。"""
        if not recommendations:
            return [
                "继续保持良好的命令行使用习惯",
                "定期回顾和总结使用经验",
                "探索新的命令和工具",
                "分享经验帮助他人",
            ]

        next_steps = []

        # 基于高优先级建议
        high_priority = [rec for rec in recommendations if rec["priority"] == "高"]
        if high_priority:
            next_steps.append(f"优先学习：{high_priority[0]['title']}")
            if len(high_priority) > 1:
                next_steps.append(f"其次关注：{high_priority[1]['title']}")

        # 基于建议类型
        command_recs = [rec for rec in recommendations if rec["type"] == "命令掌握"]
        if command_recs:
            next_steps.append(f"命令技能：{command_recs[0]['title']}")

        error_recs = [rec for rec in recommendations if rec["type"] == "错误预防"]
        if error_recs:
            next_steps.append(f"错误预防：{error_recs[0]['title']}")

        # 通用建议
        next_steps.extend(
            [
                "每天练习使用命令行15-30分钟",
                "遇到错误时仔细阅读错误信息",
                "建立个人的命令行笔记和技巧收集",
            ]
        )

        return next_steps[:6]  # 返回最多6个步骤

    def format_report_for_display(self, report: Dict[str, Any]) -> str:
        """将报告格式化为适合显示的字符串。"""
        lines = []

        # 报告标题
        lines.append("# 📊 AIS 学习成长报告")
        lines.append("")

        # AI洞察总结 - 放在最前面
        if report.get("ai_insights"):
            lines.append("## 🧠 AI智能洞察")
            lines.append(f"> {report['ai_insights']}")
            lines.append("")

        lines.append(f"**分析周期**: {report['report_info']['analysis_period']}")
        generated_time = datetime.fromisoformat(report["report_info"]["generated_at"]).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        lines.append(f"**生成时间**: {generated_time}")
        lines.append("")

        # 错误概览
        error_summary = report["error_summary"]
        lines.append("## 🔍 错误概览")
        lines.append(f"- **总错误数**: {error_summary['total_errors']} 次")

        if error_summary["most_common_commands"]:
            lines.append("- **最常出错的命令**:")
            for cmd, count in error_summary["most_common_commands"]:
                lines.append(f"  - `{cmd}`: {count} 次")

        if error_summary["most_common_error_types"]:
            lines.append("- **最常见的错误类型**:")
            for error_type, count in error_summary["most_common_error_types"]:
                lines.append(f"  - {error_type}: {count} 次")

        lines.append("")

        # 技能评估
        skill_assessment = report["skill_assessment"]
        lines.append("## 💪 技能评估")
        lines.append(f"- **当前水平**: {skill_assessment['skill_level']}")

        if skill_assessment["strengths"]:
            lines.append("- **优势领域**: " + ", ".join(skill_assessment["strengths"]))

        if skill_assessment["weaknesses"]:
            lines.append("- **需要改进**: " + ", ".join(skill_assessment["weaknesses"]))

        if skill_assessment["knowledge_gaps"]:
            lines.append("- **知识盲点**: " + ", ".join(skill_assessment["knowledge_gaps"]))

        lines.append("")

        # 改进洞察
        improvement_insights = report["improvement_insights"]
        if improvement_insights:
            lines.append("## 💡 改进洞察")
            for insight in improvement_insights:
                severity_icon = {"高": "🔥", "中": "⚠️", "低": "✓ "}.get(insight["severity"], "💡")
                lines.append(f"### {severity_icon} {insight['title']}")
                lines.append(insight["description"])
                lines.append("")

        # 学习建议
        learning_recommendations = report["learning_recommendations"]
        if learning_recommendations:
            lines.append("## 🎯 学习建议")
            for i, rec in enumerate(learning_recommendations, 1):
                priority_icon = {"高": "🔥", "中": "⚠️", "低": "💡"}.get(rec["priority"], "💡")
                lines.append(f"### {i}. {priority_icon} {rec['title']}")
                lines.append(f"**类型**: {rec['type']} | **优先级**: {rec['priority']}")
                lines.append(rec["description"])

                if rec["learning_path"]:
                    lines.append("**学习路径**:")
                    for step in rec["learning_path"]:
                        lines.append(f"- {step}")
                lines.append("")

        # 下一步行动
        next_steps = report["next_steps"]
        if next_steps:
            lines.append("## 🚀 下一步行动")
            for i, step in enumerate(next_steps, 1):
                lines.append(f"{i}. {step}")
            lines.append("")

        # 结尾
        lines.append("---")
        lines.append("💡 **提示**: 使用 `ais learn <主题>` 深入学习特定主题")
        lines.append("📚 **帮助**: 使用 `ais ask <问题>` 获取即时答案")
        lines.append("📈 **进度**: 定期运行 `ais report` 跟踪学习进度")

        return "\n".join(lines)

    def _generate_ai_insights(self, report: Dict[str, Any]) -> str:
        """生成AI洞察总结"""
        # 收集丰富的洞察数据
        insights_data = self._collect_rich_insights_data(report)

        # 构建增强版提示词
        insights_prompt = f"""
请基于用户最近30天的详细命令行数据，生成一段3-5句话的深度个性化洞察总结。

## 用户详细数据分析

### 基础统计
- 总错误数：{insights_data['basic_stats']['total_errors']}次
- 技能水平：{insights_data['basic_stats']['skill_level']}
- 独特命令数：{insights_data['basic_stats']['unique_commands']}个

### 错误模式深度分析
- 最频繁错误：{insights_data['error_patterns']['top_error_detail']}
- 错误类型分布：{insights_data['error_patterns']['error_types_summary']}
- 时间模式：{insights_data['error_patterns']['time_patterns']}

### 技能成长轨迹
- 优势技能：{insights_data['skill_analysis']['strengths_detail']}
- 改进领域：{insights_data['skill_analysis']['improvement_areas']}
- 学习进度：{insights_data['skill_analysis']['learning_velocity']}

### 环境和上下文洞察
- 主要工作环境：{insights_data['context_insights']['work_environments']}
- 项目类型分布：{insights_data['context_insights']['project_types']}
- 复杂度趋势：{insights_data['context_insights']['complexity_trend']}

### 趋势和进步指标
- 周趋势：{insights_data['trend_analysis']['weekly_trend']}
- 进步速度：{insights_data['trend_analysis']['improvement_rate']}
- 突出表现：{insights_data['trend_analysis']['notable_achievements']}

## 洞察要求
1. 发现最令人惊喜或意外的数据模式
2. 突出用户独特的学习特征和进步亮点
3. 提供具体的数字证据和对比
4. 语调积极鼓励，体现个性化关怀
5. 3-5句话，每句话都有价值和洞察力
6. 避免通用建议，专注于用户特有的发现

请生成一段让人眼前一亮的深度洞察总结：
"""

        # 调用AI生成洞察
        from ..core.ai import ask_ai
        from ..core.config import get_config

        config = get_config()
        ai_insights = ask_ai(insights_prompt, config)

        return ai_insights.strip()

    def _generate_fallback_insights(self, report: Dict[str, Any]) -> str:
        """生成备用洞察（AI不可用时）"""
        total_errors = report["error_summary"]["total_errors"]
        skill_level = report["skill_assessment"]["skill_level"]
        strengths = report["skill_assessment"]["strengths"]
        weaknesses = report["skill_assessment"]["weaknesses"]
        top_commands = report["error_summary"]["most_common_commands"][:2]

        if total_errors == 0:
            return "🌟 完美！最近30天零错误，你的命令行技能已经相当熟练了。这种稳定的表现说明你已经建立了良好的操作习惯。继续保持这种水准，你已经是命令行高手了！"
        elif total_errors < 5:
            insight = f"👏 出色表现！仅{total_errors}次错误，你正稳步向命令行专家迈进。"
            if strengths:
                insight += f"你在{strengths[0]}方面表现尤为出色。"
            insight += "这种低错误率反映了扎实的基础技能。"
            if weaknesses:
                insight += f"建议继续关注{weaknesses[0]}领域的提升。"
            return insight
        elif total_errors < 15:
            insight = (
                f"📈 稳步成长中！{total_errors}次错误反映了你的探索精神，每次错误都是进步的台阶。"
            )
            if top_commands:
                top_cmd = top_commands[0][0]
                insight += f"你在{top_cmd}命令上遇到的挑战最多，这正是学习的好机会。"
            insight += f"当前{skill_level}水平很不错，继续保持学习节奏。"
            if strengths:
                insight += f"你的{strengths[0]}技能已经成为优势。"
            return insight
        else:
            insight = (
                f"🚀 学习加速期！{total_errors}次错误说明你正在积极探索新领域，保持这种学习热情！"
            )
            if top_commands:
                top_cmd = top_commands[0][0]
                count = top_commands[0][1]
                insight += f"{top_cmd}命令出现{count}次错误，建议重点攻克。"
            insight += "频繁的尝试是掌握新技能的必经之路。"
            if strengths:
                insight += f"你在{strengths[0]}方面已经展现出天赋。"
            insight += "每个错误都在为你的技能升级积累经验。"
            return insight

    def _collect_rich_insights_data(self, report: Dict[str, Any]) -> Dict[str, Any]:
        """收集丰富的洞察数据"""
        # 获取原始错误日志进行深度分析
        error_logs = self.analyzer.get_error_logs()

        return {
            "basic_stats": self._analyze_basic_stats(report, error_logs),
            "error_patterns": self._analyze_error_patterns_deep(report, error_logs),
            "skill_analysis": self._analyze_skill_progression(report, error_logs),
            "context_insights": self._analyze_context_patterns(error_logs),
            "trend_analysis": self._analyze_trends_deep(report, error_logs),
        }

    def _analyze_basic_stats(self, report: Dict[str, Any], error_logs: List) -> Dict[str, Any]:
        """分析基础统计数据"""
        total_errors = report["error_summary"]["total_errors"]
        unique_commands = len(
            set(
                log.original_command.split()[0] if log.original_command.split() else ""
                for log in error_logs
            )
        )

        return {
            "total_errors": total_errors,
            "skill_level": report["skill_assessment"]["skill_level"],
            "unique_commands": unique_commands,
            "error_density": f"{total_errors / 30:.1f}次/天" if total_errors > 0 else "0次/天",
        }

    def _analyze_error_patterns_deep(
        self, report: Dict[str, Any], error_logs: List
    ) -> Dict[str, Any]:
        """深度分析错误模式"""
        if not error_logs:
            return {"top_error_detail": "无", "error_types_summary": "无", "time_patterns": "无"}

        # 分析最频繁的错误
        top_commands = report["error_summary"]["most_common_commands"]
        top_error_detail = "无特定模式"
        if top_commands:
            cmd, count = top_commands[0]
            percentage = (count / len(error_logs)) * 100
            top_error_detail = f"{cmd}命令({count}次，占{percentage:.1f}%)"

        # 错误类型汇总
        error_types = report["error_summary"]["most_common_error_types"][:3]
        error_types_summary = (
            ", ".join([f"{etype}({count}次)" for etype, count in error_types])
            if error_types
            else "多样化错误"
        )

        # 时间模式分析
        time_patterns = self._analyze_time_patterns(error_logs)

        return {
            "top_error_detail": top_error_detail,
            "error_types_summary": error_types_summary,
            "time_patterns": time_patterns,
        }

    def _analyze_time_patterns(self, error_logs: List) -> str:
        """分析时间模式"""
        if not error_logs:
            return "无明显时间模式"

        # 按小时分组
        hour_errors = {}
        for log in error_logs:
            hour = log.timestamp.hour
            hour_errors[hour] = hour_errors.get(hour, 0) + 1

        if not hour_errors:
            return "无明显时间模式"

        # 找出高峰时段
        peak_hour = max(hour_errors.items(), key=lambda x: x[1])
        total_errors = sum(hour_errors.values())

        if peak_hour[1] / total_errors > 0.3:  # 如果某个时段占比超过30%
            if 9 <= peak_hour[0] <= 17:
                return f"工作时间({peak_hour[0]}点)错误集中({peak_hour[1]}次)"
            elif 18 <= peak_hour[0] <= 22:
                return f"晚间学习时段({peak_hour[0]}点)最活跃({peak_hour[1]}次)"
            else:
                return f"深夜探索({peak_hour[0]}点)频繁尝试({peak_hour[1]}次)"
        else:
            return "错误时间分布均匀，无明显高峰"

    def _analyze_skill_progression(
        self, report: Dict[str, Any], error_logs: List
    ) -> Dict[str, Any]:
        """分析技能进步轨迹"""
        strengths = report["skill_assessment"]["strengths"][:2]
        weaknesses = report["skill_assessment"]["weaknesses"][:2]

        strengths_detail = "、".join(strengths) if strengths else "基础技能扎实"
        improvement_areas = "、".join(weaknesses) if weaknesses else "技能均衡发展"

        # 计算学习速度
        unique_commands = len(
            set(
                log.original_command.split()[0] if log.original_command.split() else ""
                for log in error_logs
            )
        )
        if unique_commands > 15:
            learning_velocity = "快速探索型（涉及多个领域）"
        elif unique_commands > 8:
            learning_velocity = "稳步学习型（逐步扩展）"
        elif unique_commands > 3:
            learning_velocity = "专注深入型（重点突破）"
        else:
            learning_velocity = "谨慎学习型（稳扎稳打）"

        return {
            "strengths_detail": strengths_detail,
            "improvement_areas": improvement_areas,
            "learning_velocity": learning_velocity,
        }

    def _analyze_context_patterns(self, error_logs: List) -> Dict[str, Any]:
        """分析上下文模式"""
        if not error_logs:
            return {
                "work_environments": "无数据",
                "project_types": "无数据",
                "complexity_trend": "无数据",
            }

        # 分析项目类型（从context_json中提取）
        project_types = {}
        git_usage = 0
        docker_usage = 0

        for log in error_logs:
            if log.context_json:
                try:
                    import json

                    context = json.loads(log.context_json)

                    # 项目类型统计
                    project_context = context.get("project_context", {})
                    if project_context:
                        ptype = project_context.get("project_type", "unknown")
                        if ptype != "unknown":
                            project_types[ptype] = project_types.get(ptype, 0) + 1

                    # Git使用情况
                    if context.get("git_branch"):
                        git_usage += 1

                except Exception:
                    pass

            # Docker使用情况
            if "docker" in log.original_command.lower():
                docker_usage += 1

        # 工作环境分析
        work_environments = []
        if git_usage > len(error_logs) * 0.3:
            work_environments.append("Git版本控制")
        if docker_usage > 0:
            work_environments.append("容器化开发")
        if project_types:
            top_project = max(project_types.items(), key=lambda x: x[1])
            work_environments.append(f"{top_project[0]}项目")

        work_env_summary = "、".join(work_environments) if work_environments else "通用命令行环境"

        # 项目类型分布
        if project_types:
            project_summary = "、".join(
                [f"{ptype}({count}次)" for ptype, count in project_types.items()]
            )
        else:
            project_summary = "未检测到特定项目类型"

        # 复杂度趋势
        complexity_indicators = ["docker", "git", "ssh", "chmod", "sudo"]
        complex_commands = sum(
            1
            for log in error_logs
            if any(indicator in log.original_command.lower() for indicator in complexity_indicators)
        )

        if complex_commands > len(error_logs) * 0.5:
            complexity_trend = "高复杂度操作占主导"
        elif complex_commands > len(error_logs) * 0.2:
            complexity_trend = "中等复杂度，逐步提升"
        else:
            complexity_trend = "基础操作为主"

        return {
            "work_environments": work_env_summary,
            "project_types": project_summary,
            "complexity_trend": complexity_trend,
        }

    def _analyze_trends_deep(self, report: Dict[str, Any], error_logs: List) -> Dict[str, Any]:
        """深度趋势分析"""
        if not error_logs or len(error_logs) < 7:
            return {
                "weekly_trend": "数据不足",
                "improvement_rate": "无法评估",
                "notable_achievements": "继续积累",
            }

        # 分析周趋势
        from datetime import datetime, timedelta

        now = datetime.now()
        last_week = now - timedelta(days=7)

        recent_errors = [log for log in error_logs if log.timestamp >= last_week]
        older_errors = [log for log in error_logs if log.timestamp < last_week]

        if older_errors:
            recent_rate = len(recent_errors) / 7
            older_rate = len(older_errors) / min(23, (now - error_logs[-1].timestamp).days)

            if recent_rate < older_rate * 0.7:
                weekly_trend = f"显著改善（错误率下降{(1 - recent_rate / older_rate) * 100:.0f}%）"
            elif recent_rate > older_rate * 1.3:
                weekly_trend = (
                    f"学习加速期（新挑战增加{(recent_rate / older_rate - 1) * 100:.0f}%）"
                )
            else:
                weekly_trend = "稳定发展中"
        else:
            weekly_trend = "初期学习阶段"

        # 改进速度评估
        total_errors = len(error_logs)
        days_span = (error_logs[0].timestamp - error_logs[-1].timestamp).days + 1

        if total_errors < days_span * 0.3:
            improvement_rate = "快速掌握型"
        elif total_errors < days_span * 0.8:
            improvement_rate = "稳步提升型"
        else:
            improvement_rate = "探索学习型"

        # 突出成就
        notable_achievements = []
        unique_commands = len(
            set(
                log.original_command.split()[0] if log.original_command.split() else ""
                for log in error_logs
            )
        )

        if unique_commands > 20:
            notable_achievements.append("技术栈广度超越80%用户")
        if total_errors < 5:
            notable_achievements.append("错误控制能力优秀")
        if any("docker" in log.original_command.lower() for log in error_logs):
            notable_achievements.append("勇于尝试容器化技术")
        if any("git" in log.original_command.lower() for log in error_logs):
            notable_achievements.append("版本控制技能实践")

        achievements_summary = (
            "、".join(notable_achievements) if notable_achievements else "稳步建立技能基础"
        )

        return {
            "weekly_trend": weekly_trend,
            "improvement_rate": improvement_rate,
            "notable_achievements": achievements_summary,
        }
