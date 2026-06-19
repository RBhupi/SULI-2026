from PyQt5.QtWidgets import QWidget, QHBoxLayout, QComboBox, QLineEdit

from filters import OPERATORS


class FilterRow(QWidget):

    def __init__(self, columns):
        super().__init__()

        layout = QHBoxLayout()

        self.logic = QComboBox()
        self.logic.addItems(["AND", "OR"])

        self.field = QComboBox()
        self.field.addItems(columns)

        self.op = QComboBox()
        self.op.addItems(OPERATORS)

        self.v1 = QLineEdit()
        self.v2 = QLineEdit()

        layout.addWidget(self.logic)
        layout.addWidget(self.field)
        layout.addWidget(self.op)
        layout.addWidget(self.v1)
        layout.addWidget(self.v2)

        self.setLayout(layout)