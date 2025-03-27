
from gla.models.criteria import Criteria

def test_find_entries_no_seq_single():
    c = Criteria()
    c.find_entries("entry1")
    assert "entry1" in c.entries_no_seq
    assert c.entries_no_seq["entry1"] is False

def test_find_entries_no_seq_multiple():
    c = Criteria()
    c.find_entries(["entry1", "entry2", "entry3"])
    assert "entry1" in c.entries_no_seq
    assert "entry2" in c.entries_no_seq
    assert "entry3" in c.entries_no_seq
    assert c.entries_no_seq["entry1"] is False
    assert c.entries_no_seq["entry2"] is False
    assert c.entries_no_seq["entry3"] is False

def test_find_entries_seq_single():
    c = Criteria()
    c.find_entries("entry1", seq=True)
    assert "entry1" in c.entries
    assert c.entries["entry1"] is False

def test_find_entries_seq_multiple():
    c = Criteria()
    c.find_entries(["entry1", "entry2", "entry3"], seq=True)
    assert "entry1" in c.entries
    assert "entry2" in c.entries
    assert "entry3" in c.entries
    assert c.entries["entry1"] is False
    assert c.entries["entry2"] is False
    assert c.entries["entry3"] is False

def test_find_entries_count_no_seq():
    c = Criteria()
    c.find_entries_count([("entry1",3)])
    c.find_entries_count(("entry2",1))
    assert "entry1" in c.entries_counter_no_seq
    assert c.entries_counter_no_seq["entry1"] == 3
    assert "entry2" in c.entries_counter_no_seq
    assert c.entries_counter_no_seq["entry2"] == 1

def test_find_entries_count_seq():
    c = Criteria()
    c.find_entries_count(("entry1", 3), seq=True)
    c.find_entries_count([("entry2", 1)], seq=True)
    assert "entry1" in c.entries_counter
    assert c.entries_counter["entry1"] == 3
    assert "entry2" in c.entries_counter
    assert c.entries_counter["entry2"] == 1

def test_find_entries_absent():
    c = Criteria()
    c.find_entries_absent("entry1")
    c.find_entries_absent(["entry2"])
    assert "entry1" in c.entries_counter_no_seq
    assert c.entries_counter_no_seq["entry1"] == 0
    assert "entry2" in c.entries_counter_no_seq
    assert c.entries_counter_no_seq["entry2"] == 0