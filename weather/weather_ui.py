# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'weather_window.ui'
##
## Created by: Qt User Interface Compiler version 5.15.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(500, 575)
        Dialog.setMinimumSize(QSize(500, 575))
        Dialog.setMaximumSize(QSize(500, 16777215))
        self.calendar = QCalendarWidget(Dialog)
        self.calendar.setObjectName(u"calendar")
        self.calendar.setGeometry(QRect(187, 0, 312, 183))
        self.all_day = QTableView(Dialog)
        self.all_day.setObjectName(u"all_day")
        self.all_day.setGeometry(QRect(0, 0, 180, 570))
        self.load_csv = QPushButton(Dialog)
        self.load_csv.setObjectName(u"load_csv")
        self.load_csv.setGeometry(QRect(190, 240, 131, 23))
        self.csv_path_header = QLabel(Dialog)
        self.csv_path_header.setObjectName(u"csv_path_header")
        self.csv_path_header.setGeometry(QRect(190, 190, 301, 16))
        self.csv_path = QLineEdit(Dialog)
        self.csv_path.setObjectName(u"csv_path")
        self.csv_path.setGeometry(QRect(190, 210, 301, 20))
        self.csv_path.setReadOnly(True)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.load_csv.setText(QCoreApplication.translate("Dialog", u"\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c .csv", None))
        self.csv_path_header.setText(QCoreApplication.translate("Dialog", u"\u041f\u0443\u0442\u044c \u0434\u043e \u0444\u0430\u0439\u043b\u043e\u0432 .csv :", None))
    # retranslateUi

