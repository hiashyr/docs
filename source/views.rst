Создание представлений (Views)
==============================

В этом разделе мы создадим представления для нашего проекта. Представления обрабатывают запросы пользователей и возвращают ответы с данными.

Базовое представление для страницы
----------------------------------

Рассмотрим представление ``about``, которое отвечает за простое отображение страницы. В комбинации данного представления, html-страницы и url на нее, получится отображение обычной  html-страницы.

Код представления
^^^^^^^^^^^^^^^^^

.. code-block:: python

   def about(request):
      return render(request, 'about.html')

Простой импорт данных из БД
---------------------------

Рассмотрим передачу данных из БД на примере книги:

.. code-block:: python

   from .models import Book

   def index(request):
      books = Book.objects.all()
      
      return render(request, 'index.html', {'books':books})

Здесь мы видим, что первым делом нужно произвести импорт модели из БД и задать переменную, в которую мы переносим все данные из БД. Следующим шагом мы отправляем в return кроме самого запроса и страницы еще данные из БД в виде переменной "books", которую мы можем использовать в html-страницах.

Фильтрация данных из БД
--------------------------

Если же мы хотим отфильтровать выборку данных, которую получаем, то нужно использовать срез. Выглядит это следующим образом на примере книги:

.. code-block:: python

   books = Book.objects.all()[:3]  # Первые 3 книги

Также есть и другие функции фильтрации:

Основные методы
~~~~~~~~~~~~~~~

.. code-block:: python

   # Все объекты
   books = Book.objects.all()                    # ВСЕ книги

   # Один объект
   book = Book.objects.get(id=1)                # Одна книга по ID
   book = Book.objects.get(title="Война и мир") # Одна книга по полю. (title - Поле БД) 

   # Фильтрация
   books = Book.objects.filter(genre="Роман")   # Книги жанра "Роман". (genre - Поле БД) 
   books = Book.objects.exclude(genre="Роман")  # Книги кроме жанра "Роман"

   # Первый/последний
   first_book = Book.objects.first()            # Первая книга
   last_book = Book.objects.last()              # Последняя книга


Агрегации и подсчеты
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Подсчет
   count = Book.objects.count()                 # Общее количество книг
   count = Book.objects.filter(price__lt=500).count()  # Количество дешевых книг

   # Существует ли?
   exists = Book.objects.filter(title="1984").exists()  # True/False

Поисковые операторы
^^^^^^^^^^^^^^^^^^^

В примере выше было использовано поле БД price и для него использовалась приписка __lt. Таким образом выглядят поисковые операторы в django. Вот их примеры в коде:

.. code-block:: python

   expensive_books = Book.objects.filter(price__gt=500) # Книги дороже 500 рублей
   cheap_books = Book.objects.filter(price__lte=300) # Книги дешевле или равны 300 рублей
   mid_price_books = Book.objects.filter(price__range=(200, 500)) # Книги от 200 до 500 рублей

   books = Book.objects.filter(title__contains="война") # Книги, где в названии есть "война"
   books = Book.objects.filter(title__istrartswith="преступление") # Книги, которые начинаются на "Преступление" (без учета регистра)
   books = Book.objects.filter(author__exact="Лев Толстой") # Полное совпадение автора

   from datetime import date

   today_books = Book.objects.filter(created_at__date=date.today()) # Книги добавленные сегодня
   books_24 = Book.objects.filter(created_at__year=2024) # Книги добавленные в 2024 году
   december_books = Book.objects.filter(created_at__month=12) # Книги добавленные в декабре