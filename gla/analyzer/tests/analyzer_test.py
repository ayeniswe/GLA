import os
from gla.analyzer.analyzer import Analyzer
from gla.plugins.transformer.custom_transformer import CustomTransformer
from gla.testcase.testcase import TestCase

def test_item_does_not_show_until_entries_after_are_found(get_log_path):
    # Verify a item does not show until entries after are found
    c = CustomTransformer(["ign", "time", "time", "lvl", "msg"])
    t = TestCase(seq=True)
    t.find_entries("Adding trusted root certificate authority")
    t.find_entries("Deploying SSL certificates")

    res = Analyzer(t, get_log_path("workspace.log"), custom_transformer=c)._run()

    assert len(res[0]) == 0


def test_item_does_show_after_entries_are_found(get_log_path):
    # Verify a item does not show until entries after are found - failed
    c = CustomTransformer(["ign", "time", "time", "lvl", "msg"])
    t = TestCase(seq=True)
    t.find_entries("Deploying SSL certificates")
    t.find_entries("Adding trusted root certificate authority")

    res = Analyzer(t, get_log_path("workspace.log"), custom_transformer=c)._run()

    assert "Deploying SSL certificates" in res[0]
    assert "Adding trusted root certificate authority" not in res[0]


def test_no_entries_exist_fail(get_log_path):
    # Verify none of the entries exist
    c = CustomTransformer(["ign", "time", "time", "lvl", "msg"])
    t = TestCase(seq=False)
    t.find_entries_absent("Deploying SSL certificates")
    t.find_entries_absent("machine-super")

    res = Analyzer(t, get_log_path("workspace.log"), custom_transformer=c)._run()

    assert "Deploying SSL certificates" in res[0]
    assert "machine-super" in res[0]


def test_entries_found_ignore_order(get_log_path):
    # Verify the entries are found regardless of order
    c = CustomTransformer(["ign", "time", "time", "lvl", "msg"])
    t = TestCase(seq=False)
    t.find_entries("Deploying SSL certificates")
    t.find_entries("machine4 Done")
    t.find_entries("machine10 Done")

    res = Analyzer(t, get_log_path("workspace.log"), custom_transformer=c)._run()

    assert len(res[0]) == 0


def test_entries_found_exact_count(get_log_path):
    # Verify the total count of entries are found
    c = CustomTransformer(["ign", "time", "time", "lvl", "msg"])
    t = TestCase(seq=False)
    t.find_entries_count(("machine10 Done", 2))

    res = Analyzer(t, get_log_path("workspace.log"), custom_transformer=c)._run()

    assert len(res[0]) == 0


def test_entries_found_in_order(get_log_path):
    # Verify the entries are found in order
    c = CustomTransformer(["ign", "time", "time", "lvl", "msg"])
    t = TestCase(seq=True)
    t.find_entries("machine10 Done")
    t.find_entries("machine4 Done")
    t.find_entries("Deploying SSL certificates")

    res = Analyzer(t, get_log_path("workspace.log"), custom_transformer=c)._run()

    assert len(res[0]) == 0
