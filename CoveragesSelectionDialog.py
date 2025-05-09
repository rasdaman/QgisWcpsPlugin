from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QDialog, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QLineEdit, QCheckBox, \
    QWidget, QHBoxLayout, QSizePolicy, QHeaderView, QDialogButtonBox


class CoverageSelectionDialog(QDialog):
    def __init__(self, coverages, parent=None):
        super(CoverageSelectionDialog, self).__init__(parent)
        self.setWindowTitle("Select Datacube(s) to be used in WCPS FOR clause")

        self.resize(800, 600)
        self.layout = QVBoxLayout(self)

        # Add search box
        self.search_box = QLineEdit(self)
        self.search_box.setPlaceholderText("Search by Datacube Id")
        self.layout.addWidget(self.search_box)
        self.search_box.textChanged.connect(self.search)

        self.coverages = coverages
        # Return the selected coverages after clicking on OK button
        # Store coverage id per selected checkbox
        self.selected_data = []

        self.table = TableWithCheckboxes(coverages)
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout.addWidget(self.table)

        # Create the button box
        self.button_box = QDialogButtonBox(self)
        self.button_box.setStandardButtons(QDialogButtonBox.Ok)

        # Add the button box to the layout
        self.layout.addWidget(self.button_box)

        # Connect the button signals to respective slots
        self.button_box.accepted.connect(self.accept)

    def accept(self):
        """Handle Accept action."""
        super().accept()
        self.selected_data = []
        for row_index in self.table.new_checked_check_boxes:
            coverage_id = self.table.coverages[row_index]["CoverageId"]
            self.selected_data.append(coverage_id)

    def get_selected_coverage_ids(self):
        """
        Return the selected coverage ids in the table
        """
        selected_data = self.selected_data
        return selected_data

    def closeEvent(self, event):
        """
        When closing the dialog by clicking on X button on top, then all new checked / unchecked checkboxes
        must be rollback
        """
        for index in self.table.new_checked_check_boxes:
            self.coverages[index]["checked"] = False

        for index in self.table.new_unchecked_check_boxes:
            self.coverages[index]["checked"] = True


    ################ Handle search rows by coverage Id

    def search(self):
        search_text = self.search_box.text().lower()  # Case-insensitive search
        self.filter_rows(search_text)

    def filter_rows(self, search_text=""):
        coverage_id_column_index = 1
        # Loop through each row and show/hide based on search query
        for row in range(self.table.rowCount()):
            description_text = self.table.item(row, coverage_id_column_index).text().lower()

            # If search text is in description, show the row, else hide it
            if search_text in description_text:
                self.table.setRowHidden(row, False)  # Show the row
            else:
                self.table.setRowHidden(row, True)   # Hide the row


class TableWithCheckboxes(QTableWidget):

    def __init__(self, coverages):
        self.coverages = coverages

        column_names = ["Select", "Datacube"]
        number_of_columns = len(column_names)
        number_of_rows = len(coverages)

        super().__init__(number_of_rows, number_of_columns)
        self.setHorizontalHeaderLabels(column_names)

        self.checkboxes = []  # To keep track of each checkbox
        self.checkbox_to_row_dict = {}

        # Set the Datacube column to stretch
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        # Set the Select column to fit the checkbox width
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.Interactive)

        # Store the indices of new checked / unchecked checkboxes to rollback in case closing the dialog by clicking
        # on X button
        self.new_checked_check_boxes = []
        self.new_unchecked_check_boxes = []

        # Connect cellClicked signal to custom function
        self.cellClicked.connect(self.on_cell_clicked)

        for i in range(number_of_rows):
            # Checkbox
            checkbox = QCheckBox()
            checkbox.setChecked(coverages[i]["checked"])
            checkbox.stateChanged.connect(self.handle_checkbox_event)
            self.checkboxes.append(checkbox)
            self.checkbox_to_row_dict[checkbox] = i

            container = QWidget()
            layout = QHBoxLayout(container)
            layout.addWidget(checkbox)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setAlignment(Qt.AlignCenter)
            self.setCellWidget(i, 0, container)

            # Read-only coverage id
            coverage_id = coverages[i]["CoverageId"]
            name_item = QTableWidgetItem(coverage_id)
            name_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.setItem(i, 1, name_item)

        self.highlight_checked_rows_after_loading()

    ################# Handle check / uncheck checkboxes to select / unselect coverage Ids

    def highlight_checked_rows_after_loading(self):
        """
        All selected coverages need to be highlighted when loading dialog
        """
        for i, coverage in enumerate(self.coverages):
            if coverage["checked"]:
                self.handle_highlight_row_when_checkbox_changed(self.checkboxes[i], i)

    def handle_checkbox_event(self):
        checkbox = self.sender()
        if isinstance(checkbox, QCheckBox):
            row_index = self.checkbox_to_row_dict[checkbox]

            self.handle_highlight_row_when_checkbox_changed(checkbox, row_index)

    def handle_highlight_row_when_checkbox_changed(self, checkbox, row_index):
        """
        Handle highlight / unhighlight when the checkbox is checked / unchecked
        """
        if checkbox.isChecked():
            self.new_checked_check_boxes.append(row_index)
            try:
                self.new_unchecked_check_boxes.remove(row_index)
            except ValueError:
                pass

            self.coverages[row_index]["checked"] = True
            self.__highlight_row(row_index, "yellow")

        else:
            self.new_unchecked_check_boxes.append(row_index)
            try:
                self.new_checked_check_boxes.remove(row_index)
            except ValueError:
                pass

            self.coverages[row_index]["checked"] = False
            self.__highlight_row(row_index, "none")

    def on_cell_clicked(self, row_index, col_index):
        # Check if the clicked column is the one with checkboxes (0 index)
        if col_index == 0:  # Checkbox is in the first column (index 0)
            checkbox_row_cell = self.cellWidget(row_index, col_index)  # Get the QCheckBox widget
            checkbox = checkbox_row_cell.findChild(QCheckBox)
            # Toggle the checkbox state (checked/un-checked)
            checkbox.setChecked(not checkbox.isChecked())

            self.handle_highlight_row_when_checkbox_changed(checkbox, row_index)

    def __highlight_row(self, index, color):
        # Yellow color
        back_ground_color = QColor(255, 255, 0)
        if color == "none":
            back_ground_color = QColor(255, 255, 255)

        # Highlight the checkbox cell and the entire row
        for col in range(self.columnCount()):
            if col == 0:  # Checkbox column (0 index)
                checkbox_cell = self.cellWidget(index, col)  # Get checkbox widget
                checkbox_cell.setStyleSheet(
                    f"background-color: {color}")  # Set background color for checkbox cell
            else:  # Highlight other columns in the row
                item = self.item(index, col)
                item.setBackground(back_ground_color)