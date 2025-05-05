import logging
from gla.analyzer.analyzer import Analyzer
from gla.testcase.testcase import TestCase
from termcolor import colored

logging.config.fileConfig("logging.conf")

def compare_findings_and_entries(findings, entries, seq):
    mode = "sequence" if seq else "normal"
    print(colored(f"Comparing findings and entries (Mode: {mode.capitalize()})", "blue", attrs=["bold"]))
    print(colored("-" * 50, "blue"))
    
    # For each entry, check if it exists in findings
    for key, node in entries:
        entry = node.val
        if key in findings:
            finding = findings[key].val
            # Should have been missing
            if entry.cnt == 0:          
                print(colored(f"❌ '{entry.text}' was found, but it should not have been.", "red")) 
            # Should have been found the exact number of times
            else:
                print(colored(f"❌ Expected to find '{entry.text}' {entry.cnt} time(s), but it was found {entry.cnt - finding.cnt} time(s)", "red"))
        # Should have been found the correct times or 0 if it was suppose to be missing
        else:
            print(colored(f"✅ Found '{entry.text}' {entry.cnt} time(s) in findings.", "green"))

    print("-" * 50)


t = TestCase()
t.find_entries("TAPCore Process Starting")
res = Analyzer(t, "TAPCore.log")._run()

compare_findings_and_entries(res[0], res[1], t.seq)