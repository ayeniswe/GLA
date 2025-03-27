from gla.models.criteria import Criteria

c = Criteria()

c.find_entries(["database ❌ Failed"])

with open('workspace.log', 'r') as f:
    line = f.readline()
    while line:
        # evaluate
        
        line = f.readline()
        
