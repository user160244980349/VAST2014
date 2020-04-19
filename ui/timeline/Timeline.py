from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton


class Timeline(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.layout = QVBoxLayout(self)
        self.pushButton1 = QPushButton("Яна, это твой виджет")
        self.layout.addWidget(self.pushButton1)
        self.setLayout(self.layout)
