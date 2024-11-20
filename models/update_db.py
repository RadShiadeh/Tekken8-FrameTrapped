import json

data = {}
with open("../data/replays.json", 'r') as f:
    data = json.load(f)

my_data = []
for d in data:
    if d.get("p1_name", "").lower() == "glonki" or d.get("p2_name", "").lower() == "glonki":
        my_data.append(d)
    
with open("../data/Rad_replays.json", "w") as f:
    f.write(json.dumps(my_data, indent=4))