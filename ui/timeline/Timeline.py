from random import randint
import datetime
from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from tools import database
import config
from ui.timeline.mlpTimeline import prepare_canvas, plot_draw_lines
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView



sql_create = '''CREATE TABLE `timeline_result` (
        'date_to_sort' text,
        'date' text,
        `key` text,
        `header` text,
        `rate` integer,
        `content` text
        )
'''

sql_select = '''
    SELECT date_to_sort, key, SUM(rate)
    FROM
        `timeline_result`
    GROUP BY date, key
    ORDER BY key, date_to_sort
'''

sql_select_content =  ''' 
    SELECT content
    FROM
        `timeline_result`
    WHERE 
        date = '{0}'
    AND 
        key = '{1}'    
'''

sql_select_header =  ''' 
    SELECT header
    FROM
        `timeline_result`
    WHERE 
        date_to_sort = '{0}'
    AND 
        key = '{1}'    
'''

insert_timelines = '''
    INSERT INTO 
        timeline_result
    SELECT
        substr(a.date,7,4)||substr(a.date, 4,2)||substr(a.date,1,2) date_to_sort,
         a.date,
        '{0}', 
        a.header, 
        (LENGTH(p.prerocessed_content)-LENGTH(REPLACE(p.prerocessed_content,'{0}',''))) / {3},
        f.content
    FROM 
        articles_info a
    INNER JOIN 
        all_files f 
    ON  
        f.id = a.file_id
    INNER JOIN 
        files_preprocessed_content p 
    ON 
        f.id=p.file_id
    WHERE 
        p.prerocessed_content like '% {0} %' 
    AND 
        substr(a.date,7,4)||substr(a.date, 4,2)||substr(a.date,1,2) BETWEEN '{1}' AND '{2}'  
    ORDER BY 
        date_to_sort
'''

#получение списка имен собственных
database.connect(config.database)
query = "select lastname, firstname from file_employeerecords"
records = database.execute(query)

#словарь  списка имен собственных
all_names = []
if records:
    for record in records:
        all_names.append(record[0])
        all_names.append(record[1])

class Timeline(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.init_dynamicUI()
        self.initUi(self)
        self.add_events()

    #динамические контролы (ключевые слова + цвета)
    def init_dynamicUI(self):
        self.keyButtons = {}
        self.colors = {}

    def initUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(981, 704)
        self.gridLayout_5 = QtWidgets.QGridLayout(Form)
        self.gridLayout_5.setContentsMargins(6, 6, 6, 6)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.scrollArea = QtWidgets.QScrollArea(Form)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 965, 339))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.vlMlpLayout = QtWidgets.QVBoxLayout()
        self.vlMlpLayout.setContentsMargins(6, 6, 6, 6)
        self.vlMlpLayout.setObjectName("vlMlpLayout")
        self.verticalLayout_2.addLayout(self.vlMlpLayout)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_3.addWidget(self.scrollArea, 0, 0, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_3, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.scrollArea_3 = QtWidgets.QScrollArea(Form)
        self.scrollArea_3.setWidgetResizable(True)
        self.scrollArea_3.setObjectName("scrollArea_3")
        self.scrollAreaWidgetContents_3 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 482, 339))
        self.scrollAreaWidgetContents_3.setObjectName("scrollAreaWidgetContents_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_3)
        self.verticalLayout_4.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.label.setObjectName("label")
        self.verticalLayout_4.addWidget(self.label)
        self.deStart = QtWidgets.QDateEdit(self.scrollAreaWidgetContents_3)
        self.deStart.setObjectName("deStart")
        self.verticalLayout_4.addWidget(self.deStart)
        self.label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_4.addWidget(self.label_2)
        self.deEnd = QtWidgets.QDateEdit(self.scrollAreaWidgetContents_3)
        self.deEnd.setDateTime(QtCore.QDateTime(QtCore.QDate(2099, 1, 1), QtCore.QTime(0, 0, 0)))
        self.deEnd.setMaximumDate(QtCore.QDate(7999, 12, 31))
        self.deEnd.setObjectName("deEnd")
        self.verticalLayout_4.addWidget(self.deEnd)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem)
        self.btnFind = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
        self.btnFind.setObjectName("btnFind")
        self.verticalLayout_4.addWidget(self.btnFind)
        self.scrollArea_3.setWidget(self.scrollAreaWidgetContents_3)
        self.horizontalLayout_2.addWidget(self.scrollArea_3)
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setContentsMargins(6, -1, 0, -1)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout_6 = QtWidgets.QGridLayout()
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.btnPlusIS = QtWidgets.QPushButton(Form)
        self.btnPlusIS.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.btnPlusIS.setObjectName("btnPlusIS")
        self.gridLayout_6.addWidget(self.btnPlusIS, 0, 2, 1, 1)
        self.txtKey = QtWidgets.QLineEdit(Form)
        self.txtKey.setObjectName("txtKey")
        self.gridLayout_6.addWidget(self.txtKey, 0, 0, 1, 1)
        self.btnAdd = QtWidgets.QPushButton(Form)
        self.btnAdd.setObjectName("btnAdd")
        self.gridLayout_6.addWidget(self.btnAdd, 0, 1, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_6, 2, 0, 1, 1)
        self.scrollArea_2 = QtWidgets.QScrollArea(Form)
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 474, 302))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_2)
        self.gridLayout.setObjectName("gridLayout")
        self.gbKeys = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_2)
        self.gbKeys.setObjectName("gbKeys")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.gbKeys)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea_4 = QtWidgets.QScrollArea(self.gbKeys)
        self.scrollArea_4.setWidgetResizable(True)
        self.scrollArea_4.setObjectName("scrollArea_4")
        self.scrollAreaWidgetContents_4 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_4.setGeometry(QtCore.QRect(0, 0, 448, 256))
        self.scrollAreaWidgetContents_4.setObjectName("scrollAreaWidgetContents_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_4)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.vlKeys = QtWidgets.QVBoxLayout()
        self.vlKeys.setContentsMargins(6, -1, 6, -1)
        self.vlKeys.setObjectName("vlKeys")
        self.verticalLayout_3.addLayout(self.vlKeys)
        self.scrollArea_4.setWidget(self.scrollAreaWidgetContents_4)
        self.verticalLayout.addWidget(self.scrollArea_4)
        self.gridLayout.addWidget(self.gbKeys, 0, 0, 1, 1)
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.gridLayout_4.addWidget(self.scrollArea_2, 3, 0, 1, 1)
        self.gridLayout_4.setRowMinimumHeight(0, 1)
        self.gridLayout_4.setRowMinimumHeight(1, 1)
        self.gridLayout_4.setRowMinimumHeight(2, 1)
        self.gridLayout_4.setRowMinimumHeight(3, 1)
        self.gridLayout_4.setRowStretch(3, 1)
        self.horizontalLayout_2.addLayout(self.gridLayout_4)
        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 1)
        self.gridLayout_5.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)

        # создание канвы для графика
        self.canvasTimeline = prepare_canvas(layout=self.vlMlpLayout)
        self.canvasTimeline.setVisible(True)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)


    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_2.setText(_translate("Form", "Конец временного периода"))
        self.label.setText(_translate("Form", "Начало временного периода"))
        self.btnPlusIS.setText(_translate("Form", "+И.С."))
        self.btnAdd.setText(_translate("Form", "+"))
        self.gbKeys.setTitle(_translate("Form", "Ключевые слова"))
        self.btnFind.setText(_translate("Form", "Найти"))

    def add_events(self):
        self.btnAdd.clicked.connect(self.clickedAdd)
        self.btnFind.clicked.connect(self.clickedFind)
        self.btnPlusIS.clicked.connect(self.clickedPlusIS)

    def clickedPlusIS(self):
        for name in all_names:
            self.makeKeyButton(name)

    # обработка кнопки "+" в ключевые слова
    def clickedAdd(self):
        text = self.txtKey.text()
        self.makeKeyButton(text)

    def makeKeyButton(self, text):
        if text not in self.keyButtons.keys():
            but = QtWidgets.QPushButton(self.gbKeys)
            but.setText(text)
            c = (randint(0, 255), randint(0, 255), randint(0, 255))
            color = 'rgb({}, {}, {})'.format(c[0], c[1], c[2])
            but.setStyleSheet('''
                           background-color: rgb(200,200,200);
                           border-style: outset;
                           border-width: 5px;
                           border-color: {};     
                       '''.format(color))
            but.clicked.connect(self.clickedKey)
            self.vlKeys.addWidget(but)
            self.keyButtons[text] = but
            self.colors[text] = c

    def clickedKey(self):
        sender = self.sender()
        del self.keyButtons[sender.text()]
        del self.colors[sender.text()]
        sender.deleteLater()

    def clickedFind(self):
        database.execute("DROP TABLE IF EXISTS `timeline_result`")
        database.execute(sql_create)
        if self.keyButtons:
            for key in self.keyButtons.keys():
                start = self.deStart.date().toString('yyyyMMdd')
                end = self.deEnd.date().toString('yyyyMMdd')
                database.execute(insert_timelines.format(key, start, end, len(key)))

            #получение результатов из базы
            records = database.execute(sql_select)

            #подготовка данных для графика
            lines = {}
            for item in records:
                date, key, rate = tuple(item)
                if key not in lines:
                    lines[key] = (self.colors[key], [], [], [])
                l = lines[key]
                date_d = datetime.datetime.strptime(date, "%Y%m%d").date()
                l[1].append(date_d)
                l[2].append(rate)
                header_records = database.execute(sql_select_header.format(date, key))
                hint = ''
                for header in header_records:
                    hint += header[0]
                l[3].append(hint)
            self.canvasTimeline.setVisible(False)
            plot_draw_lines(lines, self.canvasTimeline)
            self.canvasTimeline.setVisible(True)