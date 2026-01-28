import os
import django

# Указываем Django, где лежат настройки (замени 'core' на имя своей папки, если оно другое)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User

def create_superuser():
    username = 'admin_maga'
    password = 'MagaPass123!'
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username, 'admin@example.com', password)
        print(f"Суперпользователь {username} создан!")
    else:
        print(f"Пользователь {username} уже существует.")

if __name__ == '__main__':
    create_superuser()
