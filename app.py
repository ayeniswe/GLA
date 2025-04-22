from gla.analyzer.analyzer import Analyzer
from gla.plugins.transformer.custom_transformer import CustomTransformer
from gla.testcase.testcase import TestCase

c = CustomTransformer(["ign", "time", "time", "lvl", "msg"])
t = TestCase(seq=False)
t.find_entries("Deploying SSL certificates")
t.find_entries("a4 done")
t.find_entries("a10 done")
Analyzer(t, "workspace.log", custom_transformer=c).run()
