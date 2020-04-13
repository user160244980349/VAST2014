from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget

from ui.docs.Docs import Docs
from ui.emails.Emails import Emails
from ui.timeline.Timeline import Timeline


class TabWidget(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()

        # Add tabs
        self.tabs.addTab(self.tab1, "Docs list")
        self.tabs.addTab(self.tab2, "Articles timeline")
        self.tabs.addTab(self.tab3, "Email graph")

        # Visuals widgets
        self.docs = Docs(self)
        self.timeline = Timeline(self)
        self.emails = Emails(self)

        # Create first tab
        self.tab1.layout = QVBoxLayout(self)
        self.tab1.layout.addWidget(self.docs)
        self.tab1.setLayout(self.tab1.layout)

        # Create second tab
        self.tab2.layout = QVBoxLayout(self)
        self.tab2.layout.addWidget(self.timeline)
        self.tab2.setLayout(self.tab2.layout)

        # Create third tab
        self.tab3.layout = QVBoxLayout(self)
        self.tab3.layout.addWidget(self.emails)
        self.tab3.setLayout(self.tab3.layout)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
