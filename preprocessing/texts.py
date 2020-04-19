from tools import database
from tools.text import lemmatize, remove_spaces, remove_newlines, remove_specchars


def texts():
    database.execute("PRAGMA foreign_keys = OFF;")
    database.execute("DROP TABLE IF EXISTS `files_preprocessed_content`")
    database.execute("PRAGMA foreign_keys = ON;")

    query = "CREATE TABLE `files_preprocessed_content` (" \
            "`id` integer PRIMARY KEY AUTOINCREMENT, " \
            "`file_id` integer, " \
            "`content` text, " \
            "FOREIGN KEY (`file_id`) REFERENCES `all_files`(`id`))"
    database.execute(query)

    query = "SELECT `id`, `content` FROM `all_files`"
    records = database.execute(query)

    rows = []
    for record in records:
        file_id = record[0]
        file_content = record[1]

        lemmatized_content = lemmatize(
            remove_spaces(
                remove_newlines(
                    remove_specchars(
                        file_content.lower()))))

        rows.append('(' + ','.join(["'%s'" % file_id,
                                    "'%s'" % lemmatized_content]) + ')')

    query = "INSERT INTO `files_preprocessed_content` (`file_id`, `content`) VALUES {}".format(
        ','.join(rows))
    database.execute(query)
