# -*- coding: utf-8 -*-

from __future__ import print_function
from builtins import str
from builtins import zip

from PyQt5.QtWidgets import QDialog, QMessageBox, QPushButton
from PyQt5.QtCore import QObject

from .wcps_client_utilities import WCPSUtil
from .qgsnewhttpconnectionbase import Ui_qgsnewhttpconnectionbase

#global setttings and saved server list
global config
from . import config
srvlst = []

class qgsnewhttpconnectionbase(QDialog,  QObject, Ui_qgsnewhttpconnectionbase):
    MSG_BOX_TITLE = "WCPS Client"

    def __init__(self, parent, fl, toEdit, choice):
        QDialog.__init__(self, parent, fl)
        self.toEdit = toEdit
        self.idx_sel = choice
        self.parent = parent
        self.flags = fl
        self.setupUi(self)
        self.txt_NewSrvName.setFocus(True)
        self.setWindowTitle('WCPS Client') # +version())


    def accept(self):
        from .wcps_client_dialog import WCPSClientDialog
        global config
        print('IDX: ',self.idx_sel)
        srvlst = config.srv_list['servers']
        srv_name = self.txt_NewSrvName.text()
        srv_url = self.txt_NewSrvUrl.text()

        for i, array_element in enumerate(srvlst):
            if array_element[0] == srv_name and i != self.idx_sel:
                WCPSClientDialog.warning_msg("Server name already exists, choose another name.")
                return

        # verify that URL starts with http://
        if not srv_url.startswith("http"):
            WCPSClientDialog.warning_msg("Server URL must start with http or https")
            return
        else:
            response_data, mime_type = WCPSUtil.get_url_response_data(srv_url)
            if response_data is None:
                # error when accessing petascope endpoint, do not close the current opened dialog
                return

        if self.toEdit is False:
            # New button
            srvlst.append([srv_name, srv_url])
        else:
            # Edit button
            srvlst[self.idx_sel] = [srv_name, srv_url]

        config.srv_list = {'servers': srvlst }
        self.parent.write_srv_list()
        self.parent.updateServerListing()

        self.close()


