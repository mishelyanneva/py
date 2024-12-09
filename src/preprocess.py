import re

def normalize_description(description):

    description = re.sub(r'PAYPAL \*', '', description, flags=re.IGNORECASE)
    description = re.sub(r'^(WWW\.|HTTP://|HTTPS://)', '', description, flags=re.IGNORECASE)
    description = re.sub(r'[^a-zA-Z0-9\s]', '', description)
    description = re.sub(r'\s+', ' ', description).strip()
    return description.lower()
