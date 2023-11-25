from . import match_regex
import base64
import re

def get(folder):
	regex = {
		#"encrypt": "RC4|AES|DES|DESX|3DES|RSA|DSA|ECDSA|IDEA|Blowfish|Twofish|ElGamal|Diffie-Hellman",
		"base64": "([A-Za-z0-9+/]{6,}={1,2}|[A-Za-z0-9+/]{6,})",
		"telegram_id": "[^0-9](100[0-9]{10})[^0-9]",
		"known": "hakon|standby|LoaderGGPlay|AmexTroll|have been Encrypted|killbot|main_wang|vnc_open|keylog_active|sentSMS",
		}

	exclude = []

	result = {}
	for item in regex.keys():
		string_list = match_regex.inFolder(folder, regex[item], exclude)

		if item == "base64":
			valid_base64 = []
			exclude = ["endsWith"] # known false positives
			for string in string_list:
				# is odd
				if not (len(string) % 2) == 0:
					continue

				# ok, it is even!
				
				# validate base64: UPPER, lower
				if string not in exclude \
					and any(char.isupper() for char in string) \
					and any(char.islower() for char in string):
					
					try:
						message = base64.b64decode(string).decode('ascii')
						# checks if decoded base64 sting matches the regex
						if None in [re.match("[A-Za-z0-9}{)(-+/.=]", i) for i in message]:
							continue
					except:
						continue

					valid_base64.append((string, message))
			string_list = valid_base64
		
		result.update({item: string_list})

	return result
