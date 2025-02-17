from flask import Blueprint, request, jsonify
from datetime import datetime
from app import db
from app.models import Educator, Image
from app.utils.auth import token_required
from app.services.event_service import encode_file_to_base64, allowed_file

educator_bp = Blueprint('educator', __name__)

# Получение списка воспитателей с поиском
@educator_bp.route('/educators', methods=['GET'])
@token_required
def get_educators(current_user):
    search_query = request.args.get('search', '').strip()
    query = Educator.query

    if search_query:
        query = query.filter(
            (Educator.full_name.ilike(f'%{search_query}%')) |
            (Educator.description.ilike(f'%{search_query}%'))
        )

    educators = query.order_by(Educator.created_at.desc()).all()

    educators_data = []
    for educator in educators:
        educator_data = {
            'EducatorId': educator.id,
            'fullName': educator.full_name,
            'description': educator.description,
            'photo': None
        }

        if educator.photo:
            educator_data['photo'] = educator.photo.image_data if educator.photo.image_data else None

        educators_data.append(educator_data)

    return jsonify({"educators": educators_data}), 200

# Создание воспитателя
@educator_bp.route('/create-educator', methods=['POST'])
@token_required
def create_educator(current_admin):
    full_name = request.form.get('full_name')
    description = request.form.get('description')

    if not full_name or not description:
        return jsonify({"error": "Поле ФИО и описание обязательны"}), 400

    new_educator = Educator(full_name=full_name, description=description)

    # Проверка на файл (фото воспитателя)
    if 'photo' in request.files:
        file = request.files['photo']

        if allowed_file(file.filename):
            encoded_image = encode_file_to_base64(file)
            image = Image(image_data=encoded_image)
            db.session.add(image)
            db.session.commit()

            new_educator.photo_id = image.id

    db.session.add(new_educator)
    db.session.commit()

    return jsonify({"message": "Воспитатель создан"}), 201

# Редактирование воспитателя
@educator_bp.route('/edit-educator/<int:educator_id>', methods=['PUT'])
@token_required
def edit_educator(current_admin, educator_id):
    educator = Educator.query.get(educator_id)

    if not educator:
        return jsonify({"error": "Воспитатель не найден"}), 404

    full_name = request.form.get('full_name', educator.full_name)
    description = request.form.get('description', educator.description)

    # Проверка на файл и обновление фото
    if 'photo' in request.files:
        file = request.files['photo']

        if allowed_file(file.filename):
            if educator.photo_id:
                image = Image.query.get(educator.photo_id)
                if image:
                    encoded_image = encode_file_to_base64(file)
                    image.image_data = encoded_image
                    db.session.commit()
                else:
                    return jsonify({"error": "Изображение не найдено"}), 404
            else:
                encoded_image = encode_file_to_base64(file)
                image = Image(image_data=encoded_image)
                db.session.add(image)
                db.session.commit()
                educator.photo_id = image.id

    educator.full_name = full_name
    educator.description = description
    db.session.commit()

    return jsonify({"message": "Воспитатель обновлен"}), 200

# Удаление воспитателя
@educator_bp.route('/delete-educator/<int:educator_id>', methods=['DELETE'])
@token_required
def delete_educator(current_admin, educator_id):
    educator = Educator.query.get(educator_id)

    if not educator:
        return jsonify({"error": "Воспитатель не найден"}), 404

    db.session.delete(educator)
    db.session.commit()

    return jsonify({"message": "Воспитатель удален"}), 200
