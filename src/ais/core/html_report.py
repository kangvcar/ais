"""HTML格式学习成长报告生成器。"""

from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, List, Any

try:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

from .report import LearningReportGenerator
from .analysis import ErrorAnalyzer


class HTMLReportGenerator:
    """HTML格式报告生成器。"""

    def __init__(self, days_back: int = 30):
        """初始化HTML报告生成器。

        Args:
            days_back: 分析最近多少天的数据
        """
        self.days_back = days_back
        self.report_generator = LearningReportGenerator(days_back)
        self.analyzer = ErrorAnalyzer(days_back)

    def generate_html_report(self) -> str:
        """生成完整的HTML报告。"""
        if not PLOTLY_AVAILABLE:
            raise ImportError("需要安装plotly库: pip install plotly")

        # 获取基础报告数据
        report_data = self.report_generator.generate_report()
        error_logs = self.analyzer.get_error_logs()

        # 生成各种图表
        charts = self._generate_all_charts(report_data, error_logs)

        # 生成HTML内容
        html_content = self._build_html_template(report_data, charts)

        return html_content

    def _generate_all_charts(self, report_data: Dict[str, Any], error_logs: List) -> Dict[str, str]:
        """生成所有图表。"""
        charts = {}

        # 错误趋势图
        charts["error_trend"] = self._create_error_trend_chart(error_logs)

        # 技能雷达图
        charts["skill_radar"] = self._create_skill_radar_chart(report_data["skill_assessment"])

        # 时间热力图
        charts["time_heatmap"] = self._create_time_heatmap(error_logs)

        # 命令频次图
        charts["command_frequency"] = self._create_command_frequency_chart(
            report_data["error_summary"]
        )

        # 错误类型分布图
        charts["error_types"] = self._create_error_types_chart(report_data["error_summary"])

        # 学习进度图
        charts["learning_progress"] = self._create_learning_progress_chart(error_logs)

        return charts

    def _create_error_trend_chart(self, error_logs: List) -> str:
        """生成错误趋势图。"""
        if not error_logs:
            return self._create_empty_chart("暂无错误数据")

        # 按日期聚合错误数量
        daily_errors = defaultdict(int)
        for log in error_logs:
            date_str = log.timestamp.strftime("%Y-%m-%d")
            daily_errors[date_str] += 1

        # 填补缺失的日期
        start_date = datetime.now() - timedelta(days=self.days_back)
        date_range = []
        error_counts = []

        for i in range(self.days_back + 1):
            current_date = start_date + timedelta(days=i)
            date_str = current_date.strftime("%Y-%m-%d")
            date_range.append(date_str)
            error_counts.append(daily_errors.get(date_str, 0))

        # 创建图表
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=date_range,
                y=error_counts,
                mode="lines+markers",
                name="错误数量",
                line=dict(color="#ef4444", width=3),
                marker=dict(size=6, color="#ef4444"),
                fill="tonexty",
                fillcolor="rgba(239, 68, 68, 0.1)",
            )
        )

        fig.update_layout(
            title=dict(text="📈 错误趋势 (最近30天)", font=dict(size=20, color="#1f2937")),
            xaxis=dict(title="日期", gridcolor="#f3f4f6", showgrid=True),
            yaxis=dict(title="错误次数", gridcolor="#f3f4f6", showgrid=True),
            template="plotly_white",
            height=350,
            margin=dict(l=50, r=50, t=60, b=50),
            hovermode="x unified",
        )

        return fig.to_html(include_plotlyjs=False, div_id="error-trend-chart")

    def _create_skill_radar_chart(self, skill_assessment: Dict[str, Any]) -> str:
        """生成技能雷达图。"""
        # 定义技能领域
        skill_areas = {
            "基础命令": ["ls", "cd", "pwd", "cat", "mkdir", "rm"],
            "文件操作": ["find", "grep", "sed", "awk", "sort"],
            "系统管理": ["ps", "top", "kill", "chmod", "sudo"],
            "网络工具": ["curl", "wget", "ping", "ssh"],
            "Git版本控制": ["git"],
            "Docker容器": ["docker"],
        }

        # 计算各领域得分 (0-10分)
        categories = list(skill_areas.keys())
        scores = []

        strengths = skill_assessment.get("strengths", [])
        weaknesses = skill_assessment.get("weaknesses", [])

        for category in categories:
            if category in strengths:
                scores.append(8.5)  # 优势领域高分
            elif category in weaknesses:
                scores.append(3.0)  # 弱点领域低分
            else:
                scores.append(6.0)  # 默认中等分数

        # 创建雷达图
        fig = go.Figure()
        fig.add_trace(
            go.Scatterpolar(
                r=scores,
                theta=categories,
                fill="toself",
                name="当前水平",
                fillcolor="rgba(59, 130, 246, 0.3)",
                line=dict(color="#3b82f6", width=3),
                marker=dict(size=8, color="#3b82f6"),
            )
        )

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10],
                    tickvals=[2, 4, 6, 8, 10],
                    ticktext=["新手", "入门", "熟练", "精通", "专家"],
                    gridcolor="#e5e7eb",
                ),
                angularaxis=dict(gridcolor="#e5e7eb"),
            ),
            title=dict(text="🎯 技能评估雷达图", font=dict(size=20, color="#1f2937")),
            template="plotly_white",
            height=400,
            margin=dict(l=50, r=50, t=60, b=50),
        )

        return fig.to_html(include_plotlyjs=False, div_id="skill-radar-chart")

    def _create_time_heatmap(self, error_logs: List) -> str:
        """生成时间热力图。"""
        if not error_logs:
            return self._create_empty_chart("暂无时间数据")

        # 创建24小时x7天的矩阵
        time_matrix = [[0 for _ in range(24)] for _ in range(7)]

        for log in error_logs:
            hour = log.timestamp.hour
            weekday = log.timestamp.weekday()
            time_matrix[weekday][hour] += 1

        # 星期标签
        weekday_labels = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        hour_labels = [f"{h:02d}:00" for h in range(24)]

        fig = go.Figure(
            data=go.Heatmap(
                z=time_matrix,
                x=hour_labels,
                y=weekday_labels,
                colorscale=[
                    [0, "#f8fafc"],
                    [0.2, "#fef3c7"],
                    [0.4, "#fcd34d"],
                    [0.6, "#f59e0b"],
                    [0.8, "#d97706"],
                    [1, "#92400e"],
                ],
                hoverongaps=False,
                hovertemplate="%{y} %{x}<br>错误次数: %{z}<extra></extra>",
            )
        )

        fig.update_layout(
            title=dict(text="⏰ 错误时间分布热力图", font=dict(size=20, color="#1f2937")),
            xaxis=dict(title="时间", tickangle=45),
            yaxis=dict(title="星期"),
            height=300,
            margin=dict(l=80, r=50, t=60, b=80),
        )

        return fig.to_html(include_plotlyjs=False, div_id="time-heatmap")

    def _create_command_frequency_chart(self, error_summary: Dict[str, Any]) -> str:
        """生成命令频次图。"""
        top_commands = error_summary.get("most_common_commands", [])[:8]

        if not top_commands:
            return self._create_empty_chart("暂无命令数据")

        commands = [cmd for cmd, _ in top_commands]
        counts = [count for _, count in top_commands]

        fig = go.Figure(
            data=[
                go.Bar(
                    x=commands,
                    y=counts,
                    marker=dict(color="#8b5cf6", line=dict(color="#7c3aed", width=1)),
                    hovertemplate="命令: %{x}<br>错误次数: %{y}<extra></extra>",
                )
            ]
        )

        fig.update_layout(
            title=dict(text="📊 最常出错的命令", font=dict(size=20, color="#1f2937")),
            xaxis=dict(title="命令", tickangle=45),
            yaxis=dict(title="错误次数", gridcolor="#f3f4f6"),
            template="plotly_white",
            height=350,
            margin=dict(l=50, r=50, t=60, b=80),
        )

        return fig.to_html(include_plotlyjs=False, div_id="command-frequency-chart")

    def _create_error_types_chart(self, error_summary: Dict[str, Any]) -> str:
        """生成错误类型分布图。"""
        error_types = error_summary.get("most_common_error_types", [])[:6]

        if not error_types:
            return self._create_empty_chart("暂无错误类型数据")

        labels = [error_type for error_type, _ in error_types]
        values = [count for _, count in error_types]

        # 定义颜色
        colors = ["#ef4444", "#f59e0b", "#10b981", "#3b82f6", "#8b5cf6", "#ec4899"]

        fig = go.Figure(
            data=[
                go.Pie(
                    labels=labels,
                    values=values,
                    hole=0.4,
                    marker=dict(colors=colors[: len(labels)]),
                    hovertemplate="%{label}<br>次数: %{value}<br>占比: %{percent}<extra></extra>",
                )
            ]
        )

        fig.update_layout(
            title=dict(text="🔍 错误类型分布", font=dict(size=20, color="#1f2937")),
            height=350,
            margin=dict(l=50, r=50, t=60, b=50),
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        )

        return fig.to_html(include_plotlyjs=False, div_id="error-types-chart")

    def _create_learning_progress_chart(self, error_logs: List) -> str:
        """生成学习进度图。"""
        if not error_logs or len(error_logs) < 7:
            return self._create_empty_chart("数据不足以分析学习进度")

        # 按周统计
        weekly_data = defaultdict(lambda: {"errors": 0, "unique_commands": set()})

        for log in error_logs:
            week_key = log.timestamp.strftime("%Y-W%U")
            weekly_data[week_key]["errors"] += 1
            if log.original_command.split():
                weekly_data[week_key]["unique_commands"].add(log.original_command.split()[0])

        # 准备数据
        weeks = sorted(weekly_data.keys())[-8:]  # 最近8周
        error_counts = [weekly_data[week]["errors"] for week in weeks]
        command_diversity = [len(weekly_data[week]["unique_commands"]) for week in weeks]

        # 创建双轴图表
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # 错误数量
        fig.add_trace(
            go.Scatter(
                x=weeks,
                y=error_counts,
                mode="lines+markers",
                name="错误次数",
                line=dict(color="#ef4444", width=3),
                marker=dict(size=8),
            ),
            secondary_y=False,
        )

        # 命令多样性
        fig.add_trace(
            go.Scatter(
                x=weeks,
                y=command_diversity,
                mode="lines+markers",
                name="探索的命令数",
                line=dict(color="#10b981", width=3),
                marker=dict(size=8),
            ),
            secondary_y=True,
        )

        # 设置轴标题
        fig.update_xaxes(title_text="周期")
        fig.update_yaxes(title_text="错误次数", secondary_y=False, color="#ef4444")
        fig.update_yaxes(title_text="探索命令数", secondary_y=True, color="#10b981")

        fig.update_layout(
            title=dict(text="📈 学习进度趋势", font=dict(size=20, color="#1f2937")),
            template="plotly_white",
            height=350,
            margin=dict(l=50, r=50, t=60, b=50),
            hovermode="x unified",
        )

        return fig.to_html(include_plotlyjs=False, div_id="learning-progress-chart")

    def _create_empty_chart(self, message: str) -> str:
        """创建空数据占位图表。"""
        fig = go.Figure()
        fig.add_annotation(
            text=message,
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            xanchor="center",
            yanchor="middle",
            font=dict(size=16, color="#6b7280"),
        )
        fig.update_layout(
            template="plotly_white",
            height=250,
            margin=dict(l=50, r=50, t=50, b=50),
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
        )
        return fig.to_html(include_plotlyjs=False)

    def _build_html_template(self, report_data: Dict[str, Any], charts: Dict[str, str]) -> str:
        """构建HTML模板。"""
        # 获取报告基本信息
        ai_insights = report_data.get("ai_insights", "暂无AI洞察")
        total_errors = report_data["error_summary"]["total_errors"]
        skill_level = report_data["skill_assessment"]["skill_level"]
        analysis_period = report_data["report_info"]["analysis_period"]
        generated_time = datetime.fromisoformat(
            report_data["report_info"]["generated_at"]
        ).strftime("%Y-%m-%d %H:%M:%S")

        html_template = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AIS 学习成长报告</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        :root {{
            --primary-color: #3b82f6;
            --success-color: #10b981;
            --warning-color: #f59e0b;
            --error-color: #ef4444;
            --bg-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto,
                         'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #1f2937;
            background: #f8fafc;
        }}

        .header {{
            background: var(--bg-gradient);
            color: white;
            padding: 2rem 0;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}

        .header h1 {{
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }}

        .header p {{
            font-size: 1.1rem;
            opacity: 0.9;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 1rem;
        }}

        .insights-section {{
            background: white;
            margin: 2rem auto;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            border-left: 4px solid var(--primary-color);
        }}

        .insights-section h2 {{
            color: var(--primary-color);
            margin-bottom: 1rem;
            font-size: 1.5rem;
        }}

        .insights-content {{
            background: #f8fafc;
            padding: 1.5rem;
            border-radius: 8px;
            border-left: 4px solid var(--primary-color);
            font-style: italic;
            font-size: 1.1rem;
            line-height: 1.8;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin: 2rem auto;
        }}

        .stat-card {{
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            transition: transform 0.2s ease;
        }}

        .stat-card:hover {{
            transform: translateY(-2px);
        }}

        .stat-value {{
            font-size: 2rem;
            font-weight: 700;
            color: var(--primary-color);
            display: block;
        }}

        .stat-label {{
            color: #6b7280;
            font-size: 0.9rem;
            margin-top: 0.5rem;
        }}

        .charts-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 2rem;
            margin: 2rem auto;
        }}

        .chart-container {{
            background: white;
            border-radius: 12px;
            padding: 1rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        }}

        .chart-container.full-width {{
            grid-column: 1 / -1;
        }}

        .footer {{
            background: #1f2937;
            color: white;
            text-align: center;
            padding: 2rem 0;
            margin-top: 3rem;
        }}

        .footer p {{
            opacity: 0.8;
        }}

        @media (max-width: 768px) {{
            .charts-grid {{
                grid-template-columns: 1fr;
            }}

            .header h1 {{
                font-size: 2rem;
            }}

            .container {{
                padding: 0 0.5rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="container">
            <h1>📊 AIS 学习成长报告</h1>
            <p>分析周期: {analysis_period} | 生成时间: {generated_time}</p>
        </div>
    </div>

    <div class="container">
        <!-- AI洞察部分 -->
        <div class="insights-section">
            <h2>🧠 AI智能洞察</h2>
            <div class="insights-content">
                {ai_insights}
            </div>
        </div>

        <!-- 统计概览 -->
        <div class="stats-grid">
            <div class="stat-card">
                <span class="stat-value">{total_errors}</span>
                <div class="stat-label">总错误次数</div>
            </div>
            <div class="stat-card">
                <span class="stat-value">{skill_level}</span>
                <div class="stat-label">技能水平</div>
            </div>
            <div class="stat-card">
                <span class="stat-value">{analysis_period}</span>
                <div class="stat-label">分析周期</div>
            </div>
        </div>

        <!-- 图表网格 -->
        <div class="charts-grid">
            <div class="chart-container full-width">
                {charts['error_trend']}
            </div>

            <div class="chart-container">
                {charts['skill_radar']}
            </div>

            <div class="chart-container">
                {charts['command_frequency']}
            </div>

            <div class="chart-container full-width">
                {charts['time_heatmap']}
            </div>

            <div class="chart-container">
                {charts['error_types']}
            </div>

            <div class="chart-container">
                {charts['learning_progress']}
            </div>
        </div>
    </div>

    <div class="footer">
        <div class="container">
            <p>由 AIS - 上下文感知的错误分析学习助手 生成</p>
            <p style="margin-top: 0.5rem; font-size: 0.9rem;">
                💡 提示: 使用 'ais learn &lt;主题&gt;' 深入学习特定主题</p>
        </div>
    </div>
</body>
</html>
        """

        return html_template
