import config
from preprocessing.texts import texts
from preprocessing.articles import articles
from preprocessing.emails import emails
from tools import database


def preprocessing():

    database.connect(config.database)
    print(database.execute("select datetime(`birthdate`) as dates from file_employeerecords"))
    database.disconnect()

    texts()
    articles()
    emails()
