from PyQt5.QtWidgets import (
    QLabel,
    QPushButton,
    QGridLayout,
)
from PyQt5.QtCore import pyqtSignal
from tabs.base.explorer_base import BaseExplorerTab
from widgets import NumericTableWidgetItem

class LightningExplorerTab(BaseExplorerTab):

    cellSelected = pyqtSignal(str)

    TABLE_NAME = "xlma_stat_scan"

    AVAILABLE_COLUMNS = [
        "cell_uid",
        "scan_time",
        "flash_count",
        "lightning_source_count",
        "mean_flash_rate_per_min",
        "max_flash_rate_per_min",
        "total_flash_energy",
        "max_source_alt_m",
        "max_flash_area_km2",
        "n_lightning_minutes",
    ]

    def __init__(self, db):

        super().__init__(
            db,
            title="Displayed Columns",
            columns=self.AVAILABLE_COLUMNS
        )
        
        self.add_numeric_filter(
            "flash_count",
            "Flash Count"
        )
        
        self.add_numeric_filter(
            "lightning_source_count",
            "Source Count"
        )
        
        self.add_numeric_filter(
            "max_flash_rate_per_min",
            "Flash Rate"
        )
        
        self.add_numeric_filter(
            "max_flash_area_km2",
            "Flash Area"
        )
        
        self.add_numeric_filter(
            "total_flash_energy",
            "Energy"
        )
        
        self.build_filter_ui()

        self.table.itemSelectionChanged.connect(
            self.table_row_selected
        )

        self.reload_tables()

    def display_selected_row(
        self,
        values
    ):
    
        cell_uid = values.get("cell_uid", "")
        scan_time = values.get("scan_time", "")
    
        details = self.db.execute(
            """
            SELECT
                flash_count,
                lightning_source_count,
                mean_flash_rate_per_min,
                max_flash_rate_per_min,
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
            [
                cell_uid,
                scan_time,
            ]
        )
    
        if not details:
            return
    
        (
            flash_count,
            lightning_source_count,
            mean_flash_rate_per_min,
            max_flash_rate_per_min,
            total_flash_energy,
            max_source_alt_m,
            max_flash_area_km2,
            n_minutes,
            n_lightning_minutes,
            first_lightning_minute,
            last_lightning_minute,
            mean_interpolation_fraction,
        ) = details[0]
    
        text = []
    
        text.append("LIGHTNING SUMMARY")
        text.append("=================")
        text.append(f"Cell UID: {cell_uid}")
        text.append(f"Scan Time: {scan_time}")
        text.append("")
    
        text.append(f"Flash Count: {flash_count}")
        text.append(
            f"Lightning Sources: {lightning_source_count}"
        )
    
        text.append(
            f"Mean Flash Rate: {mean_flash_rate_per_min}"
        )
    
        text.append(
            f"Max Flash Rate: {max_flash_rate_per_min}"
        )
    
        text.append(
            f"Total Energy: {total_flash_energy}"
        )
    
        text.append(
            f"Max Source Altitude: {max_source_alt_m} m"
        )
    
        text.append(
            f"Max Flash Area: {max_flash_area_km2} km²"
        )
    
        text.append(
            f"Minutes In Scan: {n_minutes}"
        )
    
        text.append(
            f"Lightning Minutes: {n_lightning_minutes}"
        )
    
        text.append(
            f"First Lightning Minute: {first_lightning_minute}"
        )
    
        text.append(
            f"Last Lightning Minute: {last_lightning_minute}"
        )
    
        text.append(
            f"Mean Interpolation Fraction: "
            f"{mean_interpolation_fraction}"
        )
    
        self.append_attributes(
            text,
            values
        )
    
        self.show_details(text)
    
        if cell_uid:
            self.cellSelected.emit(cell_uid)

    def reload_tables(self):
    
        columns = self.selected_columns()
    
        if not columns:
            return
    
        column_sql = ",".join(columns)
    
        sql, params = self.build_cell_filter_sql(
            column_sql,
            "xlma_stat_scan",
            ["cell_uid"]
        )
    
        sql, params = self.build_numeric_filter_sql(
            sql,
            params
        )
    
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
