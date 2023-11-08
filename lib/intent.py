from . import match_regex

def info(folder):
	# https://developer.android.com/guide/components/intents-filters
	regex = {
		"intent": "[A-Za-z]*\.intent\.[A-Za-z]*\.[A-Za-z0-9.]*",
		"intent_extra": "[^\.](intent\.[A-Za-z]*\.[A-Za-z0-9.]*)",
		}

	exclude = []

	result = {}
	for item in regex.keys():
		result.update({item: match_regex.inFolder(folder, regex[item], exclude)})

	result["intent"] = sorted(result["intent"]) + sorted(result["intent_extra"])
	del result["intent_extra"]

	return result


