import sys
import argparse


from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget,
    QFileDialog, QAction, QMessageBox
)

from database import DatabaseManager

from tabs.database.explorer import DatabaseExplorerTab
from tabs.cells.explorer import CellExplorerTab
from tabs.events.explorer import EventExplorerTab
from tabs.lightning.explorer import LightningExplorerTab
from tabs.dashboard.overview import DashboardTab


# ---------------- MAIN WINDOW ----------------

class MainWindow(QMainWindow):

    def __init__(self, db):
        super().__init__()

        self.db = db

        self.setWindowTitle("Storm Analysis Viewer")
        self.resize(1800, 1000)

        self.tabs = QTabWidget()

        self.database_tab = DatabaseExplorerTab(self.db)
        self.cell_tab = CellExplorerTab(self.db)
        self.event_tab = EventExplorerTab(self.db)
        self.lightning_tab = LightningExplorerTab(self.db)
        self.dashboard_tab = DashboardTab(self.db)
        self.cell_tab.cellSelected.connect(self.cell_selected)
        self.dashboard_tab.cellSelected.connect(self.cell_selected)
        self.event_tab.cellSelected.connect(self.cell_selected)
        self.lightning_tab.cellSelected.connect(self.cell_selected)
        self.database_tab.cellSelected.connect(self.cell_selected)

        self.tabs.addTab(self.database_tab, "Database")
        self.tabs.addTab(self.cell_tab, "Cells")
        self.tabs.addTab(self.event_tab, "Events")
        self.tabs.addTab(self.lightning_tab, "Lightning")
        self.tabs.addTab(self.dashboard_tab, "Dashboard")

        self.cell_tab.apply_button.clicked.connect(self.cell_tab.reload_tables)
        self.cell_tab.clearFilterRequested.connect(self.clear_all_filters)
        self.event_tab.apply_button.clicked.connect(self.event_tab.reload_tables)
        self.event_tab.clearFilterRequested.connect(self.clear_all_filters)
        self.lightning_tab.apply_button.clicked.connect(self.lightning_tab.reload_tables)
        self.lightning_tab.clearFilterRequested.connect(self.clear_all_filters)

        self.setCentralWidget(self.tabs)

        self.build_menu()

    # ---------------- MENU ----------------

    def build_menu(self):
        menu = self.menuBar()
        file_menu = menu.addMenu("File")

        open_action = QAction("Open Database", self)
        open_action.triggered.connect(self.open_database)

        file_menu.addAction(open_action)

    def open_database(self):

        path, _ = QFileDialog.getOpenFileName(
            self,
            "Open SQLite Database",
            "",
            "SQLite (*.db *.sqlite *.sqlite3)"
        )

        if not path:
            return

        try:
            self.db.open(path)

            self.database_tab.reload_table()
            self.cell_tab.reload_tables()
            self.event_tab.reload_tables()
            self.lightning_tab.reload_tables()
            self.dashboard_tab.refresh()

        except Exception as e:
            QMessageBox.critical(self, "DB Error", str(e))

    
    def refresh_all(self):
    
        if hasattr(self.database_tab, "reload_table"):
            self.database_tab.reload_tables()
    
        if hasattr(self.cell_tab, "reload_tables"):
            self.cell_tab.reload_tables()
    
        if hasattr(self.event_tab, "reload_tables"):
            self.event_tab.reload_tables()
    
        if hasattr(self.lightning_tab, "reload_tables"):
            self.lightning_tab.reload_tables()
    
        self.dashboard_tab.refresh()

    def cell_selected(self, cell_uid):
    
        print("Selected cell:", cell_uid)
    
        self.cell_tab.set_cell_filter(cell_uid)
    
        self.event_tab.set_cell_filter(cell_uid)
    
        self.lightning_tab.set_cell_filter(cell_uid)

    def clear_all_filters(self):
    
        print("Clearing all cell filters")
    
        self.cell_tab.clear_filter()
    
        self.event_tab.clear_filter()
    
        self.lightning_tab.clear_filter()
    
        if hasattr(self.database_tab, "clear_filter"):
            self.database_tab.clear_filter()

# ---------------- CLI ENTRY ----------------

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", required=True)
    return parser.parse_args()


def main():

    args = parse_args()

    db = DatabaseManager()
    db.open(args.db)

    app = QApplication(sys.argv)

    win = MainWindow(db)
    print("before show")
    win.show()
    print("after show")
    win.refresh_all()
    print("after refresh")
    win.tabs.setCurrentWidget(win.dashboard_tab)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
