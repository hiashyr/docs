Работа с Git для локального репозитория
=======================================

В этом разделе рассмотрим основные команды Git для управления локальным репозиторием вашего Django проекта.

Начало работы с Git
-------------------

Инициализация репозитория
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Инициализация Git репозитория в папке проекта
   git init

   # Проверка статуса репозитория
   git status

Эта команда создает скрытую папку ``.git/`` в вашем проекте, где будут храниться все данные о версиях.

Базовые операции с файлами
--------------------------

Добавление файлов в отслеживание
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Добавить конкретный файл
   git add manage.py

   # Добавить все файлы в текущей директории
   git add .

   # Добавить все файлы с расширением .py
   git add *.py

   # Добавить все файлы в папке myapp
   git add myapp/

Создание коммитов
^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Создать коммит с сообщением
   git commit -m "Initial commit: basic Django project structure"

   # Создать коммит с подробным описанием
   git commit

   # Добавить изменения в последний коммит (если забыли что-то)
   git commit --amend

Просмотр истории и изменений
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Показать историю коммитов
   git log

   # Краткая история
   git log --oneline

   # Показать изменения в файлах
   git diff

   # Показать изменения конкретного файла
   git diff settings.py

Типичный рабочий процесс для Django проекта
-------------------------------------------

Игнорирование ненужных файлов
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Создайте файл ``.gitignore`` в корне проекта:

.. code-block:: text

   # Django
   *.pyc
   __pycache__/
   *.sqlite3
   *.log

   # Virtual environment
   venv/
   env/
   .venv/

   # Environment variables
   .env
   .env.local

   # IDE
   .vscode/
   .idea/
   *.swp
   *.swo

   # OS
   .DS_Store
   Thumbs.db

Первый коммит проекта
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Добавляем файл .gitignore
   git add .gitignore

   # Добавляем основные файлы проекта
   git add manage.py requirements.txt myproject/ myapp/

   # Создаем первый коммит
   git commit -m "Initial Django project setup"

Отмена изменений
----------------

Отмена незакоммиченных изменений
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Отменить изменения в конкретном файле
   git checkout -- settings.py

   # Отменить все незакоммиченные изменения
   git checkout -- .

   # Убрать файлы из staged (перед коммитом)
   git reset HEAD settings.py

Отмена коммитов
^^^^^^^^^^^^^^^

.. code-block:: bash

   # Отменить последний коммит, сохраняя изменения
   git reset --soft HEAD~1

   # Отменить последний коммит, удаляя изменения
   git reset --hard HEAD~1

   # Отменить конкретный коммит
   git revert COMMIT_HASH

Практические примеры для Django
-------------------------------

Добавление новой модели
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Создаем ветку для новой функциональности
   git checkout -b feature-user-model

   # Добавляем файл модели
   git add myapp/models.py

   # Создаем миграции
   git add myapp/migrations/0001_initial.py

   # Коммитим изменения
   git commit -m "Add User model with profile fields"

   # Возвращаемся в основную ветку и вливаем изменения
   git checkout main
   git merge feature-user-model

Добавление представлений и URL
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   git checkout -b feature-views

   # Добавляем views
   git add myapp/views.py
   git add myapp/urls.py

   # Добавляем шаблоны
   git add myapp/templates/

   git commit -m "Add user views and URL configuration"
   git checkout main
   git merge feature-views

Полезные команды для ежедневной работы
--------------------------------------

.. code-block:: bash

   # Показать текущий статус
   git status

   # Показать историю с графиком веток
   git log --oneline --graph --all

   # Показать кто менял файл
   git blame settings.py

   # Поиск в истории коммитов
   git log --grep="model"

   # Показать изменения между ветками
   git diff main..feature-branch

Советы по работе с Git в Django проекте
---------------------------------------

.. warning::

   Команда ``git reset --hard`` используетя для перехода к ближашему коммиту и безвозвратно удаляет изменения. Используйте осторожно!