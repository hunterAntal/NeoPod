# database_manager.py

import sqlite3
from config import DATABASE_NAME

class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE_NAME)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS podcasts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                feed_url TEXT UNIQUE,
                description TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS episodes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                podcast_id INTEGER,
                title TEXT,
                url TEXT,
                pub_date TEXT,
                duration TEXT,
                is_downloaded INTEGER DEFAULT 0,
                file_path TEXT,
                FOREIGN KEY(podcast_id) REFERENCES podcasts(id)
            )
        ''')

        self.conn.commit()

    def add_podcast(self, title, feed_url, description):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO podcasts (title, feed_url, description)
            VALUES (?, ?, ?)
        ''', (title, feed_url, description))
        self.conn.commit()

    def get_subscriptions(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, title FROM podcasts')
        return cursor.fetchall()

    def get_podcast_by_feed_url(self, feed_url):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, title FROM podcasts WHERE feed_url = ?', (feed_url,))
        return cursor.fetchone()

    def close(self):
        self.conn.close()
