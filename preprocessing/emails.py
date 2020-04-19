from pprint import pprint

from tools import database
from tools.text import remove_newlines, lemmatize, remove_spaces


def emails():

    database.execute("PRAGMA foreign_keys = OFF;")
    database.execute("DROP TABLE IF EXISTS `emailheaders_info`")
    database.execute("PRAGMA foreign_keys = ON;")

    query = "CREATE TABLE emailheaders_info (" \
            "`id` integer PRIMARY KEY AUTOINCREMENT, " \
            "`emailheader_id` integer, " \
            "`preprocessed_subject` text, " \
            "FOREIGN KEY (`emailheader_id`) REFERENCES `file_emailheaders`(`id`))"
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

    query = "INSERT INTO emailheaders_info (`emailheader_id`, `preprocessed_subject`) VALUES {}".format(
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
    database.execute("DROP TABLE IF EXISTS `email_references`")
    database.execute("PRAGMA foreign_keys = ON;")

    query = "CREATE TABLE email_references (" \
            "`id` integer PRIMARY KEY AUTOINCREMENT, " \
            "`emailheader_id` integer, " \
            "`from_id` integer, " \
            "`to_id` integer, " \
            "FOREIGN KEY (`emailheader_id`) REFERENCES `file_emailheaders`(`id`)," \
            "FOREIGN KEY (`from_id`) REFERENCES `email_addresses`(`id`)," \
            "FOREIGN KEY (`to_id`) REFERENCES `email_addresses`(`id`))"
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

    query = "INSERT INTO `email_references` (`from_id`, `to_id`, `emailheader_id`) VALUES {}".format(','.join(rows))
    database.execute(query)
