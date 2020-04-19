from preprocessing.articles import articles
from preprocessing.texts import texts
from tools.text import nltk_setup


def preprocessing():
    nltk_setup()

    texts()
    articles()
    # emails()
