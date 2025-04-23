"""
The `entry` module provides the `Entry` model, which allows specifying search terms
and conditions (such as required presence or absence)..
"""

from pydantic import BaseModel, Field

class Entry(BaseModel):
    """Represents an Entry to search"""

    text: str = Field(
        description="The actual text to search for in log entries."
    )
    """The actual text to search for in log entries."""
    cnt: int = Field(
        description="The amount of time to search for text in log entries"
        "When 0 this means to find the text absent from log entries"
    )
    """
    The actual text to search for in log entries.
    
    When `0` this means to find the text absent from log entries
    """

    class Config:
        allow_population_by_field_name = True
        validate_assignment = True
