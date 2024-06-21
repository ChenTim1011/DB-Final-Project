from flask import Blueprint, request, jsonify
import sqlite3
from config import DATABASE

favorites_bp = Blueprint('favorites', __name__)

@favorites_bp.route('/view_data/favorites', methods=['GET'])
def view_favorites():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, book_id, book_title FROM FavoriteList")
    data = cursor.fetchall()
    conn.close()
    result = [{
        "id": item[0],
        "book_id": item[1],
        "book_title": item[2]
    } for item in data]
    return jsonify(result)

@favorites_bp.route('/add_favorite', methods=['POST'])
def add_favorite():
    data = request.get_json()
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Check if the book is already in the favorites list
    cursor.execute("SELECT * FROM FavoriteList WHERE book_id = ?", (data['book_id'],))
    existing_favorite = cursor.fetchone()
    if existing_favorite:
        conn.close()
        return jsonify({"message": "該書籍已在我的最愛中！"}), 400

    # Get the book title from the Book table
    cursor.execute("SELECT book_title FROM Book WHERE id = ?", (data['book_id'],))
    book_title = cursor.fetchone()[0]
    
    # Insert into favorites
    cursor.execute("INSERT INTO FavoriteList (book_id, book_title) VALUES (?, ?)", (data['book_id'], book_title))
    conn.commit()
    conn.close()
    return jsonify({"message": "書籍已加入我的最愛！"}), 201

@favorites_bp.route('/delete_favorite/<int:book_id>', methods=['DELETE'])
def delete_favorite(book_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM FavoriteList WHERE book_id = ?", (book_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "書籍已從我的最愛中移除！"}), 200