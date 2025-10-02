Установка и настройка
=====================

Предварительные требования
--------------------------

- Python 3.8+
- PostgreSQL 12+
- Redis (опционально)

Установка
---------

1. Клонируйте репозиторий:

.. code-block:: bash

   git clone https://github.com/yourusername/yourproject.git
   cd yourproject

2. Создайте виртуальное окружение:

.. code-block:: bash

   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows

3. Установите зависимости:

.. code-block:: bash

   pip install -r requirements.txt

4. Настройте базу данных:

.. code-block:: bash

   python manage.py migrate
   python manage.py createsuperuser

5. Запустите сервер:

.. code-block:: bash

   python manage.py runserver

Приложение будет доступно по адресу http://localhost:8000