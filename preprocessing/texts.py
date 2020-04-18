import re
import nltk
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

import config
from tools import database


def texts():
    nltk.download('punkt')
    nltk.download('wordnet')
    nltk.download('stopwords')

    database.connect(config.database)

    query = "DROP TABLE IF EXISTS files_preprocessed_content"
    database.execute(query)

    query = "CREATE TABLE files_preprocessed_content (" \
            "`id` integer PRIMARY KEY AUTOINCREMENT, " \
            "`file_id` integer, " \
            "`content` text, " \
            "FOREIGN KEY (`file_id`) REFERENCES all_files(`id`))"
    database.execute(query)

    query = "SELECT `id`, `content` FROM all_files"
    records = database.execute(query)

    rows = []
    for record in records:
        rows.append('(' + ','.join(["'%s'" % record[0], "'%s'" % do_preprocess(record[1])]) + ')')

    query = "INSERT INTO files_preprocessed_content (`file_id`, `content`) VALUES {}".format(
        ','.join(rows))
    database.execute(query)

    database.disconnect()


def do_preprocess(content):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(content)
    filtered_words = [w for w in word_tokens if w not in stop_words]
    lemmatizer = WordNetLemmatizer()
    content = ' '.join([lemmatizer.lemmatize(w) for w in filtered_words])
    content = re.sub(r"[!@#$.,;&?`\'\"]", ' ', content)
    return trimm(content.lower())


def trimm(content):
    while '  ' in content:
        content = content.replace('  ', ' ')
    return content
