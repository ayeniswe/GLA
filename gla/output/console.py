from termcolor import colored
from gla.utilities.list import LinkedOrderedDict

def show(findings: LinkedOrderedDict, entries: LinkedOrderedDict, seq: bool):
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