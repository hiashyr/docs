Архитектура проекта
===================

Структура проекта
-----------------

.. code-block:: text

   myproject/
   ├── myproject/          # Настройки проекта
   │   ├── settings/
   │   ├── urls.py
   │   └── wsgi.py
   ├── apps/               # Приложения
   │   ├── users/          # Пользователи
   │   ├── tasks/          # Задачи
   │   └── api/            # REST API
   ├── static/             # Статические файлы
   ├── templates/          # Шаблоны
   └── manage.py

База данных
-----------

.. graphviz::

   digraph database {
      rankdir=LR;
      node [shape=box];
      
      User -> Task [label="1:N"];
      User -> Profile [label="1:1"];
      Task -> Comment [label="1:N"];
      Task -> Attachment [label="1:N"];
   }

Основные модели
---------------

- **User** - пользователи системы
- **Task** - задачи
- **Project** - проекты (группы задач)
- **Comment** - комментарии к задачам