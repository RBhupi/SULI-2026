import json
import os

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QListWidget,
    QPushButton, QInputDialog, QMessageBox
)


class PresetManagerDialog(QWidget):

    FILE = "resources/presets.json"

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Preset Manager")
        self.resize(500, 400)

        layout = QVBoxLayout()

        self.list = QListWidget()

        self.save_btn = QPushButton("Save Preset")
        self.delete_btn = QPushButton("Delete Preset")

        self.save_btn.clicked.connect(self.save)
        self.delete_btn.clicked.connect(self.delete)

        layout.addWidget(self.list)
        layout.addWidget(self.save_btn)
        layout.addWidget(self.delete_btn)

        self.setLayout(layout)

        self.load()

    def load(self):

        if not os.path.exists(self.FILE):
            return

        with open(self.FILE, "r") as f:
            data = json.load(f)

        self.list.clear()
        self.list.addItems(list(data.keys()))

    def save(self):

        name, ok = QInputDialog.getText(self, "Preset Name", "Enter name:")

        if not ok:
            return

        data = self._read()

        data[name] = {
            "example": "filter_config_here"
        }

        self._write(data)

        self.load()

    def delete(self):

        item = self.list.currentItem()
        if not item:
            return

        data = self._read()
        data.pop(item.text(), None)

        self._write(data)
        self.load()

    def _read(self):

        if not os.path.exists(self.FILE):
            return {}

        with open(self.FILE, "r") as f:
            return json.load(f)

    def _write(self, data):

        with open(self.FILE, "w") as f:
            json.dump(data, f, indent=4)