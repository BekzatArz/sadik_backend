import base64
from app.models import Event, Image
from app.extensions import db
from datetime import datetime

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """Проверка разрешенного расширения файла."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def encode_file_to_base64(file):
    return base64.b64encode(file.read()).decode('utf-8')

def create_event(data, file=None):
    try:
        # Преобразуем время в datetime
        event_start_time = datetime.strptime(data['event_start_time'], "%H:%M")
        
        
        event = Event(
            event_name=data['event_name'],
            event_description=data['event_description'],
            event_date=datetime.strptime(data['event_date'], "%Y-%m-%d"),
            event_start_time=event_start_time,
            event_address=data['event_address'],
            event_admin_id=data['event_admin_id'],
        )
        
        # Если передан файл, кодируем его в Base64 и сохраняем в таблицу Image
        if file and allowed_file(file.filename):
            encoded_image = encode_file_to_base64(file)
            image = Image(image_data=encoded_image)
            db.session.add(image)
            db.session.commit()  # Сохраняем изображение в базе

            # Присваиваем ID изображения в поле event_preview события
            event.event_preview = image.id
        
        # Сохраняем событие в базе данных
        db.session.add(event)
        db.session.commit()
        
        return event
    except Exception as e:
        db.session.rollback()
        print(f"Ошибка при создании события: {e}")
        return None
