"""测试报告功能。"""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta

from ais.core.analysis import ErrorAnalyzer
from ais.core.report import LearningReportGenerator
from ais.core.database import CommandLog


class TestErrorAnalyzer:
    """测试错误分析器。"""

    def test_classify_error_command_not_found(self):
        """测试命令不存在的错误分类。"""
        analyzer = ErrorAnalyzer()

        log = Mock(spec=CommandLog)
        log.original_command = "unknown_command"
        log.stderr_output = "unknown_command: command not found"

        result = analyzer._classify_error(log)
        assert result == "命令不存在"

    def test_classify_error_file_not_found(self):
        """测试文件不存在的错误分类。"""
        analyzer = ErrorAnalyzer()

        log = Mock(spec=CommandLog)
        log.original_command = "ls /nonexistent"
        log.stderr_output = (
            "ls: cannot access '/nonexistent': No such file or directory"
        )

        result = analyzer._classify_error(log)
        assert result == "文件/目录不存在"

    def test_classify_error_git_error(self):
        """测试Git错误分类。"""
        analyzer = ErrorAnalyzer()

        log = Mock(spec=CommandLog)
        log.original_command = "git status"
        log.stderr_output = "fatal: not a git repository"

        result = analyzer._classify_error(log)
        assert result == "Git操作错误"

    def test_skill_assessment_no_errors(self):
        """测试无错误时的技能评估。"""
        analyzer = ErrorAnalyzer()

        with patch.object(analyzer, "get_error_logs", return_value=[]):
            assessment = analyzer.generate_skill_assessment()

            assert assessment["skill_level"] == "初学者"
            assert assessment["strengths"] == []
            assert assessment["weaknesses"] == []
            assert assessment["knowledge_gaps"] == []

    @patch("ais.core.analysis.get_recent_logs")
    def test_error_patterns_analysis(self, mock_get_logs):
        """测试错误模式分析。"""
        # 创建模拟数据
        mock_logs = []
        for i in range(3):
            log = Mock(spec=CommandLog)
            log.original_command = "ls /nonexistent"
            log.exit_code = 2
            log.stderr_output = (
                "ls: cannot access '/nonexistent': No such file or directory"
            )
            log.timestamp = datetime.now() - timedelta(days=i)
            mock_logs.append(log)

        mock_get_logs.return_value = mock_logs

        analyzer = ErrorAnalyzer(days_back=30)
        patterns = analyzer.analyze_error_patterns()

        assert patterns["total_errors"] == 3
        assert patterns["common_commands"][0][0] == "ls"
        assert patterns["common_commands"][0][1] == 3
        assert patterns["error_types"][0][0] == "文件/目录不存在"


class TestLearningReportGenerator:
    """测试学习报告生成器。"""

    def test_generate_report_structure(self):
        """测试报告结构。"""
        generator = LearningReportGenerator(days_back=30)

        with patch.object(
            generator.analyzer,
            "analyze_error_patterns",
            return_value={
                "total_errors": 0,
                "common_commands": [],
                "error_types": [],
                "time_distribution": {},
                "improvement_trend": [],
                "analysis_period": "30天",
            },
        ):
            with patch.object(
                generator.analyzer,
                "generate_skill_assessment",
                return_value={
                    "skill_level": "初学者",
                    "strengths": [],
                    "weaknesses": [],
                    "knowledge_gaps": [],
                },
            ):
                with patch.object(
                    generator.analyzer,
                    "generate_learning_recommendations",
                    return_value=[],
                ):
                    report = generator.generate_report()

                    # 验证报告结构
                    assert "report_info" in report
                    assert "error_summary" in report
                    assert "skill_assessment" in report
                    assert "learning_recommendations" in report
                    assert "improvement_insights" in report
                    assert "next_steps" in report

    def test_format_report_for_display(self):
        """测试报告格式化。"""
        generator = LearningReportGenerator(days_back=30)

        # 创建测试报告数据
        test_report = {
            "report_info": {
                "generated_at": datetime.now().isoformat(),
                "analysis_period": "最近30天",
                "report_type": "学习成长报告",
            },
            "error_summary": {
                "total_errors": 5,
                "analysis_period": "30天",
                "most_common_commands": [("ls", 2), ("git", 1)],
                "most_common_error_types": [("文件/目录不存在", 2)],
            },
            "skill_assessment": {
                "skill_level": "中级用户",
                "strengths": [],
                "weaknesses": [],
                "knowledge_gaps": ["基础命令"],
            },
            "learning_recommendations": [],
            "improvement_insights": [],
            "next_steps": ["继续保持良好的命令行使用习惯"],
        }

        formatted = generator.format_report_for_display(test_report)

        # 验证格式化输出包含关键信息
        assert "📊 AIS 学习成长报告" in formatted
        assert "🔍 错误概览" in formatted
        assert "💪 技能评估" in formatted
        assert "🚀 下一步行动" in formatted
        assert "**总错误数**: 5 次" in formatted
        assert "**当前水平**: 中级用户" in formatted

    def test_generate_improvement_insights(self):
        """测试改进洞察生成。"""
        generator = LearningReportGenerator(days_back=30)

        # 测试错误频率较低的洞察
        error_patterns = {
            "total_errors": 3,
            "common_commands": [("ls", 2)],
            "error_types": [("文件/目录不存在", 2)],
            "improvement_trend": [],
        }

        insights = generator._generate_improvement_insights(error_patterns)

        assert len(insights) >= 1
        assert insights[0]["title"] == "错误频率较低"
        assert insights[0]["severity"] == "低"

    def test_generate_next_steps(self):
        """测试下一步行动生成。"""
        generator = LearningReportGenerator(days_back=30)

        # 测试无建议时的下一步
        next_steps = generator._generate_next_steps([])

        assert len(next_steps) > 0
        assert "继续保持良好的命令行使用习惯" in next_steps

        # 测试有建议时的下一步
        recommendations = [
            {"type": "命令掌握", "title": "深入学习 ls 命令", "priority": "高"}
        ]

        next_steps = generator._generate_next_steps(recommendations)

        assert len(next_steps) > 0
        assert any("优先学习" in step for step in next_steps)
