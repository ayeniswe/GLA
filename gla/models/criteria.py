"""
The `criteria` module provides a standardized format for analyzing and processing
`Log` data, allowing users to define criteria for identifying and interpreting logs 
from different sources. This module facilitates the integration of log entries into an 
analysis pipeline, ensuring consistency and flexibility in the handling of log data.
"""

from collections import OrderedDict
from typing import Dict

from pydantic import BaseModel, Field


class Criteria(BaseModel):
    """Represents a Criteria to follow"""
    
    entries: Dict[str, int] = Field(
        default_factory=OrderedDict,
        description="The count of occurrences of log entries."
    )
    """The number of occurrences for log entries."""
    
    class Config:
        allow_population_by_field_name = True
        validate_assignment = True
            
          