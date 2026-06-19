from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTextEdit,
    QListWidget,
)
from PyQt5.QtCore import pyqtSignal

class DashboardTab(QWidget):

    cellSelected = pyqtSignal(str)

    def __init__(self, db, engine):
        super().__init__()

        self.db = db
        self.engine = engine

        layout = QVBoxLayout(self)

        self.summary = QTextEdit()
        self.summary.setReadOnly(True)

        self.cell_list = QListWidget()
        self.cell_list.itemClicked.connect(self.cell_clicked)
        
        rows = self.db.execute(
            """
            SELECT DISTINCT cell_uid
            FROM cell_tracks
            ORDER BY cell_uid
            LIMIT 500
            """
        )
        
        for row in rows:
            self.cell_list.addItem(str(row[0]))

        layout.addWidget(self.cell_list, 1)
        layout.addWidget(self.summary, 3)

    def refresh(self):
        print('Dashboard refresh called')
        
        try:

            text = []

            #
            # Counts
            #

            tracks = self.scalar(
                "SELECT COUNT(*) FROM cell_tracks"
            )

            events = self.scalar(
                "SELECT COUNT(*) FROM cell_events"
            )

            scans = self.scalar(
                "SELECT COUNT(*) FROM cells_by_scan"
            )

            lightning = self.scalar(
                "SELECT COUNT(*) FROM xlma_stat_scan"
            )

            print("Tracks:", tracks)
            print("Events:", events)
            print("Scans:", scans)
            print("Lightning:", lightning)
            
            text.append("DATABASE SUMMARY")
            text.append("================")
            text.append(f"Tracks           : {tracks}")
            text.append(f"Events           : {events}")
            text.append(f"Cells By Scan    : {scans}")
            text.append(f"Lightning Scans  : {lightning}")
            text.append("")

            #
            # Track statistics
            #

            max_duration = self.scalar(
                "SELECT MAX(duration_seconds) FROM cell_tracks"
            )

            avg_duration = self.scalar(
                "SELECT AVG(duration_seconds) FROM cell_tracks"
            )

            max_reflectivity = self.scalar(
                "SELECT MAX(max_reflectivity) FROM cell_tracks"
            )

            text.append("TRACK SUMMARY")
            text.append("=============")
            text.append(f"Max Duration (s) : {max_duration}")
            text.append(f"Avg Duration (s) : {avg_duration:.1f}")
            text.append(f"Max Reflectivity : {max_reflectivity:.1f}")
            text.append("")

            #
            # Lightning statistics
            #

            flashes = self.scalar(
                "SELECT SUM(flash_count) FROM xlma_stat_scan"
            )

            energy = self.scalar(
                "SELECT SUM(total_flash_energy) FROM xlma_stat_scan"
            )

            text.append("LIGHTNING SUMMARY")
            text.append("=================")
            text.append(f"Total Flashes : {int(flashes)}")
            text.append(f"Total Energy  : {energy:.2f}")
            text.append("")

            #
            # Event types
            #

            cur = self.db.conn.cursor()

            cur.execute(
                """
                SELECT event_type, COUNT(*)
                FROM cell_events
                GROUP BY event_type
                ORDER BY COUNT(*) DESC
                """
            )

            rows = cur.fetchall()

            text.append("EVENT TYPES")
            text.append("===========")

            for event_type, count in rows:
                text.append(
                    f"{event_type:12} {count}"
                )

            print("Dashboard text length:", len(text))
            self.summary.setPlainText(
                "\n".join(text)
            )

        except Exception as e:
            print("Dashboard error:", e)
            self.summary.setPlainText(str(e))

    def scalar(self, sql):

        cur = self.db.conn.cursor()

        cur.execute(sql)

        row = cur.fetchone()

        if row:
            return row[0]

        return None

    def cell_clicked(self, item):
    
        cell_uid = item.text()
    
        print("Dashboard selected:", cell_uid)
    
        self.cellSelected.emit(cell_uid)