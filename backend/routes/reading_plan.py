from flask import Blueprint, request, jsonify
import sqlite3
from config import DATABASE

plan_bp = Blueprint('plan', __name__)

@plan_bp.route('/add_plan', methods=['POST'])
def add_plan():
    data = request.get_json()
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM ReadingPlan WHERE book_id = ?", (data['book_id'],))
    existing_plan = cursor.fetchone()

    if existing_plan:
        cursor.execute(
            "UPDATE ReadingPlan SET expired_date = ?, is_complete = ? WHERE book_id = ?",
            (data['expired_date'], int(data.get('is_complete', False)), data['book_id'])
        )
        conn.commit()
        conn.close()
        return jsonify({"message": "閱讀計劃已更新！"}), 200
    else:
        cursor.execute(
            "INSERT INTO ReadingPlan (book_id, expired_date, is_complete) VALUES (?, ?, ?)",
            (data['book_id'], data['expired_date'], int(data.get('is_complete', False)))
        )
        conn.commit()
        conn.close()
        return jsonify({"message": "閱讀計劃新增成功！"}), 201

@plan_bp.route('/delete_plan/<int:plan_id>', methods=['DELETE'])
def delete_plan(plan_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ReadingPlan WHERE id = ?", (plan_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "閱讀計劃刪除成功！"}), 200