from gla.analyzer.analyzer import Analyzer
from gla.plugins.transformer.custom_transformer import CustomTransformer
from gla.testcase.testcase import TestCase
from termcolor import colored



def compare_findings_and_entries(findings, entries):
    print(colored("Comparing Findings and Entries:", "blue", attrs=["bold"]))
    print(colored("-" * 50, "blue"))

    # For each entry, check if it exists in findings
    for key, node in entries._list.items():
        entry = node.val
        if key in findings._list:
            finding = findings._list[key].val
            if entry.cnt == 0:
                print(colored(f"❌ '{entry.text}' was found, but it should not have been.", "red"))
            else:
                # Here we compare the expected vs actual count of findings
                diff = finding.cnt - entry.cnt
                if diff == 0:
                    print(colored(f"✅ '{entry.text}' was found the correct number of times: {entry.cnt}.", "green"))
                else:
                    print(colored(f"⚠️ Expected to find '{entry.text}' {entry.cnt} time(s), but found {finding.cnt} time(s) ({'+' if diff > 0 else ''}{diff}).", "yellow"))
        else:
            # If the entry isn't found in findings at all
            print(colored(f"✅ '{entry.text}' was not found in findings as expected (cnt=0).", "green"))

    print(colored("-" * 50, "blue"))

c = CustomTransformer(["ign", "time", "time", "lvl", "msg"])
t = TestCase(seq=True)
t.find_entries("Adding trusted root certificate authority")
t.find_entries("Deploying SSL certificates")
res = Analyzer(t, "workspace.log", custom_transformer=c)._run()
print(res[0]._list)
print(res[1]._list)
compare_findings_and_entries(res[0], res[1])