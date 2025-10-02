Настройка окружения и установка Django
======================================

В этом разделе мы настроим окружение для разработки Django приложения на Windows.

Установка Python
----------------

1. **Скачайте Python** с официального сайта:
   https://www.python.org/downloads/

2. **При установке отметьте** "Add Python to PATH"

3. **Проверьте установку** в командной строке:

.. code-block:: batch

   python --version
   # Должно показать: Python 3.x.x

   pip --version
   # Должно показать: pip 2x.x.x

Создание виртуального окружения
-------------------------------

Виртуальное окружение изолирует зависимости вашего проекта.

.. code-block:: batch

   # Создайте папку для проекта
   mkdir myproject
   cd myproject

   # Создайте виртуальное окружение
   python -m venv venv

   # Активируйте виртуальное окружение
   venv\Scripts\activate

   # В командной строке должно появиться (venv)

Установка Django
----------------

.. code-block:: batch

   # Убедитесь что виртуальное окружение активировано
   # (должно быть (venv) в начале строки)

   # Установите Django
   pip install django

   # Проверьте установку
   python -m django --version

Создание Django проекта
-----------------------

.. code-block:: batch

   # Создайте новый Django проект
   django-admin startproject flower_shop .

   # Структура после создания:
   # flower_shop/
   # │   manage.py
   # │
   # └───flower_shop
   #         settings.py
   #         urls.py
   #         wsgi.py
   #         __init__.py

Запуск сервера разработки
-------------------------

.. code-block:: batch

   # Запустите сервер разработки
   python manage.py runserver

   # Откройте браузер и перейдите по:
   # http://127.0.0.1:8000/

   # Вы должны увидеть страницу с ракетой - "The install worked successfully!"

Базовые команды Django
----------------------

.. code-block:: batch

   # Создание приложения
   python manage.py startapp myapp

   # Создание миграций
   python manage.py makemigrations

   # Применение миграций
   python manage.py migrate

   # Создание суперпользователя
   python manage.py createsuperuser

   # Запуск тестов
   python manage.py test

Установка зависимостей:
-------------------------

В нашем проекте используются следующие зависимости:

.. code-block:: batch

   # Создайте файл зависимостей
   pip install Django
   pip install Pillow
   pip install django-crispy-forms
   pip install crispy-bootstrap5
   pip install django-widget-tweaks

Полезные команды для работы с виртуальным окружением
----------------------------------------------------

.. code-block:: batch

   # Деактивация виртуального окружения
   deactivate

   # Повторная активация (из папки проекта)
   venv\Scripts\activate

   # Просмотр установленных пакетов
   pip list

   # Установка конкретной версии Django
   pip install django==4.2.7

Следующий шаг
-------------

После настройки окружения переходите к :doc:`project-structure` чтобы создать структуру проекта.

.. note::

   **Совет:** Добавьте папку `venv` в `.gitignore` если используете Git!