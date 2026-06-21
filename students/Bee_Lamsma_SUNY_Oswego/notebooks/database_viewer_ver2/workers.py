import sqlite3
import traceback

from PyQt5.QtCore import QThread, pyqtSignal


class QueryWorker(QThread):

    completed = pyqtSignal(object, object)
    failed = pyqtSignal(str)

    def __init__(self, db, sql, params=None):
        super().__init__()
        self.db = db
        self.sql = sql
        self.params = params or []

    def run(self):
        print("Worker started")
    
        conn = None
    
        try:
            if not self.db.path:
                raise RuntimeError(
                    "Database path not set"
                )
            
            conn = sqlite3.connect(self.db.path)
    
            cur = conn.cursor()
    
            if self.params:
                cur.execute(self.sql, self.params)
            else:
                cur.execute(self.sql)
    
            rows = cur.fetchall()
            headers = [d[0] for d in cur.description]
    
            self.completed.emit(rows, headers)
    
        except Exception:
            error_text = traceback.format_exc()
        
            print(error_text)
        
            self.failed.emit(error_text)
    
        finally:
            if conn:
                conn.close()
    
            print("Worker finished")