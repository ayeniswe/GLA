from gla.testcase.testcase import TestCase

def test_find_entries_single():
    # ARRANGE
    c = TestCase()
    
    # ACT
    c.find_entries("entry1")
    
    # ASSERT
    assert c.entries["entry1"].val.cnt == 1


def test_find_entries_multiple():
    # ARRANGE
    c = TestCase()
    
    # ACT
    c.find_entries(["entry1", "entry2", "entry3"])
    
    # ASSERT
    assert c.entries["entry1"].val.cnt == 1
    assert c.entries["entry2"].val.cnt == 1
    assert c.entries["entry3"].val.cnt == 1


def test_find_entries_count():
    # ARRANGE
    c = TestCase()
    
    # ACT
    c.find_entries_count(("entry1", 3))
    c.find_entries_count([("entry2", 1)])
    
    # ASSERT
    assert c.entries["entry1"].val.cnt == 3
    assert c.entries["entry2"].val.cnt == 1


def test_find_entries_absent():
    # ARRANGE
    c = TestCase()
    
    # ACT
    c.find_entries_absent("entry1")
    c.find_entries_absent(["entry2"])
    
    # ASSERT
    assert c.entries["entry1"].val.cnt == 0
    assert c.entries["entry2"].val.cnt == 0

def test_find_entries_add_total_entries_always():
    # ARRANGE
    c = TestCase()
    
    # ACT
    c.find_entries("entry1")
    c.find_entries(["entry1", "entry2"])
    c.find_entries(["entry1", "entry2"])
    c.find_entries("entry1")
    
    # ASSERT
    assert c.entries["entry1"].val.cnt == 4
    assert c.entries["entry2"].val.cnt == 2
