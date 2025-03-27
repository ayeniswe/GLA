"""
The `criteria` module provides a standardized format for analyzing and processing
`Log` data, allowing users to define criteria for identifying and interpreting logs 
from different sources. This module facilitates the integration of log entries into an 
analysis pipeline, ensuring consistency and flexibility in the handling of log data.
"""

from typing import Dict, List, Tuple, Union
from pydantic import BaseModel, Field
from collections import OrderedDict

class Criteria(BaseModel):
    """Represents a Criteria to follow"""
    
    entries_no_seq: Dict[str, bool] = Field(
        default_factory=dict,
        description="The entries to look for during log analysis (non-sequentially)."
    )
    """Non-sequential log entries to look for during analysis."""
    
    entries: Dict[str, bool] = Field(
        default_factory=OrderedDict,
        description="The entries to look for during log analysis (sequentially)."
    )
    """Sequential log entries to look for during analysis."""
    
    entries_counter_no_seq: Dict[str, int] = Field(
        default_factory=dict,
        description="The count of occurrences of non-sequential log entries."
    )
    """The number of occurrences for non-sequential log entries."""
    
    entries_counter: Dict[str, int] = Field(
        default_factory=OrderedDict,
        description="The count of occurrences of sequential log entries."
    )
    """The number of occurrences for sequential log entries."""
    
    class Config:
        allow_population_by_field_name = True
        validate_assignment = True
        
    def find_entries(self, entries: Union[List[str], str], seq = False):
        """Add a single or multiple log entries to the search criteria where order is irrelevant

        By default, entries are treated as non-sequential. If the sequence matters, set `seq=True`
        """
        if type(entries) is list:
            for entry in entries:
                if not seq:
                    self.entries_no_seq[entry] = False
                else:
                    self.entries[entry] = False
        elif type(entries) is str:
            if not seq:
                self.entries_no_seq[entries] = False
            else:
                self.entries[entries] = False
        
    def find_entries_count(self, entries: Union[List[Tuple[str, int]], Tuple[str, int]], seq = False):
        """Add the count of occurrences for a single or multiple log entries to the search criteria

        By default, entries are treated as non-sequential. If the sequence matters, set `seq=True`
        """
        if type(entries) is list:
            for entry in entries:
                if not seq:
                    self.entries_counter_no_seq[entry[0]] = entry[1]
                else:
                    self.entries_counter[entry[0]] = entry[1]
        elif type(entries) is tuple:
            if not seq:
                self.entries_counter_no_seq[entries[0]] = entries[1]
            else:
                self.entries_counter[entries[0]] = entries[1]

    def find_entries_absent(self, entries: Union[List[str], str]):
        """Find if a single or multiple log entries are absent from the search criteria
        """
        if type(entries) is list:
            for entry in entries:
                self.find_entries_count((entry,0))
        elif type(entries) is str:
            self.find_entries_count((entries,0))
            
          