from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QComboBox, QLineEdit, QLabel
)

from filters import FilterCondition, OPERATORS, build_where
from ui.filter_row import FilterRow


class FilterBuilderDialog(QWidget):

    def __init__(self, db, table_name):
        super().__init__()

        self.db = db
        self.table_name = table_name
        self.rows = []

        self.setWindowTitle("Filter Builder")
        self.resize(900, 600)

        self.layout = QVBoxLayout()

        self.add_btn = QPushButton("Add Filter")
        self.apply_btn = QPushButton("Apply Filters")

        self.add_btn.clicked.connect(self.add_filter)
        self.apply_btn.clicked.connect(self.apply)

        self.layout.addWidget(self.add_btn)
        self.layout.addWidget(self.apply_btn)

        self.filter_area = QVBoxLayout()
        self.layout.addLayout(self.filter_area)

        self.setLayout(self.layout)

        self.columns = self.db.get_columns(self.table_name)

    def add_filter(self):
        row = FilterRow(self.columns)
        self.rows.append(row)
        self.filter_area.addWidget(row)

    def collect(self):

        filters = []

        for r in self.rows:
            filters.append(
                FilterCondition(
                    field=r.field.currentText(),
                    operator=r.op.currentText(),
                    value1=r.v1.text(),
                    value2=r.v2.text(),
                    logical_op=r.logic.currentText()
                )
            )

        return filters

    def apply(self):

        where, params = build_where(self.collect())

        sql = f'SELECT * FROM "{self.table_name}" {where}'

        rows, headers = self.db.query(sql, params)

        print("RESULTS:", len(rows))