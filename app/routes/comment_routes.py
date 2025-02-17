from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Comment, User, Event
from datetime import datetime, timedelta
import pytz

comments_bp = Blueprint('comments', __name__)
Kyrgyzstan_tz = pytz.timezone('Asia/Bishkek')


def format_time_ago(timestamp):
    if timestamp.tzinfo is None:  # Проверяем, есть ли у даты информация о таймзоне
        timestamp = Kyrgyzstan_tz.localize(timestamp)  # Приводим к зоне Asia/Bishkek

    now = datetime.now(Kyrgyzstan_tz)
    delta = now - timestamp

    if delta < timedelta(minutes=1):
        return "только что"
    elif delta < timedelta(hours=1):
        return f"{delta.seconds // 60} мин. назад"
    elif delta < timedelta(days=1):
        return f"{delta.seconds // 3600} ч. назад"
    elif delta < timedelta(days=30):
        return f"{delta.days} дн. назад"
    else:
        return timestamp.strftime("%Y-%m-%d")


# ✅ Добавление комментария или ответа
@comments_bp.route('/comments', methods=['POST'])
def add_comment():
    data = request.json
    user_id = data.get("user_id")
    event_id = data.get("event_id")
    content = data.get("content")
    parent_id = data.get("parent_id")  # parent_id нужен для ответов

    if not user_id or not event_id or not content:
        return jsonify({"error": "Все поля должны быть заполнены"}), 400

    user = User.query.get(user_id)
    event = Event.query.get(event_id)

    if not user or not event:
        return jsonify({"error": "Пользователь или событие не найдено"}), 404

    # Создаем комментарий или ответ
    comment = Comment(
        user_id=user_id,
        event_id=event_id,
        content=content,
        created_at=datetime.now(Kyrgyzstan_tz),
        parent_id=parent_id
    )
    db.session.add(comment)

    # Обновляем количество комментариев у события
    event.comments_count = (event.comments_count or 0) + 1
    db.session.commit()

    return jsonify({
        "message": "Комментарий добавлен",
        "comment_id": comment.id,
        "comments_count": event.comments_count
    }), 201


# ✅ Получение комментариев с ответами
@comments_bp.route('/events/<int:event_id>/comments', methods=['GET'])
def get_comments(event_id):
    event = Event.query.get(event_id)
    if not event:
        return jsonify({"error": "Событие не найдено"}), 404

    comments = db.session.query(
        Comment.id,
        Comment.event_id,
        Comment.user_id,
        Comment.content,
        Comment.created_at,
        User.first_name,
        User.last_name,
        Comment.parent_id
    ).join(User).filter(Comment.event_id == event_id).all()

    # 🔥 Создаем словарь комментариев по ID
    comments_dict = {c.id: {
        "id": c.id,
        "first_name": c.first_name,
        "last_name": c.last_name,
        "content": c.content,
        "user_id": c.user_id,
        "event_id": c.event_id,
        "created_at": c.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "time_ago": format_time_ago(c.created_at),
        "parent_id": c.parent_id,
        "replies": []
    } for c in comments}

    # 🔥 Строим древовидную структуру (комментарии + ответы)
    comments_data = []
    for comment in comments:
        if comment.parent_id:
            # Если есть parent_id, то это ответ, добавляем его в `replies` родительского комментария
            parent = comments_dict.get(comment.parent_id)
            if parent:
                parent["replies"].append(comments_dict[comment.id])
        else:
            # Основные комментарии без parent_id
            comments_data.append(comments_dict[comment.id])

    return jsonify({
        "comments_count": len(comments_data),
        "comments": comments_data
    })


@comments_bp.route('/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    comment = Comment.query.get(comment_id)
    if not comment:
        return jsonify({"error": "Комментарий не найден"}), 404

    event = Event.query.get(comment.event_id)

    if comment.parent_id:
        # ✅ Если это ответ, удаляем только его
        db.session.delete(comment)
        comments_removed = 1  # Удалился один ответ
    else:
        # ✅ Если это основной комментарий, считаем его и все ответы
        comments_removed = db.session.query(Comment).filter(
            (Comment.id == comment_id) | (Comment.parent_id == comment_id)
        ).count()

        # Удаляем сам комментарий и все его ответы
        db.session.query(Comment).filter(
            (Comment.id == comment_id) | (Comment.parent_id == comment_id)
        ).delete(synchronize_session=False)

    # 🔥 Обновляем счетчик комментариев у события
    if event and event.comments_count >= comments_removed:
        event.comments_count -= comments_removed

    db.session.commit()

    return jsonify({
        "message": "Комментарий удален",
        "comments_count": event.comments_count
    }), 200
