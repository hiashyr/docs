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
^^^^^^^^^^^^^^^^^^^

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

Шаблон страницы контактов (contacts.html)
------------------------------------------

Наследование базового шаблона и заголовок
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Этот блок определяет базовую структуру страницы и устанавливает заголовок вкладки браузера.

.. code-block:: django

    {% extends 'base.html' %}

    {% block title %}Контакты - МОЙ НЕ САМ{% endblock %}

    {% block content %}

Основной контейнер и заголовок страницы
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Создает основной контейнер с отступами и заголовок страницы. Класс py-5 добавляет вертикальные отступы, mb-4 - нижний отступ для заголовка.

.. code-block:: django

    <div class="container py-5"> <h1 class="mb-4">Контакты</h1>

Начало сетки строки
^^^^^^^^^^^^^^^^^^^

Инициализирует систему сетки Bootstrap, которая позволяет создавать адаптивные колонки. Строка (row) служит контейнером для колонок.

.. code-block:: django

    <div class="row">

Колонка с контактной информацией
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Левая колонка занимает 6 колонок на средних экранах и больше (col-md-6). Содержит структурированную контактную информацию с кликабельными ссылками для телефона и email.

.. code-block:: django

    <div class="col-md-6 mb-4"> <h5>Наш адрес:</h5> <p>г. ВашГород, ул. Примерная, д. 1</p> <h5>Телефон:</h5> <p><a href="tel:+79991234567">+7 (999) 123-45-67</a></p> <h5>Email:</h5> <p><a href="mailto:info@example.com">info@example.com</a></p> </div>

Колонка с картой
^^^^^^^^^^^^^^^^

Правая колонка также занимает 6 колонок. Содержит заголовок и iframe с картой. Атрибут frameborder="0" убирает границу вокруг карты.

.. code-block:: django

    <div class="col-md-6 mb-4"> <h5>Мы на карте:</h5> <div style="width: 100%"> <!-- Вставьте сюда карту, например, Яндекс или Google --> <iframe src="https://yandex.ru/map-widget/v1/?um=constructor%3Aexample" width="100%" height="300" frameborder="0"></iframe> </div> </div>

Завершение сетки и контейнера
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Закрывающие теги для строки сетки и основного контейнера. Важно соблюдать порядок закрытия тегов для правильной верстки.

.. code-block:: django

    </div> </div>

Завершение блока content
^^^^^^^^^^^^^^^^^^^^^^^^

Закрывает основной блок контента, который был открыт в начале шаблона.

.. code-block:: django

    {% endblock %}

Шаблон страницы авторизации (login.html)
---------------------------------

Данный шаблон реализует страницу входа с тремя способами авторизации: по телефону, email и логину. Используется наследование от базового шаблона и Bootstrap для стилизации.

Наследование и структура страницы
^^^^^^^^^^^^^^^^^^^

Шаблон начинается с наследования базового шаблона и объявления блока контента:

.. code-block:: django

    {% extends 'base.html' %}
    {% block content %}

Контейнер и выравнивание формы
^^^^^^^^^^^^^^^^^^^

Вся форма помещена в контейнер Bootstrap с вертикальным отступом и выравниванием по центру:

.. code-block:: django

    <div class="container py-5">
        <div class="row justify-content-center">
            <div class="col-md-8 col-lg-6">

Карточка для формы входа
^^^^^^^^^^^^^^^^^^^

Используется компонент Bootstrap Card для визуального выделения формы:

.. code-block:: django

    <div class="card shadow-sm">
        <div class="card-header bg-primary text-white">
            <h2 class="h4 mb-0 text-center">Вход в систему</h2>
        </div>
        <div class="card-body p-4">

Навигация по способам входа (табы)
^^^^^^^^^^^^^^^^^^^

Для выбора способа входа реализованы Bootstrap-навигационные табы. Активный таб определяется переменной active_tab:

.. code-block:: django

    <ul class="nav nav-tabs nav-justified mb-4" id="authTabs" role="tablist">
        <li class="nav-item" role="presentation">
            <a class="nav-link {% if active_tab == 'phone' %}active{% endif %}" 
               href="?tab=phone" id="phone-tab">
                <i class="bi bi-phone me-2"></i>По телефону
            </a>
        </li>
        <li class="nav-item" role="presentation">
            <a class="nav-link {% if active_tab == 'email' %}active{% endif %}" 
               href="?tab=email" id="email-tab">
                <i class="bi bi-envelope me-2"></i>По email
            </a>
        </li>
        <li class="nav-item" role="presentation">
            <a class="nav-link {% if active_tab == 'username' %}active{% endif %}" 
               href="?tab=username" id="login-tab">
                <i class="bi bi-person me-2"></i>По логину
            </a>
        </li>
    </ul>

Контейнер с формами для каждого способа входа
^^^^^^^^^^^^^^^^^^^

В зависимости от выбранного таба отображается соответствующая форма. Для этого используются Bootstrap tab-pane и условия Django:

.. code-block:: django

    <div class="tab-content">

Форма входа по телефону
^^^^^^^^^^^^^^^^^^^

Пользователь вводит номер телефона и пароль. Для защиты от CSRF-атак используется {% csrf_token %}. Значение поля phone подставляется из формы, если оно было введено ранее:

.. code-block:: django

    <div class="tab-pane fade {% if active_tab == 'phone' %}show active{% endif %}" id="phone">
        <form method="post">
            {% csrf_token %}
            <input type="hidden" name="auth_type" value="phone">
            <div class="mb-3">
                <label for="phone" class="form-label">Номер телефона</label>
                <input type="tel" class="form-control" id="phone" name="phone" 
                       value="{{ form.phone.value|default_if_none:'' }}" required>
            </div>
            <div class="mb-3">
                <label for="password" class="form-label">Пароль</label>
                <input type="password" class="form-control" id="password" name="password" required>
            </div>
            <div class="d-grid gap-2">
                <button type="submit" class="btn btn-primary">
                    <i class="bi bi-box-arrow-in-right me-2"></i>Войти
                </button>
            </div>
        </form>
    </div>

Форма входа по email
^^^^^^^^^^^^^^^^^^^

Пользователь вводит email и пароль. Структура аналогична предыдущей форме, но поля другие:

.. code-block:: django

    <div class="tab-pane fade {% if active_tab == 'email' %}show active{% endif %}" id="email">
        <form method="post">
            {% csrf_token %}
            <input type="hidden" name="auth_type" value="email">
            <div class="mb-3">
                <label for="email" class="form-label">Email</label>
                <input type="email" class="form-control" id="email" name="email" 
                       value="{{ form.email.value|default_if_none:'' }}" required>
            </div>
            <div class="mb-3">
                <label for="password" class="form-label">Пароль</label>
                <input type="password" class="form-control" id="password" name="password" required>
            </div>
            <div class="d-grid gap-2">
                <button type="submit" class="btn btn-primary">
                    <i class="bi bi-box-arrow-in-right me-2"></i>Войти
                </button>
            </div>
        </form>
    </div>

Форма входа по логину
^^^^^^^^^^^^^^^^^^^

Пользователь вводит логин и пароль. Для каждого способа входа используется скрытое поле auth_type для определения типа авторизации на сервере:

.. code-block:: django

    <div class="tab-pane fade {% if active_tab == 'username' %}show active{% endif %}" id="login">
        <form method="post">
            {% csrf_token %}
            <input type="hidden" name="auth_type" value="username">
            <div class="mb-3">
                <label for="username" class="form-label">Логин</label>
                <input type="text" class="form-control" id="username" name="username" 
                       value="{{ form.username.value|default_if_none:'' }}" required>
            </div>
            <div class="mb-3">
                <label for="password" class="form-label">Пароль</label>
                <input type="password" class="form-control" id="password" name="password" required>
            </div>
            <div class="d-grid gap-2">
                <button type="submit" class="btn btn-primary">
                    <i class="bi bi-box-arrow-in-right me-2"></i>Войти
                </button>
            </div>
        </form>
    </div>

Завершение блока с формами
^^^^^^^^^^^^^^^^^^^

.. code-block:: django

    </div>

Ссылки на восстановление пароля и регистрацию
^^^^^^^^^^^^^^^^^^^

Внизу карточки размещены ссылки для восстановления пароля и перехода к регистрации:

.. code-block:: django

    <div class="mt-4 text-center">
        <a href="#" class="text-decoration-none">Забыли пароль?</a>
        <span class="mx-2">|</span>
        <a href="{% url 'register' %}" class="text-decoration-none">Регистрация</a>
    </div>

Закрытие всех контейнеров и блока content
^^^^^^^^^^^^^^^^^^^

.. code-block:: django

                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

---

**Примечания:**
- Для корректной работы табов требуется подключение Bootstrap JS.
- Для каждого способа входа используется отдельная форма, но все они отправляются на один и тот же URL.
- Переменная active_tab должна устанавливаться во view для правильного отображения активного таба.
- Для безопасности используется {% csrf_token %} в каждой форме.

Если собрать все блоки, получится полный шаблон страницы авторизации с тремя способами входа.

Шаблон страницы каталога (catalog.html)
---------------------------------

Данный шаблон реализует страницу каталога товаров с фильтрами по категориям, цене и поиску, а также выводит карточки товаров с возможностью перехода к подробной информации и добавления в корзину.

Наследование и заголовок страницы
^^^^^^^^^^^^^^^^^^^

Шаблон наследует базовый шаблон и задаёт заголовок страницы. Это обеспечивает единый стиль для всех страниц сайта и правильное отображение заголовка во вкладке браузера.

.. code-block:: django

    {% extends 'base.html' %}
    {% block title %}Каталог товаров - МОЙ НЕ САМ{% endblock %}

Начало блока основного контента
^^^^^^^^^^^^^^^^^^^

Весь контент страницы помещён в блок content. Это позволяет вставлять содержимое в нужное место базового шаблона.

.. code-block:: django

    {% block content %}
    <div class="row">

Боковая панель с фильтрами (левая колонка)
^^^^^^^^^^^^^^^^^^^

В левой колонке размещена форма фильтрации товаров. Она позволяет пользователю искать товары по ключевому слову, выбирать категорию и указывать диапазон цен. Все фильтры отправляются методом GET, чтобы их можно было видеть в адресной строке и делиться ссылкой.

.. code-block:: django

    <div class="col-md-3">
        <div class="card mb-4">
            <div class="card-header bg-primary text-white">
                <h5 class="mb-0">Фильтры</h5>
            </div>
            <div class="card-body">
                <form method="get" action="{% url 'catalog' %}">

Поле поиска по названию или описанию
^^^^^^^^^^^^^^^^^^^

.. code-block:: django

    <div class="mb-3">
        <label for="search" class="form-label">Поиск</label>
        <input type="text" class="form-control" id="search" name="q" value="{{ search_query }}">
    </div>

Выпадающий список категорий
^^^^^^^^^^^^^^^^^^^

Позволяет выбрать одну из доступных категорий товаров или отобразить все товары.

.. code-block:: django

    <div class="mb-3">
        <label for="category" class="form-label">Категория</label>
        <select class="form-select" id="category" name="category">
            <option value="">Все категории</option>
            {% for category in categories %}
            <option value="{{ category.id }}" {% if selected_category == category.id|stringformat:"s" %}selected{% endif %}>
                {{ category.name }}
            </option>
            {% endfor %}
        </select>
    </div>

Поля для фильтрации по цене
^^^^^^^^^^^^^^^^^^^

Пользователь может указать минимальную и максимальную цену для поиска товаров в нужном диапазоне.

.. code-block:: django

    <div class="mb-3">
        <label for="min_price" class="form-label">Минимальная цена</label>
        <input type="number" class="form-control" id="min_price" name="min_price" value="{{ min_price }}" min="0">
    </div>
    <div class="mb-3">
        <label for="max_price" class="form-label">Максимальная цена</label>
        <input type="number" class="form-control" id="max_price" name="max_price" value="{{ max_price }}" min="0">
    </div>

Кнопки применения и сброса фильтров
^^^^^^^^^^^^^^^^^^^

.. code-block:: django

    <div class="d-grid gap-2">
        <button type="submit" class="btn btn-primary">Применить фильтры</button>
        <a href="{% url 'catalog' %}" class="btn btn-outline-secondary">Сбросить фильтры</a>
    </div>

Закрытие формы и боковой панели
^^^^^^^^^^^^^^^^^^^

.. code-block:: django

                </form>
            </div>
        </div>
    </div>

Основная область с товарами (правая колонка)
^^^^^^^^^^^^^^^^^^^

В правой колонке отображается список товаров в виде карточек. Здесь реализован вывод заголовка, проверка наличия товаров и цикл по всем найденным товарам.

.. code-block:: django

    <div class="col-md-9">
        <h2 class="mb-4">Каталог товаров</h2>
        {% if products %}
        <div class="row row-cols-1 row-cols-md-3 g-4">

Карточка товара
^^^^^^^^^^^^^^^^^^^

Каждый товар отображается в отдельной карточке. В карточке выводится изображение (или заглушка), название, описание, цена и кнопки действий.

.. code-block:: django

    <div class="col">
        <div class="card h-100">
            {% if product.image %}
            <img src="{{ product.image.url }}" class="card-img-top" alt="{{ product.name }}" style="height: 200px; object-fit: cover;">
            {% else %}
            <div class="bg-light text-center py-5">
                <span class="text-muted">Нет изображения</span>
            </div>
            {% endif %}
            <div class="card-body">
                <h5 class="card-title">{{ product.name }}</h5>
                <p class="card-text text-truncate">{{ product.description }}</p>
                <p class="card-text"><strong>Цена: {{ product.price }} ₽</strong></p>
            </div>
            <div class="card-footer d-flex justify-content-between">
                <a href="{% url 'product_detail' product.id %}" class="btn btn-primary">Подробнее</a>
                {% if request.user.is_authenticated %}
                <a href="{% url 'add_to_cart' product.id %}" class="btn btn-success">В корзину</a>
                {% endif %}
            </div>
        </div>
    </div>

Обработка отсутствия товаров
^^^^^^^^^^^^^^^^^^^

Если по выбранным фильтрам не найдено ни одного товара, выводится информативное сообщение.

.. code-block:: django

    {% else %}
    <div class="alert alert-info">
        Товары не найдены. Попробуйте изменить параметры фильтрации.
    </div>
    {% endif %}

Закрытие блоков и страницы
^^^^^^^^^^^^^^^^^^^

.. code-block:: django

    </div>
    </div>
    {% endblock %}

---

**Примечания:**
- Для фильтрации используются GET-параметры, что позволяет делиться ссылкой на отфильтрованный каталог.
- Для каждой карточки товара предусмотрена обработка отсутствия изображения.
- Кнопка "В корзину" доступна только авторизованным пользователям.
- При отсутствии товаров выводится информативное сообщение.

Если собрать все блоки, получится полный шаблон страницы каталога с фильтрами и карточками товаров.


Шаблон страницы заказов пользователя (orders.html)
---------------------------------

Данный шаблон реализует страницу просмотра всех заказов, оформленных текущим пользователем. Здесь отображается таблица с основными сведениями о каждом заказе, статусами и ссылкой на подробности.

Наследование и заголовок страницы
^^^^^^^^^^^^^^^^^^^

Шаблон наследует базовый шаблон сайта, что обеспечивает единый стиль и структуру для всех страниц.

.. code-block:: django

    {% extends 'base.html' %}
    {% block title %}Мои заказы - МОЙ НЕ САМ{% endblock %}

Блок основного контента
^^^^^^^^^^^^^^^^^^^

Весь контент страницы помещён в блок content, чтобы корректно встроиться в базовый шаблон.

.. code-block:: django

    {% block content %}
    <h1 class="mb-4">Мои заказы</h1>

Проверка наличия заказов
^^^^^^^^^^^^^^^^^^^

Перед выводом таблицы выполняется проверка: есть ли у пользователя оформленные заказы. Если заказы есть, отображается таблица, иначе — информационное сообщение.

.. code-block:: django

    {% if orders %}
    ...
    {% else %}
    <div class="alert alert-info">
        <p class="mb-0">У вас пока нет заказов. <a href="{% url 'catalog' %}" class="alert-link">Перейти в каталог</a>.</p>
    </div>
    {% endif %}

Таблица заказов
^^^^^^^^^^^^^^^^^^^

Если заказы есть, они выводятся в виде таблицы с адаптивной версткой (table-responsive). Таблица содержит следующие столбцы:
- Номер заказа
- Дата оформления
- Сумма заказа
- Статус
- Действия (ссылка на подробности)

.. code-block:: django

    <div class="table-responsive">
        <table class="table table-hover">
            <thead class="table-light">
                <tr>
                    <th scope="col">№ заказа</th>
                    <th scope="col">Дата</th>
                    <th scope="col">Сумма</th>
                    <th scope="col">Статус</th>
                    <th scope="col">Действия</th>
                </tr>
            </thead>
            <tbody>
                {% for order in orders %}
                <tr>
                    <td>{{ order.id }}</td>
                    <td>{{ order.created_at|date:"d.m.Y H:i" }}</td>
                    <td>{{ order.total_amount }} ₽</td>
                    <td>
                        ...
                    </td>
                    <td>
                        <a href="{% url 'order_detail' order.id %}" class="btn btn-sm btn-primary">Подробнее</a>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>

Столбец "Статус заказа"
^^^^^^^^^^^^^^^^^^^

Для каждого заказа отображается его статус с помощью цветных бейджей. Это позволяет быстро визуально оценить состояние заказа:
- Ожидает обработки (pending) — жёлтый бейдж
- В обработке (processing) — голубой бейдж
- Отправлен (shipped) — синий бейдж
- Доставлен (delivered) — зелёный бейдж
- Отменен (cancelled) — красный бейдж
- Прочие статусы — серый бейдж с текстом из get_status_display

.. code-block:: django

    <td>
        {% if order.status == 'pending' %}
        <span class="badge bg-warning">Ожидает обработки</span>
        {% elif order.status == 'processing' %}
        <span class="badge bg-info">В обработке</span>
        {% elif order.status == 'shipped' %}
        <span class="badge bg-primary">Отправлен</span>
        {% elif order.status == 'delivered' %}
        <span class="badge bg-success">Доставлен</span>
        {% elif order.status == 'cancelled' %}
        <span class="badge bg-danger">Отменен</span>
        {% else %}
        <span class="badge bg-secondary">{{ order.get_status_display }}</span>
        {% endif %}
    </td>

Кнопка "Подробнее"
^^^^^^^^^^^^^^^^^^^

В последнем столбце каждой строки находится кнопка, ведущая на страницу с подробной информацией о заказе. Это позволяет пользователю просмотреть состав заказа, адрес доставки и другие детали.

.. code-block:: django

    <a href="{% url 'order_detail' order.id %}" class="btn btn-sm btn-primary">Подробнее</a>

Обработка отсутствия заказов
^^^^^^^^^^^^^^^^^^^

Если у пользователя нет ни одного заказа, выводится информативное сообщение с предложением перейти в каталог товаров.

.. code-block:: django

    <div class="alert alert-info">
        <p class="mb-0">У вас пока нет заказов. <a href="{% url 'catalog' %}" class="alert-link">Перейти в каталог</a>.</p>
    </div>

Закрытие блоков и страницы
^^^^^^^^^^^^^^^^^^^

.. code-block:: django

    {% endblock %}

---

**Примечания:**
- Для каждого заказа отображается его статус с помощью цветных бейджей, что облегчает восприятие информации.
- Кнопка "Подробнее" позволяет перейти к детальной информации о заказе.
- Если заказов нет, пользователь получает понятное сообщение и ссылку на каталог.
- Используется адаптивная таблица для корректного отображения на мобильных устройствах.

Если собрать все блоки, получится полный шаблон страницы заказов пользователя с таблицей и обработкой всех возможных ситуаций.

Шаблон базового шаблона сайта (base.html)
---------------------------------

Этот шаблон определяет фундаментальную структуру всех страниц сайта, реализует подключение стилей, скриптов, выводит шапку, основной контент и футер. Все остальные шаблоны наследуют его и вставляют свой контент в специальные блоки. Такой подход обеспечивает единообразие, повторное использование кода и простоту поддержки.

**Теоретические основы базового шаблона**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Принцип наследования шаблонов Django
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Django поддерживает наследование шаблонов: базовый шаблон задаёт каркас, а дочерние шаблоны переопределяют только нужные блоки. Это позволяет:
- Избежать дублирования кода (DRY)
- Гарантировать единый стиль и структуру
- Упростить глобальные изменения (например, смена футера или шапки)

2. Статические файлы и безопасность
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Тег {% load static %} позволяет подключать CSS, JS и изображения, хранящиеся в static/. Это безопаснее, чем прямые ссылки, и работает с collectstatic на продакшене. Никогда не вставляйте пользовательский ввод в static-пути — это может привести к XSS.

3. Flex-верстка и адаптивность
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Класс d-flex flex-column h-100 на <body> и mt-auto на футере обеспечивают, что футер всегда прижат к низу, даже если контента мало. Это современный способ построения адаптивных макетов без хака с абсолютным позиционированием.

4. Блоки шаблона: расширяемость и гибкость
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- block title: позволяет задавать уникальный заголовок для каждой страницы
- block extra_css: подключение дополнительных стилей (например, только для одной страницы)
- block content: основной контент страницы, всегда переопределяется в дочерних шаблонах
- block scripts: подключение JS, специфичного для конкретной страницы

5. Включение компонентов через include
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Шапка сайта (header.html) подключается через include. Это удобно для повторяющихся элементов (меню, логотип, корзина, ссылки на вход/регистрацию). Если потребуется изменить меню — достаточно поправить один файл.

6. Bootstrap и иконки
~~~~~~~~~~~~~~~~~~~~~
Подключение Bootstrap и Bootstrap Icons через static обеспечивает кроссбраузерность, адаптивность и быстрый старт верстки. Пользовательские стили (styles.css) позволяют доработать внешний вид под нужды проекта.

7. Структура футера
~~~~~~~~~~~~~~~~~~~
Футер содержит контактную информацию и копирайт. Используется Bootstrap-сетка для корректного отображения на разных устройствах. Класс mt-auto гарантирует, что футер не "поднимается" при малом количестве контента.

8. Безопасность и best practices
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- Никогда не вставляйте пользовательские данные напрямую в <script> или <style> — используйте блоки и фильтры экранирования.
- Для подключения сторонних библиотек используйте только проверенные источники и храните их в static.
- Не храните чувствительные данные (ключи, пароли) в шаблонах.

9. Типовые ошибки при работе с base.html
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- Неопределённый block content в дочернем шаблоне — страница будет пустой.
- Ошибка в пути к static-файлу — стили или скрипты не загрузятся.
- Отсутствие mt-auto на футере — футер "поднимается" вверх.
- Дублирование блоков (например, два block content) — Django выберет первый.

10. Преимущества такой структуры
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- Масштабируемость: легко добавлять новые страницы
- Поддерживаемость: глобальные изменения делаются в одном месте
- Безопасность: централизованное подключение стилей и скриптов
- Гибкость: можно расширять шаблон через блоки без его переписывания

---

**Разбор кода по блокам**
^^^^^^^^^^^^^^^^^^^^^^^^^

Загрузка статических файлов и объявление документа
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

В начале подключается тег {% load static %}, чтобы использовать статические файлы (CSS, JS, изображения). Далее объявляется HTML5-документ с языком ru и классом h-100 для растяжения по высоте.

.. code-block:: django

    {% load static %}
    <!DOCTYPE html>
    <html lang="ru" class="h-100">

Блок <head>: мета-теги, стили и заголовок
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

В head размещаются:
- Кодировка UTF-8
- Мета-тег viewport для адаптивности
- Заголовок страницы (может быть переопределён в дочерних шаблонах через block title)
- Подключение Bootstrap, Bootstrap Icons и пользовательских стилей через static
- Блок extra_css для подключения дополнительных стилей в дочерних шаблонах

.. code-block:: django

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{% block title %}МОЙ НЕ САМ{% endblock %}</title>
        <link rel="stylesheet" href="{% static 'bootstrap.min.css' %}">
        <link rel="stylesheet" href="{% static 'bootstrap-icons.css' %}">
        <link rel="stylesheet" href="{% static 'styles.css' %}">
        {% block extra_css %}{% endblock %}
    </head>

Тело страницы: структура и блоки
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

В body используется flex-верстка для растяжения контента на всю высоту экрана. Включается шапка сайта (header.html), основной контент и футер.

.. code-block:: django

    <body class="d-flex flex-column h-100">
        {% include 'components/header.html' %}
        <main class="flex-grow-1">
            <div class="container mt-4">
                {% block content %}{% endblock %}
            </div>
        </main>
        ...
    </body>

Включение шапки сайта
~~~~~~~~~~~~~~~~~~~~~

Шапка подключается через include. Обычно в ней размещается логотип, меню, ссылки на вход/регистрацию и корзину.

.. code-block:: django

    {% include 'components/header.html' %}

Блок основного контента
~~~~~~~~~~~~~~~~~~~~~~~

Весь уникальный контент страниц вставляется в block content. Это основной механизм для наследования и переопределения содержимого в дочерних шаблонах.

.. code-block:: django

    <main class="flex-grow-1">
        <div class="container mt-4">
            {% block content %}{% endblock %}
        </div>
    </main>

Футер сайта
~~~~~~~~~~~

Футер содержит контактную информацию и копирайт. Используется Bootstrap-сетка для разметки. Класс mt-auto прижимает футер к низу экрана, если контента мало.

.. code-block:: django

    <footer class="footer bg-light py-4 mt-auto">
        <div class="container">
            <div class="row">
                <div class="col-md-6">
                    <h5>Контакты</h5>
                    <p>Телефон: +7 (123) 456-78-90</p>
                    <p>Email: info@example.com</p>
                </div>
                <div class="col-md-6 text-end">
                    <p>&copy; 2025 Магазин "МОЙ НЕ САМ". Все права защищены.</p>
                </div>
            </div>
        </div>
    </footer>

Подключение скриптов и блок scripts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

В конце body подключается основной JS Bootstrap и определяется block scripts для подключения дополнительных скриптов в дочерних шаблонах.

.. code-block:: django

    <script src="{% static 'bootstrap.bundle.min.js' %}"></script>
    {% block scripts %}{% endblock %}

Закрытие документа
~~~~~~~~~~~~~~~~~~

.. code-block:: django

    </body>
    </html>

---

**Примечания:**
- Все страницы сайта наследуют base.html и вставляют свой контент в block content.
- Для подключения стилей и скриптов используются только статические файлы.
- Футер всегда прижат к низу экрана благодаря flex-верстке.
- Блоки extra_css и scripts позволяют расширять шаблон без его изменения.
- Использование Bootstrap и flex-верстки обеспечивает современный внешний вид и адаптивность.
- Соблюдение best practices и принципов безопасности защищает сайт от типовых уязвимостей.

Если собрать все блоки, получится универсальный, безопасный и расширяемый базовый шаблон для всех страниц сайта.

Шаблон главной страницы (main_page.html)
---------------------------------

Этот шаблон реализует главную страницу интернет-магазина: слайдер, блок популярных товаров, преимущества магазина. Он служит "витриной" сайта и направляет пользователя к основным разделам.

**Теоретические основы главной страницы**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Роль главной страницы
~~~~~~~~~~~~~~~~~~~~~~~~
Главная страница — это первое, что видит пользователь. Она должна быть максимально информативной, визуально привлекательной и мотивировать к действию (например, перейти в каталог или оформить заказ).

2. Структура шаблона
~~~~~~~~~~~~~~~~~~~~
Шаблон наследует base.html, что обеспечивает единый стиль и повторное использование кода. Весь уникальный контент размещён в block content.

.. code-block:: django

    {% extends 'base.html' %}
    {% load static %}
    {% block title %}МОЙ НЕ САМ - Интернет-магазин{% endblock %}
    {% block content %}
    ...
    {% endblock %}

3. Слайдер (carousel)
~~~~~~~~~~~~~~~~~~~~~
Слайдер — это динамический элемент, который позволяет показать несколько ключевых предложений или акций. Используется компонент Bootstrap Carousel. Каждый слайд содержит изображение, заголовок, описание и кнопку действия.

.. code-block:: django

    <div id="mainSlider" class="carousel slide mb-5" data-bs-ride="carousel">
        ...
        <div class="carousel-inner">
            <div class="carousel-item active">
                <img src="..." ...>
                <div class="carousel-caption ...">
                    <h2>...</h2>
                    <p>...</p>
                    <a href="..." class="btn btn-primary">...</a>
                </div>
            </div>
            ...
        </div>
        ...
    </div>

**Теория:**
- Слайдер привлекает внимание к акциям и преимуществам.
- Использование Bootstrap обеспечивает адаптивность и кроссбраузерность.
- Кнопки на слайдах ведут к ключевым разделам (каталог, акции).

4. Блок "Популярные товары"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Этот блок выводит карточки самых популярных товаров. Используется цикл по popular_products. Для каждого товара отображается изображение, название, описание, цена и кнопки действий.

.. code-block:: django

    <div class="row row-cols-1 row-cols-md-2 row-cols-lg-4 g-4 mb-5">
        {% for product in popular_products %}
        <div class="col">
            <div class="card h-100 product-card">
                ...
            </div>
        </div>
        {% empty %}
        <div class="col-12">
            <div class="alert alert-info">
                <p>Пока нет товаров для отображения.</p>
            </div>
        </div>
        {% endfor %}
    </div>

**Теория:**
- Карточки товаров — основной способ визуального представления ассортимента.
- Если товара нет — выводится информативное сообщение.
- Кнопка "Подробнее" ведёт на страницу товара, "В корзину" — добавляет товар в корзину (только для авторизованных).
- Использование truncatechars для описания предотвращает "разбегание" карточек.

5. Блок "Преимущества магазина"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
В этом блоке перечислены ключевые преимущества магазина: быстрая доставка, гарантия качества, поддержка 24/7. Каждый пункт оформлен в виде карточки с иконкой, заголовком и описанием.

.. code-block:: django

    <div class="row mb-5">
        <div class="col-md-4 mb-4">
            <div class="card h-100 text-center p-4">
                <div class="card-body">
                    <i class="bi bi-truck display-1 text-primary mb-3"></i>
                    <h4>Быстрая доставка</h4>
                    <p class="card-text">Доставляем товары в кратчайшие сроки по всей России.</p>
                </div>
            </div>
        </div>
        ...
    </div>

**Теория:**
- Преимущества формируют доверие и мотивируют к покупке.
- Использование иконок делает блок визуально привлекательным.
- Карточки адаптивны и хорошо смотрятся на разных устройствах.

6. Адаптивность и UX
~~~~~~~~~~~~~~~~~~~~
- Все элементы используют Bootstrap-сетки и классы для адаптивности.
- Кнопки и ссылки снабжены понятными подписями и иконками.
- Вёрстка устойчива к отсутствию данных (нет товаров — есть сообщение).

7. Безопасность и best practices
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- Все данные, выводимые из переменных, проходят экранирование по умолчанию.
- Для изображений товаров предусмотрена заглушка, если файл отсутствует.
- Кнопка "В корзину" доступна только авторизованным пользователям (проверка request.user.is_authenticated).

---

**Примечания:**
- Главная страница — ключевой инструмент маркетинга и навигации.
- Использование слайдера и карточек повышает вовлечённость пользователя.
- Все блоки адаптивны и корректно отображаются на мобильных устройствах.
- Шаблон легко расширять: можно добавить новые слайды, преимущества или секции без изменения структуры.

Если собрать все блоки, получится современная, информативная и удобная главная страница интернет-магазина.