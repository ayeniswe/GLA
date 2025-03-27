"""
The `testcase` module provides classes and methods to define and manage search 
criteria for log entries. It allows users to search for specific entries in logs, 
count their occurrences, and check for the absence of entries based on user-defined 
criteria. The `TestCase` class, which inherits from `Criteria`, provides functionality 
for handling both sequential and non-sequential log entry searches.

The module includes the following features:

1. `find_entries`: Adds log entries (either as a single entry or a list of entries) 
   to the search criteria. It supports both sequential and non-sequential entry searches.
   
2. `find_entries_count`: Allows users to add entries to the search criteria with a 
   specific count, checking if the log entries appear a certain number of times. 
   It also supports sequential and non-sequential searches.

3. `find_entries_absent`: Adds log entries to the search criteria and checks 
   if they are absent from the logs (i.e., if the entry does not appear in the logs).


## Example Usage:

```python
test_case = TestCase(name="demo_test")
test_case.find_entries(["error", "critical"], seq=False)
test_case.find_entries_count([("warning", 2)], seq=True)
test_case.find_entries_absent("info")
```
"""