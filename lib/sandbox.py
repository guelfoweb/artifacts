def url(md5):
    sandboxes_url = [
        "https://tria.ge/s?q={md5}",
        "https://www.joesandbox.com/analysis/search?q={md5}",
        "https://www.virustotal.com/gui/search/{md5}",
        "https://bazaar.abuse.ch/browse.php?search=md5:{md5}",
        "https://koodous.com/apks?search={md5}",
        "https://mobsf.live/static_analyzer/{md5}/"
    ]
	
    sandboxes = [sandbox.format(md5=md5) for sandbox in sandboxes_url]
    
    return sandboxes
