from plugins.transformer.transformer import (
    DIVIDER_RE,
    LEVEL_RE,
    MODULE_RE,
    MSG_RE,
    SOURCE_RE,
    TIME_RE,
    Transformer,
)

TIME_SRC_LVL_MOD_MSG = Transformer(
    rf"{TIME_RE} {SOURCE_RE} {LEVEL_RE} {MODULE_RE} {DIVIDER_RE} {MSG_RE}",
)
"""
Transforms a `Log4j` log item with the following order:

`2020-01-01 12:34:56.789` `[main]` `ERROR` `class.example` - `Error message goes here`
"""

LVL_TIME_SRC_MOD_MSG = Transformer(
    rf"{LEVEL_RE} {TIME_RE} {SOURCE_RE} {MODULE_RE} {DIVIDER_RE} {MSG_RE}",
)
"""
Transforms a `Log4j` log item with the following order:

`ERROR` `2020-01-01 12:34:56.789` `[main]` `class.example` - `Error message goes here`
"""

TIME_LVL_SRC_MOD_MSG = Transformer(
    rf"{TIME_RE} {LEVEL_RE} {SOURCE_RE} {MODULE_RE} {DIVIDER_RE} {MSG_RE}",
)
"""
Transforms a `Log4j` log item with the following order:

`2020-01-01 12:34:56.789` `ERROR` `[main]` `class.example` - `Error message goes here`
"""

LVL_SRC_MOD_MSG = Transformer(
    rf"{LEVEL_RE} {SOURCE_RE} {MODULE_RE} {DIVIDER_RE} {MSG_RE}",
)
"""
Transforms a `Log4j` log item with the following order:

`ERROR` `[main]` `class.example` - `Error message goes here`
"""

LVL_MSG = Transformer(
    rf"{LEVEL_RE} {DIVIDER_RE} {MSG_RE}",
)
"""
Transforms a `Log4j` log item with the following order:

`ERROR` - `Error message goes here`
"""

