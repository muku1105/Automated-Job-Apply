import sqlite3
import datetime
import os
from src.config import Config

class JobTracker:
    def __init__(self):
        # Ensure the directory exists
        db_dir = os.path.dirname(Config.DB_PATH)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
        
        self.conn = sqlite3.connect(Config.DB_PATH)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company TEXT,
                title TEXT,
                url TEXT UNIQUE,
                description TEXT,
                ats_score REAL,
                status TEXT,
                applied_date TIMESTAMP
            )
        ''')
        self.conn.commit()

    def job_exists(self, url):
        cursor = self.conn.cursor()
        cursor.execute("SELECT 1 FROM jobs WHERE url = ?", (url,))
        return cursor.fetchone() is not None

    def log_job(self, company, title, url, description, score, status):
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO jobs (company, title, url, description, ats_score, status, applied_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (company, title, url, description, score, status, datetime.datetime.now()))
            self.conn.commit()
            print(f"Logged job: {title} at {company} (Score: {score})")
        except sqlite3.IntegrityError:
            print(f"Job already logged: {url}")

    def close(self):
        self.conn.close()
