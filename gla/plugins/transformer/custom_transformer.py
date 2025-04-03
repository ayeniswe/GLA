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
    "ext",
    "msg",
    "mod",
    "lvl",
    "ign",
    "time",
    "src",
}


class CustomTransformer(BaseTransformer):
    """
    The `CustomTransformer` class is responsible for handling transformation
    of user templated log messages
    """

    def __init__(self, template: List[str], delim: str = " "):
        """
        A transformer for parsing structured log entries based on a user-defined template.

        The `delim` is the delimiter used to split log entries.
        The `template` defines the expected structure of the log message.

        Template Keys:
        - `msg`  : The main content of the entry.
        - `lvl`  : A categorical label representing severity or type.
        - `src`  : The origin of the entry (e.g., filename, component, or system identifier).
        - `mod`  : An additional identifier for logical grouping or categorization.
        - `time` : A timestamp or chronological marker.
        - `ext`  : Extra fields for any additional data beyond the core structure.
        - `ign`  : Fields to ignore

        When specifiy `msg` key the transformer will pick up every part of the message.
        The key should only be specified once typically at the start of the message

        ### With default delimiter:

        ```
        >>> template = ["ign", "time", "time", "msg", "lvl"]
        >>> transformer = CustomTransformer(template)
        >>> transformer.transform("[Timestamp]: 2025-01-22 22:19:43 a fresh install [Warn]:")
        >>> Log(level='[Warn]:', module='', message='a fresh install',
        timestamp=datetime.datetime(2025, 1, 22, 22, 19, 43), source='')
        ```

        ### With custom delimiter:

        ```
        >>> template = ["time", "lvl", "src", "mod", "msg"]
        >>> transformer = CustomTransformer(template, ";")
        >>> transformer.transform("2024-05-09;WARNING;dump.py;mod;System failure detected")
        >>> Log(level='WARNING', module='mod', message='System failure detected',
        timestamp=datetime.datetime(2024, 5, 9, 0, 0), source='dump.py')
        ```
        Raises:
            ValueError: If the template is invalid or the log entry does not match
            the expected format.
        """
        # Validate template fits standard
        if len(template) == 0:
            raise ValueError("missing atleast 'one' gla log header")
        else:
            for item in template:
                if item not in LOG_HEADERS:
                    raise ValueError(f"'{item}' is not a valid gla log header")
        self.delim = delim
        self.template = template

    def transform(self, entry: str) -> Optional[Log]:
        """Transforms a log entry into a `Log` object

        Args:
            entry (str): a log entry to transform

        Raises:
            ValueError: If the log entry does not match the expected template.
        """
        pieces = entry.split(self.delim)
        if len(self.template) > len(pieces):
            raise ValueError(
                f"template {self.template} with delimiter '{self.delim}' does not \
                align with the log message: {entry}"
            )

        msg, lvl, time, mod, src = [], [], [], [], []
        i, offset = 0, 0
        while i < len(self.template):
            # We need to keep track of indice in case it
            # gets out of sync when long messages are processed
            piece = pieces[i + offset]

            if self.template[i] == "msg" and piece != "":
                offset = 0
                long_msg_end = len(pieces) - abs(len(self.template) - i) + 1
                long_msg_start = i + 1
                # Some messages can be long so
                # capture every piece
                msg.append(piece)
                for j in range(long_msg_start, long_msg_end):
                    msg.append(pieces[j])
                offset = long_msg_end - long_msg_start
            elif self.template[i] == "time" and piece:
                time.append(piece)
            elif self.template[i] == "lvl" and piece:
                lvl.append(piece)
            elif self.template[i] == "src" and piece:
                src.append(piece)
            elif self.template[i] == "mod" and piece:
                mod.append(piece)
            elif self.template[i] == "ext":
                msg.append(piece)

            i += 1

        return Log(
            level=" ".join(lvl) if lvl else None,
            module=" ".join(mod) if mod else None,
            message=" ".join(msg) if msg else None,
            timestamp=dateparser.parse(" ".join(time), languages=LANGUAGES_SUPPORTED)
            if time
            else None,
            source=" ".join(src) if src else None,
        )
