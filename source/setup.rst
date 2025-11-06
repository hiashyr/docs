Настройка окружения и установка Django
======================================

В этом разделе мы настроим окружение для разработки Django приложения на Windows.

Установка Python
----------------

1. **Проверьте установку** в командной строке:

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

Если команда не работает, то можно использовать сам файл активации виртуального окружения. Для этого нужно просто перекинуть его в терминал и нажать "Enter":

.. image:: /_static/images/venv.png
   :alt: Архитектура приложения
   :align: center
   :width: 400

Установка Django и библиотек
----------------

.. code-block:: batch

   # Убедитесь что виртуальное окружение активировано
   # (должно быть (venv) в начале строки)

   # Установите Django
   pip install django

   # Проверьте установку
   python -m django --version

   # Установие другие, нужные вам, библиотеки
   pip install pillow

Создание Django проекта
-----------------------

.. code-block:: batch

   # Создайте новый Django проект
   django-admin startproject project

   # Структура после создания:
   # myproject/
   # │   manage.py
   # │
   # └───project
   #         settings.py
   #         urls.py
   #         wsgi.py
   #         __init__.py

Запуск проекта
-------------------------

.. code-block:: batch

   # Запустите проект
   python manage.py runserver

   # Откройте браузер и перейдите по:
   # http://127.0.0.1:8000/

   # Вы должны увидеть страницу с ракетой - "The install worked successfully!"

Базовые команды Django
----------------------

.. code-block:: batch

   # Запуск приложения
   python manage.py runserver

   # Создание приложения
   python manage.py startapp myapp

   # Создание миграций
   python manage.py makemigrations

   # Применение миграций
   python manage.py migrate

   # Создание суперпользователя
   python manage.py createsuperuser


Следующий шаг
-------------

После настройки окружения переходите к :doc:`project-structure` чтобы создать структуру проекта.