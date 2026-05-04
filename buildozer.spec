[app]

# Название приложения (на экране телефона)
title = Core Project

# Внутреннее имя пакета
package.name = workoutapp

# Домен (обычно org.ваше_имя)
package.domain = org.workout

# Путь к исходникам
source.dir = .

# Включаемые расширения файлов (добавил wav для звуков!)
source.include_exts = py,png,jpg,kv,atlas,wav

# Версия приложения
version = 1.0.0

# Требуемые библиотеки
requirements = python3,kivy,kivymd,pyjnius

# Ориентация экрана
orientation = portrait

# Цвета фона (опционально)
# window.background_color = 0.95,0.94,0.92,1

# Иконка (если есть, раскомментируйте)
# icon.filename = icon.png

# Разрешения Android (для звука!)
android.permissions = INTERNET, RECORD_AUDIO, MODIFY_AUDIO_SETTINGS, VIBRATE

# Настройки Android SDK/NDK
android.api = 33
android.minapi = 21
android.ndk = 25b

# Автоматическое принятие лицензий
android.accept_sdk_license = True

# Логгирование
log_level = 2

# Игнорировать ошибки с Cython (для совместимости)
ignore_setup_py = True
