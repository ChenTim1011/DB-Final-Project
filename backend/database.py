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
            Birth_year INTEGER CHECK(Birth_year > 0)     
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Book (
            id INTEGER PRIMARY KEY,
            ISBN INTEGER NOT NULL,
            book_title TEXT NOT NULL,
            author TEXT NOT NULL,
            price INTEGER NOT NULL CHECK(price >= 0),
            category TEXT NOT NULL,
            edition INTEGER NOT NULL CHECK(edition > 0),
            current_page INTEGER NOT NULL CHECK(current_page >= 0),
            pdf_path TEXT,
            FOREIGN KEY(author) REFERENCES Author(author_name) ON DELETE CASCADE
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ReadingHistory (
            id INTEGER PRIMARY KEY,
            time_stamp TEXT NOT NULL,
            book_id INTEGER NOT NULL,
            bookpage INTEGER NOT NULL CHECK(bookpage >= 0),
            note TEXT NOT NULL,
            FOREIGN KEY(book_id) REFERENCES Book(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ReadingPlan (
            id INTEGER PRIMARY KEY,
            book_id INTEGER NOT NULL,
            expired_date TEXT NOT NULL,
            is_complete INTEGER NOT NULL CHECK(is_complete IN (0, 1)),
            FOREIGN KEY(book_id) REFERENCES Book(id) ON DELETE CASCADE
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
            FOREIGN KEY(book_id) REFERENCES Book(id) ON DELETE CASCADE
        )
    ''')

    # Adding indexes to improve performance
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_book_isbn ON Book (ISBN)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_book_author_id ON Author (author_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_note_book_id ON Note (book_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_reading_history_book_id ON ReadingHistory (book_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_reading_plan_book_id ON ReadingPlan (book_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_favorite_list_book_id ON FavoriteList (book_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_category ON Book (category)')
    conn.commit()
    conn.close()


