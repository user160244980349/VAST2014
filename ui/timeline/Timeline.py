from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QWidget, QVBoxLayout

# Fake visualization of articles timeline work

class Timeline(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.layout = QVBoxLayout(self)
        self.view = QWebEngineView(self)
        self.view.setZoomFactor(0.9)
        self.view.setFixedHeight(600)
        self.view.setFixedWidth(1450)
        self.view.load(QUrl("https://web.ics.purdue.edu/~gao338/VASTChallenge2014/POKorganization.htm"))
        self.setLayout(self.layout)
