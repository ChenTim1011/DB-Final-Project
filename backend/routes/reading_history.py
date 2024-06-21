from flask import Blueprint, request, jsonify
import sqlite3
from datetime import datetime
from config import DATABASE

history_bp = Blueprint('history', __name__)

@history_bp.route('/add_history', methods=['POST'])
def add_history():
    data = request.get_json()
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ReadingHistory (time_stamp, book_id, bookpage, note) VALUES (?, ?, ?, ?)",
                   (datetime.utcnow().isoformat(), data['book_id'], data['bookpage'], data['note']))
    conn.commit()
    conn.close()
    return jsonify({"message": "閱讀歷史新增成功！"}), 201