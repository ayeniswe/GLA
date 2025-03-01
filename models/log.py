from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class Log(BaseModel):
    """Represents a log entry"""

    level: Optional[str] = Field(
        default=None,
        description="The log level",
        # regex=r"(WARN|INFO|ERROR|NOTICE|CRITICAL|EMERGENCY|DEBUG|TRACE|ALERT)",
    )
    module: Optional[str] = Field(default=None, description="The module name")
    message: str = Field(default=..., description="The log message")
    timestamp: Optional[datetime] = Field(default=None, description="The timestamp")
    source: Optional[str] = Field(
        default=None, description="The source of the log entry"
    )

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
