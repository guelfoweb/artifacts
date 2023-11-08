import re
import ipaddress
from . import match_regex

def get(folder):
	regex = {
		"ip": "[^A-Za-z0-9\.]([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})[^A-Za-z0-9\.]",
		"url": "[A-Za-z]+://[a-zA-Z0-9./?=_%:-]*",
		"param": "model=|result=|androidid=|upload=|&upload|action=|&action|bot=|&bot|gate=|&gate|\w+\.php\?",
		#"email": "[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,6}",
		}

	exclude = [".android.com", "apache.org", "publicsuffix.org","mozilla.org","fontawesome.io",
				"googleapis.com","googleadservices.com",".googlesyndication.com",
				".google-analytics.com",".google.com","com.google.","goo.gl",
				"googleads.",".adobe.com",".doubleclick.net",".apache.org","purl.org",
				"gimp.org",".w3.org","schema.org","firebase.com","googletagmanager.com",
				"gstatic.com", "googlesource.com"]

	result = {}
	for item in regex.keys():
		result.update({item: match_regex.inFolder(folder, regex[item], exclude)})

	# check for valid url
	if result["url"]:
		regex_url = "((?!-)[A-Za-z0-9-]" + "{1,63}(?<!-)\\.)" +"+[A-Za-z]{2,6}"
		pattern = re.compile(regex_url)

		urllist = []
		for url in result["url"]:
			if re.search(pattern, url):
				# fix malformed url, like Ahttps://domain.com
				if "http://" in url or "https://" in url:
					if not url.startswith("http"):
						url = url.split("http")[1]
						url = "http{url}".format(url=url)
				urllist.append(url)
		result["url"] = urllist

	# check for valid ip address
	if result["ip"]:
		iplit = []
		for ip in result["ip"]:
			if ip.startswith("0.") or ip.endswith(".0.0"):
				continue
			try:
				ipaddress.ip_address(ip)
				iplit.append(ip)
			except:
				pass
		result["ip"] = iplit

	# remove empty strings from list
	for key in regex.keys():
		result[key] = list(filter(None, result[key]))

	return result