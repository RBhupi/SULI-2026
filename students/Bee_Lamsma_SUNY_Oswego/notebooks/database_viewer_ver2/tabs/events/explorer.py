from PyQt5.QtWidgets import (
    QLabel,
    QDoubleSpinBox,
    QPushButton,
    QGridLayout,
)
from PyQt5.QtCore import pyqtSignal
from tabs.base.explorer_base import BaseExplorerTab
from widgets import NumericTableWidgetItem

class EventExplorerTab(BaseExplorerTab):

    cellSelected = pyqtSignal(str)

    TABLE_NAME = "cell_events"

    AVAILABLE_COLUMNS = [
        "event_type",
        "source_cell_uid",
        "target_cell_uid",
        "source_scan_time",
        "target_scan_time",
        "cost",
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
            "cost",
            "Cost"
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
    
        target_uid = values.get(
            "target_cell_uid",
            ""
        )
    
        text = []
    
        text.append(
            f"Event Type: {values.get('event_type','')}"
        )
    
        text.append(
            f"Target Cell: {target_uid}"
        )
    
        text.append("")
        text.append("Event Summary")
        text.append("-------------")
        
        text.append(
            f"Source Cell: {values.get('source_cell_uid','')}"
        )
        
        text.append(
            f"Target Cell: {values.get('target_cell_uid','')}"
        )
        
        text.append(
            f"Source Scan: {values.get('source_scan_time','')}"
        )
        
        text.append(
            f"Target Scan: {values.get('target_scan_time','')}"
        )
        
        text.append(
            f"Cost: {values.get('cost','')}"
        )
    
        self.append_attributes(
            text,
            values
        )
    
        self.show_details(text)
    
        if target_uid:
            self.cellSelected.emit(
                target_uid
            )

    def reload_tables(self):
    
        columns = self.selected_columns()
    
        if not columns:
            return
    
        column_sql = ",".join(columns)
    
        sql, params = self.build_cell_filter_sql(
            column_sql,
            "cell_events",
            [
                "source_cell_uid",
                "target_cell_uid"
            ]
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