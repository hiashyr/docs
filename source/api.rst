API Documentation
=================

REST Endpoints
--------------

Tasks API
~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - Endpoint
     - Method
     - Description
   * - ``/api/tasks/``
     - GET
     - Получить список задач
   * - ``/api/tasks/``
     - POST
     - Создать новую задачу
   * - ``/api/tasks/{id}/``
     - GET
     - Получить задачу по ID
   * - ``/api/tasks/{id}/``
     - PUT
     - Обновить задачу
   * - ``/api/tasks/{id}/``
     - DELETE
     - Удалить задачу

Users API
~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - Endpoint
     - Method
     - Description
   * - ``/api/users/register/``
     - POST
     - Регистрация пользователя
   * - ``/api/users/login/``
     - POST
     - Аутентификация
   * - ``/api/users/profile/``
     - GET
     - Профиль текущего пользователя

Примеры запросов
----------------

Создание задачи:

.. code-block:: bash

   curl -X POST http://localhost:8000/api/tasks/ \\
     -H "Content-Type: application/json" \\
     -H "Authorization: Token your-token" \\
     -d '{
       "title": "Новая задача",
       "description": "Описание задачи",
       "assignee": 1
     }'

Получение списка задач:

.. code-block:: bash

   curl -X GET "http://localhost:8000/api/tasks/?status=todo" \\
     -H "Authorization: Token your-token"