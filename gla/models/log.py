"""
The `log` module is for represents a log entry from different logging tools
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Log(BaseModel):
    """Represents a log entry"""

    # Instance Attributes
    level: Optional[str] = Field(
        default=None,
        description="The severity of the log message",
        # regex=r"(WARN|INFO|ERROR|NOTICE|CRITICAL|EMERGENCY|DEBUG|TRACE|ALERT)",
    )
    """The severity of the log message"""
    module: Optional[str] = Field(
        default=None,
        description="The logger's name or process name that created the log entry",
    )
    """The logger's name or process name that created the log entry"""
    message: str = Field(default=None, description="The log message")
    """The log message"""
    timestamp: Optional[datetime] = Field(
        default=None,
        description="The date and time when the log record was created",
    )
    """The date and time when the log record was created"""
    source: Optional[str] = Field(
        default=None,
        description="The name of the host, machine, or thread that generated the log entry",
    )
    """The name of the host, machine, or thread that generated the log entry"""

    def __str__(self):
        parts = []

        if self.timestamp:
            parts.append(self.timestamp.isoformat())

        if self.level:
            parts.append(self.level.upper())

        if self.source:
            parts.append(f"[{self.source}]")

        if self.module:
            parts.append(self.module)

        if self.message:
            parts.append(f"- {self.message}")

        return " ".join(parts)

    class Config:
        allow_population_by_field_name = True
        validate_assignment = True
