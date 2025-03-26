"""
The 'custom_transformer' module defines the `CustomTransformer` class, which is responsible
for transforming JSON log messages into structured `Log` objects based on predefined
template supplied from user.
"""

from typing import List, Optional

import dateparser

from gla.constants import LANGUAGES_SUPPORTED
from gla.models.log import Log
from gla.plugins.transformer.transformer import BaseTransformer

# Only allowed template keys
LOG_HEADERS = {
    "ext",  # allow tacking onto message for more info
    "msg",
    "mod",
    "lvl",
    "time",
    "src",
}

class CustomTransformer(BaseTransformer):
    """
    The `CustomTransformer` class is responsible for handling transformation
    of user templated log messages
    """

    def __init__(self, template: List[str]):
        """
        A transformer for parsing structured log entries based on a user-defined template.

        The first element in the template is always the delimiter used to split log entries.  
        The remaining elements define the expected structure of the log message.
        
        Template Keys:
        - `msg`  : The main content of the entry.
        - `lvl`  : A categorical label representing severity or type.
        - `src`  : The origin of the entry (e.g., filename, component, or system identifier).
        - `mod`  : An additional identifier for logical grouping or categorization.
        - `time` : A timestamp or chronological marker.
        - `ext`  : Extra fields for any additional data beyond the core structure.

        ```
        template = [";", "time", "lvl", "src", "mod", "msg"]
        transformer = CustomTransformer(template)
        log_entry = "2024-05-09;WARNING;dump.py;mod;System failure detected"
        log = transformer.transform(log_entry)
        ```
        Raises:
            ValueError: If the template is invalid or the log entry does not match the expected format.
        """
        # Validate template fits standard
        if len(template) <= 1:
            raise ValueError("missing atleast 'one' gla log header")
        else:
            for i, item in enumerate(template):
                if i == 0:
                    continue
                if item not in LOG_HEADERS:
                    raise ValueError(f"'{item}' is not a valid gla log header")
        self.delim = template[0]
        self.template = template[1:len(template)]
        

    def transform(self, entry: str) -> Optional[Log]:
        """Transforms a log entry into a `Log` object

        Args:
            entry (str): a log entry to transform

        Raises:
            ValueError: If the log entry does not match the expected template.
        """
        pieces = entry.split(self.delim)
        if len(self.template) is not len(pieces):
            raise ValueError(f"{self.template} template does not align with the log message: {entry}")
        
        msg = None
        lvl = None
        time = None
        mod = None
        src = None
        for i, piece in enumerate(pieces):
            if self.template[i] == "time" and piece:
                time = piece
            elif self.template[i] == "lvl" and piece:
                lvl = piece
            elif self.template[i] == "src" and piece:
                src = piece
            elif self.template[i] == "mod" and piece:
                mod = piece
            elif piece:
                if msg:
                    msg += f" {piece}"
                else:
                    msg = piece

        return Log(
            level=lvl,
            module=mod,
            message=msg,
            timestamp=dateparser.parse(time, languages=LANGUAGES_SUPPORTED),
            source=src
        )