from flask import Blueprint, request, jsonify
import sqlite3
from config import DATABASE

author_bp = Blueprint('author', __name__)


@author_bp.route('/add_author', methods=['POST'])
def add_author():
    data = request.get_json()
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    # check if the author_name already exists
    cursor.execute("SELECT COUNT(*) FROM Author WHERE author_name = ?", (data['author_name'],))
    count = cursor.fetchone()[0]
    if count > 0:
        conn.close()
        return jsonify({"message": "不能重複新增同樣的作者"}), 400
   
    cursor.execute("INSERT INTO Author (author_name, introduction, nationality, Birth_year) VALUES (?, ?, ?, ?)",
                    (data['author_name'], data['introduction'], data['nationality'], data['Birth_year']))
    conn.commit()
    conn.close()
    return jsonify({"message": f"作者 {data['author_name']} 新增成功!"}), 200


@author_bp.route('/get_author/<author_name>', methods=['GET'])
def get_author(author_name):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Author WHERE author_name = ?", (author_name,))
    author = cursor.fetchone()
    conn.close()

    if author:
        author_info = {
            "author_id": author[0],
            "author_name": author[1],
            "introduction": author[2],
            "nationality": author[3],
            "Birth_year": author[4]
        }
        return jsonify(author_info), 200
    else:
        return jsonify({"message": "作者不存在"}), 404


@author_bp.route('/update_author', methods=['PUT'])
def update_author():
    try:
        data = request.get_json()
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # Get the original author name
        cursor.execute("SELECT author_name FROM Author WHERE author_id = ?", (data['author_id'],))
        original_author_name = cursor.fetchone()[0]


        cursor.execute('''
            UPDATE Author
            SET author_name = ?, introduction = ?, nationality = ?, Birth_year = ?
            WHERE author_id = ?
        ''', (data['author_name'], data['introduction'], data['nationality'], data['Birth_year'], data['author_id']))


        # UPDATE Book table if the author name is changed
        cursor.execute('''
            UPDATE Book
            SET author = ?
            WHERE author = ?
        ''', (data['author_name'], original_author_name))

        conn.commit()
        conn.close()

        return jsonify({"message": "作者更新成功"}), 200
    except sqlite3.IntegrityError as e:
        return jsonify({"message": f"資料庫錯誤: {str(e)}"}), 500