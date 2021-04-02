# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uploader.ui',
# licensing of 'uploader.ui' applies.
#
# Created: Wed Sep 30 12:09:32 2020
#      by: pyside2-uic  running on PySide2 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(387, 152)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.sub_name = QtWidgets.QLineEdit(self.centralwidget)
        self.sub_name.setGeometry(QtCore.QRect(0, 20, 113, 20))
        self.sub_name.setObjectName("sub_name")
        self.date = QtWidgets.QLineEdit(self.centralwidget)
        self.date.setGeometry(QtCore.QRect(130, 20, 113, 20))
        self.date.setObjectName("date")
        self.on_sale = QtWidgets.QLineEdit(self.centralwidget)
        self.on_sale.setGeometry(QtCore.QRect(270, 20, 113, 20))
        self.on_sale.setObjectName("on_sale")
        self.upload = QtWidgets.QPushButton(self.centralwidget)
        self.upload.setGeometry(QtCore.QRect(50, 90, 75, 23))
        self.upload.setObjectName("upload")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 47, 13))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(130, 0, 47, 13))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(270, 0, 47, 13))
        self.label_3.setObjectName("label_3")
        self.price = QtWidgets.QLineEdit(self.centralwidget)
        self.price.setGeometry(QtCore.QRect(0, 70, 113, 20))
        self.price.setObjectName("price")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(0, 50, 47, 13))
        self.label_4.setObjectName("label_4")
        self.image = QtWidgets.QLineEdit(self.centralwidget)
        self.image.setGeometry(QtCore.QRect(130, 70, 113, 20))
        self.image.setObjectName("image")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(130, 50, 47, 13))
        self.label_5.setObjectName("label_5")
        self.delete_2 = QtWidgets.QPushButton(self.centralwidget)
        self.delete_2.setGeometry(QtCore.QRect(150, 90, 75, 23))
        self.delete_2.setObjectName("delete_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 387, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1)
        )
        self.upload.setText(
            QtWidgets.QApplication.translate("MainWindow", "Upload", None, -1)
        )
        self.label.setText(
            QtWidgets.QApplication.translate("MainWindow", "subname", None, -1)
        )
        self.label_2.setText(
            QtWidgets.QApplication.translate("MainWindow", "dates", None, -1)
        )
        self.label_3.setText(
            QtWidgets.QApplication.translate("MainWindow", "onsale", None, -1)
        )
        self.label_4.setText(
            QtWidgets.QApplication.translate("MainWindow", "price", None, -1)
        )
        self.label_5.setText(
            QtWidgets.QApplication.translate("MainWindow", "Image", None, -1)
        )
        self.delete_2.setText(
            QtWidgets.QApplication.translate("MainWindow", "Delete", None, -1)
        )
