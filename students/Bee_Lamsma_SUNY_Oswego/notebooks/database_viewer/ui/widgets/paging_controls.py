from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel


class PagingControls(QWidget):

    def __init__(self):
        super().__init__()

        self.page = 0

        layout = QHBoxLayout()

        self.prev_btn = QPushButton("Prev")
        self.next_btn = QPushButton("Next")

        self.label = QLabel("Page 0")

        layout.addWidget(self.prev_btn)
        layout.addWidget(self.label)
        layout.addWidget(self.next_btn)

        self.setLayout(layout)

    def set_page(self, page):
        self.page = page
        self.label.setText(f"Page {page}")