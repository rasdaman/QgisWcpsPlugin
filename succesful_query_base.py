# -*- coding: utf-8 -*-

from builtins import object
from PyQt5 import QtCore, QtGui, QtWidgets

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_succesful_query_base(object):
    def setupUi(self, succesful_query_base):
        succesful_query_base.setObjectName(_fromUtf8("succesful_query_base"))
        succesful_query_base.resize(522, 124)
        self.label = QtWidgets.QLabel(succesful_query_base)
        self.label.setGeometry(QtCore.QRect(120, 10, 371, 20))
        self.label.setObjectName(_fromUtf8("label"))
        self.btnSaveResult = QtWidgets.QPushButton(succesful_query_base)
        self.btnSaveResult.setGeometry(QtCore.QRect(10, 40, 241, 28))
        self.btnSaveResult.setObjectName(_fromUtf8("btnSaveResult"))
        self.btnShowResult = QtWidgets.QPushButton(succesful_query_base)
        self.btnShowResult.setGeometry(QtCore.QRect(262, 40, 251, 28))
        self.btnShowResult.setObjectName(_fromUtf8("btnShowResult"))
        self.btnSaveAndShowResult = QtWidgets.QPushButton(succesful_query_base)
        self.btnSaveAndShowResult.setGeometry(QtCore.QRect(10, 80, 241, 28))
        self.btnSaveAndShowResult.setObjectName(_fromUtf8("btnSaveAndShowResult"))
        self.btnCancel = QtWidgets.QPushButton(succesful_query_base)
        self.btnCancel.setGeometry(QtCore.QRect(260, 80, 251, 28))
        self.btnCancel.setObjectName(_fromUtf8("btnCancel"))

        self.btnCancel.clicked.connect(succesful_query_base.close)
        self.btnSaveResult.clicked.connect(succesful_query_base.SaveResult)
        self.btnShowResult.clicked.connect(succesful_query_base.ShowResult)
        self.btnSaveAndShowResult.clicked.connect(succesful_query_base.SaveAndShowResult)

        self.retranslateUi(succesful_query_base)


        QtCore.QMetaObject.connectSlotsByName(succesful_query_base)
    def retranslateUi(self, succesful_query_base):
        succesful_query_base.setWindowTitle(QtWidgets.QApplication.translate("succesful_query_base", "Successful query", None))
        self.label.setText(QtWidgets.QApplication.translate("succesful_query_base", "Query executed successfully, select action for query output.", None))
        self.btnSaveResult.setText(QtWidgets.QApplication.translate("succesful_query_base", "Save result", None))
        self.btnSaveResult.setToolTip("Save the processed output to a local file")

        self.btnShowResult.setText(QtWidgets.QApplication.translate("succesful_query_base", "Show result in QGIS layer", None))
        self.btnSaveAndShowResult.setText(QtWidgets.QApplication.translate("succesful_query_base", "Save and show result in QGIS layer", None))

        self.btnCancel.setText(QtWidgets.QApplication.translate("succesful_query_base", "Discard result", None))
        self.btnCancel.setToolTip("Do not save result to file or show result on QGIS")