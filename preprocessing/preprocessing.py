from preprocessing.articles import articles
from preprocessing.emails import emails, emails_graph
from preprocessing.texts import texts
from tools.text import nltk_setup


def preprocessing():
    nltk_setup()

    texts()
    articles()
    emails()
    emails_graph()
