Создание HTML шаблонов
=======================

В этом разделе мы создадим HTML шаблоны для нашего приложения. Начнем с шапки сайта (header), которая отображается на всех страницах.

Шаблон header (шапка сайта)
---------------------------

Шаблон ``header`` содержит логотип, навигацию и элементы управления пользователем. Он использует Bootstrap для стилизации.

Загрузка статических файлов
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: django

   {% load static %}

**Назначение:** Загружает теги для работы со статическими файлами.

**Использование:** Позволяет использовать ``{% static %}`` для ссылок на CSS, JS, изображения

Структура header
^^^^^^^^^^^^^^^^

.. code-block:: django

   <header class="bg-light py-3 mb-4 border-bottom">
       <div class="container">
           <div class="d-flex justify-content-between align-items-center">

**Классы Bootstrap:**
- ``bg-light`` - светлый фон
- ``py-3`` - вертикальные отступы
- ``mb-4`` - нижний отступ
- ``border-bottom`` - нижняя граница
- ``container`` - центрирующий контейнер
- ``d-flex justify-content-between align-items-center`` - flex-контейнер с выравниванием

Логотип и название сайта
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: django

   <a href="{% url "main_page" %}" class="d-flex align-items-center text-decoration-none">
       <img src="{% static 'images/logo.png' %}" alt="Логотип" class="me-2" style="max-height: 40px;">
       <span class="fs-4 fw-bold text-primary">#МОЙНЕСАМ</span>
   </a>

**Элементы:**
- Ссылка на главную страницу
- Логотип из статических файлов
- Название сайта с стилями
- ``text-decoration-none`` - убирает подчеркивание ссылки

Навигационное меню
^^^^^^^^^^^^^^^^^^

.. code-block:: django

   <nav class="navbar navbar-expand-lg navbar-light">
       <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Переключить навигацию">
           <span class="navbar-toggler-icon"></span>
       </button>
       <div class="collapse navbar-collapse" id="navbarNav">
           <ul class="navbar-nav me-auto mb-2 mb-lg-0">
               <li class="nav-item">
                   <a class="nav-link" href="{% url 'catalog' %}">Каталог</a>
               </li>
               <li class="nav-item">
                   <a class="nav-link" href="{% url 'contacts' %}">Контакты</a>
               </li>
           </ul>
       </div>
   </nav>

**Особенности:**
- Адаптивное меню с кнопкой-гамбургером для мобильных устройств
- ``navbar-expand-lg`` - меню сворачивается на экранах меньше lg
- ``data-bs-toggle="collapse"`` - Bootstrap JavaScript для сворачивания/разворачивания

Блок для авторизованных пользователей
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: django

   {% if request.user.is_authenticated %}
       <a href="{% url 'cart' %}" class="btn btn-outline-primary me-2 position-relative">
           <i class="bi bi-cart"></i> Корзина
           <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
               {{ request.user.cart_items.count }}
           </span>
       </a>

**Элементы:**
- Кнопка корзины с количеством товаров
- ``position-relative`` и ``position-absolute`` для badge с количеством
- ``request.user.cart_items.count`` - количество товаров в корзине через related_name

Кнопка админки для суперпользователей
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: django

   {% if request.user.is_superuser %}
   <a href="{% url "admin:index" %}" target="_blank" class="btn btn-outline-primary me-2">Админ</a>
   {% endif %}

**Условие:** Показывается только суперпользователям
- ``target="_blank"`` - открывает в новой вкладке

Профиль пользователя
^^^^^^^^^^^^^^^^^^^^

.. code-block:: django

   <a href="{% url 'profile' %}" class="btn btn-outline-primary me-2">
       <i class="bi bi-person"></i>
       {% if user.first_name %}
           {{ user.first_name }}
       {% else %}
           Профиль
       {% endif %}
   </a>

**Логика:** Показывает имя пользователя если оно есть, иначе "Профиль"

Выход из системы
^^^^^^^^^^^^^^^^

.. code-block:: django

   <form action="{% url 'logout' %}" method="post" class="d-inline">
       {% csrf_token %}
       <button type="submit" class="btn btn-outline-danger">Выйти</button>
   </form>

**Особенности:**
- Форма с POST-запросом для безопасности
- ``{% csrf_token %}`` - защита от CSRF-атак
- ``d-inline`` - форма отображается в строку

Блок для неавторизованных пользователей
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: django

   {% else %}
       <a href="{% url "register" %}" class="btn btn-outline-primary me-2">Регистрация</a>
       <a href="{% url "login" %}" class="btn btn-primary">Войти</a>
   {% endif %}

**Элементы:** Кнопки регистрации и входа для неавторизованных пользователей

Особенности шаблона
-------------------

**Адаптивность:** Меню сворачивается на мобильных устройствах

**Безопасность:** Выход через POST-запрос с CSRF-токеном

**Динамичность:** Разный контент для авторизованных и неавторизованных пользователей

**Доступность:** ARIA-атрибуты для скринридеров

.. note::

   Убедитесь, что файл логотипа ``logo.png`` находится в папке ``static/images/``

.. warning::

   Для работы иконок Bootstrap Icons нужно подключить CDN или установить пакет в проекте.


Шаблон корзины (cart.html)
---------------------------

Шаблон ``cart.html`` отвечает за отображение всех товаров, добавленных пользователем в корзину. Он предоставляет функционал для просмотра товаров, изменения их количества, удаления и перехода к оформлению заказа.

Наследование базового шаблона и установка заголовка
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: django

   {% extends 'base.html' %}

   {% block title %}Корзина - МОЙ НЕ САМ{% endblock %}

   {% block content %}

Шаблон наследуется от базового ``base.html``, что обеспечивает consistent оформление всех страниц сайта. В блоке ``title`` устанавливается заголовок страницы, который отображается в браузере. Блок ``content`` определяет основное содержимое страницы.

Основной заголовок страницы
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: django

   <h1 class="mb-4">Корзина</h1>

Заголовок первого уровня "Корзина" с классом ``mb-4`` (margin-bottom: 1.5rem) создает достаточный отступ между заголовком и последующим содержимым.

Проверка наличия товаров в корзине
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: django

   {% if cart_items %}

Условный оператор проверяет, содержит ли переменная ``cart_items`` какие-либо элементы. Эта переменная передается из представления ``cart_view`` и содержит QuerySet всех товаров в корзине текущего пользователя. Если корзина не пуста, отображается основной интерфейс с товарами.

Создание карточки для отображения товаров
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: django

   <div class="card mb-4">
       <div class="card-header bg-primary text-white">
           <h5 class="mb-0">Товары в корзине</h5>
       </div>

Создается карточка Bootstrap с классом ``mb-4`` для нижнего отступа. Заголовок карточки ``card-header`` имеет синий фон (``bg-primary``) и белый текст, что визуально выделяет раздел с товарами.

Организация адаптивной таблицы
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: django

   <div class="card-body p-0">
       <div class="table-responsive">
           <table class="table table-hover mb-0">

В теле карточки создается адаптивная таблица. Класс ``table-responsive`` обеспечивает горизонтальную прокрутку на мобильных устройствах, а ``table-hover`` добавляет эффект подсветки строк при наведении курсора. ``p-0`` убирает внутренние отступы у card-body.

Определение структуры таблицы - заголовки столбцов
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: django

   <thead class="table-light">
       <tr>
           <th scope="col" style="width: 100px;">Фото</th>
           <th scope="col">Товар</th>
           <th scope="col" style="width: 150px;">Цена</th>
           <th scope="col" style="width: 150px;">Количество</th>
           <th scope="col" style="width: 150px;">Сумма</th>
           <th scope="col" style="width: 80px;">Действия</th>
       </tr>
   </thead>

Заголовок таблицы с светло-серым фоном (``table-light``) содержит шесть столбцов с фиксированными ширинами для обеспечения consistent отображения. Столбцы: изображение товара, название, цена за единицу, количество, общая стоимость и действия.

Начало тела таблицы и итерация по элементам корзины
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: django

   <tbody>
       {% for item in cart_items %}
       <tr>

Начинается тело таблицы, и для каждого элемента в ``cart_items`` создается новая строка. Переменная ``item`` представляет собой объект модели ``CartItem``, связывающий пользователя с товаром и количеством.

Отображение изображения товара с обработкой отсутствующего изображения
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: django

   <td>
       {% if item.product.image %}
       <img src="{{ item.product.image.url }}" alt="{{ item.product.name }}" class="img-thumbnail" style="max-width: 80px; max-height: 80px;">
       {% else %}
       <div class="bg-light text-center" style="width: 80px; height: 80px; display: flex; align-items: center; justify-content: center;">
           <span class="text-muted small">Нет фото</span>
       </div>
       {% endif %}
   </td>

В первой ячейке отображается изображение товара. Если изображение существует, показывается миниатюра с ограничением размеров 80x80 пикселей. Если изображение отсутствует, отображается серая заглушка с текстом "Нет фото", что улучшает пользовательский опыт.

Отображение информации о товаре с ссылкой на детальную страницу
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: django

   <td>
       <a href="{% url 'product_detail' item.product.id %}" class="text-decoration-none">
           <h6 class="mb-1">{{ item.product.name }}</h6>
       </a>
       {% if item.product.category %}
       <span class="text-muted small">{{ item.product.category.name }}</span>
       {% endif %}
   </td>

Название товара является ссылкой на его детальную страницу. Класс ``text-decoration-none`` убирает подчеркивание ссылки для более чистого вида. Если у товара указана категория, она отображается ниже названия серым мелким шрифтом.

Отображение цены за единицу товара
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: django

   <td>{{ item.product.price }} ₽</td>

Цена товара отображается в рублях. Значение берется из поля ``price`` модели ``Product``, связанной с текущим элементом корзины.

Интерактивная форма для изменения количества товара
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: django

   <td>
       <form action="{% url 'update_cart_item' item.id %}" method="post" class="d-flex">
           {% csrf_token %}
           <input type="number" name="quantity" value="{{ item.quantity }}" min="1" max="99" class="form-control form-control-sm" style="width: 70px;">
           <button type="submit" class="btn btn-sm btn-outline-primary ms-2">
               Обновить
           </button>
       </form>
   </td>

Форма с методом POST позволяет пользователю изменять количество товара. CSRF-токен обеспечивает защиту от межсайтовой подделки запросов. Поле ввода ограничивает количество от 1 до 99 единиц. Кнопка "Обновить" отправляет форму на сервер для обработки.

Отображение общей стоимости позиции
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: django

   <td class="fw-bold">{{ item.get_total }} ₽</td>

Общая стоимость рассчитывается методом ``get_total()`` модели ``CartItem``, который умножает цену товара на количество. Жирное начертание (``fw-bold``) визуально выделяет эту важную информацию.

Кнопка для удаления товара из корзины
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: django

   <td>
       <a href="{% url 'remove_from_cart' item.id %}" class="btn btn-sm btn-outline-danger">
           Удалить
       </a>
   </td>

Красная контурная кнопка позволяет удалить товар из корзины. Ссылка ведет на представление ``remove_from_cart``, передавая ID элемента корзины для идентификации.

Завершение строки товара и цикла по элементам
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: django

   </tr>
   {% endfor %}

Закрывающий тег ``</tr>`` завершает строку таблицы для текущего товара, а ``{% endfor %}`` завершает цикл перебора всех элементов корзины.

Подвал таблицы с расчетом общей суммы заказа
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: django

   <tfoot class="table-light">
       <tr>
           <td colspan="4" class="text-end fw-bold">Итого:</td>
           <td class="fw-bold">{{ total_amount }} ₽</td>
           <td></td>
       </tr>
   </tfoot>

В подвале таблицы отображается итоговая сумма заказа. Атрибут ``colspan="4"`` объединяет первые четыре ячейки для выравнивания надписи "Итого:". Переменная ``total_amount`` передается из представления и содержит сумму всех ``item.get_total()``.

Завершение структуры таблицы и карточки
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: django

           </table>
       </div>
   </div>

Закрывающие теги завершают структуру таблицы, контейнера адаптивности и тела карточки, обеспечивая валидность HTML-разметки.

Навигационные кнопки в подвале карточки
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: django

   <div class="card-footer">
       <div class="d-flex justify-content-between">
           <a href="{% url 'catalog' %}" class="btn btn-outline-primary">
               Продолжить покупки
           </a>
           <a href="{% url 'checkout' %}" class="btn btn-success">
               Оформить заказ
           </a>
       </div>
   </div>

В подвале карточки расположены две кнопки. Левая кнопка позволяет вернуться к покупкам, правая - зеленого цвета - ведет к оформлению заказа. Flex-контейнер с ``justify-content-between`` равномерно распределяет кнопки по ширине.

Завершение карточки и условного оператора
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: django

   </div>

Закрывающий тег ``</div>`` завершает карточку с товарами. Этот блок выполняется только если в корзине есть товары (условие ``{% if cart_items %}``).

Альтернативное сообщение для пустой корзины
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: django

   {% else %}
   <div class="alert alert-info">
       <p class="mb-0">Ваша корзина пуста. <a href="{% url 'catalog' %}" class="alert-link">Перейти в каталог</a>.</p>
   </div>
   {% endif %}

Если корзина пуста, вместо таблицы с товарами отображается информационное сообщение Bootstrap alert. Сообщение содержит ссылку на каталог товаров, побуждая пользователя начать покупки.

Завершение основного блока содержимого
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: django

   {% endblock %}

Тег ``{% endblock %}`` завершает блок ``content``, определяя конец основного содержимого страницы, которое будет вставлено в базовый шаблон.

Собрав все эти блоки кода последовательно, вы получите полностью функциональный шаблон корзины с продуманным пользовательским интерфейсом и всеми необходимыми интерактивными элементами.