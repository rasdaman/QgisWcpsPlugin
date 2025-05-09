# -*- coding: utf-8 -*-

from __future__ import print_function

import urllib.request
from base64 import b64encode
from builtins import range
import os, sys, pickle
from collections import defaultdict
from glob import glob
import xml.etree.ElementTree as ET

from qgis.core import *
from qgis.gui import *

from PyQt5.QtWidgets import QProgressDialog, QDialog, QMessageBox, QFileDialog, QApplication, QPushButton, QInputDialog, \
    QLineEdit, QHeaderView, QTableView, QAbstractItemView
from PyQt5.QtGui import QCursor, QStandardItemModel, QStandardItem
from PyQt5.QtNetwork import QNetworkRequest, QNetworkAccessManager
from PyQt5.QtCore import Qt, QFileInfo
from PyQt5 import QtXml

from .CoveragesSelectionDialog import CoverageSelectionDialog
from .succesful_query_dialog import succesful_query_dialog
from .wcps_client_dialog_base import Ui_WCPSClient, CustomInputDialog, CoveragesListTableModel
from .qgsnewhttpconnectionbasedialog import qgsnewhttpconnectionbase
from .display_txtdialog import display_txt
import xml.etree.ElementTree as ET
from typing import Union, Optional
from .wcps_client_utilities import WCPSUtil

import shutil

# global setttings and saved server list
global config
from . import config

global mode


# ---------------
# running clock icon
def mouse_busy(function):
    """
        set the mouse icon to show clock
    """

    def new_function(self):
        """
            set the mouse icon to show clock
        """
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        result = function(self)
        QApplication.restoreOverrideCursor()
        return result

    return new_function

# ---------------


class WCPSClientDialog(QDialog, Ui_WCPSClient):
    global mode
    global selected_server
    global selected_server_url
    global coverages
    global filterCondition
    global extra_format_parameters
    global selected_coverages_tuples
    global variables
    saveQuerySignal = QtCore.pyqtSignal()
    selected_coverages_tuples = []
    variables = []

    # This stores the output file after the query is processed successfully. It can be either in /tmp dir
    # or in a selected folder (e.g. in ~/Downloads) after user chose to save the output file button.
    global output_file_path

    def __init__(self, iface):
        global extra_format_parameters
        global filterCondition
        """Constructor."""
        QDialog.__init__(self)

        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect

        self.setupUi(self)
        self.iface = iface
        print(config.srv_list)
        if len(config.srv_list['servers']) > 0:
            self.btnEdit_Serv.setEnabled(True)
            self.btnDelete_Serv.setEnabled(True)
            self.updateServerListing()

        self.myWCPS = WCPSUtil()
        self.tabWidget_WCPSClient.setCurrentIndex(0)
        global mode
        mode = ""
        extra_format_parameters = ""
        filterCondition = ""
        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowCloseButtonHint
        self.successful_dialog = succesful_query_dialog(self, flags, toEdit=False, choice='')
        self.successful_dialog.saveQuerySignal.connect(self.save_query_result_to_local_file)
        self.successful_dialog.showQuerySignal.connect(self.show_output_file_on_map_canvas)
        self.successful_dialog.saveAndShowQuerySignal.connect(self.save_output_to_file_then_show_on_map_canvas)
        self.ResultEncodedFormat.addItems(["none", "png", "jpeg", "tiff", "netcdf", "json", "custom"])

    # ---------------
    # provide a pop-up warning message
    @staticmethod
    def warning_msg(msg):
        """
            present a message in a popup dialog-box
        """
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Critical)
        msgBox.setText(msg)
        msgBox.setWindowTitle("Warning")
        msgBox.addButton(QPushButton('OK'), QMessageBox.YesRole)
        msgBox.exec_()

    # ---------------
    # add a new server to the list
    def newServer(self):
        global config

        # print('btnNew: I am adding a New ServerName/URL')
        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowCloseButtonHint
        dlgNew = qgsnewhttpconnectionbase(self, flags, toEdit=False, choice='')
        dlgNew.show()
        self.btnConnectServer_Serv.setFocus(True)

    ##TODO -- sort the srv_list

    # ---------------
    # read the selected server/url params
    def get_serv_url(self):
        global serv

        sel_serv = self.cmbConnections_Serv.currentText()
        if sel_serv == '':
            WCPSClientDialog.warning_msg("Configure at least a server with working endpoint first")
            return '', ''

        idx = serv.index(sel_serv)
        sel_url = config.srv_list['servers'][idx][1]
        return sel_serv, sel_url

    def basic_auth(self, username, password):
        token = b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
        return f'Basic {token}'

    # ---------------
    # check if the url exist and if we get a respond to a simple OWS request
    @mouse_busy
    def connectServer(self):
        global config
        global serv

        selected_serv, selected_url = self.get_serv_url()
        if selected_serv == '':
            # It means there is no server selected
            return

        # Send GetCapabilities request to get the coverages list
        capabilities_url = selected_url + "?service=WCS&version=2.0.1&request=GetCapabilities"
        username, password = self.get_auth_credentials()

        self.textBrowser_Serv.setText(f"Connecting to server {selected_serv}...")
        QApplication.processEvents()

        response_data, mime_type = WCPSUtil.get_url_response_data(capabilities_url, username, password)

        if response_data is not None:
            self.handleGetCapabilitiesResponse(response_data)
        else:
            # Error connecting to server
            return

        if not self.tab_WCPSQuery.isEnabled():
            self.tab_WCPSQuery.setEnabled(True)
            self.tab_VisualQuery.setEnabled(True)

        msg = "Selected server:    " + selected_serv + "\n"
        msg += "URL:                   " + selected_url + "\nConnected successfully!"
        self.textBrowser_Serv.setText(msg)

        QApplication.changeOverrideCursor(Qt.ArrowCursor)

    def parse_tag_name(self, element: Union[ET.Element, str]) -> str:
        """
        Extract just the tag name of an XML element, removing namespace components.
        Example: "{http://www.example.com}root" -> "root"

        :param element: An XML element from which to extract the tag name.
        :return: The tag name of the element.
        """
        if isinstance(element, ET.Element):
            element = element.tag
        elif not isinstance(element, str):
            raise RuntimeError(f"Cannot parse tag name, but expected xml.etree.ElementTree.Element"
                                     f" or string argument, but got {element.__class__}.")
        return element.split('}')[-1]

    def element_to_dict(self, t: ET.Element) -> dict:
        """
        Convert an XML element into a nested dictionary.

        This function recursively converts an XML element and its children into a
        nested dictionary. The keys of the dictionary are the tag names of the XML
        elements. Attributes of the XML elements are prefixed with '@' in the
        dictionary keys, and text content is stored under a '#text' key.

        :param t: The XML element to convert.
        :return: A nested dictionary representing the structure and content of the XML element.

        :note:
            - Elements with multiple children having the same tag name are converted into lists.
            - Text content is only added to the dictionary if the element has children
              or attributes, to avoid overwriting important data with whitespace.
        """
        tag = self.parse_tag_name(t)
        d = {tag: {} if t.attrib else None}
        children = list(t)
        if children:
            dd = defaultdict(list)
            for dc in map(self.element_to_dict, children):
                for k, v in dc.items():
                    dd[k].append(v)
            d = {tag: {k: v[0] if len(v) == 1 else v for k, v in dd.items()}}
        if t.attrib:
            d[tag].update(('@' + self.parse_tag_name(k), v) for k, v in t.attrib.items())
        if t.text:
            text = t.text.strip()
            if children or t.attrib:
                if text:
                    d[tag]['#text'] = text
            else:
                d[tag] = text
        return d

    def handleGetCapabilitiesResponse(self, data_str):
        """
        Parse the WCS GetCapabilities response in XML then convert that to list of coverages and also
        put that to rows in List Datacubes tab
        """
        global coverages
        try:
            try:
                dom = self.element_to_dict(ET.fromstring(data_str))
                if 'Capabilities' in dom and 'Contents' in dom['Capabilities'] and 'CoverageSummary' in \
                        dom['Capabilities']['Contents']:
                    coverages = dom['Capabilities']['Contents']['CoverageSummary']

                    table_data_rows = []

                    # Add coverage information to the tableView
                    for coverage in coverages:
                        name = coverage['CoverageId']

                        # Extracting values for dim, axes, bbox, crs, and size
                        bbox = coverage.get('BoundingBox', {})

                        lower_corner = bbox.get('LowerCorner', '') if isinstance(bbox, dict) else ''
                        upper_corner = bbox.get('UpperCorner', '') if isinstance(bbox, dict) else ''
                        dim = bbox.get('@dimensions', '') if isinstance(bbox, dict) else ''
                        crs_uri = bbox.get('@crs', '')
                        crs = WCPSUtil.parse_crs_to_ogc_shorthand_format(crs_uri) if isinstance(bbox, dict) else ''

                        axes_param = next((param for param in coverage.get('AdditionalParameters', {}).get(
                            'AdditionalParameter', []) if param.get('Name') == 'axisList'), None)
                        axes = axes_param.get('Value', '').replace(',', ' ') if axes_param else ''

                        size_in_bytes_param = next((param for param in
                                                    coverage.get('AdditionalParameters', {}).get(
                                                        'AdditionalParameter', []) if
                                                    param.get('Name') == 'sizeInBytes'), None)
                        size_in_bytes = size_in_bytes_param.get('Value', '') if size_in_bytes_param else ''

                        try:
                            size_gb = f"{float(size_in_bytes) / 1e9:.2f} GB" if size_in_bytes else "Unknown"
                        except ValueError:
                            size_gb = "Unknown"

                        table_data_rows.append([
                            name,
                            dim,
                            axes,
                            f"{lower_corner}",
                            f"{upper_corner}",
                            crs,
                            size_gb
                        ])

                    self.tab_CoveragesList.setEnabled(True)

                    headers = ["Name", "Dim", "Axes", "Lower Bounds", "Upper Bounds", "CRS", "Size"]
                    self.coverages_list_table_model = CoveragesListTableModel(table_data_rows, headers)
                    self.coverages_list_tableView.setModel(self.coverages_list_table_model)
                    self.coverages_list_tableView.setSelectionBehavior(QTableView.SelectRows)
                    self.coverages_list_tableView.setEditTriggers(QTableView.NoEditTriggers)
                    self.coverages_list_tableView.setSelectionBehavior(QAbstractItemView.SelectItems)  # Cell selection

                    self.coverages_list_tableView.resizeColumnsToContents()

                else:
                    WCPSClientDialog.warning_msg("Error parsing XML: Unexpected XML structure.")
            except Exception as e:
                WCPSClientDialog.warning_msg("Error parsing XML: " + str(e))
        except Exception as e:
            WCPSClientDialog.warning_msg("Error processing coverages list: " + str(e))

    # modify a server entry
    def editServer(self):
        global config
        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowCloseButtonHint

        idx = self.cmbConnections_Serv.currentIndex()
        if idx == -1:
            WCPSClientDialog.warning_msg("There is no configured server to edit")
            return
        if idx < len(config.srv_list['servers']):
            select_serv = config.srv_list['servers'][idx]

            print("Selection: ", idx, " -- ", select_serv, " -- Check: ", serv[idx])

            dlgEdit = qgsnewhttpconnectionbase(self, flags, toEdit=True, choice=idx)
            dlgEdit.txt_NewSrvName.setText(select_serv[0])
            dlgEdit.txt_NewSrvUrl.setText(select_serv[1])
            dlgEdit.show()
            self.btnConnectServer_Serv.setFocus(True)

    # ---------------

    # ---------------
    # delete a server entry
    def deleteServer(self):
        global config
        idx = self.cmbConnections_Serv.currentIndex()
        if idx == -1:
            WCPSClientDialog.warning_msg("There is no configured server to delete")
            return

        if idx < len(config.srv_list['servers']):
            config.srv_list['servers'].pop(idx)

        self.write_srv_list()
        self.updateServerListing()
        self.btnConnectServer_Serv.setFocus(True)

    # ---------------

    # ---------------
    # update the server-listing shown in the selectionBar
    def updateServerListing(self):
        global serv
        global config

        # print("btnUpdateServerListing:  here we are updating the ServerList....")
        serv = []
        config.srv_list = config.read_srv_list()
        for ii in range(len(config.srv_list['servers'])):
            serv.append(config.srv_list['servers'][ii][0][:])

        self.cmbConnections_Serv.clear()
        self.cmbConnections_Serv.addItems(serv)

    # ---------------

    # ---------------
    # write the sever names/urls to a file
    @mouse_busy
    def write_srv_list(self):
        plugin_dir = os.path.dirname(os.path.realpath(__file__))
        outsrvlst = os.path.join(plugin_dir, 'config_srvlist.pkl')
        fo = open(outsrvlst, 'wb')
        pickle.dump(config.srv_list, fo, 0)
        fo.close()

    # ---------------

    # ---------------
    # get the path where the downloaded datasets shall be stored
    @mouse_busy
    def get_folder_to_store_output_file(self):
        start_dir = os.getenv("HOME")
        selected_dir = QFileDialog.getExistingDirectory(self, "Select folder path to store output file", start_dir)
        if not selected_dir.endswith(os.sep):
            selected_dir = selected_dir + os.sep

        return selected_dir

    def get_auth_credentials(self):
        username = self.UserNameLine.text()
        password = self.PasswordLine.text()
        return username, password

    ## ====== End of Server section ======
    @mouse_busy
    def exeProcessCoverage(self):
        global req_outputLoc
        global authMgr
        global mode
        global selected_serv
        global selected_url
        global output_file_path

        self.get_auth_credentials()

        selected_serv, selected_url = self.get_serv_url()
        query = self.plainTextEdit_PC.toPlainText()
        if query is None or str(query).strip() == '':
            WCPSClientDialog.warning_msg("WCPS query to request cannot be empty")
            return
        input_param = {'query': query,
                       'serv_url': selected_url
                       }

        username, password = self.get_auth_credentials()
        process_output = self.myWCPS.ProcessCoverage(input_param, username, password)

        if 'output_file_path' in process_output:
            if 'mimetype' in process_output:
                mimetype = process_output['mimetype']
            output_file_path = process_output['output_file_path']

            datatype = mimetype.split('/')
            if datatype[0] == "image" or "netcdf" in datatype:
                self.successful_dialog.show()
            else:
                showData = open(output_file_path, 'r')
                dialogMessage = showData.read()
                myDisplay_txt = display_txt(self)
                myDisplay_txt.textBrowser_Disp.setText(dialogMessage)
                myDisplay_txt.show()


    ## ====== Add data to Map Canvas ======
    # read the the downloaded datasets, register them and show them in the QGis MapCanvas
    def show_output_file_on_map_canvas(self):

        self.canvas = self.iface.mapCanvas()

        fileID = output_file_path
        disp_image = glob(fileID)
        print(disp_image)
        # check if there is a loadable coverage available (and not eg. an multipart/related gml) or an error occurred
        if len(disp_image) > 0:
            imgInfo = QFileInfo(disp_image[-1])
            img_baseName = imgInfo.baseName()
            img_layer = QgsRasterLayer(disp_image[-1], img_baseName)
            if not img_layer.isValid():
                WCPSClientDialog.warning_msg("Layer failed to load!")

            QgsProject.instance().addMapLayer(img_layer)
        else:
            WCPSClientDialog.warning_msg(f"Could not load file {fileID}")


    # load Query from file
    def loadQuery(self):
        start_dir = os.getenv("HOME")
        queryFilePath = QFileDialog.getOpenFileName(self, "Select Query File", start_dir)[0]
        if queryFilePath != '':
            self.plainTextEdit_PC.setPlainText(open(queryFilePath, 'r').read())

    # save Query to file
    def storeQuery(self):
        query = self.plainTextEdit_PC.toPlainText()
        start_dir = os.getenv("HOME")
        queryFilePath = QFileDialog.getSaveFileName(self, "Save Query File", start_dir)
        if len(queryFilePath[0]) > 0:
            open(queryFilePath[0], 'w').write(query)

    ## ====== End of Add data to Map Canvas ======
    @mouse_busy
    def save_query_result_to_local_file(self):
        # Get the output dir to store the temp file
        global output_file_path
        temp_file_path = output_file_path
        temp_file_name = os.path.basename(temp_file_path)
        selected_output_dir = self.get_folder_to_store_output_file()

        # After the file is moved, it could still be loaded to QGIS canvas, hence it needs to store the new location
        output_file_path = selected_output_dir + temp_file_name
        shutil.move(temp_file_path, output_file_path)

        # then, remove the temp dir
        os.rmdir(os.path.dirname(temp_file_path))

    def save_output_to_file_then_show_on_map_canvas(self):
        self.save_query_result_to_local_file()
        self.show_output_file_on_map_canvas()

    def select_datacubes_handler(self):
        global coverages
        global selected_coverages_tuples
        global variables
        for coverage in coverages:
            if "checked" not in coverage:
                coverage["checked"] = False

        dialog = CoverageSelectionDialog(coverages, self)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            self.lstSelectedDatacubes.clear()
            selected_coverages_tuples.clear()

            # Get the selected coverage ids from the dialog
            coverage_ids = dialog.get_selected_coverage_ids()
            COVERAGE_ITERATOR_PREFIX = "$c"
            for i, coverage_id in enumerate(coverage_ids):
                if i == 0:
                    cov_iterator = COVERAGE_ITERATOR_PREFIX
                else:
                    cov_iterator = COVERAGE_ITERATOR_PREFIX + f"{i}"

                variables.append(cov_iterator)
                self.lstSelectedDatacubes.addItem(f"{coverage_id} -> {cov_iterator}")
                selected_coverages_tuples.append((cov_iterator, coverage_id))

    def unselect_datacubes_handler(self):
        global coverages
        global selected_coverages_tuples
        self.lstSelectedDatacubes.clear()
        selected_coverages_tuples.clear()

        for coverage in coverages:
            coverage["checked"] = False

    def set_where_clause_handler(self):
        global filterCondition

        dialog = QInputDialog()
        dialog.setWindowTitle("Set Filter Condition (WCPS WHERE clause)")
        dialog.setLabelText("")
        dialog.setTextValue(filterCondition)
        line_edit = dialog.findChild(QLineEdit)
        if line_edit:
            line_edit.setPlaceholderText("e.g. avg($c) > 3000")

        dialog.resize(600, 200)
        if dialog.exec_() == QInputDialog.Accepted:
            filterCondition = dialog.textValue()

    def set_encode_extra_parameters(self):
        global extra_format_parameters
        dialog = CustomInputDialog('Set extra parameters for encode()', 'e.g. {\"nodata\": [0]}', extra_format_parameters)
        # Show the dialog and wait for the result
        dialog.exec_()
        # After the dialog is closed, get the text
        extra_format_parameters = dialog.get_input_text()

    def generate_wcps_query(self):
        global selected_coverages_tuples
        global extra_format_parameters
        global filterCondition
        global variables

        if len(selected_coverages_tuples) == 0:
            WCPSClientDialog.warning_msg("At least one datacube must be selected for WCPS FOR clause first")
            return

        # Result Expression (the return clause)
        return_expr = self.ResultExpression.toPlainText().strip()
        if return_expr == '':
            WCPSClientDialog.warning_msg("Result expression for WCPS RETURN clause must not be empty")
            return

        # Input Datacubes (the for clause)
        for_clause = "FOR "
        for i, coverage_tuple in enumerate(selected_coverages_tuples):
            coverage_iterator = coverage_tuple[0]
            coverage_id = coverage_tuple[1]

            for_clause += coverage_iterator + " IN (" + coverage_id + ")"
            if i < len(selected_coverages_tuples) - 1:
                for_clause += ", \n        "

        # 2. Filter Datacubes (the where clause)
        where_clause = ""
        if filterCondition != "":
            where_clause = f"\nWHERE {filterCondition}"

        # 4. Result Format
        encoded_format = self.ResultEncodedFormat.currentText()
        if encoded_format.lower() == 'none':
            # e.g. avg($c)
            format_clause = ""
        elif encoded_format.lower() == 'custom':
            custom_encode_format = self.CustomFormatLine.text().strip()
            if custom_encode_format == "":
                WCPSClientDialog.warning_msg("Custom encoded format must not be empty")
                return
            format_clause = f'"{custom_encode_format}"'
        else:
            # e.g. png -> "image/png"
            format_clause = f'"{encoded_format}"'

        # Append extra format parameters (if in JSON it needs to be escaped for character " if any)
        escaped_extra_format_parameters = extra_format_parameters

        if extra_format_parameters is not None and str(extra_format_parameters).strip() != "":
            if WCPSUtil.is_json(extra_format_parameters.replace('\\\"', '"')):
                if '\\\"' not in extra_format_parameters:
                    # e.g. { "nodata": [0], "geoReference":{"crs":"EPSG:4326"} } -> encode quotes to \"
                    escaped_extra_format_parameters = extra_format_parameters.replace('"', '\\"')

            format_clause += f', "{escaped_extra_format_parameters}"'

        # Construct the final query
        query = f"{for_clause}{where_clause}\nRETURN"
        encoded_expression = f"encode({return_expr}, {format_clause})"
        if encoded_format == "none":
            encoded_expression = f"{return_expr}"

        query += " " + encoded_expression

        self.plainTextEdit_PC.setPlainText(query)
        self.exeProcessCoverage()
