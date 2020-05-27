from random import randint

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QFont, QColor, QPen

from tools import database

sql_create = '''CREATE TABLE `doc_result` (
        `key` text,
        `file_name` text,
        `rate` integer,
        `content` text
        )
'''

sql_select = '''
    SELECT file_name, SUM(rate), content
    FROM
        `doc_result`
    GROUP BY file_name
    ORDER BY SUM(rate) DESC
'''

insert_doc = '''
    INSERT INTO 
        doc_result
    SELECT 
        '{0}', 
        f.name, 
        (LENGTH(p.prerocessed_content)-LENGTH(REPLACE(p.prerocessed_content,'{0}',''))) / {2},
        f.content
    FROM 
        all_files f 
    INNER JOIN 
        files_preprocessed_content p 
    ON 
        f.id=p.file_id
    WHERE 
        p.prerocessed_content like '% {0} %' 
    AND 
        f.name IN {1}
            
'''

sql_select_rate = '''
    SELECT rate FROM doc_result WHERE key='{}' AND file_name ='{}'
    '''

sql_select_content = '''SELECT content FROM doc_result WHERE name={}'''

all_files = []
names = []


class Rate(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setMinimumSize(1, 30)
        self.setMaximumHeight(30)
        self.value = {}
        self.colors = {}
        self.max = 0

    def setValue(self, value):
        self.value = value

    def setMax(self, max):
        self.max = max

    def setColors(self, colors):
        self.colors = colors

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawWidget(qp)
        qp.end()

    def drawWidget(self, qp):
        font = QFont('Serif', 7, QFont.Light)
        qp.setFont(font)

        size = self.size()
        w = size.width()
        h = size.height()

        step = int(round(w / self.max))
        start = 0
        for i in self.value.keys():
            color = self.colors[i].replace('r', '').replace('g', '').replace('b', '').replace('(', '').replace(')',
                                                                                                               '').replace(
                ',', '').split()
            # print(self.value)
            end = start + step * self.value[i]
            qp.setPen(QColor(255, 255, 255))
            qp.setBrush(QColor(int(color[0]), int(color[1]), int(color[2])))
            qp.drawRect(start, 0, start + step * self.value[i], h)
            start = end

        pen = QPen(QColor(20, 20, 20), 1, Qt.SolidLine)

        qp.setPen(pen)
        qp.setBrush(Qt.NoBrush)
        qp.drawRect(0, 0, w - 1, h - 1)


class Docs(QtWidgets.QWidget):

    def __init__(self, parent):
        super(QtWidgets.QWidget, self).__init__(parent)

        global all_files
        global names

        query = "SELECT `name` FROM `all_files`"
        records = database.execute(query)
        for record in records:
            all_files.append(record[0])

        r = database.execute("SELECT address from email_addresses")
        for i in r:
            ii = i[0].split('@')
            ii = (ii[0].lower().split('.'))
            names.append(ii[0])
            names.append(ii[1])

        self.initUI(self)

    def initUI(self, Form):

        ''' Статичная форма '''
        Form.setObjectName("Form")
        Form.resize(761, 492)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea_3 = QtWidgets.QScrollArea(Form)
        self.scrollArea_3.setWidgetResizable(True)
        self.scrollArea_3.setObjectName("scrollArea_3")
        self.scrollAreaWidgetContents_3 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 406, 202))
        self.scrollAreaWidgetContents_3.setObjectName("scrollAreaWidgetContents_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_3)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.groupBox_2 = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_3)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalLayout_4.addWidget(self.groupBox_2)
        self.scrollArea_3.setWidget(self.scrollAreaWidgetContents_3)
        self.gridLayout.addWidget(self.scrollArea_3, 3, 0, 1, 2)
        self.scrollArea = QtWidgets.QScrollArea(Form)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 406, 202))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout.addWidget(self.groupBox)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 2, 0, 1, 2)
        self.scrollArea_2 = QtWidgets.QScrollArea(Form)
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 325, 470))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.groupBox_3 = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_2)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout_6.addWidget(self.groupBox_3, 0, QtCore.Qt.AlignTop)
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.gridLayout.addWidget(self.scrollArea_2, 0, 2, 5, 1)
        self.verticalLayout_3.addLayout(self.gridLayout)

        '''То, что нужно настраивать'''

        self.fileCheck = {}
        self.keyButtons = {}
        self.colors = {}
        self.contentButtons = {}
        self.rate = {}

        for i in all_files:
            check = QtWidgets.QCheckBox(self.groupBox_2)
            check.setChecked(True)
            self.verticalLayout_5.addWidget(check)
            self.fileCheck[i] = check

        # Поле ввода ключевого слова
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setMaximumWidth(200)
        self.gridLayout.addWidget(self.lineEdit, 0, 0, 1, 1)
        # Кнопка найти
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 4, 0, 1, 2)
        # Кнопка добавить
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 0, 1, 1, 1)

        self.combo = QtWidgets.QComboBox(Form)
        self.combo.addItems(names)
        self.gridLayout.addWidget(self.combo, 1, 0, 1, 1)

        self.pushButton_10 = QtWidgets.QPushButton(Form)
        self.pushButton_10.setObjectName("pushButton_10")
        self.gridLayout.addWidget(self.pushButton_10, 1, 1, 1, 1)

        ''' Сигналы '''
        self.pushButton.clicked.connect(self.clickedAdd)
        self.pushButton_10.clicked.connect(self.clickedAdd2)
        self.pushButton_2.clicked.connect(self.clickedFind)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def clickedAdd(self):
        text = self.lineEdit.text()
        if text not in self.keyButtons.keys():
            but = QtWidgets.QPushButton(self.groupBox)
            but.setText(text)
            color = 'rgb({}, {}, {})'.format(randint(0, 255), randint(0, 255), randint(0, 255))
            but.setStyleSheet('''
                background-color: rgb(200,200,200);
                border-style: outset;
                border-width: 5px;
                border-color: {};     
            '''.format(color))
            but.clicked.connect(self.clickedKey)
            self.verticalLayout_2.addWidget(but)
            self.keyButtons[text] = but
            self.colors[text] = color

    def clickedAdd2(self):
        text = self.combo.currentText()
        if text not in self.keyButtons.keys():
            but = QtWidgets.QPushButton(self.groupBox)
            but.setText(text)
            color = 'rgb({}, {}, {})'.format(randint(0, 255), randint(0, 255), randint(0, 255))
            but.setStyleSheet('''
                background-color: rgb(200,200,200);
                border-style: outset;
                border-width: 5px;
                border-color: {};     
            '''.format(color))
            but.clicked.connect(self.clickedKey)
            self.verticalLayout_2.addWidget(but)
            self.keyButtons[text] = but
            self.colors[text] = color

    def clickedKey(self):
        sender = self.sender()
        del self.keyButtons[sender.text()]
        del self.colors[sender.text()]
        sender.deleteLater()

    def clickedFind(self):
        if self.contentButtons:
            for i in self.contentButtons.keys():
                self.contentButtons[i].deleteLater()
                self.rate[i].deleteLater()
                # del self.colors[i]

        database.execute("DROP TABLE IF EXISTS `doc_result`")
        database.execute(sql_create)
        if self.keyButtons:
            files = []
            for name in self.fileCheck.keys():
                if self.fileCheck[name].checkState():
                    files.append(name)
            files = tuple(files)

            for key in self.keyButtons.keys():
                database.execute(insert_doc.format(key, files, len(key)))

            records = database.execute(sql_select)
            if records:
                i = 0

                for record in records:
                    but = QtWidgets.QPushButton(self.groupBox_3)
                    but.setText(record[0])
                    but.setMaximumWidth(100)
                    but.setToolTip(record[2])
                    rates = {}
                    for key in self.keyButtons.keys():
                        rate = database.execute(sql_select_rate.format(key, record[0]))
                        if rate:
                            rates[key] = rate[0][0]
                        else:
                            rates[key] = 0

                    # print(rates)

                    colors = self.colors
                    # print(colors)

                    wid = Rate()
                    wid.setValue(rates)
                    wid.setMax(records[0][1])

                    wid.setColors(colors)

                    self.gridLayout_2.addWidget(but, i, 0, 1, 1)
                    self.gridLayout_2.addWidget(wid, i, 1, 1, 1)
                    i = i + 1
                    self.contentButtons[record[0]] = but
                    self.rate[record[0]] = wid

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox_2.setTitle(_translate("Form", "Список файлов"))
        for i in all_files:
            self.fileCheck[i].setText(_translate("Form", "{}".format(i)))
        self.pushButton.setText(_translate("Form", "Добавить"))
        self.groupBox.setTitle(_translate("Form", "Ключевые слова"))
        self.pushButton_2.setText(_translate("Form", "Найти"))
        self.pushButton_10.setText(_translate("Form", "Добавить"))
        self.groupBox_3.setTitle(_translate("Form", "Визуализация"))
