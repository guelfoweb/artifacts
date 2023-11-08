import os
from . import json_file

def get(result):
	# https://gist.github.com/Watsonboy1989/fa01a6869d82062c770e137107693744
	permission_categories = json_file.load_json("permission_categories.json")
	# https://developer.android.com/reference/android/Manifest.permission
	permission_description = json_file.load_json("permission_description.json")
	
	categories = {}
	not_category = []

	if not "permission" in result["activity"]:
		print ("permission not found")
		return categories

	permission_list = [item.split('.')[-1] for item in result["activity"]["permission"]]
	for k in permission_list:
		for key in permission_categories.keys():
			if k in permission_categories[key]:
				desc = ""
				if k in permission_description:
					desc = permission_description[k]
				
				if key not in categories.keys():
					categories.update({key: [(k, desc)]})
				else:
					categories[key].append((k, desc))
			else:
				not_category.append(k)

	return categories
