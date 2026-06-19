from PyQt5.QtWidgets import (
    QMainWindow, QTabWidget, QWidget,
    QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel
)

from workers import QueryWorker


class CellDrilldownWindow(QMainWindow):

    def __init__(self, db, cell_uid):
        super().__init__()

        self.db = db
        self.cell_uid = cell_uid

        self.setWindowTitle(f"Cell Drilldown: {cell_uid}")
        self.resize(1200, 800)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.build_tabs()

    def build_tabs(self):

        self.overview = QWidget()
        self.events = QWidget()
        self.volume = QWidget()
        self.scans = QWidget()
        self.lightning = QWidget()

        self.tabs.addTab(self.overview, "Overview")
        self.tabs.addTab(self.events, "Events")
        self.tabs.addTab(self.volume, "Volume")
        self.tabs.addTab(self.scans, "Scans")
        self.tabs.addTab(self.lightning, "Lightning")

        self.build_overview()
        self.load_events()
        self.load_volume()
        self.load_scans()
        self.load_lightning()

    # ---------------- OVERVIEW ----------------

    def build_overview(self):

        layout = QVBoxLayout()
        self.overview.setLayout(layout)

        self.overview_label = QLabel("Loading...")
        layout.addWidget(self.overview_label)

        sql = """
        SELECT *
        FROM cell_tracks
        WHERE cell_uid=?
        """

        self.worker = QueryWorker(self.db, sql, [self.cell_uid])
        self.worker.completed.connect(self.render_overview)
        self.worker.start()

    def render_overview(self, rows, headers):

        if not rows:
            self.overview_label.setText("No data")
            return

        self.overview_label.setText(str(rows[0]))

    # ---------------- EVENTS ----------------

    def load_events(self):

        self.events_table = QTableWidget()

        layout = QVBoxLayout()
        layout.addWidget(self.events_table)
        self.events.setLayout(layout)

        sql = """
        SELECT *
        FROM cell_events
        WHERE source_cell_uid=?
           OR target_cell_uid=?
        ORDER BY source_scan_time
        """

        self.worker = QueryWorker(self.db, sql, [self.cell_uid, self.cell_uid])
        self.worker.completed.connect(self.render_events)
        self.worker.start()

    def render_events(self, rows, headers):

        self.events_table.setColumnCount(len(headers))
        self.events_table.setRowCount(len(rows))
        self.events_table.setHorizontalHeaderLabels(headers)

        for r, row in enumerate(rows):
            for c, v in enumerate(row):
                self.events_table.setItem(r, c, QTableWidgetItem(str(v)))

    # ---------------- VOLUME ----------------

    def load_volume(self):

        self.volume_table = QTableWidget()

        layout = QVBoxLayout()
        layout.addWidget(self.volume_table)
        self.volume.setLayout(layout)

        sql = """
        SELECT *
        FROM cell_volume_stats
        WHERE cell_uid=?
        ORDER BY scan_time
        """

        self.worker = QueryWorker(self.db, sql, [self.cell_uid])
        self.worker.completed.connect(self.render_volume)
        self.worker.start()

    def render_volume(self, rows, headers):

        self.volume_table.setColumnCount(len(headers))
        self.volume_table.setRowCount(len(rows))
        self.volume_table.setHorizontalHeaderLabels(headers)

        for r, row in enumerate(rows):
            for c, v in enumerate(row):
                self.volume_table.setItem(r, c, QTableWidgetItem(str(v)))

    # ---------------- SCANS ----------------

    def load_scans(self):

        self.scans_table = QTableWidget()

        layout = QVBoxLayout()
        layout.addWidget(self.scans_table)
        self.scans.setLayout(layout)

        sql = """
        SELECT *
        FROM cells_by_scan
        WHERE cell_uid=?
        ORDER BY scan_time
        """

        self.worker = QueryWorker(self.db, sql, [self.cell_uid])
        self.worker.completed.connect(self.render_scans)
        self.worker.start()

    def render_scans(self, rows, headers):

        self.scans_table.setColumnCount(len(headers))
        self.scans_table.setRowCount(len(rows))
        self.scans_table.setHorizontalHeaderLabels(headers)

        for r, row in enumerate(rows):
            for c, v in enumerate(row):
                self.scans_table.setItem(r, c, QTableWidgetItem(str(v)))

    # ---------------- LIGHTNING ----------------

    def load_lightning(self):

        self.lightning_table = QTableWidget()

        layout = QVBoxLayout()
        layout.addWidget(self.lightning_table)
        self.lightning.setLayout(layout)

        sql = """
        SELECT *
        FROM xlma_stat_scan
        WHERE cell_uid=?
        """

        self.worker = QueryWorker(self.db, sql, [self.cell_uid])
        self.worker.completed.connect(self.render_lightning)
        self.worker.start()

    def render_lightning(self, rows, headers):

        self.lightning_table.setColumnCount(len(headers))
        self.lightning_table.setRowCount(len(rows))
        self.lightning_table.setHorizontalHeaderLabels(headers)

        for r, row in enumerate(rows):
            for c, v in enumerate(row):
                self.lightning_table.setItem(r, c, QTableWidgetItem(str(v)))