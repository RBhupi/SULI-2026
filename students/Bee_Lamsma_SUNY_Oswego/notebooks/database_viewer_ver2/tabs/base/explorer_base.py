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
    QDoubleSpinBox,
    QGridLayout,
)

from PyQt5.QtCore import Qt, pyqtSignal
from widgets import NumericTableWidgetItem

class BaseExplorerTab(QWidget):

    clearFilterRequested = pyqtSignal()
    
    def __init__(
        self,
        db,
        columns=None,
        title="Displayed Columns",
    ):
        super().__init__()

        self.db = db

        self.cell_filter = None

        self.available_columns = columns or []

        self.numeric_filters = {}

        #
        # Common widgets
        #

        self.table = QTableWidget()
        self.table.setSortingEnabled(True)

        self.detail_text = QTextEdit()
        self.detail_text.setReadOnly(True)

        self.column_selector = QListWidget()

        #
        # Build column selector automatically
        #

        for col in self.available_columns:

            item = QListWidgetItem(col)

            item.setFlags(
                item.flags()
                | Qt.ItemIsUserCheckable
            )

            item.setCheckState(Qt.Checked)

            self.column_selector.addItem(item)

        self.filter_label = QLabel(
            "Showing all cells"
        )

        self.apply_button = QPushButton(
            "Apply Columns"
        )

        self.clear_button = QPushButton(
            "Clear Cell Filter"
        )

        self.clear_button.clicked.connect(
            self.clearFilterRequested.emit
        )

        #
        # Layout
        #

        main_layout = QVBoxLayout(self)

        top_layout = QHBoxLayout()

        chooser_layout = QVBoxLayout()
        self.chooser_layout = chooser_layout

        chooser_layout.addWidget(
            QLabel(title)
        )

        chooser_layout.addWidget(
            self.column_selector
        )

        chooser_layout.addWidget(
            self.apply_button
        )

        chooser_layout.addWidget(
            self.filter_label
        )

        chooser_layout.addWidget(
            self.clear_button
        )

        top_layout.addLayout(
            chooser_layout,
            1
        )

        top_layout.addWidget(
            self.detail_text,
            1
        )

        main_layout.addLayout(
            top_layout
        )

        main_layout.addWidget(
            self.table,
            3
        )

    #
    # Common helpers
    #

    def selected_columns(self):

        cols = []

        for i in range(
            self.column_selector.count()
        ):

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

    def populate_table(
        self,
        table,
        headers,
        rows,
        item_class
    ):

        table.setSortingEnabled(False)

        table.clear()

        table.setColumnCount(
            len(headers)
        )

        table.setRowCount(
            len(rows)
        )

        table.setHorizontalHeaderLabels(
            headers
        )

        for r, row in enumerate(rows):

            for c, value in enumerate(row):

                table.setItem(
                    r,
                    c,
                    item_class(str(value))
                )

        table.resizeColumnsToContents()

        table.setSortingEnabled(True)

    #
    # Must be implemented
    #

    def reload_tables(self):

        raise NotImplementedError(
            "Derived class must implement reload_tables()"
        )

    def selected_row_values(self):
    
        row = self.table.currentRow()
    
        if row < 0:
            return None
    
        values = {}
    
        for c in range(self.table.columnCount()):
    
            header_item = self.table.horizontalHeaderItem(c)
    
            if header_item is None:
                continue
    
            header = header_item.text()
    
            item = self.table.item(row, c)
    
            values[header] = (
                item.text() if item else ""
            )
    
        return values

    def show_details(self, lines):
    
        self.detail_text.setPlainText(
            "\n".join(lines)
        )

    def append_attributes(
        self,
        text,
        values
    ):
    
        text.append("")
        text.append("Selected Attributes")
        text.append("-------------------")
    
        for name, value in values.items():
    
            text.append(
                f"{name}: {value}"
            )
    
    def display_selected_row(
        self,
        values
    ):
        raise NotImplementedError

    def table_row_selected(self):
    
        values = self.selected_row_values()
    
        if not values:
            return
    
        self.display_selected_row(values)

    def simple_reload(self, table_name):
    
        columns = self.selected_columns()
    
        if not columns:
            return
    
        sql = f"""
        SELECT {",".join(columns)}
        FROM {self.TABLE_NAME}
        LIMIT 1000
        """
    
        rows = self.db.execute(sql)
    
        self.populate_table(
            self.table,
            columns,
            rows,
            NumericTableWidgetItem
        )

    def load_table(
        self,
        table_name
    ):
    
        columns = self.selected_columns()
    
        if not columns:
            return []
    
        sql = f"""
        SELECT {",".join(columns)}
        FROM {table_name}
        LIMIT 1000
        """
    
        return self.db.execute(sql)

    def build_cell_filter_sql(
        self,
        column_sql,
        table_name,
        cell_columns
    ):
    
        sql = f"""
        SELECT {column_sql}
        FROM {table_name}
        """
    
        params = []
    
        if self.cell_filter:
    
            where_clause = " OR ".join(
                f"{col} = ?"
                for col in cell_columns
            )
    
            sql += f"""
            WHERE ({where_clause})
            """
    
            params.extend(
                [self.cell_filter]
                * len(cell_columns)
            )
    
        return sql, params

    def create_filter_spinbox(
        self,
        minimum=-999999,
        maximum=999999,
        value=None,
    ):
        box = QDoubleSpinBox()
    
        box.setRange(
            minimum,
            maximum
        )
    
        box.setDecimals(3)
    
        if value is not None:
            box.setValue(value)
    
        return box

    def add_numeric_filter(
        self,
        column,
        label,
        default_max=999999,
    ):
        min_box = self.create_filter_spinbox()
    
        max_box = self.create_filter_spinbox(
            value=default_max
        )
    
        self.numeric_filters[column] = {
            "label": label,
            "min": min_box,
            "max": max_box,
            "default_max": default_max,
        }
        
    def build_numeric_filter_sql(
        self,
        sql,
        params,
    ):
    
        conditions = []
    
        for column, cfg in self.numeric_filters.items():
    
            conditions.append(
                f"""
                (
                    {column} IS NULL
                    OR
                    (
                        {column} >= ?
                        AND {column} <= ?
                    )
                )
                """
            )
    
            params.extend(
                [
                    cfg["min"].value(),
                    cfg["max"].value(),
                ]
            )
    
        if conditions:
    
            if "WHERE" in sql.upper():
    
                sql += "\nAND\n"
    
            else:
    
                sql += "\nWHERE\n"
    
            sql += "\nAND\n".join(
                conditions
            )
    
        return sql, params

    def build_filter_ui(self):
    
        if not self.numeric_filters:
            return
    
        grid = QGridLayout()
    
        for row, (_, cfg) in enumerate(
            self.numeric_filters.items()
        ):
    
            grid.addWidget(
                QLabel(f"{cfg['label']} Min"),
                row,
                0
            )
    
            grid.addWidget(
                cfg["min"],
                row,
                1
            )
    
            grid.addWidget(
                QLabel(f"{cfg['label']} Max"),
                row,
                2
            )
    
            grid.addWidget(
                cfg["max"],
                row,
                3
            )
    
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
    
        self.chooser_layout.addWidget(
            QLabel("Numeric Filters")
        )
    
        self.chooser_layout.addLayout(
            grid
        )
    
        self.chooser_layout.addWidget(
            self.apply_filter_button
        )
    
        self.chooser_layout.addWidget(
            self.clear_numeric_button
        )

    def clear_numeric_filters(self):
    
        for cfg in self.numeric_filters.values():
    
            cfg["min"].setValue(0)
    
            cfg["max"].setValue(
                cfg["default_max"]
            )
    
        self.reload_tables()