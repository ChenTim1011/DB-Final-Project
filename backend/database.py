import sqlite3
from config import DATABASE

def create_tables():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Author (
            author_id INTEGER PRIMARY KEY,
            author_name TEXT NOT NULL,
            introduction TEXT,
            nationality TEXT,
            Birth_year INTEGER     
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Book (
            id INTEGER PRIMARY KEY,
            ISBN INTEGER NOT NULL,
            book_title TEXT NOT NULL,
            author TEXT NOT NULL,
            price INTEGER NOT NULL,
            category TEXT NOT NULL,
            edition INTEGER NOT NULL,
            current_page INTEGER NOT NULL,
            pdf_path TEXT,
            FOREIGN KEY(author) REFERENCES Author(author_name) ON DELETE CASCADE
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ReadingHistory (
            id INTEGER PRIMARY KEY,
            time_stamp TEXT NOT NULL,
            book_id INTEGER NOT NULL,
            bookpage INTEGER NOT NULL,
            note TEXT NOT NULL,
            FOREIGN KEY(book_id) REFERENCES Book(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ReadingPlan (
            id INTEGER PRIMARY KEY,
            book_id INTEGER NOT NULL,
            expired_date TEXT NOT NULL,
            is_complete INTEGER NOT NULL,
            FOREIGN KEY(book_id) REFERENCES Book(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Note (
            id INTEGER PRIMARY KEY,
            book_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY(book_id) REFERENCES Book(id) ON DELETE CASCADE
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS FavoriteList (
            id INTEGER PRIMARY KEY,
            book_id INTEGER NOT NULL,
            book_title TEXT NOT NULL,
            FOREIGN KEY(book_id) REFERENCES Book(id)
        )
    ''')


    cursor.execute('CREATE INDEX IF NOT EXISTS idx_category ON Book (category)')
    conn.commit()
    conn.close()

def update_database_schema():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON") 
    # Add pdf_path column if it doesn't exist
    cursor.execute("PRAGMA table_info(Book)")
    columns = [column[1] for column in cursor.fetchall()]
    if 'pdf_path' not in columns:
        cursor.execute("ALTER TABLE Book ADD COLUMN pdf_path TEXT")
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_category ON Book (category)')
    conn.commit()
    conn.close()
