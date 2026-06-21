from PyQt5.QtWidgets import QTableWidgetItem

class NumericTableWidgetItem(QTableWidgetItem):

    def __lt__(self, other):

        try:
            return float(self.text()) < float(other.text())

        except (ValueError, TypeError):

            return self.text() < other.text()