from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QComboBox, QPushButton, QLabel,
    QTableWidget, QTableWidgetItem, QSpinBox
)

from workers import QueryWorker
from PyQt5.QtCore import pyqtSignal
from widgets import NumericTableWidgetItem

class DatabaseExplorerTab(QWidget):

    cellSelected = pyqtSignal(str)

    def __init__(self, db):
        super().__init__()
        self.db = db
        self.worker = None

        self.page = 0
        self.page_size = 1000

        self.sort_col = None
        self.sort_order = "ASC"

        self.headers = []

        self.build_ui()
        self.reload_tables()   

    def build_ui(self):

        layout = QVBoxLayout()

        top = QHBoxLayout()
        
        self.table_selector = QComboBox()

        self.table_selector.currentIndexChanged.connect(self.table_changed)
        self.refresh = QPushButton("Load")
        
        self.prev_btn = QPushButton("Previous")
        self.next_btn = QPushButton("Next")
        
        self.page_label = QLabel("Page 1")
        
        self.page_size_spin = QSpinBox()
        self.page_size_spin.setRange(100, 10000)
        self.page_size_spin.setSingleStep(100)
        self.page_size_spin.setValue(1000)
        
        self.refresh.clicked.connect(self.load)
        self.prev_btn.clicked.connect(self.prev_page)
        self.next_btn.clicked.connect(self.next_page)
        self.page_size_spin.valueChanged.connect(self.change_page_size)
        
        top.addWidget(QLabel("Table"))
        top.addWidget(self.table_selector)
        
        top.addWidget(QLabel("Rows"))
        top.addWidget(self.page_size_spin)
        
        top.addWidget(self.refresh)
        
        top.addWidget(self.prev_btn)
        top.addWidget(self.next_btn)
        
        top.addWidget(self.page_label)
        

        self.refresh.clicked.connect(self.load)

        top.addWidget(QLabel("Table"))
        top.addWidget(self.table_selector)
        top.addWidget(self.refresh)

        layout.addLayout(top)

        self.grid = QTableWidget()
        self.grid.setSortingEnabled(True)
        layout.addWidget(self.grid)
        self.grid.itemSelectionChanged.connect(self.row_selected)

        self.setLayout(layout)


    def build_sql(self):
    
        t = self.table_selector.currentText()
    
        print("Current table:", t)
    
        if not t:
            return None
    
        sql = f'SELECT * FROM "{t}"'
    
        if self.sort_col:
            sql += f' ORDER BY "{self.sort_col}" {self.sort_order}'
    
        sql += f" LIMIT {self.page_size} OFFSET {self.page * self.page_size}"
    
        print(sql)
    
        return sql

    def load(self):
    
        if self.worker is not None and self.worker.isRunning():
            return
    
        self.refresh.setEnabled(False)
    
        sql = self.build_sql()
    
        if not sql:
            self.refresh.setEnabled(True)
            return
    
        self.worker = QueryWorker(self.db, sql)
    
        self.worker.completed.connect(self.render)
        self.worker.failed.connect(print)
    
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.finished.connect(self.query_finished)
    
        self.worker.start()
    
    
    def query_finished(self):
        self.refresh.setEnabled(True)
        self.worker = None

    def reload_tables(self):
        tables = self.db.get_tables()
    
        print("Loaded tables:", tables)
    
        self.table_selector.clear()
        self.table_selector.addItems(tables)
    
        if tables:
            self.load()

    def render(self, rows, headers):
        print(f"Rendering {len(rows)} rows")
    
        self.headers = headers
        
        self.grid.setColumnCount(len(headers))
        self.grid.setRowCount(len(rows))
        self.grid.setHorizontalHeaderLabels(headers)

        self.grid.setSortingEnabled(False)
    
        for r, row in enumerate(rows):
            for c, v in enumerate(row):
                self.grid.setItem(
                    r,
                    c,
                    NumericTableWidgetItem(str(v))
                )

        self.grid.setSortingEnabled(True)
    
        # Update page display
        self.page_label.setText(f"Page {self.page + 1}")
    
        # Enable/disable navigation buttons
        self.prev_btn.setEnabled(self.page > 0)
    
        # If we got fewer rows than page_size, we're on the last page
        self.next_btn.setEnabled(len(rows) >= self.page_size)

        self.last_row_count = len(rows)

        self.page_label.setText(f"Page {self.page + 1}")
    
        self.prev_btn.setEnabled(self.page > 0)
        self.next_btn.setEnabled(len(rows) >= self.page_size)

    def change_page_size(self):
        self.page_size = self.page_size_spin.value()
        self.page = 0
        self.update_page_label()
        self.load()

    def update_page_label(self):
        self.page_label.setText(f"Page {self.page + 1}")
    
    def next_page(self):
    
        if hasattr(self, "last_row_count") and self.last_row_count < self.page_size:
            return
    
        self.page += 1
        self.page_label.setText(f"Page {self.page + 1}")
        self.load()
    
    def prev_page(self):
        if self.page > 0:
            self.page -= 1
            self.update_page_label()
            self.load()
            
    def table_changed(self):
        self.page = 0
        self.update_page_label()
        self.load()

    def row_selected(self):
        row = self.grid.currentRow()
    
        if row < 0:
            return
    
        cell_uid = None
    
        for c in range(self.grid.columnCount()):
    
            header = self.grid.horizontalHeaderItem(c)
    
            if not header:
                continue
    
            if header.text() == "cell_uid":
    
                item = self.grid.item(row, c)
    
                if item:
                    cell_uid = item.text()
    
                break
    
        if cell_uid:
    
            print("Database selected cell:", cell_uid)
    
            self.cellSelected.emit(cell_uid)