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

class CellExplorerTab(QWidget):

    cellSelected = pyqtSignal(str)
    def __init__(self, db, engine):
        super().__init__()
    
        self.db = db
        self.engine = engine
    
        #
        # Widgets
        #
    
        self.track_table = QTableWidget()
        self.track_table.setSortingEnabled(True)
    
        self.detail_text = QTextEdit()
        self.detail_text.setReadOnly(True)
        self.selected_label = QLabel("No cell selected")
    
        self.available_columns = [
            "cell_uid",
            "scan_time",
            "cell_area_sqkm",
            "radar_reflectivity_max",
            "radar_reflectivity_mean",
            "area_40dbz_km2",
            "age_seconds",
            "cell_centroid_mass_lat",
            "cell_centroid_mass_lon",
            "radar_velocity_mean",
        ]
    
        self.column_selector = QListWidget()

        #
        # Numeric filters
        #
        
        self.area_min = QDoubleSpinBox()
        self.area_max = QDoubleSpinBox()
        
        self.refl_min = QDoubleSpinBox()
        self.refl_max = QDoubleSpinBox()
        
        self.age_min = QDoubleSpinBox()
        self.age_max = QDoubleSpinBox()
        
        for widget in [
            self.area_min,
            self.area_max,
            self.refl_min,
            self.refl_max,
            self.age_min,
            self.age_max,
        ]:
            widget.setRange(-999999, 999999)
        
        self.area_max.setValue(999999)
        self.refl_max.setValue(999999)
        self.age_max.setValue(999999)
        
        self.apply_filter_button = QPushButton(
            "Apply Filters"
        )
        
        self.apply_filter_button.clicked.connect(
            self.reload_tables
        )
        
        self.clear_filter_button = QPushButton(
            "Clear Filters"
        )
        
        self.clear_filter_button.clicked.connect(
            self.clear_filters
        )
    
        for col in self.available_columns:
            item = QListWidgetItem(col)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Checked)
            self.column_selector.addItem(item)
    
        self.apply_button = QPushButton("Apply Columns")
        self.apply_button.clicked.connect(self.reload_tables)
    
        #
        # Layout
        #
        
        main_layout = QVBoxLayout(self)
        
        top_layout = QHBoxLayout()
        
        chooser_layout = QVBoxLayout()
        
        chooser_layout.addWidget(QLabel("Displayed Columns"))
        chooser_layout.addWidget(self.column_selector)
        chooser_layout.addWidget(self.apply_button)
        self.filter_label = QLabel("Showing all cells")
        chooser_layout.addWidget(self.filter_label)
        chooser_layout.addWidget(self.selected_label)

        #
        # Filter layout
        #
        
        filter_grid = QGridLayout()
        
        filter_grid.addWidget(
            QLabel("Area Min"),
            0, 0
        )
        
        filter_grid.addWidget(
            self.area_min,
            0, 1
        )
        
        filter_grid.addWidget(
            QLabel("Area Max"),
            0, 2
        )
        
        filter_grid.addWidget(
            self.area_max,
            0, 3
        )
        
        filter_grid.addWidget(
            QLabel("Reflectivity Min"),
            1, 0
        )
        
        filter_grid.addWidget(
            self.refl_min,
            1, 1
        )
        
        filter_grid.addWidget(
            QLabel("Reflectivity Max"),
            1, 2
        )
        
        filter_grid.addWidget(
            self.refl_max,
            1, 3
        )
        
        filter_grid.addWidget(
            QLabel("Age Min"),
            2, 0
        )
        
        filter_grid.addWidget(
            self.age_min,
            2, 1
        )
        
        filter_grid.addWidget(
            QLabel("Age Max"),
            2, 2
        )
        
        filter_grid.addWidget(
            self.age_max,
            2, 3
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
            self.clear_filter_button
        )
        
        top_layout.addLayout(chooser_layout,1)
        top_layout.addWidget(self.detail_text,1)
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.track_table,3)
        
        #
        # Signals
        #
    
        self.track_table.itemSelectionChanged.connect(
            self.track_selected
        )
    
        #
        # Initial load
        #
    
        self.reload_tables()

    def reload_tables(self):

        self.track_table.setSortingEnabled(False)
        
        columns = self.selected_columns()
        
        if not columns:
            return
        
        column_sql = ",".join(columns)
        
        sql = f"""
        SELECT {column_sql}
        FROM cells_by_scan
        WHERE
            cell_area_sqkm >= ?
        AND cell_area_sqkm <= ?
        AND radar_reflectivity_max >= ?
        AND radar_reflectivity_max <= ?
        AND age_seconds >= ?
        AND age_seconds <= ?
        LIMIT 1000
        """
        
        rows = self.db.execute(
            sql,
            [
                self.area_min.value(),
                self.area_max.value(),
        
                self.refl_min.value(),
                self.refl_max.value(),
        
                self.age_min.value(),
                self.age_max.value(),
            ]
        )

        headers = columns

        self.track_table.setColumnCount(len(headers))
        self.track_table.setRowCount(len(rows))
        self.track_table.setHorizontalHeaderLabels(headers)

        for r, row in enumerate(rows):
            for c, value in enumerate(row):
                self.track_table.setItem(
                    r,
                    c,
                    NumericTableWidgetItem(str(value))
                )

        self.track_table.resizeColumnsToContents()
        self.track_table.setSortingEnabled(True)

        self.filter_label.setText(
            f"Area {self.area_min.value():.0f}-{self.area_max.value():.0f} km² | "
            f"Refl {self.refl_min.value():.0f}-{self.refl_max.value():.0f} dBZ | "
            f"Age {self.age_min.value():.0f}-{self.age_max.value():.0f} s"
        )

    def track_selected(self):
    
        row = self.track_table.currentRow()
    
        if row < 0:
            return
    
        cell_uid = None

        row_values = {}
        
        for c in range(self.track_table.columnCount()):
        
            header = self.track_table.horizontalHeaderItem(c).text()
        
            item = self.track_table.item(row, c)
        
            value = item.text() if item else ""
        
            row_values[header] = value
        
            if header == "cell_uid":
                cell_uid = value

        if cell_uid:
            self.selected_label.setText(f"Selected Cell: {cell_uid}")
    
        rows = self.db.execute(
            """
            SELECT
                first_seen_time,
                last_seen_time,
                duration_seconds,
                max_area_sqkm,
                max_reflectivity,
                origin_type,
                termination_type
            FROM cell_tracks
            WHERE cell_uid = ?
            """,
            [cell_uid]
        )
    
        if not rows:
            return
    
        track = rows[0]
    
        text = []
    
        text.append("CELL SUMMARY")
        text.append("============")
        text.append(f"Cell UID: {cell_uid}")
        text.append("")
        text.append(f"Duration: {track[2]:.0f} s")
        text.append(f"Max Area: {track[3]:.1f} km²")
        text.append(f"Max Reflectivity: {track[4]:.1f} dBZ")
        text.append(f"Origin: {track[5]}")
        text.append(f"Termination: {track[6]}")

        text.append("")
        text.append("Selected Cell Attributes")
        text.append("-----------------------")
        
        for name, value in row_values.items():
        
            if name == "cell_uid":
                continue
        
            text.append(f"{name}: {value}")
    
        self.detail_text.setPlainText("\n".join(text))
        
        if cell_uid:
            self.cellSelected.emit(cell_uid)

    def selected_columns(self):
    
        cols = []
    
        for i in range(
            self.column_selector.count()
        ):
    
            item = self.column_selector.item(i)
    
            if item.checkState() == Qt.Checked:
                cols.append(item.text())
    
        return cols

    def select_cell(self, cell_uid):

        print("Cell tab selecting:", cell_uid)
        for row in range(self.track_table.rowCount()):
    
            for col in range(self.track_table.columnCount()):
    
                header = self.track_table.horizontalHeaderItem(col)
    
                if not header:
                    continue
    
                if header.text() != "cell_uid":
                    continue
    
                item = self.track_table.item(row, col)
    
                if item and item.text() == cell_uid:
    
                    self.track_table.selectRow(row)
    
                    self.track_table.scrollToItem(item)
    
                    return

    def clear_filters(self):

        self.area_min.setValue(0)
        self.area_max.setValue(999999)
    
        self.refl_min.setValue(0)
        self.refl_max.setValue(999999)
    
        self.age_min.setValue(0)
        self.age_max.setValue(999999)
    
        self.reload_tables()