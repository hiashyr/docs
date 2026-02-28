Создание HTML шаблонов
=======================

В этом разделе разберемся как настроить html-шаблоны, использовать static и ссылки.

Первым делом создаем файл, от которого мы будем наследовать элементы страницы. Обычно он называется base.html. Создаем в директории templates.

Базовая html-структура
----------------------

Для начала работы с html файлом нужно задать его структуру. Для этого в html файлах нужно в первой строке написать "!" и нажать клавишу "tab".
Получится готовая струтура html с head и body:

.. code-block:: html

    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document</title>
    </head>
    <body>

    </body>
    </html>

Следующим шагом нам нужно заполнить страницу данными, которые мы хотим увидеть на каждой странице проекта. Обычно это импорт css-стилей, js-кода и навигация.

Импорт css и js
---------------

Таким образом нам нужно подключить Bootstrap css и js. Импорт css указываем в head, а script в конец body:

.. code-block:: html

    <link href="путь к css-файлу" rel="stylesheet">

    <script src="путь к js-файлу"></script>

Если же мы хотим использовать собственные стили, то лучшим решением будет создать файл styles.css в ранее созданной директории static. Импорт из такой директории осуществляется через следующую запись:

.. code-block:: django

    href="{% static "путь к файлу относительно папки static" %}"

    #Пример подключения styles.css из папки static
    <link href="{% static "styles.css" %}" rel="stylesheet">

Статика
-------

Не забываем про загрузку статических файлов на странице, где мы их используем (Пишется в начале файла):

.. code-block:: django

    {% load static %}

После подключения стилей и js нужно написать блоки для базовой страницы.

.. note::

    Все блоки можно найти в документации Bootstrap 5. Она уже загружена в Zeal.

Таким образом взяв стандартную панель навигации, добавляем ее в наш base.html. Получилось это таким образом:

.. code-block:: django

    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">Navbar</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                <li class="nav-item">
                <a class="nav-link active" aria-current="page" href="{% url "home" %}">Home</a>
                </li>
                <li class="nav-item">
                <a class="nav-link" href="{% url "about" %}">About</a>
                </li>
            </ul>
            </div>
        </div>
    </nav>

Указание ссылок
---------------

После вставки панели навигации возникает вопрос о вставке ссылок на страницы. Подробно о ссылках рассказывается здесь: :doc:`urls`.

Если говорить в кратце, то для передачи ссылки на страницу необходимо наличие ссылки на эту страницу в urls.py. Для каждой url в этом файле можно установить параметр name. По нему мы и будем указывать url:

.. code-block:: django

    # Использование в urls.py
    path('', views.index, name='home'),
    path('about', views.about, name='about')

.. code-block:: django

    # Использование в html
    <a class="nav-link active" aria-current="page" href="{% url "home" %}">Home</a>
    <a class="nav-link" href="{% url "about" %}">About</a>

Блок контента
---------------

Если мы хотим использовать базовый шаблон для других страниц и на этих страницах вносить дополнительную информацию, то необходимо обозначить место для дополнения в шаблоне следующим образом:

.. code-block:: django

    {% block content %}
    
    {% endblock content %}

Таким образом мы показываем, что в этом месте будет блок контента, написанный на других страницах.

Наследование
------------

После того как мы закончили работу над базовым шаблоном, нужно указать для страниц наследование от этого шаблона. Для этого в начале html-файла нужно указать:

.. code-block:: django

    {% extends 'base.html' %}

    # В таком случае статика пишется следующей строкой
    {% load static %}

Теперь нам нужно указать, что мы используем блок контента, который указали ранее в базовом шаблоне, поэтому содержимое страницы должно начинаться с ``{% block content %}`` и заканчиваться ``{% endblock content %}``.

Итог
----

Таким образом у нас получается шаблон, в котором прописаны импорты и элементы, которые можно использовать на всех страницах, а также в базовом шаблоне указан блок контента, который используется для наследования от базового шаблона. Выглядить это должно следующим образом:

.. code-block:: html:

    #base.html:

    {% load static %}
    <!DOCTYPE html>
    ...
    <head>
    ...
    </head>

    <body>
    ...
        {% block content %}
    
        {% endblock content %}
    ...
    </body>
    </html>

.. code-block:: html:

    #index.html:

    {% extends 'base.html' %}
    {% load static %}
    {% block content %}
        ...
    {% endblock content %}

Использование данных из бд для передачи на фронт
------------------------------------------------

Рассмотрим простой пример, в котором мы создадим простую модель книги с двумя полями.

Таким образом у нас есть models:

.. code-block:: python

    from django.db import models

    class Book(models.Model):
        title = models.CharField("Название книги", max_length=100)
        author = models.CharField("Автор", max_length=100)
        
        def __str__(self):
            return self.title

Через view мы возьмем записи записи всех книг:

.. code-block:: python

    from django.shortcuts import render
    from .models import Book  # импортируем модель

    def index(request):
        # Получаем ВСЕ книги из базы данных
        books = Book.objects.all()
        
        # Передаем книги в шаблон
        return render(request, 'index.html', {'books': books})

Теперь в шаблонах через цикл for мы передаем данные из бд:

.. code-block:: django

    {% for book in books %}
        <div>
            <h3>{{ book.title }}</h3>
            <p>Автор: {{ book.author }}</p>
        </div>
    {% endfor %}

То есть для переноса данных нужно задать во views переменную, которой будет обозначены данные на фронте и пройтись по этой переменной циклом for.

Если рассмотреть более реальный пример, то получится следующее:

Наша модель книги, для которой мы задаем статус:

.. code-block:: python

    from django.db import models

    class Book(models.Model):
        
        STATUS_CHOICES = [
            ('available', 'В наличии'),
            ('out_of_stock', 'Нет в наличии'),
            ('coming_soon', 'Скоро в продаже'),
        ]
        
        title = models.CharField("Название книги", max_length=100)
        author = models.CharField("Автор", max_length=100)
        price = models.DecimalField("Цена", max_digits=6, decimal_places=2)
        status = models.CharField(
            "Статус",
            max_length=20,
            choices=STATUS_CHOICES,
            default='available'
        )
        
        def __str__(self):
            return self.title

Получаем все книги через view:

.. code-block:: python

    from django.shortcuts import render
    from .models import Book

    def index(request):
        books = Book.objects.all()
        
        return render(request, 'index.html', {'books': books})

.. note::

   Учтите, что цикл for будет проходить по количеству элементов из БД, которое вы указали во views. То есть если вы указали три записи, то выведутся три. Если же вывели все, то выведутся все.

После настройки шаблонов можно перейти к :doc:`urls`, чтобы задать пути нашим страницам. Также можно перейти к шагу с :doc:`views`