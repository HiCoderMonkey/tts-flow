from datetime import datetime, timezone


def utc_now() -> datetime:
    """获取当前UTC时间（时区感知）"""
    return datetime.now(timezone.utc)


def utc_timestamp() -> float:
    """获取当前UTC时间戳"""
    return datetime.now(timezone.utc).timestamp()


def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """格式化datetime为字符串"""
    return dt.strftime(format_str)


def parse_datetime(date_str: str, format_str: str = "%Y-%m-%d %H:%M:%S") -> datetime:
    """解析字符串为datetime"""
    return datetime.strptime(date_str, format_str).replace(tzinfo=timezone.utc) 