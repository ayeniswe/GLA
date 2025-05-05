"""
The `result` module defines standard result codes for signaling success or failure
states across an application or system.
"""

from enum import Enum

class Result(Enum):
    Ok = 0
    Error = -1