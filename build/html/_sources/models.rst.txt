Создание моделей базы данных
============================

В этом разделе мы создадим модели для нашего приложения и разберем поля. Разберем на примере простой модели Book

.. note::

   Расширение для VSCode "Django" сильно упрощает работу с бд и не только. Благодаря ему можно использовать встроенные конструкции и уже в них вносить корректировки

Модель пользователя
^^^^^^^^^^^
Первым делом нужно обозначить модель, указав ее название. Также нужно помнить, что модели и поля бд находятся в моделе "models". Поэтому обращение к ним происходит через models. Создаем кастомную модель пользователя, которая расширяет стандартную модель Django.

.. code-block:: python

   # Обязательной импорт
   from django.contrib.auth.models import AbstractUser 
   from django.db import models
   from django.utils.translation import gettext_lazy as _

   class CustomUser(AbstractUser):
   # Дополнительные поля к стандартной модели User
   phone = models.CharField(max_length=15, blank=True, verbose_name='Телефон')
   avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Аватар')
   birth_date = models.DateField(blank=True, null=True, verbose_name='Дата рождения')

   class Meta:
       verbose_name = 'Пользователь'
       verbose_name_plural = 'Пользователи'
       
   def __str__(self):
       return self.username

.. note::

Не забывайте, что стандартные username, email и password уже указаны для модели User и их без крайней необходимости переопределять не нужно

Также для переопределения модели User нужно указать этот факт в settings.py вот такой строкой кода:

.. code-block:: python

   AUTH_USER_MODEL = 'main.CustomUser'

Строковые поля
^^^^^^^^^^^^^^

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
^^^^^^^^^^^^^

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
^^^^^^^^^^^

BooleanField
~~~~~~~~~~~~

Поле для хранения True/False значений.

**Пример:**

.. code-block:: python

   is_active = models.BooleanField(default=True)
   is_published = models.BooleanField(default=False)

Дата и время
^^^^^^^^^^^

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
^^^^^^^^^^^

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

.. note::

   Значение поля upload_to указывается относительно MEDIA_ROOT, который должен быть указан в settings

Специальные поля
^^^^^^^^^^^

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
^^^^^^^^^^^

ForeignKey
~~~~~~~~~~

Поле для связи "один-ко-многим" с другой моделью.

**Параметры:**
- ``to`` - модель для связи
- ``on_delete`` - поведение при удалении связанного объекта
- ``related_name`` - имя для обратной связи

**Один пользователь может создать несколько заявок:**

.. code-block:: python

   class CustomUser(models.Model):
   username = models.CharField(max_length=100)
   email = models.EmailField()

   class Application(models.Model):
   title = models.CharField(max_length=200)
   description = models.TextField()
   user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='applications')

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
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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
        ('new', 'Новая'),
        ('in_progress', 'В работе'),
        ('completed', 'Завершена'),
        ('rejected', 'Отклонена'),
    ]

    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='new',
        verbose_name='Статус'
    )

Класс Meta и __str__
^^^^^^^^^^^^^^^^^^^^

Класс Meta
~~~~~~~~~~

Класс Meta внутри модели - это способ задать "мета-информацию" о модели, которая не относится к отдельным полям, а описывает модель в целом

**Пример на пользователе:**

.. code-block:: python

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
      

__str__
~~~~~~~~~~

Метод __str__ определяет строковое представление объекта. Это то, что ты видишь когда объект выводится в консоли, админке, формах и т.д. Без __str__ в админке будут отображаться объекты как "Book object (1)", что не информативно.

**Пример на пользователе:**

.. code-block:: python

    def __str__(self):
        return self.username

После редактирования базы данных нужно создать и применить миграции:

.. code-block:: batch

   # Создание миграций
   python manage.py makemigrations

   # Применение миграций
   python manage.py migrate

.. note::

   Перед использованием миграций обязательно делать коммит, потому что миграция может сломать базу данных так, что ее нельзя будет восстановить

.. note::

   Чтобы управлять данными из БД, можно добавить модель в admin.py с помощью следующего кода:

   .. code-block:: django
      
      # Пример использования модели Book
      from django.contrib import admin
      from .models import Application

      admin.site.register(Application)

После настройки БД можно перейти к :doc:`templates` чтобы создать html-шаблоны для страниц.