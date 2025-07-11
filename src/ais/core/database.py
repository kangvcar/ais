"""数据库存储模块。"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

from sqlmodel import SQLModel, Field, create_engine, Session, select


class CommandLog(SQLModel, table=True):
    """命令执行日志模型。"""

    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.now)
    username: str
    original_command: str
    exit_code: int
    stderr_output: Optional[str] = None
    context_json: Optional[str] = None  # JSON 字符串存储上下文
    ai_explanation: Optional[str] = None
    ai_suggestions_json: Optional[str] = None  # JSON 字符串存储建议


def get_database_path() -> Path:
    """获取数据库文件路径。"""
    data_dir = Path.home() / ".local" / "share" / "ais"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir / "history.db"


def get_engine():
    """获取数据库引擎。"""
    db_path = get_database_path()
    return create_engine(f"sqlite:///{db_path}")


def init_database():
    """初始化数据库。"""
    engine = get_engine()
    SQLModel.metadata.create_all(engine)


def save_command_log(
    username: str,
    command: str,
    exit_code: int,
    stderr: str = None,
    context: Dict[str, Any] = None,
    ai_explanation: str = None,
    ai_suggestions: List[Dict[str, Any]] = None,
) -> int:
    """保存命令日志到数据库。"""
    init_database()

    log = CommandLog(
        username=username,
        original_command=command,
        exit_code=exit_code,
        stderr_output=stderr,
        context_json=json.dumps(context) if context else None,
        ai_explanation=ai_explanation,
        ai_suggestions_json=(
            json.dumps(ai_suggestions) if ai_suggestions else None
        ),
    )

    engine = get_engine()
    with Session(engine) as session:
        session.add(log)
        session.commit()
        session.refresh(log)
        return log.id


def _execute_query(statement) -> List[CommandLog]:
    """执行数据库查询的通用函数。"""
    init_database()
    engine = get_engine()
    with Session(engine) as session:
        return session.exec(statement).all()


def get_recent_logs(limit: int = 10) -> List[CommandLog]:
    """获取最近的命令日志。"""
    statement = (
        select(CommandLog).order_by(CommandLog.timestamp.desc()).limit(limit)
    )
    return _execute_query(statement)


def get_log_by_id(log_id: int) -> Optional[CommandLog]:
    """根据 ID 获取日志。"""
    init_database()
    engine = get_engine()
    with Session(engine) as session:
        return session.get(CommandLog, log_id)


def get_similar_commands(command: str, limit: int = 5) -> List[CommandLog]:
    """获取相似的命令日志。"""
    keywords = command.split()[:3]  # 取前3个词

    statement = (
        select(CommandLog)
        .where(CommandLog.exit_code != 0)  # 只查询失败的命令
        .order_by(CommandLog.timestamp.desc())
        .limit(limit * 3)
    )

    all_logs = _execute_query(statement)

    # 简单的相似性过滤
    similar_logs = []
    for log in all_logs:
        log_words = log.original_command.split()
        if any(keyword in log_words for keyword in keywords):
            similar_logs.append(log)
            if len(similar_logs) >= limit:
                break

    return similar_logs
