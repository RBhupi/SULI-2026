from PyQt5.QtWidgets import (
    QLabel,
    QDoubleSpinBox,
    QPushButton,
    QGridLayout,
)
from PyQt5.QtCore import pyqtSignal
from tabs.base.explorer_base import BaseExplorerTab
from widgets import NumericTableWidgetItem

class CellExplorerTab(BaseExplorerTab):

    cellSelected = pyqtSignal(str)

    TABLE_NAME = "cells_by_scan"

    AVAILABLE_COLUMNS = [
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

    def __init__(self, db):

        super().__init__(
            db,
            title="Displayed Columns",
            columns=self.AVAILABLE_COLUMNS
        )

        #
        # Numeric filters
        #
        
        self.add_numeric_filter(
            "cell_area_sqkm",
            "Area"
        )
        
        self.add_numeric_filter(
            "radar_reflectivity_max",
            "Reflectivity"
        )
        
        self.add_numeric_filter(
            "age_seconds",
            "Age"
        )
        
        self.build_filter_ui()

        self.table.itemSelectionChanged.connect(
            self.table_row_selected
        )

        self.reload_tables()

    def reload_tables(self):
    
        columns = self.selected_columns()
    
        if not columns:
            return
    
        column_sql = ",".join(columns)
    
        sql, params = self.build_cell_filter_sql(
            column_sql,
            "cells_by_scan",
            ["cell_uid"]
        )
    
        sql, params = self.build_numeric_filter_sql(
            sql,
            params
        )
    
        sql += "\nLIMIT 1000"
    
        rows = self.db.execute(
            sql,
            params
        )
    
        self.populate_table(
            self.table,
            columns,
            rows,
            NumericTableWidgetItem
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

    def display_selected_row(self, values):
    
        cell_uid = values["cell_uid"]
    
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
        text.append(f"Duration: {track[2]}")
        text.append(f"Max Area: {track[3]}")
        text.append(f"Max Reflectivity: {track[4]}")
        text.append(f"Origin: {track[5]}")
        text.append(f"Termination: {track[6]}")
    
        self.append_attributes(
            text,
            values
        )
    
        self.show_details(text)
    
        self.cellSelected.emit(cell_uid)

