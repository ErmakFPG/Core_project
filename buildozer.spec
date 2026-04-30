[app]
# Название программы (на экране телефона)
title = My First App

# Внутреннее имя пакета (уникальный идентификатор)
package.name = myapp

# Домен вашего сайта (обычно org.ваше_имя)
package.domain = org.username

# Файл, с которого всё начинается
source.dir = .

# ВАЖНО: Укажите все нужные библиотеки
requirements = python3,kivy,kivymd,requests,openssl

# Ориентация экрана
orientation = portrait

# Иконка (поместите файл в папку с проектом)
icon.filename = my_icon.png

# Целевая версия Android (рекомендую 31 или 33)
android.api = 33
android.minapi = 21
android.ndk = 25b

# Обязательно согласитесь с лицензией (для автоматической сборки)
android.accept_sdk_license = True
