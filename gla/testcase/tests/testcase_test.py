from gla.testcase.testcase import TestCase


def test_find_entries_single():
    c = TestCase()
    c.find_entries("entry1")
    assert "entry1" in c.entries
    assert c.entries["entry1"] is 1


def test_find_entries_multiple():
    c = TestCase()
    c.find_entries(["entry1", "entry2", "entry3"])
    assert "entry1" in c.entries
    assert "entry2" in c.entries
    assert "entry3" in c.entries
    assert c.entries["entry1"] is 1
    assert c.entries["entry2"] is 1
    assert c.entries["entry3"] is 1


def test_find_entries_count():
    c = TestCase()
    c.find_entries_count(("entry1", 3))
    c.find_entries_count([("entry2", 1)])
    assert "entry1" in c.entries
    assert c.entries["entry1"] == 3
    assert "entry2" in c.entries
    assert c.entries["entry2"] == 1


def test_find_entries_absent():
    c = TestCase()
    c.find_entries_absent("entry1")
    c.find_entries_absent(["entry2"])
    assert "entry1" in c.entries
    assert c.entries["entry1"] == 0
    assert "entry2" in c.entries
    assert c.entries["entry2"] == 0
