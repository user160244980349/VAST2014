from pprint import pprint

from tools import database
from tools.text import remove_newlines, lemmatize, remove_spaces


def emails():

    database.execute("PRAGMA foreign_keys = OFF;")
    database.execute("DROP TABLE IF EXISTS `emailheaders_info`")
    database.execute("PRAGMA foreign_keys = ON;")

    query = "CREATE TABLE emailheaders_info (" \
            "`id` integer PRIMARY KEY AUTOINCREMENT, " \
            "`email_id` integer, " \
            "`lemmatized_subject` text, " \
            "FOREIGN KEY (`email_id`) REFERENCES `file_emailheaders`(`id`))"
    database.execute(query)

    query = "SELECT `id`, `subject` " \
            "FROM `file_emailheaders`"
    records = database.execute(query)

    rows = []
    for record in records:
        email_id = record[0]
        email_subject = record[1]

        subject = remove_spaces(remove_newlines(email_subject.lower()))

        rows.append('(' + ','.join([
            "%d" % email_id,
            "'%s'" % lemmatize(subject)]) + ')')

    query = "INSERT INTO emailheaders_info (`email_id`, `lemmatized_subject`) VALUES {}".format(
        ','.join(rows))
    database.execute(query)


def emails_graph():

    database.execute("PRAGMA foreign_keys = OFF;")
    database.execute("DROP TABLE IF EXISTS `email_addresses`")
    database.execute("PRAGMA foreign_keys = ON;")

    query = "CREATE TABLE email_addresses (" \
            "`id` integer PRIMARY KEY AUTOINCREMENT, " \
            "`address` text)"
    database.execute(query)

    query = "SELECT DISTINCT `from` FROM `file_emailheaders`"
    addresses = database.execute(query)

    rows = []
    for address in addresses:
        rows.append("(" + "'%s'" % address[0] + ")")

    query = "INSERT INTO `email_addresses` (address) VALUES {}".format(','.join(rows))
    database.execute(query)

    database.execute("PRAGMA foreign_keys = OFF;")
    database.execute("DROP TABLE IF EXISTS `emails_references`")
    database.execute("PRAGMA foreign_keys = ON;")

    query = "CREATE TABLE emails_references (" \
            "`id` integer PRIMARY KEY AUTOINCREMENT, " \
            "`email_id` integer, " \
            "`from` integer, " \
            "`to` integer, " \
            "FOREIGN KEY (`email_id`) REFERENCES `file_emailheaders`(`id`)," \
            "FOREIGN KEY (`from`) REFERENCES `email_addresses`(`id`)," \
            "FOREIGN KEY (`to`) REFERENCES `email_addresses`(`id`))"
    database.execute(query)

    query = "SELECT `from`, `to`, `id` FROM `file_emailheaders`"
    email_items = database.execute(query)

    rows = []
    for email_item in email_items:
        addresses = str.split(email_item[1], ", ")
        for address in addresses:
            rows.append("(" + "(SELECT `id` FROM `email_addresses` WHERE `address` = '%s')" % email_item[0] + "," +
                        "(SELECT `id` FROM `email_addresses` WHERE `address` = '%s')" % address + "," +
                        "%d" % email_item[2] + ")")

    query = "INSERT INTO `emails_references` (`from`, `to`, `email_id`) VALUES {}".format(','.join(rows))
    database.execute(query)
