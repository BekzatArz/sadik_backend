from flask import Blueprint, request, jsonify, current_app
from app.models import Event, Image
from app.extensions import db
from app.utils.auth import token_required
from werkzeug.utils import secure_filename
import os
from app.services.event_service import create_event, allowed_file
import base64
from datetime import datetime
import re


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def encode_file_to_base64(file):
    return base64.b64encode(file.read()).decode('utf-8')

event_bp = Blueprint('event', __name__)

# Создание события..........................................................................................
@event_bp.route('/create-event', methods=['POST'])
@token_required
def create_event_route(current_admin):
    event_name = request.form.get('event_name')
    event_description = request.form.get('event_description')
    event_date = request.form.get('event_date')
    start_time = request.form.get('start_time')
    event_address = request.form.get('event_address')
    file = request.files.get('file')

    if not all([event_name, event_description, event_date, start_time, event_address]):
        return jsonify({"error": "Не все обязательные поля заполнены"}), 400
    
    if file and not allowed_file(file.filename):
        return jsonify({"error": "Неверный тип файла"}), 400
    
    data = {
        "event_name": event_name,
        "event_description": event_description,
        "event_date": event_date,
        "event_start_time": start_time,
        "event_address": event_address,
        "event_admin_id": current_admin.id
    }

    event = create_event(data, file) if file else create_event(data, None)
    if not event:
        return jsonify({"error": "Ошибка при создании события"}), 500

    return jsonify({"message": "Событие создано", "event_id": event.id}), 201

# Получение списка событий.................................................................................
@event_bp.route('/events', methods=['GET'])
@token_required
def get_events_route(current_user):
    user_id = current_user.id
    search_query = request.args.get('search', '').strip()

    query = Event.query

    if search_query:
        query = query.filter(
            (Event.event_name.ilike(f'%{search_query}%')) |
            (Event.event_description.ilike(f'%{search_query}%')) |
            (Event.event_address.ilike(f'%{search_query}%'))
        )

    events = query.order_by(Event.created_at.desc()).all()

    events_data_list = []
    for event in events:
        event_data = {
            'event_id': event.id,
            'event_name': event.event_name,
            'event_description': event.event_description,
            'event_date': event.event_date.strftime("%Y-%m-%d"),
            'event_start_time': event.event_start_time.strftime("%H:%M"),
            'event_address': event.event_address,
            'comments_count': event.comments_count
        }

        if event.event_preview:
            image = Image.query.get(event.event_preview)
            if image:
                event_data['event_preview'] = f'{image.image_data}' if image.image_data else None
            else:
                event_data['event_preview'] = None

        events_data_list.append(event_data)

    return jsonify({"events": events_data_list}), 200

# Получение событий администратора..........................................................................
@event_bp.route('/admin-events', methods=['GET'])
@token_required
def get_admins_events(current_admin):
    admin_id = current_admin.id
    
    events = Event.query.filter_by(event_admin_id=admin_id).order_by(Event.created_at.desc()).all()

    events_data_list = []
    for event in events:
        event_data = {
            "event_id": event.id,
            'event_name': event.event_name,
            'event_description': event.event_description,
            'event_date': event.event_date.strftime("%Y-%m-%d"),
            'event_start_time': event.event_start_time.strftime("%H:%M"),
            'event_address': event.event_address,
            'comments_count': event.comments_count
        }

        if event.event_preview:
            image = Image.query.get(event.event_preview)
            if image:
                event_data['event_preview'] = f'{image.image_data}' if image.image_data else None
            else:
                event_data['event_preview'] = None

        events_data_list.append(event_data)

    return jsonify({"events": events_data_list}), 200

#Получение одного события....................................................................................
@event_bp.route('/admin-event/<int:event_id>', methods=['GET'])
@token_required
def get_admin_event(current_admin, event_id):
    event = Event.query.filter_by(id=event_id, event_admin_id=current_admin.id).first()
    
    if not event:
        return jsonify({"error": "Событие не найдено или у вас нет прав на просмотр"}), 403
    
    event_data = {
        "event_id": event.id,
        "event_name": event.event_name,
        "event_description": event.event_description,
        "event_date": event.event_date.strftime("%Y-%m-%d"),
        "event_start_time": event.event_start_time.strftime("%H:%M"),
        "event_address": event.event_address,
        "comments_count": event.comments_count
    }
    
    if event.event_preview:
        image = Image.query.get(event.event_preview)
        event_data['event_preview'] = f'{image.image_data}' if image and image.image_data else None
    else:
        event_data['event_preview'] = None
    
    return jsonify(event_data), 200

@event_bp.route('/edit-event/<int:event_id>', methods=['PUT'])
@token_required
def edit_event(current_admin, event_id):
    # Ищем событие по ID и проверяем права администратора
    event = Event.query.filter_by(id=event_id, event_admin_id=current_admin.id).first()
    
    if not event:
        return jsonify({"error": "Событие не найдено или у вас нет прав на редактирование"}), 403
    
    # Получаем данные из формы или оставляем старые значения
    event_name = request.form.get('event_name', event.event_name)
    event_description = request.form.get('event_description', event.event_description)
    event_date = request.form.get('event_date', event.event_date)
    event_start_time = request.form.get('event_start_time', event.event_start_time)
    event_address = request.form.get('event_address', event.event_address)
    
    print(f"Received time: '{event_start_time}'")  # Логируем перед обработкой

    # Проверка на файл и обновление изображения
    if 'event_preview' in request.files:
        file = request.files['event_preview']
        
        if allowed_file(file.filename):  # Проверяем, что файл имеет разрешенное расширение
            # Если у события уже есть изображение, находим его по ID
            if event.event_preview:
                image = Image.query.get(event.event_preview)  # Находим изображение по старому ID
                if image:
                    # Кодируем новый файл в base64 и обновляем старое изображение
                    encoded_image = encode_file_to_base64(file)
                    image.image_data = encoded_image  # Обновляем данные изображения
                    db.session.commit()  # Сохраняем изменения в базе
                else:
                    return jsonify({"error": "Изображение не найдено"}), 404
            else:
                # Если изображения нет, создаем новое изображение и сохраняем
                encoded_image = encode_file_to_base64(file)
                image = Image(image_data=encoded_image)
                db.session.add(image)
                db.session.commit()
                event.event_preview = image.id  # Присваиваем новое изображение событию

    # Обновляем остальные данные события
    try:
        if event_date:
            event.event_date = datetime.strptime(event_date, "%Y-%m-%d")

        # Извлекаем только время (часы и минуты), игнорируя секунды
        if event_start_time:
            time_part = event_start_time.split(" ")[-1]  # Берем только HH:MM:SS
            print(f"Extracted time: {time_part}")  # Логируем извлеченное время
            
            # Обрезаем секунды и преобразуем время в формат HH:MM
            time_without_seconds = time_part[:5]  # Получаем только первые 5 символов (HH:MM)
            print(f"Time without seconds: {time_without_seconds}")  # Логируем время без секунд
            
            # Преобразуем в формат времени, добавив текущую дату
            event.event_start_time = datetime.combine(datetime.today(), datetime.strptime(time_without_seconds, "%H:%M").time())

    except ValueError as e:
        return jsonify({"error": f"Ошибка преобразования времени или даты: {str(e)}"}), 400

    # Обновление остальных данных
    event.event_name = event_name
    event.event_description = event_description
    event.event_address = event_address
    
    # Сохраняем изменения в базе данных
    db.session.commit()  
    
    return jsonify({"message": "Событие обновлено"}), 200

#Удаления ивента..........................................................................................
@event_bp.route('/delete-event/<int:event_id>', methods=['DELETE'])
@token_required
def delete_event(current_admin, event_id):
    # Ищем событие, которое удаляет администратор
    event = Event.query.filter_by(id=event_id, event_admin_id=current_admin.id).first()
    
    if not event:
        return jsonify({"error": "Событие не найдено или у вас нет прав на удаление"}), 403
    
    db.session.delete(event)
    db.session.commit()
    
    return jsonify({"message": "Событие удалено"}), 200
