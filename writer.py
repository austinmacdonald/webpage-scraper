import json
from amex import amex_dict
from chase import chase_dict
from wellsfargo import wells_fargo_dict

with open("output/amex.json", "w") as output:
	json.dump(amex_dict, output, indent = 2)

with open("output/chase.json", "w") as output:
	json.dump(chase_dict, output, indent = 2)

with open("output/wells_fargo.json", "w") as output:
	json.dump(wells_fargo_dict, output, indent = 2)