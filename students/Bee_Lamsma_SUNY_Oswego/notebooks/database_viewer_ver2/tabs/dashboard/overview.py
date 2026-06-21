from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTextEdit,
    QListWidget,
)
from PyQt5.QtCore import pyqtSignal

class DashboardTab(QWidget):

    cellSelected = pyqtSignal(str)

    def __init__(self, db):
        super().__init__()

        self.db = db

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

            tracks = self.db.scalar(
                "SELECT COUNT(*) FROM cell_tracks"
            )

            events = self.db.scalar(
                "SELECT COUNT(*) FROM cell_events"
            )

            scans = self.db.scalar(
                "SELECT COUNT(*) FROM cells_by_scan"
            )

            lightning = self.db.scalar(
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
            
            max_duration = self.db.scalar(
                """
                SELECT MAX(duration_seconds)
                FROM cell_tracks
                """
            )
            
            avg_duration = self.db.scalar(
                """
                SELECT AVG(duration_seconds)
                FROM cell_tracks
                """
            )
            
            max_area = self.db.scalar(
                """
                SELECT MAX(max_area_sqkm)
                FROM cell_tracks
                """
            )
            
            avg_area = self.db.scalar(
                """
                SELECT AVG(max_area_sqkm)
                FROM cell_tracks
                """
            )
            
            max_reflectivity = self.db.scalar(
                """
                SELECT MAX(max_reflectivity)
                FROM cell_tracks
                """
            )
            
            avg_reflectivity = self.db.scalar(
                """
                SELECT AVG(max_reflectivity)
                FROM cell_tracks
                """
            )

            long_lived_tracks = self.db.scalar(
                """
                SELECT COUNT(*)
                FROM cell_tracks
                WHERE duration_seconds >= 3600
                """
            )
            
            merge_events = self.db.scalar(
                """
                SELECT COUNT(*)
                FROM cell_events
                WHERE event_type = 'merge'
                """
            )
            
            split_events = self.db.scalar(
                """
                SELECT COUNT(*)
                FROM cell_events
                WHERE event_type = 'split'
                """
            )
            
            text.append("TRACK SUMMARY")
            text.append("=============")
            
            text.append(
                f"Max Duration (s)   : {max_duration or 0}"
            )
            
            text.append(
                f"Avg Duration (s)   : {(avg_duration or 0):.1f}"
            )
            
            text.append(
                f"Max Area (km²)     : {(max_area or 0):.2f}"
            )
            
            text.append(
                f"Avg Area (km²)     : {(avg_area or 0):.2f}"
            )
            
            text.append(
                f"Max Reflectivity   : {(max_reflectivity or 0):.1f}"
            )
            
            text.append(
                f"Avg Reflectivity   : {(avg_reflectivity or 0):.1f}"
            )

            text.append(
                f"Tracks >= 1 hr     : {long_lived_tracks}"
            )
            
            text.append(
                f"Merge Events       : {merge_events}"
            )
            
            text.append(
                f"Split Events       : {split_events}"
            )
            
            text.append("")

            #
            # Lightning statistics
            #
            
            flashes = self.db.scalar(
                "SELECT SUM(flash_count) FROM xlma_stat_scan"
            )
            
            energy = self.db.scalar(
                "SELECT SUM(total_flash_energy) FROM xlma_stat_scan"
            )
            
            avg_flash_rate = self.db.scalar(
                """
                SELECT AVG(mean_flash_rate_per_min)
                FROM xlma_stat_scan
                """
            )
            
            max_flash_rate = self.db.scalar(
                """
                SELECT MAX(max_flash_rate_per_min)
                FROM xlma_stat_scan
                """
            )
            
            avg_flash_area = self.db.scalar(
                """
                SELECT AVG(max_flash_area_km2)
                FROM xlma_stat_scan
                """
            )
            
            max_flash_area = self.db.scalar(
                """
                SELECT MAX(max_flash_area_km2)
                FROM xlma_stat_scan
                """
            )
            
            avg_source_count = self.db.scalar(
                """
                SELECT AVG(lightning_source_count)
                FROM xlma_stat_scan
                """
            )
            
            max_source_count = self.db.scalar(
                """
                SELECT MAX(lightning_source_count)
                FROM xlma_stat_scan
                """
            )
            
            avg_lightning_minutes = self.db.scalar(
                """
                SELECT AVG(n_lightning_minutes)
                FROM xlma_stat_scan
                """
            )
            
            max_lightning_minutes = self.db.scalar(
                """
                SELECT MAX(n_lightning_minutes)
                FROM xlma_stat_scan
                """
            )
            
            text.append("LIGHTNING SUMMARY")
            text.append("=================")
            
            text.append(f"Total Flashes        : {int(flashes or 0)}")
            text.append(f"Total Energy         : {(energy or 0):.2f}")
            
            text.append(f"Max Flash Rate       : {(max_flash_rate or 0):.2f}")
            text.append(f"Avg Flash Rate       : {(avg_flash_rate or 0):.2f}")
            
            text.append(f"Max Flash Area km²   : {(max_flash_area or 0):.2f}")
            text.append(f"Avg Flash Area km²   : {(avg_flash_area or 0):.2f}")
            
            text.append(f"Max Source Count     : {int(max_source_count or 0)}")
            text.append(f"Avg Source Count     : {(avg_source_count or 0):.1f}")
            
            text.append(f"Max LTG Minutes Per Scan      : {int(max_lightning_minutes or 0)}")
            text.append(f"Avg LTG Minutes Per Scan      : {(avg_lightning_minutes or 0):.1f}")
            
            text.append("")
            #
            # Event types
            #

            rows = self.db.execute(
                """
                SELECT event_type, COUNT(*)
                FROM cell_events
                GROUP BY event_type
                ORDER BY COUNT(*) DESC
                """
            )

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

    def cell_clicked(self, item):
    
        cell_uid = item.text()
    
        print("Dashboard selected:", cell_uid)
    
        self.cellSelected.emit(cell_uid)