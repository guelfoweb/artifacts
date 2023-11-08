import json
from . import json_file

def _similarity_decrease(db, patterns, matches, influence):
	#print (len(db), len(patterns), len(matches))
	if len(db) == 0 and len(patterns) == 0:
		similarity = 100

	elif len(db) == 0 and len(patterns) > 0:
			similarity = 100 - len(patterns) * 10
			if len(patterns) > 5:
				similarity = 0
	
	elif len(db) > 0 and len(patterns) == 0:
			similarity = 100 - len(db) * 10
			if len(db) > 5:
				similarity = 0
	else:
		delta = abs(len(db) - len(patterns))
		if influence:
			delta = 0
		similarity = (len(matches) / len(patterns) * 100) - delta

	return similarity

def get(patterns):
	db_file = "patterns.json"
	db_json = json_file.load_json(db_file)
	
	# permission
	pattern_perm = [p.split('.')[-1] for p in patterns["permission"]]
	# application
	pattern_app = [p.split('.')[-1] for p in patterns["application"]]
	# intent
	pattern_int = [p.split('.')[-1] for p in patterns["intent"]]

	result = {}

	for family in db_json.keys():

		influence = False

		for key in db_json[family]:
			db = [d.split('.')[-1] for d in db_json[family][key]]
			pattern = [p.split('.')[-1] for p in patterns[key]]
			
			matches = [w for w in pattern if w in db]
			delta = abs(len(db) - len(pattern))
			
			similarity = _similarity_decrease(db, pattern, matches, influence)
			
			if similarity >= 90:
				influence = True

			if family in result.keys():
				result[family].update({key: similarity})
			else:
				result.update({family: {key: similarity}})

	#print (result)

	stats = {}
	value = {}
	for family in result:
		permission  = result[family]["permission"]
		application = result[family]["application"]
		intent      = result[family]["intent"]

		value.update({family: {"permission": round(permission, 2), "application": round(application, 2), "intent": round(intent, 2)}})

		hit = permission + application + intent
		hit = round(hit/3, 2)

		stats.update({family: hit})
		#print (stats)

	# sort keys
	stats = sorted(stats.items(), key=lambda x:x[1], reverse=True)
	# return first key
	# list(stats)[0]
	family_name  = list(stats)[0][0]
	family_match = list(stats)[0][1]
	family = {"name": family_name, "match": family_match, "value": value[family_name]}
	
	return family 

