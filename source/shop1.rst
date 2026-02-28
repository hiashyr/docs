<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tea Shop - Документация проекта</title>
</head>
<body>
    <div class="container">
        <!-- Заголовок -->
        <div class="header">
            <h1>🍵 Tea Shop Project</h1>
            <p>Полная документация всех файлов проекта Django</p>
        </div>
        
        <!-- Навигация -->
        <div class="nav-menu">
            <h3>📂 Быстрая навигация по файлам:</h3>
            <a href="#about-html">about.html</a>
            <a href="#base-html">base.html</a>
            <a href="#cart-html">cart.html</a>
            <a href="#contacts-html">contacts.html</a>
            <a href="#login-html">login.html</a>
            <a href="#navbar-html">navbar.html</a>
            <a href="#profile-html">profile.html</a>
            <a href="#register-html">register.html</a>
            <a href="#tea-list-html">tea_list.html</a>
            <a href="#admin-py">admin.py</a>
            <a href="#apps-py">apps.py</a>
            <a href="#models-py">models.py</a>
            <a href="#urls-py">urls.py</a>
            <a href="#views-py">views.py</a>
            <a href="#style-css">style.css</a>
            <a href="#create-sample-py">create_sample_data.py</a>
        </div>

        <!-- ==================== about.html ==================== -->
        <div class="file-section" id="about-html">
            <div class="file-header">
                <h2>📄 about.html</h2>
                <span class="file-type">HTML Template</span>
            </div>
            <div class="code-container">
                <pre><code>&lt;!DOCTYPE html&gt;
&lt;html&gt;
&lt;head&gt;
    &lt;title&gt;О нас - Чайный Магазин&lt;/title&gt;
    &lt;style&gt;
        body { 
            font-family: 'Arial', sans-serif; 
            background: #fff5f5; 
            color: #555; 
        }
        .container { 
            max-width: 800px; 
            margin: 0 auto; 
            padding: 20px; 
        }
        .nav { 
            background: white; 
            padding: 15px; 
            border-radius: 10px; 
            margin-bottom: 20px; 
        }
        .nav a { 
            margin: 0 10px; 
            text-decoration: none; 
            color: #e91e63; 
        }
    &lt;/style&gt;
&lt;/head&gt;
&lt;body&gt;
    &lt;div class="container"&gt;
        {% include 'products/navbar.html' %}
        
        &lt;h1&gt;О нашей чайной лавке&lt;/h1&gt;
        &lt;p&gt;Мы собираем самые нежные и ароматные чаи со всего мира!&lt;/p&gt;
        
        &lt;div style="background: white; padding: 20px; border-radius: 15px;"&gt;
            &lt;h3&gt;Наша миссия:&lt;/h3&gt;
            &lt;p&gt;Дарить радость и уют через каждую чашечку чая!&lt;/p&gt;
            
            &lt;h3&gt;Почему мы?&lt;/h3&gt;
            &lt;ul&gt;
                &lt;li&gt;Только натуральные ингредиенты&lt;/li&gt;
                &lt;li&gt;Милые упаковки с цветочками&lt;/li&gt;
                &lt;li&gt;Быстрая доставка с любовью&lt;/li&gt;
                &lt;li&gt;Персональные рекомендации&lt;/li&gt;
            &lt;/ul&gt;
        &lt;/div&gt;
    &lt;/div&gt;
&lt;/body&gt;
&lt;/html&gt;</code></pre>
            </div>
        </div>

        <!-- ==================== base.html ==================== -->
        <div class="file-section" id="base-html">
            <div class="file-header">
                <h2>📄 base.html</h2>
                <span class="file-type">HTML Template (Base)</span>
            </div>
            <div class="code-container">
                <pre><code>&lt;!DOCTYPE html&gt;
&lt;html&gt;
&lt;head&gt;
    &lt;title&gt;{% block title %}Чайная фея{% endblock %}&lt;/title&gt;
    {% load static %}
    &lt;link rel="stylesheet" href="{% static 'css/style.css' %}"&gt;
    &lt;meta name="viewport" content="width=device-width, initial-scale=1.0"&gt;
&lt;/head&gt;
&lt;body&gt;
    &lt;!-- Навбар --&gt;
    &lt;div class="container"&gt;
        &lt;nav class="nav"&gt;
            &lt;a href="{% url 'tea_list' %}" class="nav-logo"&gt;
                &lt;span class="logo-icon"&gt;🍵&lt;/span&gt;
                &lt;span&gt;Чайная Фея&lt;/span&gt;
            &lt;/a&gt;
            &lt;div class="nav-links"&gt;
                &lt;a href="{% url 'tea_list' %}" class="btn"&gt;Главная&lt;/a&gt;
                &lt;a href="{% url 'cart_view' %}" class="btn btn-cart"&gt;Корзина&lt;/a&gt;
                &lt;a href="{% url 'about' %}" class="btn"&gt;О нас&lt;/a&gt;
                &lt;a href="{% url 'contacts' %}" class="btn"&gt;Контакты&lt;/a&gt;
                {% if user.is_authenticated %}
                    &lt;a href="{% url 'profile' %}" class="btn"&gt;{{ user.username }}&lt;/a&gt;
                    &lt;form method="post" action="{% url 'logout' %}" style="display: inline;"&gt;
                        {% csrf_token %}
                        &lt;button type="submit" class="btn btn-remove"&gt;Выйти&lt;/button&gt;
                    &lt;/form&gt;
                {% else %}
                    &lt;a href="{% url 'login' %}" class="btn btn-login"&gt;Войти&lt;/a&gt;
                    &lt;a href="{% url 'register' %}" class="btn btn-register"&gt;Регистрация&lt;/a&gt;
                {% endif %}
            &lt;/div&gt;
        &lt;/nav&gt;
    &lt;/div&gt;
    
    &lt;!-- Контент --&gt;
    &lt;div class="container"&gt;
        {% if messages %}
            &lt;div class="messages"&gt;
                {% for message in messages %}
                    &lt;div class="message {% if message.tags %}{{ message.tags }}{% endif %}"
                         style="background: #e8f5e8; color: #2e7d32; padding: 15px; 
                                border-radius: 15px; margin: 15px 0; 
                                border-left: 5px solid #4CAF50;"&gt;
                        {{ message }}
                    &lt;/div&gt;
                {% endfor %}
            &lt;/div&gt;
        {% endif %}
        {% block content %}{% endblock %}
    &lt;/div&gt;
    
    &lt;!-- Скрипты --&gt;
    &lt;script&gt;
        document.addEventListener('DOMContentLoaded', function() {
            const cards = document.querySelectorAll('.tea-card');
            cards.forEach(card => {
                card.addEventListener('mouseenter', function() {
                    this.style.transform = 'translateY(-5px)';
                });
                card.addEventListener('mouseleave', function() {
                    this.style.transform = 'translateY(0)';
                });
            });
        });
    &lt;/script&gt;
&lt;/body&gt;
&lt;/html&gt;</code></pre>
            </div>
        </div>

        <!-- ==================== cart.html ==================== -->
        <div class="file-section" id="cart-html">
            <div class="file-header">
                <h2>📄 cart.html</h2>
                <span class="file-type">HTML Template</span>
            </div>
            <div class="code-container">
                <pre><code>&lt;!DOCTYPE html&gt;
&lt;html&gt;
&lt;head&gt;
    &lt;title&gt;Корзина - Милый Чайный Магазинчик&lt;/title&gt;
    &lt;style&gt;
        body {
            font-family: 'Arial', sans-serif;
            background-color: #fff5f5;
            color: #555;
            margin: 0;
            padding: 20px;
        }
        .nav {
            background: white;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            text-align: center;
        }
        .nav a {
            margin: 0 15px;
            text-decoration: none;
            color: #e91e63;
            font-weight: bold;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 15px;
        }
        .cart-item {
            display: flex;
            align-items: center;
            padding: 15px;
            border-bottom: 1px solid #ffe6ea;
        }
        .cart-item:last-child {
            border-bottom: none;
        }
        .item-image {
            width: 80px;
            height: 80px;
            border-radius: 10px;
            object-fit: cover;
            margin-right: 20px;
        }
        .item-details {
            flex: 1;
        }
        .quantity-controls {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .quantity-input {
            width: 60px;
            padding: 5px;
            border: 1px solid #ffb6c1;
            border-radius: 5px;
            text-align: center;
        }
        .btn {
            background: #e91e63;
            color: white;
            padding: 8px 15px;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
        }
        .btn-remove {
            background: #ff6b6b;
        }
        .total {
            text-align: right;
            font-size: 24px;
            font-weight: bold;
            color: #e91e63;
            margin-top: 20px;
            padding-top: 20px;
            border-top: 2px solid #ffe6ea;
        }
        .empty-cart {
            text-align: center;
            padding: 40px;
        }
        .messages {
            margin-bottom: 20px;
        }
        .message {
            padding: 10px;
            border-radius: 5px;
            margin: 5px 0;
        }
        .success {
            background: #e8f5e8;
            color: #2e7d32;
        }
        .error {
            background: #ffebee;
            color: #c62828;
        }
    &lt;/style&gt;
&lt;/head&gt;
&lt;body&gt;
    &lt;div class="nav"&gt;
        &lt;a href="{% url 'tea_list' %}"&gt;Главная&lt;/a&gt;
        &lt;a href="{% url 'cart_view' %}"&gt;Корзина&lt;/a&gt;
        &lt;a href="{% url 'about' %}"&gt;О нас&lt;/a&gt;
        &lt;a href="{% url 'contacts' %}"&gt;Контакты&lt;/a&gt;
        {% if user.is_authenticated %}
            &lt;a href="{% url 'profile' %}"&gt;Профиль ({{ user.username }})&lt;/a&gt;
            &lt;form method="post" action="{% url 'logout' %}" style="display: inline;"&gt;
                {% csrf_token %}
                &lt;button type="submit" style="background: none; border: none; 
                       color: #e91e63; cursor: pointer;"&gt;Выйти&lt;/button&gt;
            &lt;/form&gt;
        {% else %}
            &lt;a href="{% url 'login' %}"&gt;Войти&lt;/a&gt;
            &lt;a href="{% url 'register' %}"&gt;Регистрация&lt;/a&gt;
        {% endif %}
    &lt;/div&gt;
    
    &lt;div class="container"&gt;
        &lt;h1 style="text-align: center;"&gt;Твоя корзина&lt;/h1&gt;
        
        &lt;!-- Сообщения --&gt;
        &lt;div class="messages"&gt;
            {% for message in messages %}
                &lt;div class="message {% if message.tags %}{{ message.tags }}{% endif %}"&gt;
                    {{ message }}
                &lt;/div&gt;
            {% endfor %}
        &lt;/div&gt;
        
        {% if cart_items %}
            {% for item in cart_items %}
                &lt;div class="cart-item"&gt;
                    {% if item.product.image %}
                        &lt;img src="{{ item.product.image.url }}" 
                             alt="{{ item.product.name }}" 
                             class="item-image"&gt;
                    {% else %}
                        &lt;div style="width: 80px; height: 80px; background: #ffe6ea; 
                             border-radius: 10px; display: flex; 
                             align-items: center; justify-content: center;"&gt;
                            &lt;span style="color: #e91e63; font-size: 24px;"&gt;🍵&lt;/span&gt;
                        &lt;/div&gt;
                    {% endif %}
                    
                    &lt;div class="item-details"&gt;
                        &lt;h3 style="margin: 0;"&gt;{{ item.product.name }}&lt;/h3&gt;
                        &lt;p style="margin: 5px 0; color: #e91e63; font-weight: bold;"&gt;
                            {{ item.product.price }} руб. × {{ item.quantity }} = {{ item.total_price }} руб.
                        &lt;/p&gt;
                    &lt;/div&gt;
                    
                    &lt;div class="quantity-controls"&gt;
                        &lt;form method="post" action="{% url 'update_cart' item.id %}" 
                              style="display: flex; align-items: center; gap: 10px;"&gt;
                            {% csrf_token %}
                            &lt;input type="number" name="quantity" value="{{ item.quantity }}" 
                                   min="1" class="quantity-input"&gt;
                            &lt;button type="submit" class="btn"&gt;Обновить&lt;/button&gt;
                        &lt;/form&gt;
                        &lt;a href="{% url 'remove_from_cart' item.id %}" class="btn btn-remove"&gt;🗑️&lt;/a&gt;
                    &lt;/div&gt;
                &lt;/div&gt;
            {% endfor %}
            
            &lt;div class="total"&gt;
                Итого: {{ total }} руб.
            &lt;/div&gt;
            
            &lt;div style="text-align: center; margin-top: 30px;"&gt;
                &lt;button class="btn" style="padding: 15px 30px; font-size: 18px;"&gt;
                    Оформить заказ
                &lt;/button&gt;
            &lt;/div&gt;
        {% else %}
            &lt;div class="empty-cart"&gt;
                &lt;h2&gt;Корзина пуста&lt;/h2&gt;
                &lt;p&gt;Добавь что-нибудь вкусненькое из нашего каталога!&lt;/p&gt;
                &lt;a href="{% url 'tea_list' %}" class="btn" style="margin-top: 20px;"&gt;
                    Перейти к чаям
                &lt;/a&gt;
            &lt;/div&gt;
        {% endif %}
    &lt;/div&gt;
&lt;/body&gt;
&lt;/html&gt;</code></pre>
            </div>
        </div>

        <!-- ==================== contacts.html ==================== -->
        <div class="file-section" id="contacts-html">
            <div class="file-header">
                <h2>📄 contacts.html</h2>
                <span class="file-type">HTML Template</span>
            </div>
            <div class="code-container">
                <pre><code>&lt;!DOCTYPE html&gt;
&lt;html&gt;
&lt;head&gt;
    &lt;title&gt;Tea Shop&lt;/title&gt;
    &lt;style&gt;
        body { 
            font-family: 'Arial', sans-serif; 
            background: #fff5f5; 
            color: #555; 
        }
        .container { 
            max-width: 800px; 
            margin: 0 auto; 
            padding: 20px; 
        }
        .contact-card { 
            background: white; 
            padding: 20px; 
            border-radius: 15px; 
            margin: 10px 0; 
        }
    &lt;/style&gt;
&lt;/head&gt;
&lt;body&gt;
    &lt;div class="container"&gt;
        {% include 'products/navbar.html' %}
        
        &lt;h1&gt;Наши контакты&lt;/h1&gt;
        
        &lt;div class="contact-card"&gt;
            &lt;h3&gt;Чайная лавка "Милый Чай"&lt;/h3&gt;
            &lt;p&gt;Адрес: ул. Цветочная, д. 15&lt;/p&gt;
            &lt;p&gt;Телефон: +7 (999) 123-45-67&lt;/p&gt;
            &lt;p&gt;Email: hello@cutetea.ru&lt;/p&gt;
            &lt;p&gt;Время работы: 10:00 - 20:00&lt;/p&gt;
        &lt;/div&gt;
        
        &lt;div class="contact-card"&gt;
            &lt;h3&gt;Напиши нам!&lt;/h3&gt;
            &lt;form&gt;
                &lt;input type="text" placeholder="Твое имя" 
                       style="padding: 10px; margin: 5px; width: 200px;"&gt;&lt;br&gt;
                &lt;input type="email" placeholder="Твой email" 
                       style="padding: 10px; margin: 5px; width: 200px;"&gt;&lt;br&gt;
                &lt;textarea placeholder="Сообщение" 
                          style="padding: 10px; margin: 5px; width: 300px; height: 100px;"&gt;&lt;/textarea&gt;&lt;br&gt;
                &lt;button style="background: #e91e63; color: white; padding: 10px 20px; 
                               border: none; border-radius: 10px;"&gt;Отправить&lt;/button&gt;
            &lt;/form&gt;
        &lt;/div&gt;
    &lt;/div&gt;
&lt;/body&gt;
&lt;/html&gt;</code></pre>
            </div>
        </div>

        <!-- ==================== login.html ==================== -->
        <div class="file-section" id="login-html">
            <div class="file-header">
                <h2>📄 login.html</h2>
                <span class="file-type">HTML Template</span>
            </div>
            <div class="code-container">
                <pre><code>&lt;!DOCTYPE html&gt;
&lt;html&gt;
&lt;head&gt;
    &lt;title&gt;Вход - Милый Чайный Магазинчик&lt;/title&gt;
    &lt;style&gt;
        body { 
            font-family: 'Arial', sans-serif; 
            background: #fff5f5; 
            color: #555; 
        }
        .container { 
            max-width: 400px; 
            margin: 50px auto; 
            padding: 20px; 
            background: white; 
            border-radius: 15px; 
        }
        .form-input { 
            width: 100%; 
            padding: 10px; 
            margin: 10px 0; 
            border: 1px solid #ffb6c1; 
            border-radius: 10px; 
        }
        .btn { 
            background: #e91e63; 
            color: white; 
            padding: 10px 20px; 
            border: none; 
            border-radius: 10px; 
            width: 100%; 
        }
    &lt;/style&gt;
&lt;/head&gt;
&lt;body&gt;
    &lt;div class="container"&gt;
        &lt;h2 style="text-align: center;"&gt;Вход в аккаунт&lt;/h2&gt;
        
        {% if messages %}
            {% for message in messages %}
                &lt;div style="background: #ffebee; color: #c62828; 
                            padding: 10px; border-radius: 5px; margin: 10px 0;"&gt;
                    {{ message }}
                &lt;/div&gt;
            {% endfor %}
        {% endif %}
        
        &lt;form method="post"&gt;
            {% csrf_token %}
            &lt;input type="text" name="username" placeholder="Имя пользователя" 
                   class="form-input" required&gt;
            &lt;input type="password" name="password" placeholder="Пароль" 
                   class="form-input" required&gt;
            &lt;button type="submit" class="btn"&gt;Войти&lt;/button&gt;
        &lt;/form&gt;
        
        &lt;p style="text-align: center; margin-top: 20px;"&gt;
            Нет аккаунта? 
            &lt;a href="{% url 'register' %}" style="color: #e91e63;"&gt;Зарегистрируйся тут!&lt;/a&gt;
        &lt;/p&gt;
    &lt;/div&gt;
&lt;/body&gt;
&lt;/html&gt;</code></pre>
            </div>
        </div>

        <!-- ==================== navbar.html ==================== -->
        <div class="file-section" id="navbar-html">
            <div class="file-header">
                <h2>📄 navbar.html</h2>
                <span class="file-type">HTML Template (Partial)</span>
            </div>
            <div class="code-container">
                <pre><code>&lt;nav class="nav"&gt;
    &lt;a href="{% url 'tea_list' %}"&gt;Главная&lt;/a&gt;
    &lt;a href="{% url 'about' %}"&gt;О нас&lt;/a&gt;
    &lt;a href="{% url 'contacts' %}"&gt;Контакты&lt;/a&gt;
    
    {% if user.is_authenticated %}
        &lt;a href="{% url 'profile' %}"&gt;Профиль ({{ user.username }})&lt;/a&gt;
        &lt;form method="post" action="{% url 'logout' %}" style="display: inline;"&gt;
            {% csrf_token %}
            &lt;button type="submit" style="background: none; border: none; 
                   color: #e91e63; cursor: pointer;"&gt;Выйти&lt;/button&gt;
        &lt;/form&gt;
    {% else %}
        &lt;a href="{% url 'login' %}"&gt;Войти&lt;/a&gt;
        &lt;a href="{% url 'register' %}"&gt;Регистрация&lt;/a&gt;
    {% endif %}
    
    &lt;a href="{% url 'cart_view' %}"&gt;Корзина&lt;/a&gt;
&lt;/nav&gt;</code></pre>
            </div>
        </div>

        <!-- ==================== profile.html ==================== -->
        <div class="file-section" id="profile-html">
            <div class="file-header">
                <h2>📄 profile.html</h2>
                <span class="file-type">HTML Template</span>
            </div>
            <div class="code-container">
                <pre><code>&lt;!DOCTYPE html&gt;
&lt;html&gt;
&lt;head&gt;
    &lt;title&gt;Профиль - Милый Чайный Магазинчик&lt;/title&gt;
    &lt;style&gt;
        body { 
            font-family: 'Arial', sans-serif; 
            background: #fff5f5; 
            color: #555; 
        }
        .container { 
            max-width: 600px; 
            margin: 0 auto; 
            padding: 20px; 
        }
        .profile-card { 
            background: white; 
            padding: 20px; 
            border-radius: 15px; 
            text-align: center; 
        }
    &lt;/style&gt;
&lt;/head&gt;
&lt;body&gt;
    &lt;div class="container"&gt;
        {% include 'products/navbar.html' %}
        
        &lt;div class="profile-card"&gt;
            &lt;h2&gt;Твой профиль&lt;/h2&gt;
            &lt;p&gt;Привет, {{ user.username }}!&lt;/p&gt;
            &lt;p&gt;Ты зарегистрировалась: {{ user.date_joined|date:"d.m.Y" }}&lt;/p&gt;
            
            &lt;div style="margin: 20px 0;"&gt;
                &lt;h3&gt;Твои бонусы:&lt;/h3&gt;
                &lt;p&gt;100 баллов за регистрацию&lt;/p&gt;
                &lt;p&gt;Скидка 10% на первый заказ&lt;/p&gt;
            &lt;/div&gt;
            
            &lt;form method="post" action="{% url 'logout' %}"&gt;
                {% csrf_token %}
                &lt;button type="submit" style="background: #e91e63; color: white; 
                               padding: 10px 20px; border: none; border-radius: 10px;"&gt;
                    Выйти
                &lt;/button&gt;
            &lt;/form&gt;
        &lt;/div&gt;
    &lt;/div&gt;
&lt;/body&gt;
&lt;/html&gt;</code></pre>
            </div>
        </div>

        <!-- ==================== register.html ==================== -->
        <div class="file-section" id="register-html">
            <div class="file-header">
                <h2>📄 register.html</h2>
                <span class="file-type">HTML Template</span>
            </div>
            <div class="code-container">
                <pre><code>&lt;!DOCTYPE html&gt;
&lt;html&gt;
&lt;head&gt;
    &lt;title&gt;Регистрация - Tea Shop&lt;/title&gt;
    &lt;style&gt;
        body { 
            font-family: 'Arial', sans-serif; 
            background: #fff5f5; 
            color: #555; 
        }
        .container { 
            max-width: 400px; 
            margin: 50px auto; 
            padding: 20px; 
            background: white; 
            border-radius: 15px; 
        }
        .form-input { 
            width: 100%; 
            padding: 10px; 
            margin: 10px 0; 
            border: 1px solid #ffb6c1; 
            border-radius: 10px; 
        }
        .btn { 
            background: #e91e63; 
            color: white; 
            padding: 10px 20px; 
            border: none; 
            border-radius: 10px; 
            width: 100%; 
        }
    &lt;/style&gt;
&lt;/head&gt;
&lt;body&gt;
    &lt;div class="container"&gt;
        &lt;h2 style="text-align: center;"&gt;Регистрация&lt;/h2&gt;
        
        &lt;form method="post"&gt;
            {% csrf_token %}
            {% for field in form %}
                &lt;div&gt;
                    {{ field.label_tag }}&lt;br&gt;
                    {{ field }}&lt;br&gt;
                    {% if field.help_text %}
                        &lt;small style="color: #888;"&gt;{{ field.help_text }}&lt;/small&gt;
                    {% endif %}
                    {% for error in field.errors %}
                        &lt;p style="color: red;"&gt;{{ error }}&lt;/p&gt;
                    {% endfor %}
                &lt;/div&gt;
            {% endfor %}
            
            &lt;button type="submit" class="btn"&gt;Создать аккаунт&lt;/button&gt;
        &lt;/form&gt;
        
        &lt;p style="text-align: center; margin-top: 20px;"&gt;
            Уже есть аккаунт? 
            &lt;a href="{% url 'login' %}" style="color: #e91e63;"&gt;Войди тут!&lt;/a&gt;
        &lt;/p&gt;
    &lt;/div&gt;
&lt;/body&gt;
&lt;/html&gt;</code></pre>
            </div>
        </div>

        <!-- ==================== tea_list.html ==================== -->
        <div class="file-section" id="tea-list-html">
            <div class="file-header">
                <h2>📄 tea_list.html</h2>
                <span class="file-type">HTML Template</span>
            </div>
            <div class="code-container">
                <pre><code>{% extends 'products/base.html' %}
{% load static %}

{% block content %}
&lt;div style="display: flex;"&gt;
    &lt;!-- Сайдбар с категориями --&gt;
    &lt;div class="sidebar" style="width: 250px; background: white; padding: 25px; 
         border-radius: 20px; margin-right: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);"&gt;
        &lt;h3 style="margin-top: 0; color: #e91e63;"&gt;Категории&lt;/h3&gt;
        &lt;a href="?" class="btn" style="display: block; text-align: center; 
           margin: 10px 0; background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);"&gt;
            Все чаи
        &lt;/a&gt;
        &lt;a href="?" class="btn" style="display: block; text-align: center; 
           margin: 10px 0; background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);"&gt;
            Зеленые
        &lt;/a&gt;
        &lt;a href="?" class="btn" style="display: block; text-align: center; 
           margin: 10px 0; background: linear-gradient(135deg, #E91E63 0%, #AD1457 100%);"&gt;
            Цветочные
        &lt;/a&gt;
        &lt;a href="?" class="btn" style="display: block; text-align: center; 
           margin: 10px 0; background: linear-gradient(135deg, #FF6B6B 0%, #EE5A52 100%);"&gt;
            Фруктовые
        &lt;/a&gt;
    &lt;/div&gt;
    
    &lt;!-- Основной контент --&gt;
    &lt;div style="flex: 1;"&gt;
        &lt;div class="welcome-banner floating"&gt;
            &lt;h1 style="margin: 0; color: #e91e63;"&gt;
                Добро пожаловать в наш Чайный Мир!
            &lt;/h1&gt;
            &lt;p style="font-size: 18px; margin: 10px 0;"&gt;
                Открой для себя волшебство в каждой чашке
            &lt;/p&gt;
            {% if not user.is_authenticated %}
                &lt;p&gt;Зарегистрируйся и получи скидку 10% на первый заказ!&lt;/p&gt;
                &lt;a href="{% url 'register' %}" class="btn btn-register" 
                   style="font-size: 18px;"&gt;
                    Получить скидку
                &lt;/a&gt;
            {% endif %}
        &lt;/div&gt;
        
        &lt;div style="text-align: center;"&gt;
            {% for tea in teas %}
                &lt;div class="tea-card"&gt;
                    {% if tea.image %}
                        &lt;img src="{{ tea.image.url }}" alt="{{ tea.name }}" 
                             class="tea-image"&gt;
                    {% else %}
                        &lt;div style="background: linear-gradient(135deg, #ffe6ea 0%, 
                             #ffcdd2 100%); height: 200px; border-radius: 15px; 
                             display: flex; align-items: center; justify-content: center;"&gt;
                            &lt;span style="color: #e91e63; font-size: 48px;" 
                                  class="floating"&gt;🍵&lt;/span&gt;
                        &lt;/div&gt;
                    {% endif %}
                    
                    &lt;h3 style="color: #e91e63; margin: 15px 0;"&gt;{{ tea.name }}&lt;/h3&gt;
                    &lt;p style="color: #666; line-height: 1.5;"&gt;{{ tea.description }}&lt;/p&gt;
                    
                    {% if tea.ingredients %}
                        &lt;p&gt;&lt;strong&gt;Состав:&lt;/strong&gt; {{ tea.ingredients }}&lt;/p&gt;
                    {% endif %}
                    
                    &lt;div style="display: flex; justify-content: space-around; margin: 15px 0;"&gt;
                        {% if tea.weight %}
                            &lt;span style="background: #e3f2fd; padding: 5px 10px; 
                                  border-radius: 15px; color: #1976D2;"&gt;
                                {{ tea.weight }}г
                            &lt;/span&gt;
                        {% endif %}
                        {% if tea.brewing_time %}
                            &lt;span style="background: #f3e5f5; padding: 5px 10px; 
                                  border-radius: 15px; color: #7B1FA2;"&gt;
                                {{ tea.brewing_time }} мин
                            &lt;/span&gt;
                        {% endif %}
                    &lt;/div&gt;
                    
                    &lt;p style="color: #e91e63; font-weight: bold; 
                       font-size: 24px; margin: 15px 0;"&gt;
                        {{ tea.price }} руб.
                    &lt;/p&gt;
                    
                    &lt;a href="{% url 'add_to_cart' tea.id %}" class="btn" 
                       style="width: 100%;"&gt;
                        В корзину
                    &lt;/a&gt;
                &lt;/div&gt;
            {% empty %}
                &lt;div class="tea-card" style="width: 100%;"&gt;
                    &lt;h3 style="color: #e91e63;"&gt;Пока нет чаев в магазине&lt;/h3&gt;
                    &lt;p&gt;Добавь первый чай через админку!&lt;/p&gt;
                    &lt;a href="/admin" class="btn"&gt;Перейти в админку&lt;/a&gt;
                &lt;/div&gt;
            {% endfor %}
        &lt;/div&gt;
    &lt;/div&gt;
&lt;/div&gt;
{% endblock %}</code></pre>
            </div>
        </div>

        <!-- ==================== admin.py ==================== -->
        <div class="file-section" id="admin-py">
            <div class="file-header">
                <h2>🐍 admin.py</h2>
                <span class="file-type">Python (Django Admin)</span>
            </div>
            <div class="code-container">
                <pre><code><span class="keyword">from</span> django.contrib <span class="keyword">import</span> admin
<span class="keyword">from</span> .models <span class="keyword">import</span> TeaProduct, Cart

<span class="keyword">@admin.register</span>(TeaProduct)
<span class="keyword">class</span> <span class="function">TeaProductAdmin</span>(admin.ModelAdmin):
    list_display = [<span class="string">'name'</span>, <span class="string">'price'</span>, <span class="string">'is_available'</span>]
    list_filter = [<span class="string">'is_available'</span>]
    search_fields = [<span class="string">'name'</span>]

<span class="keyword">@admin.register</span>(Cart)
<span class="keyword">class</span> <span class="function">CartAdmin</span>(admin.ModelAdmin):
    list_display = [<span class="string">'user'</span>, <span class="string">'product'</span>, <span class="string">'quantity'</span>, <span class="string">'added_at'</span>]
    list_filter = [<span class="string">'added_at'</span>]</code></pre>
            </div>
        </div>

        <!-- ==================== apps.py ==================== -->
        <div class="file-section" id="apps-py">
            <div class="file-header">
                <h2>🐍 apps.py</h2>
                <span class="file-type">Python (Django App Config)</span>
            </div>
            <div class="code-container">
                <pre><code><span class="keyword">from</span> django.apps <span class="keyword">import</span> AppConfig

<span class="keyword">class</span> <span class="function">ProductsConfig</span>(AppConfig):
    default_auto_field = <span class="string">'django.db.models.BigAutoField'</span>
    name = <span class="string">'products'</span></code></pre>
            </div>
        </div>

        <!-- ==================== models.py ==================== -->
        <div class="file-section" id="models-py">
            <div class="file-header">
                <h2>🐍 models.py</h2>
                <span class="file-type">Python (Django Models)</span>
            </div>
            <div class="code-container">
                <pre><code><span class="keyword">from</span> django.db <span class="keyword">import</span> models
<span class="keyword">from</span> django.contrib.auth.models <span class="keyword">import</span> User

<span class="keyword">class</span> <span class="function">TeaProduct</span>(models.Model):
    name = models.CharField(max_length=<span class="number">100</span>, verbose_name=<span class="string">"Название чая"</span>)
    description = models.TextField(verbose_name=<span class="string">"Описание"</span>)
    price = models.DecimalField(max_digits=<span class="number">8</span>, decimal_places=<span class="number">2</span>, 
                                verbose_name=<span class="string">"Цена"</span>)
    image = models.ImageField(upload_to=<span class="string">'teas/'</span>, blank=<span class="keyword">True</span>, 
                              null=<span class="keyword">True</span>, verbose_name=<span class="string">"Картинка"</span>)
    is_available = models.BooleanField(default=<span class="keyword">True</span>, 
                       verbose_name=<span class="string">"В наличии"</span>)
    
    <span class="keyword">def</span> <span class="function">__str__</span>(self):
        <span class="keyword">return</span> self.name
    
    <span class="keyword">class</span> Meta:
        verbose_name = <span class="string">"Чайный продукт"</span>
        verbose_name_plural = <span class="string">"Чайные продукты"</span>


<span class="keyword">class</span> <span class="function">Cart</span>(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, 
             verbose_name=<span class="string">"Пользователь"</span>)
    product = models.ForeignKey(TeaProduct, on_delete=models.CASCADE, 
                verbose_name=<span class="string">"Товар"</span>)
    quantity = models.PositiveIntegerField(default=<span class="number">1</span>, 
                   verbose_name=<span class="string">"Количество"</span>)
    added_at = models.DateTimeField(auto_now_add=<span class="keyword">True</span>, 
                    verbose_name=<span class="string">"Дата добавления"</span>)
    
    <span class="keyword">def</span> <span class="function">__str__</span>(self):
        <span class="keyword">return</span> f<span class="string">"{self.user.username} - {self.product.name}"</span>
    
    <span class="keyword">def</span> <span class="function">total_price</span>(self):
        <span class="keyword">return</span> self.product.price * self.quantity
    
    <span class="keyword">class</span> Meta:
        verbose_name = <span class="string">"Корзина"</span>
        verbose_name_plural = <span class="string">"Корзины"</span></code></pre>
            </div>
        </div>

        <!-- ==================== urls.py ==================== -->
        <div class="file-section" id="urls-py">
            <div class="file-header">
                <h2>🐍 urls.py</h2>
                <span class="file-type">Python (Django URLs)</span>
            </div>
            <div class="code-container">
                <pre><code><span class="keyword">from</span> django.urls <span class="keyword">import</span> path
<span class="keyword">from</span> django.contrib.auth <span class="keyword">import</span> views <span class="keyword">as</span> auth_views
<span class="keyword">from</span> . <span class="keyword">import</span> views

urlpatterns = [
    path(<span class="string">''</span>, views.tea_list, name=<span class="string">'tea_list'</span>),
    path(<span class="string">'about/'</span>, views.about, name=<span class="string">'about'</span>),
    path(<span class="string">'contacts/'</span>, views.contacts, name=<span class="string">'contacts'</span>),
    path(<span class="string">'register/'</span>, views.register, name=<span class="string">'register'</span>),
    path(<span class="string">'profile/'</span>, views.profile, name=<span class="string">'profile'</span>),
    path(<span class="string">'login/'</span>, auth_views.LoginView.as_view(
         template_name=<span class="string">'products/login.html'</span>), name=<span class="string">'login'</span>),
    path(<span class="string">'logout/'</span>, auth_views.LogoutView.as_view(), name=<span class="string">'logout'</span>),
    
    <span class="comment"># Пути для корзины</span>
    path(<span class="string">'cart/'</span>, views.cart_view, name=<span class="string">'cart_view'</span>),
    path(<span class="string">'add-to-cart/&lt;int:product_id&gt;/'</span>, views.add_to_cart, 
         name=<span class="string">'add_to_cart'</span>),
    path(<span class="string">'remove-from-cart/&lt;int:item_id&gt;/'</span>, views.remove_from_cart, 
         name=<span class="string">'remove_from_cart'</span>),
    path(<span class="string">'update-cart/&lt;int:item_id&gt;/'</span>, views.update_cart, 
         name=<span class="string">'update_cart'</span>),
]</code></pre>
            </div>
        </div>

        <!-- ==================== views.py ==================== -->
        <div class="file-section" id="views-py">
            <div class="file-header">
                <h2>🐍 views.py</h2>
                <span class="file-type">Python (Django Views)</span>
            </div>
            <div class="code-container">
                <pre><code><span class="keyword">from</span> django.shortcuts <span class="keyword">import</span> render, redirect, get_object_or_404
<span class="keyword">from</span> django.contrib.auth <span class="keyword">import</span> login, authenticate
<span class="keyword">from</span> django.contrib.auth.forms <span class="keyword">import</span> UserCreationForm
<span class="keyword">from</span> django.contrib.auth.decorators <span class="keyword">import</span> login_required
<span class="keyword">from</span> django.contrib <span class="keyword">import</span> messages
<span class="keyword">from</span> .models <span class="keyword">import</span> TeaProduct, Cart

<span class="keyword">def</span> <span class="function">tea_list</span>(request):
    teas = TeaProduct.objects.filter(is_available=<span class="keyword">True</span>)
    <span class="keyword">return</span> render(request, <span class="string">'products/tea_list.html'</span>, {<span class="string">'teas'</span>: teas})

<span class="keyword">def</span> <span class="function">about</span>(request):
    <span class="keyword">return</span> render(request, <span class="string">'products/about.html'</span>)

<span class="keyword">def</span> <span class="function">contacts</span>(request):
    <span class="keyword">return</span> render(request, <span class="string">'products/contacts.html'</span>)

<span class="keyword">def</span> <span class="function">register</span>(request):
    <span class="keyword">if</span> request.method == <span class="string">'POST'</span>:
        form = UserCreationForm(request.POST)
        <span class="keyword">if</span> form.is_valid():
            user = form.save()
            login(request, user)
            <span class="keyword">return</span> redirect(<span class="string">'tea_list'</span>)
    <span class="keyword">else</span>:
        form = UserCreationForm()
    <span class="keyword">return</span> render(request, <span class="string">'products/register.html'</span>, {<span class="string">'form'</span>: form})

<span class="keyword">@login_required</span>
<span class="keyword">def</span> <span class="function">profile</span>(request):
    <span class="keyword">return</span> render(request, <span class="string">'products/profile.html'</span>)

<span class="keyword">def</span> <span class="function">add_to_cart</span>(request, product_id):
    <span class="keyword">if not</span> request.user.is_authenticated:
        messages.error(request, <span class="string">'Нужно войти в аккаунт чтобы добавить в корзину!'</span>)
        <span class="keyword">return</span> redirect(<span class="string">'login'</span>)
    
    product = get_object_or_404(TeaProduct, id=product_id)
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={<span class="string">'quantity'</span>: <span class="number">1</span>}
    )
    
    <span class="keyword">if not</span> created:
        cart_item.quantity += <span class="number">1</span>
        cart_item.save()
        messages.success(request, f<span class="string">'Добавлен ещё один "{product.name}" в корзину!'</span>)
    <span class="keyword">else</span>:
        messages.success(request, f<span class="string">'"{product.name}" добавлен в корзину! 💖'</span>)
    
    <span class="keyword">return</span> redirect(<span class="string">'tea_list'</span>)

<span class="keyword">def</span> <span class="function">cart_view</span>(request):
    <span class="keyword">if not</span> request.user.is_authenticated:
        messages.error(request, <span class="string">'Войдите в аккаунт чтобы посмотреть корзину'</span>)
        <span class="keyword">return</span> redirect(<span class="string">'login'</span>)
    
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.total_price() <span class="keyword">for</span> item <span class="keyword">in</span> cart_items)
    
    <span class="keyword">return</span> render(request, <span class="string">'products/cart.html'</span>, {
        <span class="string">'cart_items'</span>: cart_items,
        <span class="string">'total'</span>: total
    })

<span class="keyword">def</span> <span class="function">remove_from_cart</span>(request, item_id):
    <span class="keyword">if not</span> request.user.is_authenticated:
        <span class="keyword">return</span> redirect(<span class="string">'login'</span>)
    
    cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f<span class="string">'"{product_name}" удалён из корзины'</span>)
    <span class="keyword">return</span> redirect(<span class="string">'cart_view'</span>)

<span class="keyword">def</span> <span class="function">update_cart</span>(request, item_id):
    <span class="keyword">if not</span> request.user.is_authenticated:
        <span class="keyword">return</span> redirect(<span class="string">'login'</span>)
    
    cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
    new_quantity = request.POST.get(<span class="string">'quantity'</span>)
    
    <span class="keyword">if</span> new_quantity <span class="keyword">and</span> new_quantity.isdigit():
        cart_item.quantity = int(new_quantity)
        <span class="keyword">if</span> cart_item.quantity > <span class="number">0</span>:
            cart_item.save()
            messages.success(request, <span class="string">'Количество обновлено!'</span>)
        <span class="keyword">else</span>:
            cart_item.delete()
            messages.success(request, <span class="string">'Товар удалён из корзины'</span>)
    
    <span class="keyword">return</span> redirect(<span class="string">'cart_view'</span>)</code></pre>
            </div>
        </div>

        <!-- ==================== style.css ==================== -->
        <div class="file-section" id="style-css">
            <div class="file-header">
                <h2>🎨 style.css</h2>
                <span class="file-type">CSS Stylesheet</span>
            </div>
            <div class="code-container">
                <pre><code><span class="comment">/* Основные стили */</span>
body {
    font-family: <span class="string">'Arial'</span>, sans-serif;
    background: linear-gradient(135deg, #fff5f5 0%, #ffe6ea 100%);
    color: #555;
    margin: 0;
    padding: 0;
    min-height: 100vh;
}

<span class="comment">/* Контейнеры */</span>
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

<span class="comment">/* Навбар */</span>
.nav {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    padding: 15px 30px;
    border-radius: 20px;
    margin-bottom: 30px;
    box-shadow: 0 4px 20px rgba(233, 30, 99, 0.1);
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.nav-logo {
    display: flex;
    align-items: center;
    gap: 15px;
    text-decoration: none;
    color: #e91e63;
    font-weight: bold;
    font-size: 24px;
}

.logo-icon {
    font-size: 32px;
    animation: bounce 2s infinite;
}

@keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-5px); }
}

.nav-links {
    display: flex;
    align-items: center;
    gap: 20px;
}

<span class="comment">/* Кнопки */</span>
.btn {
    background: linear-gradient(135deg, #e91e63 0%, #ad1457 100%);
    color: white;
    padding: 12px 25px;
    border: none;
    border-radius: 25px;
    text-decoration: none;
    display: inline-block;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(233, 30, 99, 0.3);
    position: relative;
    overflow: hidden;
}

.btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(233, 30, 99, 0.4);
}

.btn:active {
    transform: translateY(0);
}

.btn::before {
    content: <span class="string">''</span>;
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, 
              rgba(255,255,255,0.3), transparent);
    transition: left 0.5s;
}

.btn:hover::before {
    left: 100%;
}

.btn-cart {
    background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
}

.btn-login {
    background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
}

.btn-register {
    background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%);
}

.btn-remove {
    background: linear-gradient(135deg, #ff4444 0%, #cc0000 100%);
    padding: 8px 15px;
    font-size: 14px;
}

<span class="comment">/* Карточки */</span>
.tea-card {
    background: white;
    border-radius: 20px;
    padding: 25px;
    margin: 15px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    text-align: center;
    width: 280px;
    display: inline-block;
    vertical-align: top;
    transition: all 0.3s ease;
    border: 2px solid transparent;
}

.tea-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 35px rgba(233, 30, 99, 0.15);
    border-color: #ffb6c1;
}

.tea-image {
    width: 100%;
    height: 200px;
    border-radius: 15px;
    object-fit: cover;
    margin-bottom: 15px;
}

<span class="comment">/* Баннеры */</span>
.welcome-banner {
    background: linear-gradient(135deg, #ffe6ea 0%, #ffcdd2 100%);
    padding: 25px;
    border-radius: 20px;
    text-align: center;
    margin: 25px 0;
    border: 2px dashed #e91e63;
}

<span class="comment">/* Формы */</span>
.form-input {
    width: 100%;
    padding: 12px 20px;
    margin: 10px 0;
    border: 2px solid #ffb6c1;
    border-radius: 25px;
    background: white;
    font-size: 16px;
    transition: all 0.3s ease;
}

.form-input:focus {
    outline: none;
    border-color: #e91e63;
    box-shadow: 0 0 0 3px rgba(233, 30, 99, 0.1);
}

<span class="comment">/* Анимации */</span>
@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
}

.floating {
    animation: float 3s ease-in-out infinite;
}

<span class="comment">/* Специальные элементы */</span>
.heart {
    color: #e91e63;
    animation: heartbeat 1.5s ease-in-out infinite;
}

@keyframes heartbeat {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.1); }
}

<span class="comment">/* Адаптивность */</span>
@media (max-width: 768px) {
    .nav {
        flex-direction: column;
        gap: 15px;
    }
    
    .nav-links {
        flex-wrap: wrap;
        justify-content: center;
    }
    
    .tea-card {
        width: 100%;
        margin: 10px 0;
    }
}</code></pre>
            </div>
        </div>

        <!-- ==================== create_sample_data.py ==================== -->
        <div class="file-section" id="create-sample-py">
            <div class="file-header">
                <h2>🐍 create_sample_data.py</h2>
                <span class="file-type">Python (Data Script)</span>
            </div>
            <div class="code-container">
                <pre><code><span class="keyword">import</span> os
<span class="keyword">import</span> django

os.environ.setdefault(<span class="string">'DJANGO_SETTINGS_MODULE'</span>, <span class="string">'tea_shop.settings'</span>)
django.setup()

<span class="keyword">from</span> products.models <span class="keyword">import</span> Category, TeaProduct
<span class="keyword">from</span> django.contrib.auth.models <span class="keyword">import</span> User

<span class="comment"># Создаем категории</span>
categories_data = [
    {<span class="string">'name'</span>: <span class="string">'Зеленые чаи'</span>, 
     <span class="string">'description'</span>: <span class="string">'Нежные и освежающие зеленые чаи'</span>},
    {<span class="string">'name'</span>: <span class="string">'Цветочные чаи'</span>, 
     <span class="string">'description'</span>: <span class="string">'Чай с лепестками цветов и бутонами'</span>},
    {<span class="string">'name'</span>: <span class="string">'Фруктовые чаи'</span>, 
     <span class="string">'description'</span>: <span class="string">'Яркие и сладкие фруктовые смеси'</span>},
    {<span class="string">'name'</span>: <span class="string">'Травяные сборы'</span>, 
     <span class="string">'description'</span>: <span class="string">'Уютные и полезные травяные чаи'</span>},
]

<span class="keyword">for</span> cat_data <span class="keyword">in</span> categories_data:
    Category.objects.get_or_create(**cat_data)

<span class="comment"># Создаем чаи</span>
teas_data = [
    {
        <span class="string">'name'</span>: <span class="string">'Жасминовый сон'</span>,
        <span class="string">'description'</span>: <span class="string">'Нежный зеленый чай с лепестками жасмина'</span>,
        <span class="string">'price'</span>: <span class="number">450</span>,
        <span class="string">'category'</span>: Category.objects.get(name=<span class="string">'Зеленые чаи'</span>),
        <span class="string">'ingredients'</span>: <span class="string">'Зеленый чай, лепестки жасмина'</span>,
        <span class="string">'weight'</span>: <span class="number">100</span>,
        <span class="string">'brewing_time'</span>: <span class="number">3</span>
    },
    {
        <span class="string">'name'</span>: <span class="string">'Клубничная фея'</span>,
        <span class="string">'description'</span>: <span class="string">'Сладкий фруктовый чай с кусочками клубники'</span>,
        <span class="string">'price'</span>: <span class="number">380</span>,
        <span class="string">'category'</span>: Category.objects.get(name=<span class="string">'Фруктовые чаи'</span>),
        <span class="string">'ingredients'</span>: <span class="string">'Гибискус, клубника, яблоко, шиповник'</span>,
        <span class="string">'weight'</span>: <span class="number">100</span>,
        <span class="string">'brewing_time'</span>: <span class="number">5</span>
    },
    {
        <span class="string">'name'</span>: <span class="string">'Розовое облако'</span>,
        <span class="string">'description'</span>: <span class="string">'Ароматный чай с бутонами роз и ванилью'</span>,
        <span class="string">'price'</span>: <span class="number">520</span>,
        <span class="string">'category'</span>: Category.objects.get(name=<span class="string">'Цветочные чаи'</span>),
        <span class="string">'ingredients'</span>: <span class="string">'Черный чай, бутоны роз, ваниль'</span>,
        <span class="string">'weight'</span>: <span class="number">100</span>,
        <span class="string">'brewing_time'</span>: <span class="number">4</span>
    },
    {
        <span class="string">'name'</span>: <span class="string">'Вечерний уют'</span>,
        <span class="string">'description'</span>: <span class="string">'Успокаивающий травяной сбор с мятой и ромашкой'</span>,
        <span class="string">'price'</span>: <span class="number">290</span>,
        <span class="string">'category'</span>: Category.objects.get(name=<span class="string">'Травяные сборы'</span>),
        <span class="string">'ingredients'</span>: <span class="string">'Мята, ромашка, мелисса, липа'</span>,
        <span class="string">'weight'</span>: <span class="number">100</span>,
        <span class="string">'brewing_time'</span>: <span class="number">7</span>
    }
]

<span class="keyword">for</span> tea_data <span class="keyword">in</span> teas_data:
    TeaProduct.objects.get_or_create(**tea_data)

print(<span class="string">"Данные успешно созданы!"</span>)</code></pre>
            </div>
        </div>

        <!-- Footer -->
        <div class="footer">
            <p>🍵 <strong>Tea Shop Project</strong> — Документация проекта Django</p>
            <p>© 2025 Все права защищены</p>
            <p style="margin-top: 15px;">
                <em>Для копирования кода используйте кнопку над каждым файлом</em>
            </p>
        </div>
    </div>

    <script>
        // Функция копирования кода
        document.querySelectorAll('.copy-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const codeBlock = this.parentElement.nextElementSibling.querySelector('code');
                const text = codeBlock.innerText;
                
                navigator.clipboard.writeText(text).then(() => {
                    const originalText = this.innerText;
                    this.innerText = '✓ Скопировано!';
                    this.style.background = '#4CAF50';
                    
                    setTimeout(() => {
                        this.innerText = originalText;
                        this.style.background = '#e91e63';
                    }, 2000);
                });
            });
        });

        // Плавная прокрутка к якорям
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    </script>
</body>
</html>