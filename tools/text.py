import re

import nltk
from dateutil.parser import parse
from nltk import word_tokenize, WordNetLemmatizer
from nltk.corpus import stopwords


def remove_quotes(string):
    return re.sub(r'[\'\"]', ' ', string)


def remove_newlines(string):
    return re.sub(r'\n+', ' ', string)


def remove_spaces(string):
    return re.sub(r'\s{2,}', ' ', string)


def remove_specchars(string):
    return re.sub(r'[!@#$.,;&?`]', ' ', string)


def normalize_date(value):
    if is_date(value):
        return parse(value).strftime('%d-%m-%Y %H:%M:%S')
    else:
        return value


def is_date(string, fuzzy=False):
    try:
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False


def nltk_setup():
    nltk.download('punkt')
    nltk.download('wordnet')
    nltk.download('stopwords')


def lemmatize(content):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(content)
    filtered_words = [w for w in word_tokens if w not in stop_words]
    lemmatizer = WordNetLemmatizer()
    content = ' '.join([lemmatizer.lemmatize(w) for w in filtered_words])

    return content.lower()
