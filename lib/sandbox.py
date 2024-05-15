def url(sha256):
	sandboxes_url = [
		"https://tria.ge/s?q=",
		"https://www.joesandbox.com/analysis/search?q=",
		"https://www.virustotal.com/gui/search/",
		"https://bazaar.abuse.ch/browse.php?search=sha256:",
		"https://koodous.com/apks/"
		]
	sandboxes = [sandbox+sha256 for sandbox in sandboxes_url]
	return sandboxes