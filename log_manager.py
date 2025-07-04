"""
日志管理模块
实现实时日志队列和格式化功能
"""

import queue
import time
from typing import List, Dict, Optional, Callable
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import threading

class LogLevel(Enum):
    """日志级别枚举"""
    INFO = "INFO"
    DEBUG = "DEBUG"
    WARNING = "WARNING"
    ERROR = "ERROR"
    TOOL = "TOOL"
    THINKING = "THINKING"
    RESULT = "RESULT"

@dataclass
class LogEvent:
    """日志事件数据结构"""
    level: LogLevel
    message: str
    timestamp: str
    metadata: Optional[Dict] = None
    
    def to_markdown(self) -> str:
        """转换为Markdown格式"""
        # 根据日志级别设置不同的样式
        level_styles = {
            LogLevel.INFO: "💬",
            LogLevel.DEBUG: "🔍",
            LogLevel.WARNING: "⚠️",
            LogLevel.ERROR: "❌",
            LogLevel.TOOL: "🛠️",
            LogLevel.THINKING: "🤔",
            LogLevel.RESULT: "✅"
        }
        
        prefix = level_styles.get(self.level, "📝")
        
        # 构建日志消息
        log_md = f"{prefix} **{self.level.value}** [{self.timestamp}] {self.message}"
        
        # 添加元数据（如果有）
        if self.metadata and len(self.metadata) > 0:
            metadata_str = "\n```json\n"
            for key, value in self.metadata.items():
                metadata_str += f"{key}: {value}\n"
            metadata_str += "```"
            log_md += metadata_str
            
        return log_md

class LogQueueManager:
    """日志队列管理器"""
    
    def __init__(self, max_logs: int = 100):
        """
        初始化日志队列管理器
        
        Args:
            max_logs: 最大日志数量
        """
        self.log_queue = queue.Queue()
        self.log_history: List[LogEvent] = []
        self.max_logs = max_logs
        self.callbacks: List[Callable[[LogEvent], None]] = []
        self.lock = threading.Lock()
        
    def add_log(self, level: LogLevel, message: str, metadata: Optional[Dict] = None) -> None:
        """
        添加日志
        
        Args:
            level: 日志级别
            message: 日志消息
            metadata: 元数据（可选）
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_event = LogEvent(level=level, message=message, timestamp=timestamp, metadata=metadata)
        
        # 添加到队列
        self.log_queue.put(log_event)
        
        # 添加到历史记录
        with self.lock:
            self.log_history.append(log_event)
            # 保持历史记录在最大数量以内
            if len(self.log_history) > self.max_logs:
                self.log_history = self.log_history[-self.max_logs:]
        
        # 触发回调
        for callback in self.callbacks:
            try:
                callback(log_event)
            except Exception as e:
                print(f"日志回调错误: {str(e)}")
    
    def get_logs(self) -> List[LogEvent]:
        """获取所有日志"""
        with self.lock:
            return list(self.log_history)
    
    def get_logs_markdown(self) -> str:
        """获取所有日志的Markdown格式"""
        logs = self.get_logs()
        return "\n\n".join([log.to_markdown() for log in logs])
    
    def clear_logs(self) -> None:
        """清除所有日志"""
        with self.lock:
            self.log_history.clear()
            # 清空队列
            while not self.log_queue.empty():
                try:
                    self.log_queue.get_nowait()
                except queue.Empty:
                    break
    
    def register_callback(self, callback: Callable[[LogEvent], None]) -> None:
        """
        注册日志回调函数
        
        Args:
            callback: 回调函数，接收LogEvent参数
        """
        self.callbacks.append(callback)
    
    def unregister_callback(self, callback: Callable[[LogEvent], None]) -> None:
        """
        注销日志回调函数
        
        Args:
            callback: 要注销的回调函数
        """
        if callback in self.callbacks:
            self.callbacks.remove(callback)

# 全局日志管理器实例
log_manager = LogQueueManager()

# 便捷日志函数
def log_info(message: str, metadata: Optional[Dict] = None) -> None:
    """记录INFO级别日志"""
    log_manager.add_log(LogLevel.INFO, message, metadata)

def log_debug(message: str, metadata: Optional[Dict] = None) -> None:
    """记录DEBUG级别日志"""
    log_manager.add_log(LogLevel.DEBUG, message, metadata)

def log_warning(message: str, metadata: Optional[Dict] = None) -> None:
    """记录WARNING级别日志"""
    log_manager.add_log(LogLevel.WARNING, message, metadata)

def log_error(message: str, metadata: Optional[Dict] = None) -> None:
    """记录ERROR级别日志"""
    log_manager.add_log(LogLevel.ERROR, message, metadata)

def log_tool(message: str, metadata: Optional[Dict] = None) -> None:
    """记录工具调用日志"""
    log_manager.add_log(LogLevel.TOOL, message, metadata)

def log_thinking(message: str, metadata: Optional[Dict] = None) -> None:
    """记录思考过程日志"""
    log_manager.add_log(LogLevel.THINKING, message, metadata)

def log_result(message: str, metadata: Optional[Dict] = None) -> None:
    """记录结果日志"""
    log_manager.add_log(LogLevel.RESULT, message, metadata)
