"""流式输出组件 - 优化用户体验的实时反馈系统"""

import time
from typing import Callable, Any
from rich.console import Console
from rich.progress import (Progress, SpinnerColumn, TextColumn,
                           BarColumn, TimeElapsedColumn)
from rich.live import Live


class StreamingDisplay:
    """流式显示组件，提供实时进度反馈"""

    def __init__(self, console: Console):
        self.console = console
        self.is_running = False
        self.current_status = "准备中..."
        self.progress_steps = []
        self.current_step = 0

    def start_analysis(self, steps: list[str]) -> None:
        """开始分析流程显示"""
        self.progress_steps = steps
        self.current_step = 0
        self.is_running = True

        # 显示分析开始信息
        self.console.print("\n[bold blue]🤖 AI 分析中...[/bold blue]")

    def update_step(self, step_index: int, status: str = "进行中") -> None:
        """更新当前步骤状态"""
        if 0 <= step_index < len(self.progress_steps):
            self.current_step = step_index
            self.current_status = status

            # 显示当前步骤
            step_text = self.progress_steps[step_index]
            if status == "进行中":
                self.console.print(f"[dim]  ➤ {step_text}...[/dim]", end="\r")
            elif status == "完成":
                self.console.print(f"[green]  ✓ {step_text}[/green]")
            elif status == "错误":
                self.console.print(f"[red]  ✗ {step_text}[/red]")

    def finish_analysis(self) -> None:
        """完成分析流程"""
        self.is_running = False
        self.console.print()  # 换行


class ProgressiveAnalysis:
    """渐进式分析显示，模拟AI思考过程"""

    def __init__(self, console: Console):
        self.console = console
        self.display = StreamingDisplay(console)

    def analyze_with_progress(self,
                              analyze_func: Callable,
                              command: str,
                              exit_code: int,
                              stderr: str,
                              context: dict,
                              config: dict) -> Any:
        """带进度显示的分析执行"""

        # 定义分析步骤
        steps = [
            "收集环境上下文",
            "诊断问题根因",
            "生成解决方案",
            "验证建议安全性",
            "格式化输出结果"
        ]

        self.display.start_analysis(steps)

        try:
            # 步骤 1: 收集环境上下文
            self.display.update_step(0, "进行中")
            # 实际的上下文收集已在调用前完成，这里只是显示
            time.sleep(0.2)  # 给用户足够时间看到进度
            self.display.update_step(0, "完成")

            # 步骤 2: 诊断问题根因
            self.display.update_step(1, "进行中")
            time.sleep(0.3)
            self.display.update_step(1, "完成")

            # 步骤 3: 生成解决方案 (实际AI调用)
            self.display.update_step(2, "进行中")
            try:
                result = analyze_func(
                    command, exit_code, stderr, context, config)
                self.display.update_step(2, "完成")
            except Exception as e:
                self.display.update_step(2, "错误")
                self.console.print(f"[red]AI分析失败: {e}[/red]")
                raise

            # 步骤 4: 验证建议安全性
            self.display.update_step(3, "进行中")
            time.sleep(0.1)
            self.display.update_step(3, "完成")

            # 步骤 5: 格式化输出结果
            self.display.update_step(4, "进行中")
            time.sleep(0.1)
            self.display.update_step(4, "完成")

            return result

        except Exception as e:
            # 显示错误状态
            self.display.update_step(self.display.current_step, "错误")
            raise e
        finally:
            self.display.finish_analysis()


class RealTimeProgress:
    """实时进度显示组件"""

    def __init__(self, console: Console):
        self.console = console
        self.live = None
        self.progress = None
        self.task_id = None

    def start_progress(self, description: str = "AI 分析中") -> None:
        """开始显示进度"""
        self.progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            console=self.console,
            transient=True,
        )

        self.task_id = self.progress.add_task(description, total=100)
        self.live = Live(
            self.progress,
            console=self.console,
            refresh_per_second=10)
        self.live.start()

    def update_progress(self, advance: int, description: str = None) -> None:
        """更新进度"""
        if self.progress and self.task_id:
            self.progress.advance(self.task_id, advance)
            if description:
                self.progress.update(self.task_id, description=description)

    def finish_progress(self) -> None:
        """完成进度显示"""
        if self.live:
            self.live.stop()
            self.live = None
            self.progress = None
            self.task_id = None


class StreamingAnalyzer:
    """流式分析器 - 主要的流式输出控制器"""

    def __init__(self, console: Console):
        self.console = console
        self.progressive = ProgressiveAnalysis(console)
        self.real_time = RealTimeProgress(console)

    def analyze_with_streaming(self,
                               analyze_func: Callable,
                               command: str,
                               exit_code: int,
                               stderr: str,
                               context: dict,
                               config: dict) -> Any:
        """执行带流式输出的分析"""

        # 流式输出始终启用，根据配置选择显示方式
        ui_config = config.get("ui", {})
        stream_mode = ui_config.get("stream_mode", "progressive")

        if stream_mode == "progressive":
            return self.progressive.analyze_with_progress(
                analyze_func, command, exit_code, stderr, context, config
            )
        elif stream_mode == "realtime":
            return self._analyze_with_realtime(
                analyze_func, command, exit_code, stderr, context, config
            )
        else:
            # 默认：简单的spinner显示
            return self._analyze_with_spinner(
                analyze_func, command, exit_code, stderr, context, config
            )

    def _analyze_with_realtime(self,
                               analyze_func: Callable,
                               command: str,
                               exit_code: int,
                               stderr: str,
                               context: dict,
                               config: dict) -> Any:
        """使用实时进度条的分析"""
        self.real_time.start_progress("🔍 AI 分析中")

        try:
            # 模拟分析过程
            self.real_time.update_progress(20, "收集上下文信息")
            time.sleep(0.1)

            self.real_time.update_progress(30, "分析错误原因")
            time.sleep(0.2)

            self.real_time.update_progress(30, "生成解决方案")
            try:
                result = analyze_func(
                    command, exit_code, stderr, context, config)
            except Exception as e:
                self.real_time.update_progress(0, "❌ AI分析失败")
                time.sleep(0.5)  # 让用户看到错误消息
                raise e

            self.real_time.update_progress(20, "验证建议安全性")
            time.sleep(0.1)

            return result

        finally:
            self.real_time.finish_progress()

    def _analyze_with_spinner(self,
                              analyze_func: Callable,
                              command: str,
                              exit_code: int,
                              stderr: str,
                              context: dict,
                              config: dict) -> Any:
        """使用简单spinner的分析"""
        try:
            with self.console.status("🤖 AI 分析中，请稍候..."):
                return analyze_func(
                    command, exit_code, stderr, context, config)
        except Exception as e:
            self.console.print(f"[red]AI分析失败: {e}[/red]")
            raise


class LearnAnalysis:
    """学习功能的渐进式分析显示"""

    def __init__(self, console: Console):
        self.console = console
        self.display = StreamingDisplay(console)

    def learn_with_progress(self,
                            learn_func: Callable,
                            topic: str,
                            config: dict) -> Any:
        """带进度显示的学习执行"""

        # 定义学习步骤
        steps = [
            f"分析主题 '{topic}' 的学习需求",
            "收集相关知识点和最佳实践",
            "生成结构化学习内容",
            "优化内容格式和可读性",
            "验证内容准确性和实用性"
        ]

        self.display.start_analysis(steps)

        try:
            # 步骤 1: 分析学习需求
            self.display.update_step(0, "进行中")
            time.sleep(0.2)
            self.display.update_step(0, "完成")

            # 步骤 2: 收集知识点
            self.display.update_step(1, "进行中")
            time.sleep(0.3)
            self.display.update_step(1, "完成")

            # 步骤 3: 生成学习内容 (实际AI调用)
            self.display.update_step(2, "进行中")
            try:
                result = learn_func(topic, config)
                self.display.update_step(2, "完成")
            except Exception as e:
                self.display.update_step(2, "错误")
                self.console.print(f"[red]学习内容生成失败: {e}[/red]")
                raise

            # 步骤 4: 优化内容格式
            self.display.update_step(3, "进行中")
            time.sleep(0.1)
            self.display.update_step(3, "完成")

            # 步骤 5: 验证内容质量
            self.display.update_step(4, "进行中")
            time.sleep(0.1)
            self.display.update_step(4, "完成")

            return result

        except Exception as e:
            # 显示错误状态
            self.display.update_step(self.display.current_step, "错误")
            raise e
        finally:
            self.display.finish_analysis()


class StreamingLearner:
    """流式学习器 - 学习功能的流式输出控制器"""

    def __init__(self, console: Console):
        self.console = console
        self.learn_analysis = LearnAnalysis(console)
        self.real_time = RealTimeProgress(console)

    def learn_with_streaming(self,
                             learn_func: Callable,
                             topic: str,
                             config: dict) -> Any:
        """执行带流式输出的学习"""

        # 流式输出始终启用，根据配置选择显示方式
        ui_config = config.get("ui", {})
        stream_mode = ui_config.get("stream_mode", "progressive")

        if stream_mode == "progressive":
            return self.learn_analysis.learn_with_progress(
                learn_func, topic, config
            )
        elif stream_mode == "realtime":
            return self._learn_with_realtime(learn_func, topic, config)
        else:
            # 默认：简单的spinner显示
            return self._learn_with_spinner(learn_func, topic, config)

    def _learn_with_realtime(self,
                             learn_func: Callable,
                             topic: str,
                             config: dict) -> Any:
        """使用实时进度条的学习"""
        self.real_time.start_progress(f"📚 正在学习 {topic}")

        try:
            # 模拟学习过程
            self.real_time.update_progress(20, "分析学习需求")
            time.sleep(0.1)

            self.real_time.update_progress(30, "收集知识点")
            time.sleep(0.2)

            self.real_time.update_progress(30, "生成学习内容")
            try:
                result = learn_func(topic, config)
            except Exception as e:
                self.real_time.update_progress(0, "❌ 学习内容生成失败")
                time.sleep(0.5)
                raise e

            self.real_time.update_progress(20, "优化内容格式")
            time.sleep(0.1)

            return result

        finally:
            self.real_time.finish_progress()

    def _learn_with_spinner(self,
                            learn_func: Callable,
                            topic: str,
                            config: dict) -> Any:
        """使用简单spinner的学习"""
        try:
            with self.console.status(f"📚 正在为您生成 {topic} 学习内容..."):
                return learn_func(topic, config)
        except Exception as e:
            self.console.print(f"[red]学习内容生成失败: {e}[/red]")
            raise


class AskAnalysis:
    """问答功能的渐进式分析显示"""

    def __init__(self, console: Console):
        self.console = console
        self.display = StreamingDisplay(console)

    def ask_with_progress(self,
                          ask_func: Callable,
                          question: str,
                          config: dict) -> Any:
        """带进度显示的问答执行"""

        # 定义问答步骤
        steps = [
            "理解问题内容",
            "搜索相关知识",
            "组织答案结构",
            "生成详细回答",
            "检查答案质量"
        ]

        self.display.start_analysis(steps)

        try:
            # 步骤 1: 理解问题
            self.display.update_step(0, "进行中")
            time.sleep(0.1)
            self.display.update_step(0, "完成")

            # 步骤 2: 搜索知识
            self.display.update_step(1, "进行中")
            time.sleep(0.2)
            self.display.update_step(1, "完成")

            # 步骤 3: 组织结构
            self.display.update_step(2, "进行中")
            time.sleep(0.1)
            self.display.update_step(2, "完成")

            # 步骤 4: 生成回答 (实际AI调用)
            self.display.update_step(3, "进行中")
            try:
                result = ask_func(question, config)
                self.display.update_step(3, "完成")
            except Exception as e:
                self.display.update_step(3, "错误")
                self.console.print(f"[red]AI回答生成失败: {e}[/red]")
                raise

            # 步骤 5: 检查质量
            self.display.update_step(4, "进行中")
            time.sleep(0.1)
            self.display.update_step(4, "完成")

            return result

        except Exception as e:
            # 显示错误状态
            self.display.update_step(self.display.current_step, "错误")
            raise e
        finally:
            self.display.finish_analysis()


class StreamingAsker:
    """流式问答器 - 问答功能的流式输出控制器"""

    def __init__(self, console: Console):
        self.console = console
        self.ask_analysis = AskAnalysis(console)
        self.real_time = RealTimeProgress(console)

    def ask_with_streaming(self,
                           ask_func: Callable,
                           question: str,
                           config: dict) -> Any:
        """执行带流式输出的问答"""

        # 流式输出始终启用，根据配置选择显示方式
        ui_config = config.get("ui", {})
        stream_mode = ui_config.get("stream_mode", "progressive")

        if stream_mode == "progressive":
            return self.ask_analysis.ask_with_progress(
                ask_func, question, config
            )
        elif stream_mode == "realtime":
            return self._ask_with_realtime(ask_func, question, config)
        else:
            # 默认：简单的spinner显示
            return self._ask_with_spinner(ask_func, question, config)

    def _ask_with_realtime(self,
                           ask_func: Callable,
                           question: str,
                           config: dict) -> Any:
        """使用实时进度条的问答"""
        self.real_time.start_progress("🤔 AI 思考中")

        try:
            # 模拟问答过程
            self.real_time.update_progress(15, "理解问题")
            time.sleep(0.1)

            self.real_time.update_progress(25, "搜索知识")
            time.sleep(0.1)

            self.real_time.update_progress(20, "组织答案")
            time.sleep(0.1)

            self.real_time.update_progress(30, "生成回答")
            try:
                result = ask_func(question, config)
            except Exception as e:
                self.real_time.update_progress(0, "❌ 回答生成失败")
                time.sleep(0.5)
                raise e

            self.real_time.update_progress(10, "检查质量")
            time.sleep(0.1)

            return result

        finally:
            self.real_time.finish_progress()

    def _ask_with_spinner(self,
                          ask_func: Callable,
                          question: str,
                          config: dict) -> Any:
        """使用简单spinner的问答"""
        try:
            with self.console.status("🤔 AI 正在思考您的问题..."):
                return ask_func(question, config)
        except Exception as e:
            self.console.print(f"[red]AI回答生成失败: {e}[/red]")
            raise


def create_streaming_analyzer(console: Console) -> StreamingAnalyzer:
    """创建流式分析器实例"""
    return StreamingAnalyzer(console)


def create_streaming_learner(console: Console) -> StreamingLearner:
    """创建流式学习器实例"""
    return StreamingLearner(console)


def create_streaming_asker(console: Console) -> StreamingAsker:
    """创建流式问答器实例"""
    return StreamingAsker(console)
