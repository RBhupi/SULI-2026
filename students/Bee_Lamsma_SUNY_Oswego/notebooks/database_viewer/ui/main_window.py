from PyQt5.QtWidgets import QMainWindow, QTabWidget

from tabs.database.explorer import DatabaseExplorerTab
from tabs.cells.explorer import CellExplorerTab
from tabs.events.explorer import EventExplorerTab
from tabs.lightning.explorer import LightningExplorerTab
from tabs.dashboard.overview import DashboardTab


class MainWindow(QMainWindow):

    def __init__(self, db, engine):
        super().__init__()

        self.db = db
        self.engine = engine

        self.setWindowTitle("Storm Analysis Viewer")
        self.resize(1800, 1000)

        self.tabs = QTabWidget()

        self.database_tab = DatabaseExplorerTab(db, engine)
        self.cells_tab = CellExplorerTab(db, engine)
        self.events_tab = EventExplorerTab(db, engine)
        self.lightning_tab = LightningExplorerTab(db, engine)
        self.dashboard_tab = DashboardTab(db, engine)

        self.tabs.addTab(self.database_tab, "Database")
        self.tabs.addTab(self.cells_tab, "Cells")
        self.tabs.addTab(self.events_tab, "Events")
        self.tabs.addTab(self.lightning_tab, "Lightning")
        self.tabs.addTab(self.dashboard_tab, "Dashboard")

        self.setCentralWidget(self.tabs)

    def refresh_all(self):
        self.database_tab.reload()
        self.cells_tab.reload()
        self.events_tab.reload()
        self.lightning_tab.reload()
        self.dashboard_tab.refresh()