
from gla.analyzer.analyzer import Analyzer
from gla.plugins.transformer.custom_transformer import CustomTransformer
from gla.testcase.testcase import TestCase

import logging
import logging.config

logging.config.fileConfig('logging.conf')

# # Verify a item does not show until entries after are found
# c = CustomTransformer(["ign", "time", "time", "lvl", "msg"])
# t = TestCase(seq=True)
# t.find_entries("Adding trusted root certificate authority")
# t.find_entries("Deploying SSL certificates")
# Analyzer(t, "workspace.log", custom_transformer=c)._run()

# # Verify a item does not show until entries after are found - failed
# c = CustomTransformer(["ign", "time", "time", "lvl", "msg"])
# t = TestCase(seq=True)
# t.find_entries("Deploying SSL certificates")
# t.find_entries("Adding trusted root certificate authority")
# Analyzer(t, "workspace.log", custom_transformer=c)._run()

# # Verify none of the entries exist
# c = CustomTransformer(["ign", "time", "time", "lvl", "msg"])
# t = TestCase(seq=False)
# t.find_entries_absent("Deploying SSL certificates")
# t.find_entries_absent("ge-avsim")
# Analyzer(t, "workspace.log", custom_transformer=c)._run()

# # Verify the entries are found regardless of order
# c = CustomTransformer(["ign", "time", "time", "lvl", "msg"])
# t = TestCase(seq=False)
# t.find_entries("Deploying SSL certificates")
# t.find_entries("a4 Done")
# t.find_entries("a10 Done")
# Analyzer(t, "workspace.log", custom_transformer=c)._run()

# # Verify the total count of entries are found
# c = CustomTransformer(["ign", "time", "time", "lvl", "msg"])
# t = TestCase(seq=False)
# t.find_entries_count(("a10 Done", 2))
# Analyzer(t, "workspace.log", custom_transformer=c)._run()

# # Verify the entries are found in order
# c = CustomTransformer(["ign", "time", "time", "lvl", "msg"])
# t = TestCase(seq=True)
# t.find_entries("Deploying SSL certificates")
# t.find_entries("a10 Done")
# t.find_entries("a4 Done")
# Analyzer(t, "workspace.log", custom_transformer=c)._run()