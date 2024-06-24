from flask import Blueprint, request, jsonify
import sqlite3
from datetime import datetime
from config import DATABASE
def get_book_ids():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM Book")
    return [id[0] for id in cursor.fetchall()]


history_bp = Blueprint('history', __name__)

@history_bp.route('/add_history', methods=['POST'])
def add_history():
    data = request.get_json()
    if data['book_id'].strip() == '':
        return jsonify({"message": "書籍ID不得空白！"}), 200
    if not int(data['book_id']) in get_book_ids():
        return jsonify({"message": "書籍ID不存在！"}), 201
    if data['bookpage'].strip() == '':
        return jsonify({"message": "書頁不得空白！"}), 200
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d') 
    cursor.execute("INSERT INTO ReadingHistory (time_stamp, book_id, bookpage, note) VALUES (?, ?, ?, ?)",
                   (timestamp, data['book_id'], data['bookpage'], data['note']))
    conn.commit()
    conn.close()
    return jsonify({"message": "閱讀歷史新增成功！"}), 201


@history_bp.route('/delete_history/<int:history_id>', methods=['DELETE'])
def delete_history(history_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ReadingHistory WHERE id = ?", (history_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "閱讀歷史刪除成功！"}), 200