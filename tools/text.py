import re


def remove_quotes(string):
    return re.sub(r'[\'\"]', '', string)
