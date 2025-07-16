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
        learning_recommendations = (
            self.analyzer.generate_learning_recommendations()
        )

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
            "improvement_insights": self._generate_improvement_insights(
                error_patterns
            ),
            "next_steps": self._generate_next_steps(learning_recommendations),
        }

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
                        f"在过去{self.days_back}天里仅发生了{total_errors}次错误，"
                        "表现优秀！"
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

    def _generate_next_steps(
        self, recommendations: List[Dict[str, Any]]
    ) -> List[str]:
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
        high_priority = [
            rec for rec in recommendations if rec["priority"] == "高"
        ]
        if high_priority:
            next_steps.append(f"优先学习：{high_priority[0]['title']}")
            if len(high_priority) > 1:
                next_steps.append(f"其次关注：{high_priority[1]['title']}")

        # 基于建议类型
        command_recs = [
            rec for rec in recommendations if rec["type"] == "命令掌握"
        ]
        if command_recs:
            next_steps.append(f"命令技能：{command_recs[0]['title']}")

        error_recs = [
            rec for rec in recommendations if rec["type"] == "错误预防"
        ]
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
        lines.append(
            f"**分析周期**: {report['report_info']['analysis_period']}"
        )
        generated_time = datetime.fromisoformat(
            report["report_info"]["generated_at"]
        ).strftime("%Y-%m-%d %H:%M:%S")
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
            lines.append(
                "- **优势领域**: " + ", ".join(skill_assessment["strengths"])
            )

        if skill_assessment["weaknesses"]:
            lines.append(
                "- **需要改进**: " + ", ".join(skill_assessment["weaknesses"])
            )

        if skill_assessment["knowledge_gaps"]:
            lines.append(
                "- **知识盲点**: "
                + ", ".join(skill_assessment["knowledge_gaps"])
            )

        lines.append("")

        # 改进洞察
        improvement_insights = report["improvement_insights"]
        if improvement_insights:
            lines.append("## 💡 改进洞察")
            for insight in improvement_insights:
                severity_icon = {"高": "🔥", "中": "⚠️", "低": "✅"}.get(
                    insight["severity"], "💡"
                )
                lines.append(f"### {severity_icon} {insight['title']}")
                lines.append(insight["description"])
                lines.append("")

        # 学习建议
        learning_recommendations = report["learning_recommendations"]
        if learning_recommendations:
            lines.append("## 🎯 学习建议")
            for i, rec in enumerate(learning_recommendations, 1):
                priority_icon = {"高": "🔥", "中": "⚠️", "低": "💡"}.get(
                    rec["priority"], "💡"
                )
                lines.append(f"### {i}. {priority_icon} {rec['title']}")
                lines.append(
                    f"**类型**: {rec['type']} | **优先级**: {rec['priority']}"
                )
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
