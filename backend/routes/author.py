from flask import Blueprint, request, jsonify
import sqlite3
from config import DATABASE

author_bp = Blueprint('author', __name__)


@author_bp.route('/add_author', methods=['POST'])
def add_author():
    data = request.get_json()
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
   
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
    data = request.get_json()
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE Author
        SET author_name = ?, introduction = ?, nationality = ?, Birth_year = ?
        WHERE author_id = ?
    ''', (data['author_name'], data['introduction'], data['nationality'], data['Birth_year'], data['author_id']))

    conn.commit()
    conn.close()

    return jsonify({"message": "作者更新成功"}), 200