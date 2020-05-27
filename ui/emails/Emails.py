from random import randint

import numpy as np
from PyQt5 import QtCore, QtWidgets

from tools import database
from ui.emails.mlpEmails import prepare_canvas, plot_draw_lines

sql_create = '''CREATE TABLE `email_result` (
        sender text,
        recipient text,
        subject text
        )
'''

sql_select = '''
    SELECT sender, recipient, subject
    FROM
        `email_result`
'''

insert_doc = '''
    insert into email_result (subject, sender, recipient)
    SELECT preprocessed_subject as subject, sa.address as sender, ra.address as recipient 
    FROM email_references er
    inner join emailheaders_info ei
    on er.emailheader_id = ei.emailheader_id
    inner join email_addresses sa on sa.id = from_id
    inner join email_addresses ra on ra.id = to_id
    where sender in {1} and subject like '%{0}%'
    UNION
    SELECT preprocessed_subject as subject, sa.address as sender, ra.address as recipient 
    FROM email_references er
    inner join emailheaders_info ei
    on er.emailheader_id = ei.emailheader_id
    inner join email_addresses sa on sa.id = from_id
    inner join email_addresses ra on ra.id = to_id
    where recipient in {1} and subject like '%{0}%'

'''

sql_select_rate = '''
    SELECT rate FROM doc_result WHERE key='{}' AND file_name ='{}'
    '''

sql_select_content = '''SELECT content FROM doc_result WHERE name={}'''

records = None
all_addresses = None


class Emails(QtWidgets.QWidget):

    def __init__(self, parent):
        super(QtWidgets.QWidget, self).__init__(parent)

        global records
        global all_addresses

        query = "select id, address from email_addresses"
        records = database.execute(query)

        all_addresses = {}
        if records:
            for record in records:
                all_addresses[record[1]] = record[0]

        self.init_dynamicUI()
        self.initUI(self)
        self.add_events()

    def init_dynamicUI(self):
        self.addressCheck = {}
        self.keyButtons = {}
        self.colors = {}

    def initUI(self, Form):
        # ***  статические компоненты из дизайнера******
        Form.setObjectName("Form")
        Form.resize(988, 896)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.scrollArea = QtWidgets.QScrollArea(Form)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 986, 894))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setContentsMargins(6, 6, 6, 6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.gbUsers = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.gbUsers.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.gbUsers.setObjectName("gbUsers")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.gbUsers)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.saUsers = QtWidgets.QScrollArea(self.gbUsers)
        self.saUsers.setWidgetResizable(True)
        self.saUsers.setObjectName("saUsers")
        self.scrollAreaWidgetContents_3 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 370, 376))
        self.scrollAreaWidgetContents_3.setObjectName("scrollAreaWidgetContents_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_3)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.vaUsers = QtWidgets.QVBoxLayout()
        self.vaUsers.setObjectName("vaUsers")
        self.verticalLayout_4.addLayout(self.vaUsers)
        self.saUsers.setWidget(self.scrollAreaWidgetContents_3)
        self.verticalLayout_2.addWidget(self.saUsers)
        self.verticalLayout.addWidget(self.gbUsers)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.txtKey = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.txtKey.setObjectName("txtKey")
        self.horizontalLayout.addWidget(self.txtKey)
        self.btnAdd = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnAdd.sizePolicy().hasHeightForWidth())
        self.btnAdd.setSizePolicy(sizePolicy)
        self.btnAdd.setObjectName("btnAdd")
        self.horizontalLayout.addWidget(self.btnAdd)
        self.gridLayout_2.addLayout(self.horizontalLayout, 2, 0, 1, 1)
        self.btnFind = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.btnFind.setObjectName("btnFind")
        self.gridLayout_2.addWidget(self.btnFind, 4, 0, 1, 1)
        self.gbKeys = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.gbKeys.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.gbKeys.setObjectName("gbKeys")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.gbKeys)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.saKeys = QtWidgets.QScrollArea(self.gbKeys)
        self.saKeys.setWidgetResizable(True)
        self.saKeys.setObjectName("saKeys")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 370, 376))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.vaKeys = QtWidgets.QVBoxLayout()
        self.vaKeys.setObjectName("vaKeys")
        self.verticalLayout_8.addLayout(self.vaKeys)
        self.saKeys.setWidget(self.scrollAreaWidgetContents_2)
        self.verticalLayout_6.addWidget(self.saKeys)
        self.verticalLayout_5.addLayout(self.verticalLayout_6)
        self.gridLayout_2.addWidget(self.gbKeys, 3, 0, 1, 1)
        self.gridLayout_2.setRowStretch(0, 1)
        self.gridLayout_2.setRowStretch(3, 1)
        self.horizontalLayout_3.addLayout(self.gridLayout_2)
        self.scrollArea_4 = QtWidgets.QScrollArea(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea_4.sizePolicy().hasHeightForWidth())
        self.scrollArea_4.setSizePolicy(sizePolicy)
        self.scrollArea_4.setWidgetResizable(True)
        self.scrollArea_4.setObjectName("scrollArea_4")
        self.scrollAreaWidgetContents_4 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_4.setGeometry(QtCore.QRect(0, 0, 586, 892))
        self.scrollAreaWidgetContents_4.setObjectName("scrollAreaWidgetContents_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_4)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.vaDiagram = QtWidgets.QVBoxLayout()
        self.vaDiagram.setObjectName("vaDiagram")
        self.verticalLayout_3.addLayout(self.vaDiagram)
        self.scrollArea_4.setWidget(self.scrollAreaWidgetContents_4)
        self.horizontalLayout_3.addWidget(self.scrollArea_4)
        self.horizontalLayout_3.setStretch(0, 2)
        self.horizontalLayout_3.setStretch(1, 3)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout_2.addWidget(self.scrollArea)
        self.horizontalLayout_2.setStretch(0, 2)

        # ***список #адресов**********
        self.add_addresses(Form)

        # создание канвы для графика
        self.canvasEmails = prepare_canvas(layout=self.vaDiagram)
        self.canvasEmails.setVisible(True)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.gbUsers.setTitle(_translate("Form", "Пользователи"))
        self.btnAdd.setText(_translate("Form", "Добавить"))
        self.btnFind.setText(_translate("Form", "Найти"))
        self.gbKeys.setTitle(_translate("Form", "Ключевые слова"))
        # ***список #адресов**********
        self.retranslate_addresses(_translate)

    def add_events(self):
        self.btnAdd.clicked.connect(self.clickedAdd)
        self.btnFind.clicked.connect(self.clickedFind)

    # динамические виджеты-адреса
    def add_addresses(self, Form):
        for address in all_addresses.keys():
            check = QtWidgets.QCheckBox(self.gbUsers)
            check.setChecked(True)
            # начальное значение = 75 для читаемости текста на фоне элемента
            c = (randint(75, 255), randint(75, 255), randint(75, 255))
            color = 'rgb({}, {}, {})'.format(c[0], c[1], c[2])
            check.setStyleSheet('''
                            background-color: {}; 
                        '''.format(color))
            self.colors[address] = c
            self.vaUsers.addWidget(check)
            self.addressCheck[address] = check

    def retranslate_addresses(self, _translate):
        for address, id in all_addresses.items():
            if address in self.addressCheck:
                self.addressCheck[address].setText(_translate("Form", "{}".format(address)))

    # обработка кнопки Добавить в ключевые слова
    def clickedAdd(self):
        text = self.txtKey.text()
        if text not in self.keyButtons.keys():
            but = QtWidgets.QPushButton(self.gbKeys)
            but.setText(text)
            but.clicked.connect(self.clickedKey)
            self.vaKeys.addWidget(but)
            self.keyButtons[text] = but

    # удаление кнопки с ключевым словом из списка
    def clickedKey(self):
        sender = self.sender()
        del self.keyButtons[sender.text()]
        sender.deleteLater()

    def clickedFind(self):
        database.execute("DROP TABLE IF EXISTS `email_result`")
        database.execute(sql_create)
        addresses = ['']
        for address in self.addressCheck.keys():
            if self.addressCheck[address].checkState():
                addresses.append(address)
        addresses = tuple(addresses)

        if self.keyButtons:
            for key in self.keyButtons.keys():
                database.execute(insert_doc.format(key, addresses))
        else:
            database.execute(insert_doc.format('', addresses))
        records = database.execute(sql_select)

        names = {}
        flux = []
        for item in records:
            sender, recipient, subject = tuple(item)
            if sender not in names:
                names[sender] = len(names.items())
            if recipient not in names:
                names[recipient] = len(names.items())

        N = len(names.items())
        flux = np.zeros((N, N))
        headers = [[[''] for x in range(N)] for x in range(N)]
        for item in records:
            sender, recipient, subject = tuple(item)
            sender_idx = names[sender]
            recipient_idx = names[recipient]
            flux[sender_idx][recipient_idx] += 1
            headers[sender_idx][recipient_idx].append(subject)
        names = list(names.keys())
        colors = [self.colors[name] for name in names]
        self.canvasEmails.setVisible(False)
        plot_draw_lines([names, colors, flux, headers], self.canvasEmails)
        self.canvasEmails.setVisible(True)
