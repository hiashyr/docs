Проект "Корочки.есть"
=====================

Описание проекта
----------------
Образовательный портал для записи на онлайн курсы. Пользователи могут регистрироваться,
подавать заявки на обучение и оставлять отзывы.

Структура проекта
-----------------
- base.html - базовый шаблон
- home.html - главная страница
- applications.html - список заявок
- add_review.html - добавление отзыва
- create_application.html - создание заявки
- login.html - страница входа
- register.html - страница регистрации

Base.html
=========

Назначение
----------
Базовый шаблон, от которого наследуются все остальные страницы.

Код
---
.. code-block:: html

    {% load static %}

    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{% block title %}Корочки.есть{% endblock %}</title>
        <meta name="description" content="{% block description %}Онлайн курсы дополнительного профессионального образования{% endblock %}">
        <meta name="keywords" content="{% block keywords %}курсы, обучение, образование{% endblock %}">
        
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="{% static 'styles.css' %}" rel="stylesheet">
    </head>
    <body>
        <!-- Навигационная панель -->
        <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
            <div class="container">
                <a class="navbar-brand fw-bold" href="{% url 'home' %}">📚 Корочки.есть</a>
                
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarMain">
                    <span class="navbar-toggler-icon"></span>
                </button>

                <div class="collapse navbar-collapse" id="navbarMain">
                    <ul class="navbar-nav ms-auto">
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'home' %}">Главная</a>
                        </li>
                        
                        {% if user.is_authenticated %}
                            <li class="nav-item">
                                <a class="nav-link" href="{% url 'applications' %}">Мои заявки</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link" href="{% url 'create_application' %}">Подать заявку</a>
                            </li>
                            {% if user.is_staff %}
                            <li class="nav-item">
                                <a class="nav-link" href="/admin/">Админка</a>
                            </li>
                            {% endif %}
                            <li class="nav-item">
                                <a class="nav-link text-warning" href="{% url 'logout' %}">Выйти ({{ user.username }})</a>
                            </li>
                        {% else %}
                            <li class="nav-item">
                                <a class="nav-link" href="{% url 'login' %}">Войти</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link btn btn-outline-light btn-sm px-3" href="{% url 'register' %}">Регистрация</a>
                            </li>
                        {% endif %}
                    </ul>
                </div>
            </div>
        </nav>

        <!-- Основной контент -->
        <main class="container my-4">
            {% block content %}{% endblock %}
        </main>

        <!-- Простой подвал -->
        <footer class="bg-light py-4 mt-5 border-top">
            <div class="container">
                <div class="row">
                    <div class="col-md-6">
                        <p class="mb-0">© {% now "Y" %} Корочки.есть - онлайн курсы</p>
                    </div>
                    <div class="col-md-6 text-end">
                        <p class="mb-0 text-muted small">Все права защищены</p>
                    </div>
                </div>
            </div>
        </footer>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>

Структура
---------
- **Шапка**: навигационная панель с логотипом и меню
- **Основной блок**: контейнер для контента страниц
- **Подвал**: информация о копирайте

Home.html
=========

Назначение
----------
Главная страница портала с информацией о курсах.

Код
---
.. code-block:: html

    {% extends 'base.html' %}
    {% load static %}

    {% block title %}Главная - Корочки.есть{% endblock %}
    {% block description %}Запишитесь на онлайн курсы программирования, веб-дизайна и баз данных. Официальные документы.{% endblock %}
    {% block keywords %}курсы, программирование, веб-дизайн, базы данных, обучение{% endblock %}

    {% block content %}
    <!-- Приветственный блок -->
    <div class="row mb-5">
        <div class="col-12 text-center">
            <h1 class="display-4 mb-3">Добро пожаловать на портал "Корочки.есть"</h1>
            <p class="lead text-muted">Онлайн курсы дополнительного профессионального образования</p>
            
            {% if not user.is_authenticated %}
                <div class="mt-4">
                    <a href="{% url 'register' %}" class="btn btn-primary btn-lg me-2">Начать обучение</a>
                    <a href="{% url 'login' %}" class="btn btn-outline-primary btn-lg">Войти</a>
                </div>
            {% else %}
                <div class="mt-4">
                    <a href="{% url 'create_application' %}" class="btn btn-success btn-lg me-2">➕ Новая заявка</a>
                    <a href="{% url 'applications' %}" class="btn btn-outline-success btn-lg">📋 Мои заявки</a>
                </div>
            {% endif %}
        </div>
    </div>

    <!-- Слайдер -->
    <div class="row justify-content-center mb-5">
        <div class="col-lg-10">
            <div id="mainSlider" class="carousel slide shadow rounded overflow-hidden" data-bs-ride="carousel">
                <div class="carousel-indicators">
                    <button type="button" data-bs-target="#mainSlider" data-bs-slide-to="0" class="active"></button>
                    <button type="button" data-bs-target="#mainSlider" data-bs-slide-to="1"></button>
                    <button type="button" data-bs-target="#mainSlider" data-bs-slide-to="2"></button>
                    <button type="button" data-bs-target="#mainSlider" data-bs-slide-to="3"></button>
                </div>

                <div class="carousel-inner">
                    <div class="carousel-item active">
                        <img src="{% static 'images/slide1.jpg' %}" class="d-block w-100" style="height: 350px; object-fit: cover;" alt="Программирование">
                        <div class="carousel-caption d-none d-md-block bg-dark bg-opacity-50 rounded p-3">
                            <h5>Основы алгоритмизации и программирования</h5>
                            <p>Научитесь основам программирования и созданию алгоритмов</p>
                        </div>
                    </div>
                    <div class="carousel-item">
                        <img src="{% static 'images/slide2.jpg' %}" class="d-block w-100" style="height: 350px; object-fit: cover;" alt="Веб-дизайн">
                        <div class="carousel-caption d-none d-md-block bg-dark bg-opacity-50 rounded p-3">
                            <h5>Основы веб-дизайна</h5>
                            <p>Освойте современные тенденции в создании веб-интерфейсов</p>
                        </div>
                    </div>
                    <div class="carousel-item">
                        <img src="{% static 'images/slide3.jpg' %}" class="d-block w-100" style="height: 350px; object-fit: cover;" alt="Базы данных">
                        <div class="carousel-caption d-none d-md-block bg-dark bg-opacity-50 rounded p-3">
                            <h5>Основы проектирования баз данных</h5>
                            <p>Изучите принципы проектирования и работы с базами данных</p>
                        </div>
                    </div>
                    <div class="carousel-item">
                        <img src="{% static 'images/slide4.jpg' %}" class="d-block w-100" style="height: 350px; object-fit: cover;" alt="Дипломы">
                        <div class="carousel-caption d-none d-md-block bg-dark bg-opacity-50 rounded p-3">
                            <h5>Получите документы об образовании</h5>
                            <p>Официальные документы после успешного завершения курсов</p>
                        </div>
                    </div>
                </div>

                <button class="carousel-control-prev" type="button" data-bs-target="#mainSlider" data-bs-slide="prev">
                    <span class="carousel-control-prev-icon"></span>
                </button>
                <button class="carousel-control-next" type="button" data-bs-target="#mainSlider" data-bs-slide="next">
                    <span class="carousel-control-next-icon"></span>
                </button>
            </div>
        </div>
    </div>

    <!-- Карточки курсов -->
    <div class="row">
        <div class="col-md-4 mb-4">
            <div class="card h-100 shadow-sm">
                <div class="card-body text-center">
                    <div class="display-4 mb-3">💻</div>
                    <h5 class="card-title">Основы алгоритмизации</h5>
                    <p class="card-text text-muted">Изучите основы программирования, алгоритмы и структуры данных.</p>
                    <a href="{% url 'create_application' %}" class="btn btn-outline-primary">Записаться</a>
                </div>
            </div>
        </div>
        <div class="col-md-4 mb-4">
            <div class="card h-100 shadow-sm">
                <div class="card-body text-center">
                    <div class="display-4 mb-3">🎨</div>
                    <h5 class="card-title">Веб-дизайн</h5>
                    <p class="card-text text-muted">Освойте создание современных веб-интерфейсов и UX/UI дизайн.</p>
                    <a href="{% url 'create_application' %}" class="btn btn-outline-primary">Записаться</a>
                </div>
            </div>
        </div>
        <div class="col-md-4 mb-4">
            <div class="card h-100 shadow-sm">
                <div class="card-body text-center">
                    <div class="display-4 mb-3">🗄️</div>
                    <h5 class="card-title">Базы данных</h5>
                    <p class="card-text text-muted">Научитесь проектировать и работать с базами данных.</p>
                    <a href="{% url 'create_application' %}" class="btn btn-outline-primary">Записаться</a>
                </div>
            </div>
        </div>
    </div>

    <script>
    document.addEventListener('DOMContentLoaded', function() {
        var slider = new bootstrap.Carousel(document.getElementById('mainSlider'), {
            interval: 3000,
            wrap: true
        });
    });
    </script>
    {% endblock %}

Структура
---------
1. **Приветственный блок** - заголовок и кнопки действий
2. **Слайдер** - 4 изображения с описанием курсов
3. **Карточки курсов** - 3 карточки с описанием направлений

Applications.html
=================

Назначение
----------
Страница со списком всех заявок пользователя.

Код
---
.. code-block:: html

    {% extends 'base.html' %}
    {% load static %}

    {% block title %}Мои заявки - Корочки.есть{% endblock %}
    {% block description %}Просмотр ваших заявок на обучение и отзывов{% endblock %}
    {% block keywords %}заявки, обучение, отзывы, статусы{% endblock %}

    {% block content %}
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h2>Мои заявки</h2>
        <a href="{% url 'create_application' %}" class="btn btn-primary">
            ➕ Новая заявка
        </a>
    </div>

    {% if applications %}
        <div class="row">
            {% for application in applications %}
            <div class="col-md-6 mb-4">
                <div class="card h-100 shadow-sm
                    {% if application.status == 'new' %}border-success border-2
                    {% elif application.status == 'in_progress' %}border-warning border-2
                    {% elif application.status == 'completed' %}border-secondary border-2{% endif %}">
                    
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-start mb-3">
                            <h5 class="card-title mb-0">{{ application.get_course_display }}</h5>
                            <span class="badge 
                                {% if application.status == 'new' %}bg-success
                                {% elif application.status == 'in_progress' %}bg-warning text-dark
                                {% else %}bg-secondary{% endif %} fs-6">
                                {{ application.get_status_display }}
                            </span>
                        </div>

                        <p class="card-text">
                            <strong>Дата начала:</strong> {{ application.desired_start_date|date:"d.m.Y" }}<br>
                            <strong>Способ оплаты:</strong> {{ application.get_payment_method_display }}<br>
                            <strong>Подана:</strong> {{ application.created_at|date:"d.m.Y H:i" }}
                        </p>

                        {% if application.status == 'completed' %}
                            <div class="mt-3 pt-3 border-top">
                                {% if application.review %}
                                    <div class="bg-light p-3 rounded">
                                        <strong>Ваш отзыв:</strong><br>
                                        Оценка: {{ application.review.rating }}/5<br>
                                        {{ application.review.text }}
                                    </div>
                                {% else %}
                                    <a href="{% url 'add_review' application.id %}" class="btn btn-outline-primary">
                                        📝 Оставить отзыв
                                    </a>
                                {% endif %}
                            </div>
                        {% endif %}
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    {% else %}
        <div class="text-center py-5">
            <h4 class="mb-3">У вас пока нет заявок</h4>
            <p class="text-muted mb-4">Подайте первую заявку на обучение!</p>
            <a href="{% url 'create_application' %}" class="btn btn-primary btn-lg">Подать заявку</a>
        </div>
    {% endif %}
    {% endblock %}

Особенности
-----------
- **Цветовая индикация статусов**:
  * Зеленая рамка - новая заявка
  * Желтая рамка - в процессе
  * Серая рамка - завершена
- **Для завершенных заявок**: отображение отзыва или кнопка для его добавления

Add_review.html
===============

Назначение
----------
Страница для добавления отзыва о пройденном курсе.

Код
---
.. code-block:: html

    {% extends 'base.html' %}

    {% block title %}Отзыв - Корочки.есть{% endblock %}
    {% block description %}Оставьте отзыв о пройденном курсе{% endblock %}
    {% block keywords %}отзыв, оценка, курс, обучение{% endblock %}

    {% block content %}
    <h2 class="mb-4">Оставить отзыв</h2>

    <div class="card mb-4 shadow-sm">
        <div class="card-body">
            <h5 class="card-title">Информация о курсе</h5>
            <p class="mb-1"><strong>Курс:</strong> {{ application.get_course_display }}</p>
            <p class="mb-1"><strong>Дата начала:</strong> {{ application.desired_start_date|date:"d.m.Y" }}</p>
            <p class="mb-0"><strong>Способ оплаты:</strong> {{ application.get_payment_method_display }}</p>
        </div>
    </div>

    <form method="post" class="needs-validation">
        {% csrf_token %}

        {% for field in form %}
        <div class="mb-3">
            <label for="{{ field.id_for_label }}" class="form-label fw-bold">{{ field.label }}</label>
            {{ field }}
            {% if field.help_text %}
                <div class="form-text">{{ field.help_text }}</div>
            {% endif %}
            {% if field.errors %}
                <div class="text-danger small">
                    {% for error in field.errors %}
                        {{ error }}
                    {% endfor %}
                </div>
            {% endif %}
        </div>
        {% endfor %}

        <button type="submit" class="btn btn-primary">Опубликовать отзыв</button>
        <a href="{% url 'applications' %}" class="btn btn-outline-secondary">Отмена</a>
    </form>
    {% endblock %}

Структура
---------
1. **Карточка с информацией о курсе**
2. **Форма для отзыва** (автоматически генерируется из Django формы)

Create_application.html
======================

Назначение
----------
Страница для создания новой заявки на обучение.

Код
---
.. code-block:: html

    {% extends 'base.html' %}

    {% block title %}Подача заявки - Корочки.есть{% endblock %}
    {% block description %}Подайте заявку на онлайн курс обучения{% endblock %}
    {% block keywords %}заявка, курс, обучение, подать{% endblock %}

    {% block content %}
    <div class="row justify-content-center">
        <div class="col-md-8">
            <h2 class="mb-4">Подача заявки на курс</h2>
            
            <div class="card shadow-sm">
                <div class="card-body">
                    <form method="post">
                        {% csrf_token %}
                        
                        {% for field in form %}
                        <div class="mb-3">
                            <label for="{{ field.id_for_label }}" class="form-label fw-bold">{{ field.label }}</label>
                            {{ field }}
                            {% if field.help_text %}
                                <div class="form-text">{{ field.help_text }}</div>
                            {% endif %}
                            {% if field.errors %}
                                <div class="text-danger small">
                                    {% for error in field.errors %}
                                        {{ error }}
                                    {% endfor %}
                                </div>
                            {% endif %}
                        </div>
                        {% endfor %}
                        
                        <div class="d-grid gap-2">
                            <button type="submit" class="btn btn-primary btn-lg">Отправить заявку</button>
                            <a href="{% url 'home' %}" class="btn btn-outline-secondary">Отмена</a>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
    {% endblock %}

Login.html
==========

Назначение
----------
Страница авторизации пользователей.

Код
---
.. code-block:: html

    {% extends 'base.html' %}

    {% block title %}Вход - Корочки.есть{% endblock %}
    {% block description %}Войдите в свой аккаунт для доступа к курсам{% endblock %}
    {% block keywords %}вход, авторизация, аккаунт{% endblock %}

    {% block content %}
    <div class="row justify-content-center">
        <div class="col-md-6">
            <h2 class="mb-4 text-center">Авторизация</h2>
            
            <div class="card shadow-sm">
                <div class="card-body p-4">
                    {% if messages %}
                        {% for message in messages %}
                            <div class="alert alert-danger">{{ message }}</div>
                        {% endfor %}
                    {% endif %}

                    <form method="post">
                        {% csrf_token %}
                        
                        <div class="mb-3">
                            <label for="username" class="form-label fw-bold">Логин</label>
                            <input type="text" class="form-control form-control-lg" id="username" name="username" required>
                        </div>

                        <div class="mb-4">
                            <label for="password" class="form-label fw-bold">Пароль</label>
                            <input type="password" class="form-control form-control-lg" id="password" name="password" required>
                        </div>

                        <div class="d-grid gap-2">
                            <button type="submit" class="btn btn-primary btn-lg">Войти</button>
                        </div>
                    </form>
                    
                    <hr class="my-4">
                    
                    <p class="text-center mb-0">
                        Еще нет аккаунта? <a href="{% url 'register' %}" class="text-primary">Зарегистрироваться</a>
                    </p>
                </div>
            </div>
        </div>
    </div>
    {% endblock %}

Register.html
============

Назначение
----------
Страница регистрации новых пользователей.

Код
---
.. code-block:: html

    {% extends 'base.html' %}

    {% block title %}Регистрация - Корочки.есть{% endblock %}
    {% block description %}Создайте аккаунт для доступа к онлайн курсам{% endblock %}
    {% block keywords %}регистрация, аккаунт, запись на курсы{% endblock %}

    {% block content %}
    <div class="row justify-content-center">
        <div class="col-md-8">
            <h2 class="mb-4 text-center">Регистрация</h2>
            
            <div class="card shadow-sm">
                <div class="card-body p-4">
                    <form method="post">
                        {% csrf_token %}
                        
                        {% for field in form %}
                        <div class="mb-3">
                            <label for="{{ field.id_for_label }}" class="form-label fw-bold">{{ field.label }}</label>
                            {{ field }}
                            {% if field.help_text %}
                                <div class="form-text">{{ field.help_text }}</div>
                            {% endif %}
                            {% if field.errors %}
                                <div class="text-danger small">
                                    {% for error in field.errors %}
                                        {{ error }}
                                    {% endfor %}
                                </div>
                            {% endif %}
                        </div>
                        {% endfor %}
                        
                        <div class="d-grid gap-2">
                            <button type="submit" class="btn btn-primary btn-lg">Создать пользователя</button>
                        </div>
                    </form>
                    
                    <hr class="my-4">
                    
                    <p class="text-center mb-0">
                        Уже есть аккаунт? <a href="{% url 'login' %}" class="text-primary">Войти</a>
                    </p>
                </div>
            </div>
        </div>
    </div>

    <script>
    // Маска для телефона
    const phoneInput = document.getElementById('id_phone');
    if(phoneInput) {
        phoneInput.addEventListener('input', function(e) {
            let x = e.target.value.replace(/\D/g, '').match(/(\d{0,1})(\d{0,3})(\d{0,3})(\d{0,2})(\d{0,2})/);
            e.target.value = !x[2] ? x[1] : x[1] + '(' + x[2] + (x[3] ? ')' + x[3] : '') + (x[4] ? '-' + x[4] : '') + (x[5] ? '-' + x[5] : '');
        });
    }
    </script>
    {% endblock %}

Используемые технологии
=======================
- **Django** - backend фреймворк
- **Bootstrap 5** - CSS фреймворк для стилей
- **HTML5** - разметка страниц
- **JavaScript** - для интерактивности (слайдер, маска телефона)

Примечания
==========
.. note::
   Все страницы наследуются от base.html, что обеспечивает единый стиль и структуру.

.. warning::
   Для работы слайдера необходимо наличие изображений в папке static/images/