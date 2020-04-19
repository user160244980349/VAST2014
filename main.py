import sys

from PyQt5 import QtWidgets

import config
from initialization.initialization import initialization
from preprocessing.preprocessing import preprocessing
from tools import database, fsys
from ui.Window import Window


def main():

    app = QtWidgets.QApplication([])
    window = Window()

    database.connect(config.database)

    if not fsys.islocked(config.resources + "/.initialization.lock"):
        initialization()
        fsys.lock(config.resources + "/.initialization.lock")

    if not fsys.islocked(config.resources + "/.preprocessing.lock"):
        preprocessing()
        fsys.lock(config.resources + "/.preprocessing.lock")

    window.show()

    sys.exit(app_exit(app))


def app_exit(app):
    app.exec()
    database.disconnect()


if __name__ == '__main__':
    main()
