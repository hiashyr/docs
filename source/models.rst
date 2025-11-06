Создание моделей базы данных
============================

В этом разделе мы создадим модели для нашего приложения и разберем поля. Разберем на примере простой модели Book

.. note::

   Расширение для VSCode "Django" сильно упрощает работу с бд. Благодаря ему можно использовать встроенные конструкции и уже в них вносить корректировки

Модель Book
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Первым делом нужно обозначить модель, указав ее название. Также нужно помнить, что модели и поля бд находятся в моделе "models". Поэтому обращение к ним происходит через models.

.. code-block:: python

   class Book (models.Model):

Дальше нужно обозначить поля БД. Они различаются по типам данных, которые хранят.

Строковые поля
--------------

CharField
~~~~~~~~~

Поле для хранения строк фиксированной или переменной длины.

**Параметры:**
- ``max_length`` (обязательный) - максимальная длина строки
- ``blank`` - разрешить пустые значения в формах
- ``null`` - разрешить NULL в базе данных

**Пример:**

.. code-block:: python

   name = models.CharField(max_length=100)
   title = models.CharField(max_length=200, blank=True)

TextField
~~~~~~~~~

Поле для хранения больших текстов.

**Параметры:**
- ``blank`` - разрешить пустые значения
- ``null`` - разрешить NULL

**Пример:**

.. code-block:: python

   description = models.TextField()
   content = models.TextField(blank=True)

Числовые поля
-------------

IntegerField
~~~~~~~~~~~~

Поле для хранения целых чисел.

**Параметры:**
- ``blank`` - разрешить пустые значения
- ``null`` - разрешить NULL
- ``default`` - значение по умолчанию

**Пример:**

.. code-block:: python

   age = models.IntegerField()
   quantity = models.IntegerField(default=0)

DecimalField
~~~~~~~~~~~~

Поле для хранения десятичных чисел с фиксированной точностью. Отлично подходит для обозначения цены.

**Параметры:**
- ``max_digits`` - максимальное количество цифр
- ``decimal_places`` - количество знаков после запятой
- ``default`` - значение по умолчанию

**Пример:**

.. code-block:: python

   price = models.DecimalField(max_digits=10, decimal_places=2)
   rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)

FloatField
~~~~~~~~~~

Поле для хранения чисел с плавающей точкой.

**Пример:**

.. code-block:: python

   temperature = models.FloatField()
   percentage = models.FloatField(default=0.0)

Булевы поля
-----------

BooleanField
~~~~~~~~~~~~

Поле для хранения True/False значений.

**Пример:**

.. code-block:: python

   is_active = models.BooleanField(default=True)
   is_published = models.BooleanField(default=False)

Дата и время
------------

DateTimeField
~~~~~~~~~~~~~

Поле для хранения даты и времени.

**Параметры:**
- ``auto_now`` - автоматически устанавливать при сохранении
- ``auto_now_add`` - автоматически устанавливать при создании

**Пример:**

.. code-block:: python

   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)

DateField
~~~~~~~~~

Поле для хранения только даты (без времени).

**Пример:**

.. code-block:: python

   birth_date = models.DateField()
   event_date = models.DateField(auto_now_add=True)

TimeField
~~~~~~~~~

Поле для хранения только времени (без даты).

**Пример:**

.. code-block:: python

   start_time = models.TimeField()
   end_time = models.TimeField()

Файловые поля
-------------

ImageField
~~~~~~~~~~

Поле для загрузки изображений (требует Pillow).

**Параметры:**
- ``upload_to`` - путь для сохранения изображений
- ``height_field`` - поле для автоматического сохранения высоты
- ``width_field`` - поле для автоматического сохранения ширины

**Пример:**

.. code-block:: python

   avatar = models.ImageField(upload_to='uploads/')
   photo = models.ImageField(
       upload_to='uploads/',
       height_field='image_height',
       width_field='image_width'
   )

Специальные поля
----------------

EmailField
~~~~~~~~~~

Поле для email адресов с автоматической валидацией.

**Пример:**

.. code-block:: python

   email = models.EmailField(max_length=254)

URLField
~~~~~~~~

Поле для URL адресов с автоматической валидацией.

**Пример:**

.. code-block:: python

   website = models.URLField(max_length=200)
   profile_url = models.URLField(max_length=200, blank=True)

Связи между моделями
--------------------

ForeignKey
~~~~~~~~~~

Поле для связи "один-ко-многим" с другой моделью.

**Параметры:**
- ``to`` - модель для связи
- ``on_delete`` - поведение при удалении связанного объекта
- ``related_name`` - имя для обратной связи

**У одного автора может быть написано несколько книг:**

.. code-block:: python

   class Author(models.Model):
      name = models.CharField(max_length=100)

   class Book(models.Model):
      title = models.CharField(max_length=100)
      author = models.ForeignKey(Author, on_delete=models.CASCADE)

ManyToManyField
~~~~~~~~~~~~~~~

Поле для связи "многие-ко-многим" с другой моделью.

**Параметры:**
- ``through`` - промежуточная модель для дополнительных полей

**Книга может иметь несколько авторов, и автор может написать несколько книг:**

.. code-block:: python

   class Book(models.Model):
      title = models.CharField(max_length=100)
      authors = models.ManyToManyField('Author')

   class Author(models.Model):
      name = models.CharField(max_length=100)

OneToOneField
~~~~~~~~~~~~~

Поле для связи "один-к-одному" с другой моделью.

**Один пользователь → один профиль:**

.. code-block:: python

   class User(models.Model):
      username = models.CharField(max_length=100)

   class Profile(models.Model):
      user = models.OneToOneField(User, on_delete=models.CASCADE)
      bio = models.TextField()

Общие параметры для всех полей
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``verbose_name`` - человеко-читаемое имя поля
- ``help_text`` - текст подсказки для форм
- ``choices`` - ограничение возможных значений
- ``default`` - значение по умолчанию
- ``unique`` - требование уникальности значений
- ``blank`` - разрешение пустых значений в формах
- ``null`` - разрешение NULL в базе данных

**Пример с общими параметрами:**

.. code-block:: python

   STATUS_CHOICES = [
       ('draft', 'Черновик'),
       ('published', 'Опубликовано'),
       ('archived', 'В архиве'),
   ]

   status = models.CharField(
       max_length=20,
       choices=STATUS_CHOICES,
       default='draft',
       verbose_name='Статус',
       help_text='Статус записи'
   )

Класс Meta и __str__
--------------------

Класс Meta
~~~~~~~~~~

Класс Meta внутри модели - это способ задать "мета-информацию" о модели, которая не относится к отдельным полям, а описывает модель в целом

**Пример на книге:**

.. code-block:: python

   class Book(models.Model):
      title = models.CharField(max_length=100)
      author = models.CharField(max_length=100)
      price = models.DecimalField(max_digits=6, decimal_places=2)
      
      class Meta:
         # Имя таблицы в БД (по умолчанию: appname_modelname)
         db_table = 'books'
         
         # Человеко-читаемые имена
         verbose_name = 'Книга'
         verbose_name_plural = 'Книги'
         
         # Сортировка по умолчанию
         ordering = ['title', '-price']  # по названию (возр.), затем по цене (убыв.)
         
         # Права доступа
         permissions = [
               ('can_mark_returned', 'Set book as returned'),
         ]
         
         # Ограничения уникальности
         unique_together = ['title', 'author']
         
         # Индексы для оптимизации
         indexes = [
               models.Index(fields=['title']),
               models.Index(fields=['author', 'price']),
         ]
      

__str__
~~~~~~~~~~

Метод __str__ определяет строковое представление объекта. Это то, что ты видишь когда объект выводится в консоли, админке, формах и т.д. Без __str__ в админке будут отображаться объекты как "Book object (1)", что не информативно.

**Пример на книге:**

.. code-block:: python

   # Плохо - без __str__
   class Book(models.Model):
      title = models.CharField(max_length=100)
      
   # В админке: "Book object (1)"

   # Хорошо - с __str__
   class Book(models.Model):
      title = models.CharField(max_length=100)
      
      def __str__(self):
         return self.title

   # В админке: "Война и мир"

После редактирования базы данных нужно создать и применить миграции:

.. code-block:: batch

   # Создание миграций
   python manage.py makemigrations

   # Применение миграций
   python manage.py migrate

.. note::

   Перед использованием миграций обязательно делать коммит, потому что миграция может сломать базу данных так, что ее нельзя будет восстановить