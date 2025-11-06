Создание структуры проекта
=======================================

В этом разделе мы создадим структуру для нашего приложения и настроим файлы для работы системы.

Создание Django приложения
-----------------------

.. code-block:: batch

   # Создайте приложение django
   python manage.py startapp main

   # Структура после создания:
   # myproject/
   # │   manage.py
   # │
   # └───project
   # |       settings.py
   # |       urls.py
   # |       wsgi.py
   # |       __init__.py
   # └───main
   #         admin.py
   #         apps.py
   #         models.py
   #         tests.py
   #         views.py

Настройка settings.py
---------------------

Теперь нужно зарегистрировать наше приложение в настройках проекта. 
Откройте файл `project/settings.py` и найдите раздел `INSTALLED_APPS`:

.. code-block:: python
   :linenos:
   :emphasize-lines: 11-14

   INSTALLED_APPS = [
       'django.contrib.admin',
       'django.contrib.auth',
       'django.contrib.contenttypes',
       'django.contrib.sessions',
       'django.contrib.messages',
       'django.contrib.staticfiles',
       # Добавляем наше приложение
       'main'
   ]

Создание папок для статических и медиа файлов
---------------------------------------------

.. code-block:: batch

   # Создайте папки в директории приложения main
   mkdir static
   mkdir templates

В папке static будем хранить стили, изображения. В папке templates будем хранить html-шаблоны.

После настройки окружения переходите к :doc:`models` чтобы создать структуру проекта.