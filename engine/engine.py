from plugins.transformer.log4j_transformer import Log4jTransformer


class Engine:
    def __init__(self):
        """Initialize the `GLA` engine"""
        # Setup transformers
        # Log dates resolve in the following order of high concern: year, month, day
        # Example 02-2020-01 or 02-01-2020 both will resolve to 2020-02-01 - year, month, day
        Log4jTransformer(
            [
                # Standard log4j format but different orders
                r"^(?P<time>\d{4}-\d{2}-\d{2})\s+\[(?P<thread>\w+)\]\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<mod>[\w.]+)\s+-\s+(?P<msg>.+)",
                r"^(?P<time>\d{2}-\d{4}-\d{2})\s+\[(?P<thread>\w+)\]\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<mod>[\w.]+)\s+-\s+(?P<msg>.+)",
                r"^(?P<time>\d{2}-\d{2}-\d{4})\s+\[(?P<thread>\w+)\]\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<mod>[\w.]+)\s+-\s+(?P<msg>.+)",
                r"^(?P<time>\d{2}-\d{2}-\d{4})\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+\[(?P<thread>\w+)\]\s+(?P<mod>[\w.]+)\s+-\s+(?P<msg>.+)",
                r"^(?P<time>\d{2}-\d{2}-\d{4})\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<mod>[\w.]+)\s+(?P<msg>.+)\s+\[(?P<thread>\w+)\]",
                r"^(?P<time>\d{2}-\d{2}-\d{4})\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<mod>[\w.]+)\s+\[(?P<thread>\w+)\]\s+-\s+(?P<msg>.+)",
                r"^(?P<time>\d{2}-\d{2}-\d{4})\s+(?P<mod>[\w.]+)\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<msg>.+)\s+\[(?P<thread>\w+)\]",
                r"^(?P<time>\d{2}-\d{2}-\d{4})\s+(?P<mod>[\w.]+)\s+(?P<msg>.+)\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+\[(?P<thread>\w+)\]",
                r"^(?P<time>\d{2}-\d{2}-\d{4})\s+(?P<mod>[\w.]+)\s+(?P<msg>.+)\s+\[(?P<thread>\w+)\]\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)",
                r"^(?P<time>\d{2}-\d{2}-\d{4})\s+(?P<msg>.+)\s+\[(?P<thread>\w+)\]\s+(?P<mod>[\w.]+)\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)",
                r"^(?P<time>\d{2}-\d{2}-\d{4})\s+(?P<msg>.+)\s+\[(?P<thread>\w+)\]\s+(?P<mod>[\w.]+)\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)",
                r"^\[(?P<thread>\w+)\]\s+(?P<time>\d{2}-\d{2}-\d{4})\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<mod>[\w.]+)\s+-\s+(?P<msg>.+)",
                r"^\[(?P<thread>\w+)\]\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<time>\d{2}-\d{2}-\d{4})\s+(?P<mod>[\w.]+)\s+-\s+(?P<msg>.+)",
                r"^\[(?P<thread>\w+)\]\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<mod>[\w.]+)\s+(?P<time>\d{2}-\d{2}-\d{4})\s+-\s+(?P<msg>.+)",
                r"^\[(?P<thread>\w+)\]\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<mod>[\w.]+)\s+(?P<msg>.+)\s+(?P<time>\d{2}-\d{2}-\d{4})",
                r"^(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+\[(?P<thread>\w+)\]\s+(?P<mod>[\w.]+)\s+(?P<msg>.+)\s+(?P<time>\d{2}-\d{2}-\d{4})",
                r"^(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<mod>[\w.]+)\s+\[(?P<thread>\w+)\]\s+(?P<msg>.+)\s+(?P<time>\d{2}-\d{2}-\d{4})",
                r"^(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<mod>[\w.]+)\s+(?P<msg>.+)\s+\[(?P<thread>\w+)\]\s+(?P<time>\d{2}-\d{2}-\d{4})",
                r"^(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<mod>[\w.]+)\s+(?P<msg>.+)\s+(?P<time>\d{2}-\d{2}-\d{4})\s+\[(?P<thread>\w+)\]",
                r"^(?P<mod>[\w.]+)\s+(?P<time>\d{2}-\d{2}-\d{4})\s+(?P<msg>.+)\s+\[(?P<thread>\w+)\]\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)",
                r"^(?P<mod>[\w.]+)\s+(?P<time>\d{2}-\d{2}-\d{4})\s+\[(?P<thread>\w+)\]\s+(?P<msg>.+)\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)",
                r"^(?P<mod>[\w.]+)\s+(?P<time>\d{2}-\d{2}-\d{4})\s+\[(?P<thread>\w+)\]\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+-\s+(?P<msg>.+)",
                r"^(?P<mod>[\w.]+)\s+\[(?P<thread>\w+)\]\s+(?P<time>\d{2}-\d{2}-\d{4})\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+-\s+(?P<msg>.+)",
                r"^(?P<mod>[\w.]+)\s+\[(?P<thread>\w+)\]\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<time>\d{2}-\d{2}-\d{4})\s+-\s+(?P<msg>.+)",
                r"^(?P<mod>[\w.]+)\s+\[(?P<thread>\w+)\]\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<msg>.+)\s+(?P<time>\d{2}-\d{2}-\d{4})",
                r"^(?P<mod>[\w.]+)\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+\[(?P<thread>\w+)\]\s+(?P<msg>.+)\s+(?P<time>\d{2}-\d{2}-\d{4})",
                r"^(?P<mod>[\w.]+)\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<msg>.+)\s+\[(?P<thread>\w+)\]\s+(?P<time>\d{2}-\d{2}-\d{4})",
                r"^(?P<mod>[\w.]+)\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<msg>.+)\s+(?P<time>\d{2}-\d{2}-\d{4})\s+\[(?P<thread>\w+)\]",
                r"^(?P<mod>[\w.]+)\s+(?P<msg>.+)\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+(?P<time>\d{2}-\d{2}-\d{4})\s+\[(?P<thread>\w+)\]",
                r"^(?P<mod>[\w.]+)\s+(?P<msg>.+)\s+(?P<time>\d{2}-\d{2}-\d{4})\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)\s+\[(?P<thread>\w+)\]",
                r"^(?P<mod>[\w.]+)\s+(?P<msg>.+)\s+(?P<time>\d{2}-\d{2}-\d{4})\s+\[(?P<thread>\w+)\]\s+(?P<lvl>ERROR|WARN|INFO|DEBUG|TRACE)",
            ]
        )
