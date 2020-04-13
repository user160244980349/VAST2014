from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDesktopWidget

from ui.TabWidget import TabWidget


class Window(QtWidgets.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.setWindowTitle("VAST2014MC1")
        self.left = 0
        self.top = 0
        self.right = 800
        self.bot = 600
        self.setGeometry(self.left, self.top, self.right, self.bot)
        self.center()

        self.tab_widget = TabWidget(self)
        self.setCentralWidget(self.tab_widget)

    def center(self):
        qt_rectangle = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())
