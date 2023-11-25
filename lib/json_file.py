import os
import json

def load_json(file):
	f = open("data" + os.sep + file)
	return json.load(f)

def write_json(data, file):
	with open("data" + os.sep +file, 'w') as outfile:
		json.dump(data, outfile)