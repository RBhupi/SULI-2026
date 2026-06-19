from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QFileDialog
)

from exports.exporter import export_csv, export_excel


class ExportDialog(QWidget):

    def __init__(self, rows, headers):
        super().__init__()

        self.rows = rows
        self.headers = headers

        self.setWindowTitle("Export Data")
        self.resize(300, 200)

        self.build_ui()

    def build_ui(self):

        layout = QVBoxLayout()

        self.csv_btn = QPushButton("Export CSV")
        self.excel_btn = QPushButton("Export Excel")

        self.csv_btn.clicked.connect(self.export_csv)
        self.excel_btn.clicked.connect(self.export_excel)

        layout.addWidget(self.csv_btn)
        layout.addWidget(self.excel_btn)

        self.setLayout(layout)

    def export_csv(self):

        path, _ = QFileDialog.getSaveFileName(self, "Save CSV", "", "CSV (*.csv)")
        if path:
            export_csv(self.rows, self.headers, path)

    def export_excel(self):

        path, _ = QFileDialog.getSaveFileName(self, "Save Excel", "", "Excel (*.xlsx)")
        if path:
            export_excel(self.rows, self.headers, path)