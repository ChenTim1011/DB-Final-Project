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
            ISBN INTEGER ,
            book_title TEXT NOT NULL,
            author TEXT ,
            price INTEGER  CHECK(price >= 0),
            category TEXT ,
            edition INTEGER CHECK(edition > 0),
            current_page INTEGER CHECK(current_page >= 0),
            pdf_path TEXT,
            FOREIGN KEY(author) REFERENCES Author(author_name) ON DELETE CASCADE
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ReadingHistory (
            id INTEGER PRIMARY KEY,
            time_stamp TEXT ,
            book_id INTEGER NOT NULL,
            bookpage INTEGER CHECK(bookpage >= 0),
            note TEXT NOT NULL,
            FOREIGN KEY(book_id) REFERENCES Book(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ReadingPlan (
            id INTEGER PRIMARY KEY,
            book_id INTEGER ,
            expired_date TEXT ,
            is_complete INTEGER  CHECK(is_complete IN (0, 1)),
            FOREIGN KEY(book_id) REFERENCES Book(id) ON DELETE CASCADE
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Note (
            id INTEGER PRIMARY KEY,
            book_id INTEGER NOT NULL,
            title TEXT ,
            content TEXT ,
            created_at TEXT ,
            updated_at TEXT ,
            FOREIGN KEY(book_id) REFERENCES Book(id) ON DELETE CASCADE
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS FavoriteList (
            id INTEGER PRIMARY KEY,
            book_id INTEGER NOT NULL,
            book_title TEXT ,
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


def insert_initial_data():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM Author")
    author_count = cursor.fetchone()[0]
    # check if Author table has data
    if author_count == 0:
        cursor.executescript('''
        INSERT INTO Author (author_name, introduction, nationality, birth_year) VALUES
        ("J.D. Salinger", "J.D. Salinger was an American writer known for his widely-read novel The Catcher in the Rye.", "USA", 1919),
        ("Rstudio Group", "Rstudio Group is known for developing the R programming language and environment.", "USA", NULL),
        ("Unknown", "Unknown author of the ancient Indian epic, the Mahabharata.", "India", NULL),
        ("Kant", "Immanuel Kant was a German philosopher who is considered a central figure in modern philosophy.", "Germany", 1724),
        ("K. Marx", "Karl Marx was a German philosopher, economist, historian, sociologist, political theorist, journalist and socialist revolutionary.", "Germany", 1818),
        ("Jane Austen", "Jane Austen was an English novelist known primarily for her six major novels.", "UK", 1775),
        ("George Orwell", "George Orwell was an English novelist and essayist, journalist and critic.", "UK", 1903),
        ("曹雪芹", "Cao Xueqin was a Chinese writer during the Qing dynasty, best known as the author of Dream of the Red Chamber.", "China", 1715),
        ("Charles Dickens", "Charles Dickens was an English writer and social critic.", "UK", 1812),
        ("Charles Darwin", "Charles Darwin was an English naturalist, geologist and biologist, best known for his contributions to evolutionary biology.", "UK", 1809),
        ("Friedrich Nietzsche", "Friedrich Nietzsche was a German philosopher, cultural critic, composer, poet, writer, and philologist.", "Germany", 1844),
        ("Henry David Thoreau", "Henry David Thoreau was an American naturalist, essayist, poet, and philosopher.", "USA", 1817),
        ("Gabriel Garcia Marquez", "Gabriel Garcia Marquez was a Colombian novelist, short-story writer, screenwriter, and journalist.", "Colombia", 1927),
        ("Miguel de Cervantes", "Miguel de Cervantes was a Spanish writer widely regarded as the greatest writer in the Spanish language.", "Spain", 1547),
        ("Franz Kafka", "Franz Kafka was a German-speaking Bohemian writer who is widely regarded as one of the major figures of 20th-century literature.", "Czech Republic", 1883),
        ("劉慈欣", "Liu Cixin is a Chinese science fiction writer, known for his Three-Body Problem series.", "China", 1963),
        ("J.K. Rowling", "J.K. Rowling is a British author, best known for the Harry Potter series.", "UK", 1965),
        ("George R.R. Martin", "George R.R. Martin is an American novelist and short-story writer, screenwriter, and television producer.", "USA", 1948);
        ''')

    #check if Book table has data
    cursor.execute("SELECT COUNT(*) FROM Book")
    book_count = cursor.fetchone()[0]

    if book_count == 0:
        cursor.executescript('''
        INSERT INTO Book (ISBN, book_title, author, price, category, edition, current_page, pdf_path) VALUES
        (9789867412, "麥田捕手", "J.D. Salinger", 450, "文學", 1, 100, NULL),
        (9789578626, "R語言生物資訊", "Rstudio Group", 320, "科學", 2, 150, NULL),
        (9789573286, "摩訶婆羅多", "Unknown", 520, "歷史", 3, 200, NULL),
        (9789578691, "純粹理性批判", "Kant", 300, "哲學", 1, 250, NULL),
        (9789866785, "資本論", "K. Marx", 420, "社會學", 2, 300, NULL),
        (9789573486, "傲慢與偏見", "Jane Austen", 320, "西洋文學", 3, 320, NULL),
        (9789578964, "1984", "George Orwell", 520, "西洋文學", 1, 520, NULL),
        (9789766485, "紅樓夢", "曹雪芹", 300, "中國文學", 2, 300, NULL),
        (9789867413, "遠大前程", "Charles Dickens", 400, "西洋文學", 1, 450, NULL),
        (9789578627, "物種起源", "Charles Darwin", 350, "科學", 2, 500, NULL),
        (9789573287, "大衛科波菲爾", "Charles Dickens", 450, "西洋文學", 3, 150, NULL),
        (9789578692, "尼采全集", "Friedrich Nietzsche", 600, "哲學", 1, 100, NULL),
        (9789866786, "查拉圖斯特拉如是說", "Friedrich Nietzsche", 400, "哲學", 2, 200, NULL),
        (9789573487, "瓦爾登湖", "Henry David Thoreau", 300, "文學", 3, 250, NULL),
        (9789578965, "百年孤寂", "Gabriel Garcia Marquez", 350, "文學", 1, 300, NULL),
        (9789766486, "堂吉訶德", "Miguel de Cervantes", 500, "西洋文學", 2, 350, NULL),
        (9789867414, "變形記", "Franz Kafka", 250, "文學", 1, 400, NULL),
        (9789578628, "三體", "劉慈欣", 450, "科幻", 2, 450, NULL),
        (9789573288, "哈利波特", "J.K. Rowling", 600, "奇幻", 3, 500, NULL),
        (9789578693, "冰與火之歌", "George R.R. Martin", 700, "奇幻", 1, 550, NULL);
        ''')
    conn.commit()
    conn.close()