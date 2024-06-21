from flask import Blueprint, request, jsonify, render_template
import sqlite3
from datetime import datetime
from config import DATABASE

notes_bp = Blueprint('notes', __name__)

@notes_bp.route('/notes/<int:book_id>', methods=['GET'])
def view_notes(book_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT book_title FROM Book WHERE id = ?", (book_id,))
    book_title = cursor.fetchone()[0]
    cursor.execute("SELECT * FROM Note WHERE book_id = ?", (book_id,))
    notes = cursor.fetchall()
    conn.close()
    return render_template('notes.html', book_id=book_id, book_title=book_title, notes=notes)

@notes_bp.route('/delete_note/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Note WHERE id = ?", (note_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "筆記已刪除！"}), 200

@notes_bp.route('/add_note', methods=['POST'])
def add_note():
    data = request.get_json()
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Note (book_id, title, content, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
                   (data['book_id'], data['title'], data['content'], datetime.utcnow().isoformat(), datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()
    return jsonify({"message": "筆記已新增！"}), 201

@notes_bp.route('/update_note', methods=['PUT'])
def update_note():
    data = request.get_json()
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("UPDATE Note SET title = ?, content = ?, updated_at = ? WHERE id = ?",
                   (data['title'], data['content'], datetime.utcnow().isoformat(), data['id']))
    conn.commit()
    conn.close()
    return jsonify({"message": "筆記已更新！"}), 200
