import base64
import re
from . import match_regex

def get(folder):
    regex = {
        "base64": r"([A-Za-z0-9+/]{6,}={1,2}|[A-Za-z0-9+/]{6,})",
        "telegram_id": r"[^0-9](100[0-9]{10})[^0-9]",
        "known": r"strapp_url|hakon|standby|LoaderGGPlay|AmexTroll|have been Encrypted|killbot|main_wang|vnc_open|keylog_active|sentSMS|jsdkfh|ping"
    }

    exclude = ["endsWith", "Visually"]  # known false positives
    result = {}

    # Compile regex patterns for efficiency
    compiled_regex = {key: re.compile(pattern) for key, pattern in regex.items()}

    # Process each regex category
    for category, pattern in compiled_regex.items():
        string_list = match_regex.inFolder(folder, pattern.pattern, exclude)

        if category == "base64":
            valid_base64 = []

            # Process base64 strings
            for string in string_list:
                # Skip strings with odd length
                if len(string) % 2 != 0:
                    continue

                # Validate base64 format
                if string not in exclude and any(char.isupper() for char in string) and any(char.islower() for char in string):
                    try:
                        decoded_message = base64.b64decode(string).decode('ascii')
                        # Check if decoded message matches allowed characters
                        if all(re.match(r"[A-Za-z0-9}{)(-+/.=]", char) for char in decoded_message):
                            valid_base64.append((string, decoded_message))
                    except (base64.binascii.Error, UnicodeDecodeError):
                        # Skip invalid base64 strings
                        continue

            string_list = valid_base64
        
        result[category] = string_list

    return result
