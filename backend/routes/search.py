from flask import Blueprint, request, jsonify
import sqlite3
from config import DATABASE

search_bp = Blueprint('search', __name__)

@search_bp.route('/search_by_category', methods=['GET'])
def search_by_category():
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

@search_bp.route('/search_book/<int:book_id>', methods=['GET'])
def search_book(book_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Book WHERE id = ?", (book_id,))
    book = cursor.fetchone()
    conn.close()
    if book:
        result = {
            "id": book[0],
            "ISBN": book[1],
            "book_title": book[2],
            "author": book[3],
            "price": book[4],
            "category": book[5],
            "edition": book[6],
            "current_page": book[7]
        }
        return jsonify(result)
    else:
        return jsonify({"message": "書籍未找到！"}), 404


@search_bp.route('/view_data/<table>', methods=['GET'])
def view_data(table):
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