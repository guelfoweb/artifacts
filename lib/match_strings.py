from . import match_regex
import base64

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
		# validate base64: UPPER, lower, num3r1c
		if item == "base64":
			valid_base64 = []
			for string in string_list:
				# is odd
				if not (len(string) % 2) == 0:
					continue
				# ok, it is even!
				if any(char.isupper() for char in string) and any(char.islower() for char in string) and any(char.isnumeric() for char in string):
					try:
						base64_bytes  = string.encode('ascii')
						message_bytes = base64.b64decode(base64_bytes)
						message       = message_bytes.decode('ascii')
						#print (message)
					except:
						continue
					valid_base64.append((string, message))
			string_list = valid_base64
		
		result.update({item: string_list})

	return result
