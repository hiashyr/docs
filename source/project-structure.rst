Создание структуры проекта Flower Shop
=======================================

В этом разделе мы создадим структуру для нашего интернет-магазина цветов "Flower Shop". 
Мы создадим основной проект и три приложения: main, orders и user_auth.

Создание Django проекта
-----------------------

Убедитесь, что вы находитесь в папке проекта и виртуальное окружение активировано:

.. code-block:: batch

   # Активируйте виртуальное окружение (если еще не активировано)
   venv\Scripts\activate

   # Создайте Django проект с именем ekz
   django-admin startproject ekz .

   # Структура после создания:
   # .
   # │   manage.py
   # │
   # └───ekz
   #         settings.py
   #         urls.py
   #         wsgi.py
   #         __init__.py

Создание приложений
-------------------

Django приложения - это модули, которые выполняют конкретные функции. 
Создадим приложение для нашего магазина:

.. code-block:: batch

   python manage.py startapp 

Структура проекта после создания приложений:

.. code-block:: text

   flower_shop_project/
   │   manage.py
   │
   ├───ekz/                 # Настройки проекта
   │   │   settings.py
   │   │   urls.py
   │   │   wsgi.py
   │   │   __init__.py
   │   │
   │   └───__pycache__/
   │
   ├───front/                        # Основное приложение
   │   │   admin.py
   │   │   apps.py
   │   │   models.py
   │   │   tests.py
   │   │   views.py
   │   │   __init__.py
   │   │
   │   └───migrations/
   │           __init__.py
   │
   └───venv/                        # Виртуальное окружение

Настройка settings.py
---------------------

Теперь нужно зарегистрировать наши приложения в настройках проекта. 
Откройте файл `ekz/settings.py` и найдите раздел `INSTALLED_APPS`:

.. code-block:: python
   :linenos:
   :emphasize-lines: 11-14

   # flower_shop/settings.py

   INSTALLED_APPS = [
       'django.contrib.admin',
       'django.contrib.auth',
       'django.contrib.contenttypes',
       'django.contrib.sessions',
       'django.contrib.messages',
       'django.contrib.staticfiles',
       
       # Наше приложение
       'front'
   ]

Настройка базы данных
---------------------

По умолчанию Django использует SQLite. Для нашего магазина это подойдет на этапе разработки:

.. code-block:: python

   # flower_shop/settings.py

   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.sqlite3',
           'NAME': BASE_DIR / 'db.sqlite3',
       }
   }


Настройка статических файлов
----------------------------

Добавьте в конец `settings.py`:

.. code-block:: python

   # Статические файлы (CSS, JavaScript, Images)
   STATIC_URL = '/static/'
   STATICFILES_DIRS = [
       BASE_DIR / "static",
   ]

   # Медиа файлы (загружаемые пользователями)
   MEDIA_URL = '/media/'
   MEDIA_ROOT = BASE_DIR / 'media'

   DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

   # Использование кастомного пользователя
   AUTH_USER_MODEL = 'front.CustomUser'

   # Ссылка для редиректа после авторизации
   LOGOUT_REDIRECT_URL = '/'


Создание папок для статических и медиа файлов
---------------------------------------------

.. code-block:: batch

   # Создайте папки в корне проекта
   mkdir static
   mkdir media
   mkdir templates

   # В директории templates создаем pages и components

Структура теперь выглядит так:

.. code-block:: text

   ekz_project/
   │   manage.py
   │   db.sqlite3
   │
   ├───front/
   ├───ekz/
   ├───static/           # CSS, JS, изображения
   ├───media/            # Загружаемые файлы
   ├───templates/        # HTML шаблоны
   └───venv/