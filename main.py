from PyQt5 import QtWidgets

from ui.Question import Question
from ui.Window import Window
from preprocessing.preprocessing import preprocessing
from initialization.initialization import initialization
import sys


def main():

    app = QtWidgets.QApplication([])
    window = Window()

    if Question("Is init needed?").ask():
        initialization()
        pass

    if Question("Is preprocessing needed?").ask():
        preprocessing()
        pass

    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
