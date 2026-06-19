from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt


class TableView(QTableWidget):

    def __init__(self):
        super().__init__()

        self.headers = []

        self.setSortingEnabled(True)

    def load_data(self, rows, headers):

        self.headers = headers

        self.setColumnCount(len(headers))
        self.setRowCount(len(rows))
        self.setHorizontalHeaderLabels(headers)

        for r, row in enumerate(rows):
            for c, v in enumerate(row):
                item = QTableWidgetItem(str(v))

                # numeric sorting support
                try:
                    item.setData(Qt.UserRole, float(v))
                except:
                    pass

                self.setItem(r, c, item)