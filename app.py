from flask import Flask, request, jsonify, render_template
import sqlite3
from datetime import datetime

app = Flask(__name__)
DATABASE = 'library.db'

def create_tables():
    """Create the necessary tables in the database."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Book (
            id INTEGER PRIMARY KEY,
            ISBN TEXT NOT NULL,
            book_title TEXT NOT NULL,
            author TEXT NOT NULL,
            price INTEGER NOT NULL,
            category TEXT NOT NULL,
            edition TEXT NOT NULL,
            current_page INTEGER NOT NULL
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
    conn.commit()
    conn.close()

@app.route('/')
def index():
    """Render the main HTML page."""
    return render_template('index.html')

@app.route('/check_book', methods=['POST'])
def check_book():
    """Check if a book with the same title already exists."""
    data = request.get_json()
    book_title = data['book_title']
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Book WHERE book_title = ?", (book_title,))
    existing_book = cursor.fetchone()
    conn.close()
    if existing_book:
        return jsonify({"message": "已有同名書籍，是否仍要新增？", "existing": True}), 200
    return jsonify({"existing": False}), 200

@app.route('/add_book', methods=['POST'])
def add_book():
    """Add a new book to the database."""
    data = request.get_json()
    book_title = data['book_title']
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Book WHERE book_title = ?", (book_title,))
    existing_book = cursor.fetchone()

    if existing_book:
        if '(' in book_title:
            count = int(book_title.split('(')[1].split(')')[0]) + 1
            new_book_title = f"{book_title.split('(')[0]}({count})"
        else:
            new_book_title = f"{book_title}(1)"
    else:
        new_book_title = book_title

    cursor.execute("INSERT INTO Book (ISBN, book_title, author, price, category, edition, current_page) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                   (data['ISBN'], new_book_title, data['author'], data['price'], data['category'], data['edition'], data['current_page']))
    conn.commit()
    conn.close()
    return jsonify({"message": f"書籍 {new_book_title} 新增成功！"}), 201

@app.route('/add_history', methods=['POST'])
def add_history():
    """Add a new reading history record."""
    data = request.get_json()
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ReadingHistory (time_stamp, book_id, bookpage, note) VALUES (?, ?, ?, ?)", 
                   (datetime.utcnow().isoformat(), data['book_id'], data['bookpage'], data['note']))
    conn.commit()
    conn.close()
    return jsonify({"message": "閱讀歷史新增成功！"}), 201

@app.route('/add_plan', methods=['POST'])
def add_plan():
    """Add or update a reading plan."""
    data = request.get_json()
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Check if a reading plan for the same book already exists
    cursor.execute("SELECT * FROM ReadingPlan WHERE book_id = ?", (data['book_id'],))
    existing_plan = cursor.fetchone()

    if existing_plan:
        # Update existing reading plan
        cursor.execute(
            "UPDATE ReadingPlan SET expired_date = ?, is_complete = ? WHERE book_id = ?",
            (data['expired_date'], int(data.get('is_complete', False)), data['book_id'])
        )
        conn.commit()
        conn.close()
        return jsonify({"message": "閱讀計劃已更新！"}), 200
    else:
        # Add new reading plan
        cursor.execute(
            "INSERT INTO ReadingPlan (book_id, expired_date, is_complete) VALUES (?, ?, ?)",
            (data['book_id'], data['expired_date'], int(data.get('is_complete', False)))
        )
        conn.commit()
        conn.close()
        return jsonify({"message": "閱讀計劃新增成功！"}), 201

@app.route('/update_page', methods=['PUT'])
def update_page():
    """Update the current page of a book."""
    data = request.get_json()
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("UPDATE Book SET current_page = ? WHERE id = ?", (data['current_page'], data['book_id']))
    conn.commit()
    conn.close()
    return jsonify({"message": "目前頁數更新成功！"}), 200

@app.route('/delete_data', methods=['DELETE'])
def delete_data():
    """Delete a record from the specified table."""
    data = request.get_json()
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    if data['table'] == '書籍':
        cursor.execute("SELECT * FROM Book WHERE id = ?", (data['id'],))
        item = cursor.fetchone()
        if item:
            cursor.execute("DELETE FROM Book WHERE id = ?", (data['id'],))
        else:
            conn.close()
            return jsonify({"message": "書籍ID不存在！"}), 404
    elif data['table'] == '閱讀歷史':
        cursor.execute("SELECT * FROM ReadingHistory WHERE id = ?", (data['id'],))
        item = cursor.fetchone()
        if item:
            cursor.execute("DELETE FROM ReadingHistory WHERE id = ?", (data['id'],))
        else:
            conn.close()
            return jsonify({"message": "閱讀歷史ID不存在！"}), 404
    elif data['table'] == '閱讀計劃':
        cursor.execute("SELECT * FROM ReadingPlan WHERE id = ?", (data['id'],))
        item = cursor.fetchone()
        if item:
            cursor.execute("DELETE FROM ReadingPlan WHERE id = ?", (data['id'],))
        else:
            conn.close()
            return jsonify({"message": "閱讀計劃ID不存在！"}), 404
    else:
        conn.close()
        return jsonify({"message": "無效的表格名稱！"}), 400
    conn.commit()
    conn.close()
    return jsonify({"message": "資料刪除成功！"}), 200

@app.route('/search_by_category', methods=['GET'])
def search_by_category():
    """Search books by category."""
    category = request.args.get('category')
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Book WHERE category = ?", (category,))
    books = cursor.fetchall()
    conn.close()
    return jsonify([{
        "id": book[0],
        "ISBN": book[1],
        "book_title": book[2],
        "author": book[3],
        "price": book[4],
        "category": book[5],
        "edition": book[6],
        "current_page": book[7]
    } for book in books])

@app.route('/search_by_name', methods=['GET'])
def search_by_name():
    """Search books by name."""
    name = request.args.get('name')
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Book WHERE book_title LIKE ?", ('%' + name + '%',))
    books = cursor.fetchall()
    conn.close()
    return jsonify([{
        "id": book[0],
        "ISBN": book[1],
        "book_title": book[2],
        "author": book[3],
        "price": book[4],
        "category": book[5],
        "edition": book[6],
        "current_page": book[7]
    } for book in books])

@app.route('/view_data/<table>', methods=['GET'])
def view_data(table):
    """View data from the specified table."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    if table == 'books':
        cursor.execute("SELECT * FROM Book")
        data = cursor.fetchall()
        result = [{
            "id": item[0],
            "ISBN": item[1],
            "book_title": item[2],
            "author": item[3],
            "price": item[4],
            "category": item[5],
            "edition": item[6],
            "current_page": item[7]
        } for item in data]
    elif table == 'history':
        cursor.execute("SELECT * FROM ReadingHistory")
        data = cursor.fetchall()
        result = [{
            "id": item[0],
            "time_stamp": item[1],
            "book_id": item[2],
            "bookpage": item[3],
            "note": item[4]
        } for item in data]
    elif table == 'plan':
        cursor.execute("SELECT * FROM ReadingPlan")
        data = cursor.fetchall()
        result = [{
            "id": item[0],
            "book_id": item[1],
            "expired_date": item[2],
            "is_complete": item[3]
        } for item in data]
    else:
        conn.close()
        return jsonify({"message": "無效的表格名稱！"}), 400
    conn.close()
    return jsonify(result)

if __name__ == '__main__':
    create_tables()  # Create tables
    app.run(debug=True)
