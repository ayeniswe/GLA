"""
The `analyzer` module is responsible for analyzing log messages based on predefined criteria.
"""

from gla.models.criteria import Criteria


class Analyzer:
    def __init__(self, crit: Criteria):
        self.crit = crit
