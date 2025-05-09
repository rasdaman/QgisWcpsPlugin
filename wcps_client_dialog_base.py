# -*- coding: utf-8 -*-

from builtins import object
from PyQt5.QtWidgets import QTabWidget, QWidget, QGroupBox, QLabel, QComboBox, QPushButton, QCheckBox, QListWidget, \
    QTableView, QAbstractItemView, QVBoxLayout, QTextEdit, QDialog, QSizePolicy, QHBoxLayout, QGridLayout, QHeaderView
from PyQt5.QtWidgets import QTextBrowser, QPlainTextEdit, QLineEdit, QToolButton, QApplication
from PyQt5.QtCore import QRect, QMetaObject, Qt, QAbstractTableModel
from PyQt5.QtGui import QFont, QStandardItemModel
from qgis._gui import QgsAuthConfigSelect

_fromUtf8 = lambda s: s


class Ui_WCPSClient(object):
    def setupUi(self, WCPSClient):
        # Parent container
        WCPSClient.setObjectName("WCPSClient")
        WCPSClient.resize(675, 518)

        # Main layout
        main_layout = QVBoxLayout(WCPSClient)

        # Tab widget
        self.tabWidget_WCPSClient = QTabWidget()
        self.tabWidget_WCPSClient.setObjectName("tabWidget_WCPSClient")
        main_layout.addWidget(self.tabWidget_WCPSClient)

        # ---------------------
        # 1. Tab: Server
        # ---------------------
        self.tab_Serv = QWidget()
        self.tab_Serv.setObjectName("tab_Serv")
        self.tabWidget_WCPSClient.addTab(self.tab_Serv, "Server")

        tab_layout = QVBoxLayout(self.tab_Serv)

        # --- GroupBox: Connection controls ---
        self.groupBox = QGroupBox("Connections")
        self.groupBox.setObjectName("groupBox")
        group_layout = QVBoxLayout(self.groupBox)

        self.cmbConnections_Serv = QComboBox()
        self.cmbConnections_Serv.setObjectName("cmbConnections_Serv")
        group_layout.addWidget(self.cmbConnections_Serv)

        btn_row = QHBoxLayout()
        self.btnConnectServer_Serv = QPushButton("Connect")
        self.btnNew_Serv = QPushButton("New")
        self.btnEdit_Serv = QPushButton("Edit")
        self.btnDelete_Serv = QPushButton("Delete")

        btn_row.addWidget(self.btnConnectServer_Serv)
        btn_row.addWidget(self.btnNew_Serv)
        btn_row.addWidget(self.btnEdit_Serv)
        btn_row.addWidget(self.btnDelete_Serv)
        group_layout.addLayout(btn_row)

        tab_layout.addWidget(self.groupBox)

        # --- Label ---
        self.label_2 = QLabel("Server message:")
        font = QFont()
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        tab_layout.addWidget(self.label_2)

        # --- Text browser ---
        self.textBrowser_Serv = QTextBrowser()
        self.textBrowser_Serv.setObjectName("textBrowser_Serv")
        tab_layout.addWidget(self.textBrowser_Serv)

        # --- GroupBox: Username and password ---
        self.groupBox_3 = QGroupBox("Authentication")
        self.groupBox_3.setObjectName("groupBox_3")
        auth_layout = QGridLayout(self.groupBox_3)

        self.label_3 = QLabel("Username:")
        self.label_3.setObjectName("label_3")
        auth_layout.addWidget(self.label_3, 0, 0)

        self.UserNameLine = QLineEdit()
        self.UserNameLine.setObjectName("UserNameLine")
        auth_layout.addWidget(self.UserNameLine, 0, 1)

        self.label_4 = QLabel("Password:")
        self.label_4.setObjectName("label_4")
        auth_layout.addWidget(self.label_4, 1, 0)

        self.PasswordLine = QLineEdit()
        self.PasswordLine.setObjectName("PasswordLine")
        auth_layout.addWidget(self.PasswordLine, 1, 1)

        tab_layout.addWidget(self.groupBox_3)

        # --- Close Button ---
        self.btnClose_Serv = QPushButton("Close")
        self.btnClose_Serv.setObjectName("btnClose_Serv")
        btn_close_layout = QHBoxLayout()
        btn_close_layout.addStretch()
        btn_close_layout.addWidget(self.btnClose_Serv)
        tab_layout.addLayout(btn_close_layout)

        # ---------------------
        # 2. Tab: Visual Query Editor
        # ---------------------
        self.tab_VisualQuery = QWidget()
        self.tab_VisualQuery.setObjectName("tab_VisualQuery")
        self.tab_VisualQuery.setEnabled(False)

        self.tabWidget_WCPSClient.addTab(self.tab_VisualQuery, "Visual Query Editor")

        tab_layout = QVBoxLayout(self.tab_VisualQuery)

        # --- Row: Add/Delete Datacube buttons ---
        btn_datacube_row = QHBoxLayout()
        self.btnAddDatacube = QPushButton("Add Datacube")
        self.btnAddDatacube.setObjectName("btnAddDatacube")
        btn_datacube_row.addWidget(self.btnAddDatacube)

        btn_datacube_row.addStretch()

        self.btnDeleteDatacube = QPushButton("Delete Datacube")
        self.btnDeleteDatacube.setObjectName("btnDeleteDatacube")
        btn_datacube_row.addWidget(self.btnDeleteDatacube)
        tab_layout.addLayout(btn_datacube_row)

        # --- Label and list of datacubes ---
        self.label_5 = QLabel("Selected Datacubes:")
        self.label_5.setObjectName("label_5")
        tab_layout.addWidget(self.label_5)

        self.lstSelectedDatacubes = QListWidget()
        self.lstSelectedDatacubes.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.lstSelectedDatacubes.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.lstSelectedDatacubes.setStyleSheet("color: black;")
        self.lstSelectedDatacubes.setObjectName("lstDatacubes")
        tab_layout.addWidget(self.lstSelectedDatacubes)

        # --- Filter Button (fixed width on left) ---
        filter_row = QHBoxLayout()
        self.btnSetFilter = QPushButton("Set Filter")
        filter_row.addWidget(self.btnSetFilter)
        filter_row.addStretch()  # pushes the button to the left without stretching it
        tab_layout.addLayout(filter_row)

        # --- Label and expression editor ---
        self.label_6 = QLabel("Result Expression:")
        self.label_6.setObjectName("label_6")
        tab_layout.addWidget(self.label_6)

        self.ResultExpression = QPlainTextEdit()
        self.ResultExpression.setObjectName("ResultExpression")
        self.ResultExpression.setPlaceholderText("e.g. ($c.nir - $c.red) / ($c.nir + $c.red)")
        tab_layout.addWidget(self.ResultExpression)

        # --- Label and encoded format ---
        self.label_7 = QLabel("Encoding Format:")
        self.label_7.setObjectName("label_7")
        tab_layout.addWidget(self.label_7)

        self.ResultEncodedFormat = QComboBox()
        self.ResultEncodedFormat.setObjectName("ResultFormat")
        self.ResultEncodedFormat.currentIndexChanged.connect(self.on_encode_result_combobox_changed)
        self.ResultEncodedFormat.setToolTip(
            "Select the encoding output. If none is selected then no encode() exists in generated WCPS query")
        tab_layout.addWidget(self.ResultEncodedFormat)

        # --- Custom format line edit ---
        self.CustomFormatLine = QLineEdit()
        self.CustomFormatLine.setObjectName("CustomFormatLine")
        self.CustomFormatLine.setToolTip(
            "When encoding format is set to custom, then one can enter a server's supported encoding format here")
        tab_layout.addWidget(self.CustomFormatLine)

        # --- Format parameters and evaluate button row ---
        btn_eval_row = QHBoxLayout()
        self.btnFormatParameters = QPushButton("Format Parameters")
        self.btnFormatParameters.setObjectName("btnFormatParameters")
        self.btnFormatParameters.setToolTip(
            "Specify extra parameters for the selected encoding output to be used in WCPS encode()")
        btn_eval_row.addWidget(self.btnFormatParameters)

        btn_eval_row.addStretch()

        self.btnEvaluate = QPushButton("Evaluate")
        self.btnEvaluate.setObjectName("btnEvaluate")
        btn_eval_row.addWidget(self.btnEvaluate)

        tab_layout.addLayout(btn_eval_row)


        # ---------------------
        # 3. Tab: WCPS Query Editor
        # ---------------------
        self.tab_WCPSQuery = QWidget()
        self.tab_WCPSQuery.setEnabled(False)
        self.tabWidget_WCPSClient.addTab(self.tab_WCPSQuery, "WCPS Query Editor")

        # Create layout for the tab
        tab_layout = QVBoxLayout(self.tab_WCPSQuery)

        # --- Group Box Layout ---
        self.groupBox_2 = QGroupBox("Group Box", self.tab_WCPSQuery)
        self.groupBox_2.setObjectName("groupBox_2")
        group_box_layout = QVBoxLayout(self.groupBox_2)

        # --- Plain Text Edit (inside group box) ---
        self.plainTextEdit_PC = QPlainTextEdit(self.groupBox_2)
        self.plainTextEdit_PC.setObjectName("plainTextEdit_PC")
        self.plainTextEdit_PC.setPlaceholderText(
            'e.g. FOR $c in (mean_summer_airtemp) \n       RETURN encode($c, "image/png")')
        group_box_layout.addWidget(self.plainTextEdit_PC)

        tab_layout.addWidget(self.groupBox_2)

        # --- Buttons layout ---
        button_row = QHBoxLayout()

        self.btnStore_Query = QPushButton("Store Query")
        self.btnStore_Query.setObjectName("btnStore_Query")
        button_row.addWidget(self.btnStore_Query)

        self.btnLoad_Query = QPushButton("Load Query")
        self.btnLoad_Query.setObjectName("btnLoad_Query")
        button_row.addWidget(self.btnLoad_Query)

        self.pushButton_PC = QPushButton("Execute")
        self.pushButton_PC.setObjectName("pushButton_PC")
        button_row.addWidget(self.pushButton_PC)

        button_row.addStretch()

        self.btnClose_PC = QPushButton("Close")
        self.btnClose_PC.setObjectName("btnClose_PC")
        button_row.addWidget(self.btnClose_PC)

        tab_layout.addLayout(button_row)

        # ---------------------
        # 4. Tab: Datacubes List
        # ---------------------
        self.tab_CoveragesList = QWidget()
        self.tab_CoveragesList.setEnabled(False)
        self.tabWidget_WCPSClient.addTab(self.tab_CoveragesList, "Coverages List")
        self.tab_CoveragesList.setObjectName("tab_CoveragesList")

        # Create the main layout for the tab
        tab_layout = QVBoxLayout(self.tab_CoveragesList)

        # Create the filter text box
        self.search_by_coverage_id_TextBox = QLineEdit(self)
        self.search_by_coverage_id_TextBox.setPlaceholderText("Search by Datacube Id")
        self.search_by_coverage_id_TextBox.textChanged.connect(self.on_search_by_coverage_id_in_coverages_list_table_changed)
        tab_layout.addWidget(self.search_by_coverage_id_TextBox)

        # --- Table View ---
        self.coverages_list_tableView = QTableView(self.tab_CoveragesList)
        self.coverages_list_tableView.setObjectName("tableView")
        self.coverages_list_tableView.setWordWrap(False)
        self.coverages_list_tableView.setAlternatingRowColors(False)
        self.coverages_list_tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # Set selection behavior
        self.coverages_list_tableView.setSelectionBehavior(QAbstractItemView.SelectRows)

        # Add table view to the layout
        tab_layout.addWidget(self.coverages_list_tableView)

        # Set the layout for the tab
        self.tab_CoveragesList.setLayout(tab_layout)

        self.coverages_list_tableView.horizontalHeader().setStretchLastSection(True)
        self.coverages_list_tableView.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        ##############  ---------------- End of setting tabs layout

        self.retranslateUi(WCPSClient)
        self.tabWidget_WCPSClient.setCurrentIndex(2)

        self.btnClose_Serv.clicked.connect(WCPSClient.close)
        self.btnClose_PC.clicked.connect(WCPSClient.close)
        self.btnConnectServer_Serv.clicked.connect(WCPSClient.connectServer)
        self.btnNew_Serv.clicked.connect(WCPSClient.newServer)
        self.btnEdit_Serv.clicked.connect(WCPSClient.editServer)
        self.btnDelete_Serv.clicked.connect(WCPSClient.deleteServer)
        self.pushButton_PC.clicked.connect(WCPSClient.exeProcessCoverage)
        self.btnLoad_Query.clicked.connect(WCPSClient.loadQuery)
        self.btnStore_Query.clicked.connect(WCPSClient.storeQuery)
        self.btnAddDatacube.clicked.connect(WCPSClient.select_datacubes_handler)
        self.btnDeleteDatacube.clicked.connect(WCPSClient.unselect_datacubes_handler)
        self.btnSetFilter.clicked.connect(WCPSClient.set_where_clause_handler)
        self.btnFormatParameters.clicked.connect(WCPSClient.set_encode_extra_parameters)
        self.btnEvaluate.clicked.connect(WCPSClient.generate_wcps_query)
        QMetaObject.connectSlotsByName(WCPSClient)

    def retranslateUi(self, WCPSClient):
        WCPSClient.setWindowTitle(QApplication.translate("WCPSClient", "WCPS datacube query", None))

        self.groupBox.setTitle(QApplication.translate("WCPSClient", "Server Connections:", None))
        self.btnConnectServer_Serv.setText(QApplication.translate("WCPSClient", "Connect", None))
        self.btnNew_Serv.setText(QApplication.translate("WCPSClient", "New", None))
        self.btnEdit_Serv.setText(QApplication.translate("WCPSClient", "Edit", None))
        self.btnDelete_Serv.setText(QApplication.translate("WCPSClient", "Delete", None))
        self.label_2.setText(QApplication.translate("WCPSClient", "Connecting Server Log", None))
        self.groupBox_3.setTitle(QApplication.translate("WCPSClient", "Rasdaman User Credentials", None))
        self.label_3.setText(QApplication.translate("WCPSClient", "Username", None))
        self.label_4.setText(QApplication.translate("WCPSClient", "Password", None))
        self.btnClose_Serv.setText(QApplication.translate("WCPSClient", "Close", None))
        self.btnClose_Serv.setToolTip("Close the plugin window")

        self.tabWidget_WCPSClient.setTabText(self.tabWidget_WCPSClient.indexOf(self.tab_Serv),
                                             QApplication.translate("WCPSClient", "Server", None))
        self.groupBox_2.setTitle(QApplication.translate("WCPSClient", "WCPS Query Editor", None))
        self.pushButton_PC.setText(QApplication.translate("WCPSClient", "Submit", None))
        self.pushButton_PC.setToolTip("Send WCPS query to server to process and get response")

        self.btnClose_PC.setText(QApplication.translate("WCPSClient", "Close", None))
        self.btnClose_PC.setToolTip("Close the plugin window")

        self.btnLoad_Query.setText(QApplication.translate("WCPSClient", "Load Query", None))
        self.btnLoad_Query.setToolTip("Load a WCPS query stored in a local text file to the editing text editor")

        self.tabWidget_WCPSClient.setTabText(self.tabWidget_WCPSClient.indexOf(self.tab_WCPSQuery),
                                             QApplication.translate("WCPSClient", "WCPS Query Editor", None))
        self.btnStore_Query.setText(QApplication.translate("WCPSClient", "Store Query", None))
        self.btnStore_Query.setToolTip("Store the current editing WCPS query to a local file")

        self.tabWidget_WCPSClient.setTabText(self.tabWidget_WCPSClient.indexOf(self.tab_CoveragesList),
                                             QApplication.translate("WCPSClient", "Datacubes List", None))

        self.tab_VisualQuery.setWindowTitle(QApplication.translate("WCPSClient", "Visual Query Editor", None))
        self.btnAddDatacube.setText(QApplication.translate("WCPSClient", "Select datacube(s)", None))
        self.btnAddDatacube.setToolTip("Select datacube(s) to be used in FOR clause in WCPS query")

        self.btnDeleteDatacube.setText(QApplication.translate("WCPSClient", "Clear Selected", None))
        self.btnDeleteDatacube.setToolTip("Unselect all selected datacubes used in FOR clause in WCPS query")

        self.label_5.setText(QApplication.translate("WCPSClient", "Selected Datacubes for FOR clause", None))
        self.btnSetFilter.setText(QApplication.translate("WCPSClient", "Set filter condition", None))
        self.btnSetFilter.setToolTip("Set condition for WHERE clause in WCPS query")

        self.label_6.setText(QApplication.translate("WCPSClient",
                                                    "Result expression", None))

        self.label_7.setText(QApplication.translate("WCPSClient", "Result encoded format", None))

        self.btnFormatParameters.setText(QApplication.translate("WCPSClient", "Set format parameters", None))
        self.btnEvaluate.setText(QApplication.translate("WCPSClient", "Evaluate", None))

    def on_encode_result_combobox_changed(self, index):
        value = self.ResultEncodedFormat.itemText(index)
        if value == "custom":
            self.CustomFormatLine.setEnabled(True)
            self.CustomFormatLine.setPlaceholderText("e.g. application/gml+xml")
        else:
            self.CustomFormatLine.setEnabled(False)
            self.CustomFormatLine.setPlaceholderText("")

        if value == "none":
            self.btnFormatParameters.setEnabled(False)
        else:
            self.btnFormatParameters.setEnabled(True)

    def on_search_by_coverage_id_in_coverages_list_table_changed(self):
        """
        # When searching coverages by pattern in Datacubes List table
        """
        filter_text = self.search_by_coverage_id_TextBox.text()
        self.coverages_list_table_model.setFilterText(filter_text)


class CustomInputDialog(QDialog):
    def __init__(self, window_title, text_holder_content, input_text_for_textbox=""):
        super().__init__()

        self.setWindowTitle(window_title)

        # Set up layout
        layout = QVBoxLayout()

        # Create QTextEdit widget for multiline text input
        self.text_edit = QTextEdit(self)
        self.text_edit.setPlaceholderText(text_holder_content)
        self.text_edit.setText(input_text_for_textbox)

        # Add text edit and button to layout
        layout.addWidget(self.text_edit)

        # Create a horizontal layout for the button
        button_layout = QHBoxLayout()

        # Create submit button
        self.submit_button = QPushButton("Submit", self)

        # Set button size policy to prevent stretching horizontally
        size_policy = self.submit_button.sizePolicy()
        size_policy.setHorizontalPolicy(QSizePolicy.Fixed)  # Prevent horizontal stretching
        size_policy.setVerticalPolicy(QSizePolicy.Preferred)  # Allow vertical stretching
        self.submit_button.setSizePolicy(size_policy)

        # Add a stretchable space before the button, pushing it to the right
        button_layout.addStretch(1)  # Add stretch space to the left
        button_layout.addWidget(self.submit_button)  # Add the button to the layout

        # Set the button layout to the main layout
        layout.addLayout(button_layout)

        # Connect button to function
        self.submit_button.clicked.connect(self.submit_text)

        # Variable to store the input text
        self.input_text = None

        self.setLayout(layout)

        self.resize(600, 300)  # Set initial size (width x height)

    def submit_text(self):
        # Get the input text and print it (or process it as needed)
        self.input_text = self.text_edit.toPlainText()
        self.accept()  # Close the dialog

    def get_input_text(self):
        return self.input_text  # Return the entered text


class CoveragesListTableModel(QAbstractTableModel):
    """
    This class is subclass of QAbstractTableModel which can show coverages in tab Datacubes List much faster
    """
    def __init__(self, data, headers):
        super().__init__()
        self._all_data = data  # store original data
        self._data = data[:]   # filtered data, starts as full copy
        self._headers = headers
        self._filter_text = ""

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._headers) + 1  # Add one extra column for row numbers

    def data(self, index, role):
        if role == Qt.DisplayRole:
            if index.column() == 0:  # First column shows the row number
                return str(index.row() + 1)  # Row numbers start from 1
            else:
                return self._data[index.row()][index.column() - 1]  # Subtract 1 to get the actual data
        return None

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if section == 0:
                    return "No."  # The header for the row number column
                else:
                    return self._headers[section - 1]  # Subtract 1 to match the original headers
        return None

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled  # Read-only

    def setFilterText(self, text):
        self._filter_text = text.lower()
        self._data = []

        # Filter rows based on the second column (index 0)
        for row in self._all_data:
            coverage_id = str(row[0].lower())  # Assuming you filter based on the first column (coverage_id)
            if self._filter_text in coverage_id:
                self._data.append(row)

        # Update the model with the filtered data
        self.beginResetModel()  # Notify that the model data is being reset
        self.endResetModel()  # Notify that the reset is complete
