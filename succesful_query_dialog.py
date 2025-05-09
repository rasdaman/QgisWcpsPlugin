# -*- coding: utf-8 -*-

from __future__ import print_function
from builtins import str
from builtins import zip

from PyQt5.QtWidgets import QDialog, QMessageBox, QPushButton
from PyQt5.QtCore import *
from qgis.PyQt import QtCore

from .succesful_query_base import Ui_succesful_query_base


class succesful_query_dialog(QDialog,  QObject, Ui_succesful_query_base):
    MSG_BOX_TITLE = "WCPS Client"
    saveQuerySignal = QtCore.pyqtSignal()
    showQuerySignal = QtCore.pyqtSignal()
    saveAndShowQuerySignal = QtCore.pyqtSignal()

    def __init__(self, parent, fl, toEdit, choice):
        QDialog.__init__(self, parent, fl)
        self.toEdit = toEdit
        self.idx_sel = choice
        self.parent = parent
        self.flags = fl
        self.setupUi(self)
        self.setWindowTitle('WCPS Client') # +version())

    def SaveResult(self):
        self.saveQuerySignal.emit()
        self.close()


    def ShowResult(self):
        self.showQuerySignal.emit()
        self.close()


    def SaveAndShowResult(self):
        self.saveAndShowQuerySignal.emit()
        self.close()



