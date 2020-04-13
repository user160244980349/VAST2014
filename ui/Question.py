from PyQt5.QtWidgets import QWidget, QMessageBox


class Question(QWidget):

    def __init__(self, question):
        super().__init__()
        self.question = question
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 200

    def ask(self):
        answer = False
        if QMessageBox.question(self,
                                'Message',
                                self.question,
                                QMessageBox.Yes | QMessageBox.No,
                                QMessageBox.No) == QMessageBox.Yes:
            answer = True
        return answer
