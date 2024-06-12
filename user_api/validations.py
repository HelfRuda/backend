from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
UserModel = get_user_model()

def custom_validation(data):
    if 'email' not in data:
        raise ValidationError('Отсутствует ключ "email" в данных запроса')
    if 'username' not in data:
        raise ValidationError('Отсутствует ключ "username" в данных запроса')
    if 'password' not in data:
        raise ValidationError('Отсутствует ключ "password" в данных запроса')

    email = data['email'].strip()
    username = data['username'].strip()
    password = data['password'].strip()

    if not email or UserModel.objects.filter(email=email).exists():
        raise ValidationError('Пожалуйста, укажите другой адрес электронной почты')

    if not password or len(password) < 8:
        raise ValidationError('Пароль должен содержать минимум 8 символов')

    if not username:
        raise ValidationError('Пожалуйста, выберите имя пользователя')

    return data


def validate_email(data):
    email = data['email'].strip()
    if not email:
        raise ValidationError('мыло нужно')
    return True

def validate_username(data):
    username = data['username'].strip()
    if not username:
        raise ValidationError('имя впиши')
    return True

def validate_password(data):
    password = data['password'].strip()
    if not password:
        raise ValidationError('про пароль забыл')
    return True