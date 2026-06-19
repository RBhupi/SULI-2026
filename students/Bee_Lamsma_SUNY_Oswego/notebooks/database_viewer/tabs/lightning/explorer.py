from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QTextEdit,
    QTableWidget,
    QTableWidgetItem,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QDoubleSpinBox,
    QGridLayout,
)

from PyQt5.QtCore import Qt, pyqtSignal

from widgets import NumericTableWidgetItem

class LightningExplorerTab(QWidget):

    cellSelected = pyqtSignal(str)
    def __init__(self, db, engine):
        super().__init__()
        
        self.db = db
        self.engine = engine
        self.cell_filter = None

        print(self.db.get_columns("xlma_stat_scan"))
        
        #
        # Widgets
        #

        self.lightning_table = QTableWidget()
        self.lightning_table.setSortingEnabled(True)

        self.detail_text = QTextEdit()
        self.detail_text.setReadOnly(True)

        #
        # Numeric Filters
        #
        
        self.flash_min = QDoubleSpinBox()
        self.flash_max = QDoubleSpinBox()
        
        self.source_min = QDoubleSpinBox()
        self.source_max = QDoubleSpinBox()
        
        self.rate_min = QDoubleSpinBox()
        self.rate_max = QDoubleSpinBox()
        
        self.energy_min = QDoubleSpinBox()
        self.energy_max = QDoubleSpinBox()
        
        for widget in [
            self.flash_min,
            self.flash_max,
            self.source_min,
            self.source_max,
            self.rate_min,
            self.rate_max,
            self.energy_min,
            self.energy_max,
        ]:
            widget.setRange(-999999999, 999999999)
        
        self.flash_max.setValue(999999999)
        self.source_max.setValue(999999999)
        self.rate_max.setValue(999999999)
        self.energy_max.setValue(999999999)
        
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

        self.available_columns = [
            "cell_uid",
            "scan_time",
        
            "flash_count",
            "lightning_source_count",
        
            "max_flash_rate_per_min",
            "mean_flash_rate_per_min",
        
            "total_flash_energy",
        
            "max_source_alt_m",
        
            "max_flash_area_km2",
        
            "n_minutes",
            "n_lightning_minutes",
        
            "first_lightning_minute",
            "last_lightning_minute",
        
            "mean_interpolation_fraction",
        
            "scan_time_unix",
        ]

        self.column_selector = QListWidget()
        self.column_selector.setFixedWidth(250)

        for col in self.available_columns:
            item = QListWidgetItem(col)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Checked)
            self.column_selector.addItem(item)

        self.apply_button = QPushButton("Apply Columns")
        self.apply_button.clicked.connect(self.reload_tables)

        self.filter_label = QLabel("Showing all cells")
        
        self.clear_button = QPushButton("Clear Cell Filter")
        self.clear_button.clicked.connect(self.clear_filter)
        
        #
        # Layout
        #

        main_layout = QVBoxLayout(self)

        top_layout = QHBoxLayout()

        chooser_layout = QVBoxLayout()
        
        chooser_layout.addWidget(QLabel("Displayed Columns"))
        chooser_layout.addWidget(self.column_selector)
        chooser_layout.addWidget(self.apply_button)
        chooser_layout.addWidget(self.filter_label)
        chooser_layout.addWidget(self.clear_button)
        
        filter_grid = QGridLayout()
        
        filter_grid.addWidget(
            QLabel("Flash Min"),
            0, 0
        )
        filter_grid.addWidget(
            self.flash_min,
            0, 1
        )
        
        filter_grid.addWidget(
            QLabel("Flash Max"),
            0, 2
        )
        filter_grid.addWidget(
            self.flash_max,
            0, 3
        )
        
        filter_grid.addWidget(
            QLabel("Source Min"),
            1, 0
        )
        filter_grid.addWidget(
            self.source_min,
            1, 1
        )
        
        filter_grid.addWidget(
            QLabel("Source Max"),
            1, 2
        )
        filter_grid.addWidget(
            self.source_max,
            1, 3
        )
        
        filter_grid.addWidget(
            QLabel("Rate Min"),
            2, 0
        )
        filter_grid.addWidget(
            self.rate_min,
            2, 1
        )
        
        filter_grid.addWidget(
            QLabel("Rate Max"),
            2, 2
        )
        filter_grid.addWidget(
            self.rate_max,
            2, 3
        )
        
        filter_grid.addWidget(
            QLabel("Energy Min"),
            3, 0
        )
        filter_grid.addWidget(
            self.energy_min,
            3, 1
        )
        
        filter_grid.addWidget(
            QLabel("Energy Max"),
            3, 2
        )
        filter_grid.addWidget(
            self.energy_max,
            3, 3
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

        top_layout.addLayout(chooser_layout, 1)
        top_layout.addWidget(self.detail_text, 1)

        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.lightning_table, 3)

        #
        # Signals
        #

        self.lightning_table.itemSelectionChanged.connect(
            self.lightning_selected
        )

        self.reload_tables()

    def reload_tables(self):

        self.lightning_table.setSortingEnabled(False)
        
        columns = self.selected_columns()
        
        if not columns:
            return
        
        column_sql = ",".join(columns)
        
        if self.cell_filter:
        
            sql = f"""
            SELECT {column_sql}
            FROM xlma_stat_scan
            WHERE
                cell_uid = ?
                AND flash_count >= ?
                AND flash_count <= ?
                AND lightning_source_count >= ?
                AND lightning_source_count <= ?
                AND mean_flash_rate_per_min >= ?
                AND mean_flash_rate_per_min <= ?
                AND total_flash_energy >= ?
                AND total_flash_energy <= ?
            LIMIT 1000
            """
        
            rows = self.db.execute(
                sql,
                [
                    self.cell_filter,
        
                    self.flash_min.value(),
                    self.flash_max.value(),
        
                    self.source_min.value(),
                    self.source_max.value(),
        
                    self.rate_min.value(),
                    self.rate_max.value(),
        
                    self.energy_min.value(),
                    self.energy_max.value(),
                ]
            )
        
        else:
        
            sql = f"""
            SELECT {column_sql}
            FROM xlma_stat_scan
            WHERE
                flash_count >= ?
                AND flash_count <= ?
                AND lightning_source_count >= ?
                AND lightning_source_count <= ?
                AND mean_flash_rate_per_min >= ?
                AND mean_flash_rate_per_min <= ?
                AND total_flash_energy >= ?
                AND total_flash_energy <= ?
            LIMIT 1000
            """
        
            rows = self.db.execute(
                sql,
                [
                    self.flash_min.value(),
                    self.flash_max.value(),
        
                    self.source_min.value(),
                    self.source_max.value(),
        
                    self.rate_min.value(),
                    self.rate_max.value(),
        
                    self.energy_min.value(),
                    self.energy_max.value(),
                ]
            )

        if self.cell_filter:
        
            self.filter_label.setText(
                f"Cell: {self.cell_filter} | "
                f"{len(rows)} rows"
            )
        
        else:
        
            self.filter_label.setText(
                f"Showing all cells | "
                f"{len(rows)} rows"
            )


        self.lightning_table.setColumnCount(len(columns))
        self.lightning_table.setRowCount(len(rows))
        self.lightning_table.setHorizontalHeaderLabels(columns)

        for r, row in enumerate(rows):
            for c, value in enumerate(row):

                self.lightning_table.setItem(
                    r,
                    c,
                    NumericTableWidgetItem(str(value))
                )

        self.lightning_table.resizeColumnsToContents()
        self.lightning_table.setSortingEnabled(True)

    def lightning_selected(self):

        row = self.lightning_table.currentRow()
    
        if row < 0:
            return
    
        row_values = {}
    
        cell_uid = None
        scan_time = None
    
        for c in range(self.lightning_table.columnCount()):
    
            header_item = self.lightning_table.horizontalHeaderItem(c)
    
            if header_item is None:
                continue
    
            header = header_item.text()
    
            item = self.lightning_table.item(row, c)
    
            value = item.text() if item else ""
    
            row_values[header] = value
    
            if header == "cell_uid":
                cell_uid = value
    
            elif header == "scan_time":
                scan_time = value
    
        #
        # Cross-tab filtering
        #
    
        if cell_uid:
            self.cellSelected.emit(cell_uid)
    
        #
        # Load full lightning record
        #
    
        details = self.db.execute(
            """
            SELECT
                flash_count,
                lightning_source_count,
                max_flash_rate_per_min,
                mean_flash_rate_per_min,
                total_flash_energy,
                max_source_alt_m,
                max_flash_area_km2,
                n_minutes,
                n_lightning_minutes,
                first_lightning_minute,
                last_lightning_minute,
                mean_interpolation_fraction
            FROM xlma_stat_scan
            WHERE cell_uid = ?
            AND scan_time = ?
            LIMIT 1
            """,
            [cell_uid, scan_time]
        )
    
        text = []
    
        text.append(f"Cell UID: {cell_uid}")
        text.append(f"Scan Time: {scan_time}")
        text.append("")
    
        if details:
    
            (
                flash_count,
                lightning_source_count,
                max_flash_rate_per_min,
                mean_flash_rate_per_min,
                total_flash_energy,
                max_source_alt_m,
                max_flash_area_km2,
                n_minutes,
                n_lightning_minutes,
                first_lightning_minute,
                last_lightning_minute,
                mean_interpolation_fraction,
            ) = details[0]
    
            text.append("Lightning Summary")
            text.append("-----------------")
    
            text.append(f"Flash Count: {flash_count}")
            text.append(f"Source Count: {lightning_source_count}")
    
            text.append(f"Max Flash Rate: {max_flash_rate_per_min}")
            text.append(f"Mean Flash Rate: {mean_flash_rate_per_min}")
    
            text.append(f"Total Energy: {total_flash_energy}")
    
            text.append(f"Max Source Altitude: {max_source_alt_m} m")
    
            text.append(f"Max Flash Area: {max_flash_area_km2} km²")
    
            text.append(f"Minutes In Window: {n_minutes}")
            text.append(f"Lightning Minutes: {n_lightning_minutes}")
    
            text.append(f"First Lightning Minute: {first_lightning_minute}")
            text.append(f"Last Lightning Minute: {last_lightning_minute}")
    
            text.append(
                f"Mean Interpolation Fraction: "
                f"{mean_interpolation_fraction}"
            )
    
        text.append("")
        text.append("Selected Attributes")
        text.append("-------------------")
    
        for name, value in row_values.items():
            text.append(f"{name}: {value}")
    
        self.detail_text.setPlainText(
            "\n".join(text)
        )

    def selected_columns(self):

        cols = []

        for i in range(self.column_selector.count()):

            item = self.column_selector.item(i)

            if item.checkState() == Qt.Checked:
                cols.append(item.text())

        return cols

    def clear_filter(self):
    
        self.cell_filter = None
    
        self.reload_tables()

    def set_cell_filter(self, cell_uid):
    
        self.cell_filter = cell_uid
    
        self.reload_tables()

    def clear_numeric_filters(self):

        self.flash_min.setValue(0)
        self.flash_max.setValue(999999999)
    
        self.source_min.setValue(0)
        self.source_max.setValue(999999999)
    
        self.rate_min.setValue(0)
        self.rate_max.setValue(999999999)
    
        self.energy_min.setValue(0)
        self.energy_max.setValue(999999999)
    
        self.reload_tables()