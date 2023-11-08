def url(md5):
	sandboxes_url = [
		"https://tria.ge/s?q=",
		"https://www.joesandbox.com/search?q=",
		"https://www.virustotal.com/gui/search/",
		"https://bazaar.abuse.ch/browse.php?search=md5:"
		]
	sandboxes = [sandbox+md5 for sandbox in sandboxes_url]
	return sandboxes