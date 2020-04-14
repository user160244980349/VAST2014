from PyQt5.QtWidgets import QWidget, QMessageBox


class Question(QWidget):

    def __init__(self, question):
        super().__init__()
        self.question = question

    def ask(self):
        answer = False
        if QMessageBox.question(self,
                                'Message',
                                self.question,
                                QMessageBox.Yes | QMessageBox.No,
                                QMessageBox.No) == QMessageBox.Yes:
            answer = True
        return answer
