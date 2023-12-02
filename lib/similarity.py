import json
from . import json_file
from prettytable import PrettyTable

def jaccard_similarity(set1, set2):
	# intersection of two sets
	intersection = len(set1.intersection(set2))
	# Unions of two sets
	union = len(set1.union(set2))
	
	return intersection / union

def dataset(lista):
	# return set of data
	return set([p.split('.')[-1] for p in lista])

def get(set_a, all_families):
	# reference list
	p = dataset(set_a["permission"])
	a = dataset(set_a["application"])
	i = dataset(set_a["intent"])

	# load json database
	json_data = json_file.load_json("patterns.json")

	stats  = {}
	values = {}

	for family in json_data.keys():
		# database json_data
		p1 = dataset(json_data[family]["permission"])
		a1 = dataset(json_data[family]["application"])
		i1 = dataset(json_data[family]["intent"])

		# jaccard similarity of two sets
		permission  = jaccard_similarity(p, p1) * 100
		application = jaccard_similarity(a, a1) * 100
		intent      = jaccard_similarity(i, i1) * 100

		# collect all values
		values.update({family: {"permission": round(permission, 2), "application": round(application, 2), "intent": round(intent, 2)}})

		similarity = permission + application + intent
		similarity = round(similarity/3, 2)
		
		stats.update({family: similarity})

	# sort stats keys
	stats = sorted(stats.items(), key=lambda x:x[1], reverse=True)
	
	if all_families:
		headers = ['family', 'permission', 'application', 'intent', 'total']
		myTable = PrettyTable(headers)
		for item in stats:
			family = item[0]
			total = item[1]
			permission = values[family]['permission']
			application = values[family]['application']
			intent = values[family]['intent']
			myTable.add_row([family, permission, application, intent, total])
		return myTable
	
	family_name  = list(stats)[0][0]
	family_match = list(stats)[0][1]

	match = {"name": family_name, "match": family_match, "value": values[family_name]}

	return match
