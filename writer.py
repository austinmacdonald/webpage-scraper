import json
from amex import amex_dict
from chase import chase_dict
from wellsfargo import wells_fargo_dict

json_dict = [
    amex_dict,
    chase_dict,
    wells_fargo_dict,
]

with open("output.json", "w") as output:
    json.dump(json_dict, output, indent=2)
