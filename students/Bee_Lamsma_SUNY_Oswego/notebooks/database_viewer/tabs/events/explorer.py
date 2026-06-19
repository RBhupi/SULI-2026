from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QTextEdit,
    QTableWidget,
    QTableWidgetItem,
    QDoubleSpinBox,
    QGridLayout,
)

from PyQt5.QtCore import Qt, pyqtSignal

from widgets import NumericTableWidgetItem

class EventExplorerTab(QWidget):

    cellSelected = pyqtSignal(str)
    def __init__(self, db, engine):
        super().__init__()

        self.db = db
        self.engine = engine
        self.cell_filter = None
        self.filter_label = QLabel("Showing all cells")

        self.available_columns = [
            "event_type",
            "source_cell_uid",
            "target_cell_uid",
            "source_scan_time",
            "target_scan_time",
            "cost",
        ]
        
        self.column_selector = QListWidget()

        for col in self.available_columns:
            item = QListWidgetItem(col)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Checked)
            self.column_selector.addItem(item)

        #
        # Widgets
        #

        self.event_table = QTableWidget()
        self.event_table.setSortingEnabled(True)

        self.detail_text = QTextEdit()
        self.detail_text.setReadOnly(True)

        self.event_selector = QListWidget()

        #
        # Numeric Filters
        #
        
        self.cost_min = QDoubleSpinBox()
        self.cost_max = QDoubleSpinBox()
        
        self.cost_min.setRange(-999999, 999999)
        self.cost_max.setRange(-999999, 999999)
        
        self.cost_max.setValue(999999)
        
        self.apply_filter_button = QPushButton(
            "Apply Filters"
        )
        
        self.apply_filter_button.clicked.connect(
            self.reload_tables
        )
        
        self.clear_numeric_button = QPushButton(
            "Clear Numeric Filters"
        )
        
        self.clear_numeric_button.clicked.connect(
            self.clear_numeric_filters
        )

        for event_type in [
            "INITIATION",
            "CONTINUE",
            "MERGE",
            "SPLIT",
            "TERMINATION",
        ]:
            item = QListWidgetItem(event_type)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Checked)
            self.event_selector.addItem(item)

        self.refresh_button = QPushButton("Apply Filter")
        self.refresh_button.clicked.connect(self.reload_tables)
        self.clear_button = QPushButton("Clear Cell Filter")
        self.clear_button.clicked.connect(self.clear_filter)

        #
        # Layout
        #

        main_layout = QVBoxLayout(self)

        top_layout = QHBoxLayout()

        chooser_layout = QVBoxLayout()
        chooser_layout.addWidget(QLabel("Event Types"))
        chooser_layout.addWidget(self.event_selector)
        chooser_layout.addWidget(self.refresh_button)
        self.filter_label = QLabel("Showing all cells")
        chooser_layout.addWidget(self.filter_label)
        self.clear_button = QPushButton("Clear Cell Filter")
        self.clear_button.clicked.connect(self.clear_filter)
        chooser_layout.addWidget(self.clear_button)
        filter_grid = QGridLayout()
        
        filter_grid.addWidget(
            QLabel("Cost Min"),
            0, 0
        )
        
        filter_grid.addWidget(
            self.cost_min,
            0, 1
        )
        
        filter_grid.addWidget(
            QLabel("Cost Max"),
            0, 2
        )
        
        filter_grid.addWidget(
            self.cost_max,
            0, 3
        )
        
        chooser_layout.addWidget(
            QLabel("Numeric Filters")
        )
        
        chooser_layout.addLayout(
            filter_grid
        )
        
        chooser_layout.addWidget(
            self.apply_filter_button
        )
        
        chooser_layout.addWidget(
            self.clear_numeric_button
        )
        top_layout.addLayout(chooser_layout,1)
        top_layout.addWidget(self.detail_text,1)
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.event_table,3)
        self.event_table.itemSelectionChanged.connect(self.event_selected)

        self.reload_tables()

    def reload_tables(self):

        self.event_table.setSortingEnabled(False)
        
        self.event_table.clear()
        self.event_table.setRowCount(0)
        self.event_table.setColumnCount(0)
        
        columns = self.selected_columns()

        if not columns:
            return
    
        column_sql = ",".join(columns)

        event_types = self.selected_event_types()

        if not event_types:
            return
        
        event_placeholders = ",".join(
            ["?"] * len(event_types)
        )
        
        if self.cell_filter:
        
            sql = f"""
            SELECT {column_sql}
            FROM cell_events
            WHERE
            event_type IN ({event_placeholders})
            AND
            (
                source_cell_uid = ?
                OR target_cell_uid = ?
            )
            AND
            (
                cost IS NULL
                OR (
                    cost >= ?
                    AND cost <= ?
                )
            )
            LIMIT 1000
            """
        
            rows = self.db.execute(
                sql,
                [
                    *event_types,
                
                    self.cell_filter,
                    self.cell_filter,
                
                    self.cost_min.value(),
                    self.cost_max.value(),
                ]
            )
        
        else:
        
            sql = f"""
            SELECT {column_sql}
            FROM cell_events
            WHERE
            event_type IN ({event_placeholders})
            AND
            (
                cost IS NULL
                OR (
                    cost >= ?
                    AND cost <= ?
                )
            )
            LIMIT 1000
            """
        
            rows = self.db.execute(
                sql,
                [
                    *event_types,
                
                    self.cost_min.value(),
                    self.cost_max.value(),
                ]
            )
    
        headers = columns
    
        self.event_table.setColumnCount(len(headers))
        self.event_table.setRowCount(len(rows))
        self.event_table.setHorizontalHeaderLabels(headers)
    
        for r, row in enumerate(rows):
    
            for c, value in enumerate(row):
    
                self.event_table.setItem(
                    r,
                    c,
                    NumericTableWidgetItem(
                        str(value)
                    )
                )
    
        self.event_table.resizeColumnsToContents()
        self.event_table.setSortingEnabled(True)

        if self.cell_filter:

            self.filter_label.setText(
                f"Cell: {self.cell_filter} | "
                f"Cost {self.cost_min.value():.1f} - "
                f"{self.cost_max.value():.1f}"
            )
        
        else:
        
            self.filter_label.setText(
                f"Showing all cells | "
                f"Cost {self.cost_min.value():.1f} - "
                f"{self.cost_max.value():.1f}"
            )

        print(f"Loaded {len(rows)} events")

    def event_selected(self):
    
        row = self.event_table.currentRow()
    
        if row < 0:
            return
    
        values = {}
    
        for c in range(self.event_table.columnCount()):
    
            header_item = self.event_table.horizontalHeaderItem(c)
    
            if header_item is None:
                continue
    
            header = header_item.text()
    
            item = self.event_table.item(row, c)
    
            values[header] = (
                item.text() if item else ""
            )

        target_uid = values.get(
            "target_cell_uid",
            ""
        )
        
        if target_uid:
            self.cellSelected.emit(target_uid)
    
        text = []
    
        #
        # Header
        #
    
        text.append(
            f"Event Type: {values.get('event_type', '')}"
        )
    
        text.append(
            f"Target Cell: {values.get('target_cell_uid', '')}"
        )
    
        text.append("")
    
        #
        # Event Summary
        #
    
        text.append("Event Summary")
        text.append("-------------")
    
        text.append(
            f"Source Cell: {values.get('source_cell_uid', '')}"
        )
    
        text.append(
            f"Target Cell: {values.get('target_cell_uid', '')}"
        )
    
        text.append(
            f"Source Scan: {values.get('source_scan_time', '')}"
        )
    
        text.append(
            f"Target Scan: {values.get('target_scan_time', '')}"
        )
    
        text.append(
            f"Cost: {values.get('cost', '')}"
        )
    
        text.append("")
    
        #
        # Selected Attributes
        #
    
        text.append("Selected Attributes")
        text.append("-------------------")
    
        for name, value in values.items():
    
            text.append(
                f"{name}: {value}"
            )
    
        self.detail_text.setPlainText(
            "\n".join(text)
        )

    def set_cell_filter(self, cell_uid):
    
        self.cell_filter = cell_uid
    
        self.reload_tables()

    def clear_filter(self):

        self.cell_filter = None
    
        self.reload_tables()

    def clear_numeric_filters(self):

        self.cost_min.setValue(-999999)
        self.cost_max.setValue(999999)
    
        self.reload_tables()

    def selected_columns(self):

        cols = []
    
        for i in range(self.column_selector.count()):
    
            item = self.column_selector.item(i)
    
            if item.checkState() == Qt.Checked:
                cols.append(item.text())
    
        return cols

    def selected_event_types(self):
    
        types = []
    
        for i in range(self.event_selector.count()):
    
            item = self.event_selector.item(i)
    
            if item.checkState() == Qt.Checked:
                types.append(item.text())
    
        return types