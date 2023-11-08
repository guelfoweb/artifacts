import json

def load_json(file):
	f = open(file)
	return json.load(f)

def write_json(data, file):
	with open(file, 'w') as outfile:
		json.dump(data, outfile)