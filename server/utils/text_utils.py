import re

def is_hebrew(text):
    return bool(re.search(r'[\u0590-\u05FF]', text))
