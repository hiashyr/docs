Создание моделей базы данных
============================

В этом разделе мы создадим модели для нашего магазина цветов. У нас есть три приложения, и для каждого мы создадим соответствующие модели.

Настройка пользовательской модели
---------------------------------

Сначала настроим кастомную модель пользователя в приложении `user_auth`.

**user_auth/models.py:**

.. code-block:: python
   :linenos:

   from django.db import models
   from django.contrib.auth.models import AbstractUser
   from django.core.validators import RegexValidator


   class CustomUser(AbstractUser):
       """Расширенная модель пользователя"""
       name_validator = RegexValidator(
           regex=r'^[а-яА-ЯёЁ\s\-]+$',
           message='Разрешены только кириллица, пробел и тире'
       )
       login_validator = RegexValidator(
           regex=r'^[a-zA-Z0-9\-]+$',
           message='Разрешены только латиница, цифры и тире'
       )
       
       first_name = models.CharField(
           max_length=150, 
           validators=[name_validator],
           verbose_name='Имя'
       )
       last_name = models.CharField(
           max_length=150, 
           validators=[name_validator],
           verbose_name='Фамилия'
       )
       patronymic = models.CharField(
           max_length=150, 
           blank=True,
           validators=[name_validator],
           verbose_name='Отчество'
       )
       username = models.CharField(
           max_length=150,
           unique=True,
           validators=[login_validator],
           verbose_name='Логин'
       )
       email = models.EmailField(unique=True, verbose_name='Email')
       
       class Meta:
           verbose_name = 'Пользователь'
           verbose_name_plural = 'Пользователи'
       
       def get_full_name(self):
           """Полное имя пользователя"""
           full_name = f"{self.last_name} {self.first_name}"
           if self.patronymic:
               full_name += f" {self.patronymic}"
           return full_name.strip()
       
       def __str__(self):
           return self.get_full_name() or self.username

Обновление настроек для кастомной модели пользователя
-----------------------------------------------------

Теперь нужно указать Django использовать нашу кастомную модель пользователя. 
Откройте `flower_shop/settings.py` и добавьте:

.. code-block:: python
   :emphasize-lines: 1

   # flower_shop/settings.py

   AUTH_USER_MODEL = 'user_auth.CustomUser'

   INSTALLED_APPS = [
       # ...
       'user_auth',
       # ...
   ]

Модели для основного приложения (main)
--------------------------------------

Создадим модели для товаров, категорий и контента главной страницы.

**main/models.py:**

.. code-block:: python
   :linenos:

   from django.db import models
   from django.contrib.auth.models import User
   from django.core.validators import MinValueValidator, RegexValidator
   from django.core.exceptions import ValidationError


   class Category(models.Model):
       """Модель категории товаров"""
       name = models.CharField(
           max_length=100, 
           verbose_name='Название категории',
           validators=[RegexValidator(
               regex=r'^[а-яА-ЯёЁ0-9\s\-]+$',
               message='Название может содержать только кириллицу, цифры, пробелы и тире'
           )]
       )
       description = models.TextField(blank=True, verbose_name='Описание')
       created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
       
       class Meta:
           verbose_name = 'Категория'
           verbose_name_plural = 'Категории'
           ordering = ['name']
       
       def __str__(self):
           return self.name


   class Product(models.Model):
       """Модель товара"""
       name = models.CharField(
           max_length=200, 
           verbose_name='Название',
           validators=[RegexValidator(
               regex=r'^[а-яА-ЯёЁ0-9\s\-]+$',
               message='Название может содержать только кириллицу, цифры, пробелы и тире'
           )]
       )
       description = models.TextField(verbose_name='Описание')
       price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена', validators=[MinValueValidator(0)])
       image = models.ImageField(upload_to='products/', verbose_name='Изображение')
       category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
       country = models.CharField(max_length=100, verbose_name='Страна-производитель')
       year = models.IntegerField(verbose_name='Год выпуска', validators=[MinValueValidator(1900)])
       model = models.CharField(max_length=100, verbose_name='Модель')
       stock_quantity = models.PositiveIntegerField(default=0, verbose_name='Количество на складе')
       is_available = models.BooleanField(default=True, verbose_name='В наличии')
       created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
       updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
       
       def clean(self):
           """Валидация модели"""
           if self.price < 0:
               raise ValidationError({'price': 'Цена не может быть отрицательной'})
           if self.stock_quantity < 0:
               raise ValidationError({'stock_quantity': 'Количество на складе не может быть отрицательным'})
       
       def save(self, *args, **kwargs):
           """Автоматическое обновление статуса наличия"""
           # Обновляем статус наличия в зависимости от количества
           self.is_available = self.stock_quantity > 0
           super().save(*args, **kwargs)
       
       class Meta:
           verbose_name = 'Товар'
           verbose_name_plural = 'Товары'
           ordering = ['-created_at']
       
       def __str__(self):
           return self.name


   class SliderImage(models.Model):
       """Модель для слайдера на главной странице"""
       title = models.CharField(max_length=200, verbose_name='Заголовок')
       description = models.TextField(blank=True, verbose_name='Описание')
       image = models.ImageField(upload_to='slider/', verbose_name='Изображение')
       is_active = models.BooleanField(default=True, verbose_name='Активно')
       order = models.PositiveIntegerField(default=0, verbose_name='Порядок')
       
       class Meta:
           verbose_name = 'Слайд'
           verbose_name_plural = 'Слайды'
           ordering = ['order']
       
       def __str__(self):
           return self.title


   class Contact(models.Model):
       """Модель контактной информации"""
       address = models.CharField(max_length=300, verbose_name='Адрес')
       phone = models.CharField(max_length=20, verbose_name='Телефон')
       email = models.EmailField(verbose_name='Email')
       map_image = models.ImageField(upload_to='contacts/', blank=True, verbose_name='Карта')
       
       class Meta:
           verbose_name = 'Контакт'
           verbose_name_plural = 'Контакты'
       
       def __str__(self):
           return f"Контакты - {self.address}"

Модели для приложения заказов (orders)
--------------------------------------

Создадим модели для управления заказами и корзиной.

**orders/models.py:**

.. code-block:: python
   :linenos:

   from django.db import models
   from django.contrib.auth import get_user_model
   from django.db.models.signals import post_save
   from django.dispatch import receiver
   from main.models import Product

   User = get_user_model()


   class Order(models.Model):
       """Модель заказа"""
       STATUS_CHOICES = [
           ('new', 'Новый'),
           ('confirmed', 'Подтвержден'),
           ('cancelled', 'Отменен'),
       ]
       
       user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
       status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Статус')
       created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
       updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
       cancellation_reason = models.TextField(blank=True, verbose_name='Причина отмены')
       
       class Meta:
           verbose_name = 'Заказ'
           verbose_name_plural = 'Заказы'
           ordering = ['-created_at']
       
       def __str__(self):
           return f"Заказ #{self.id} - {self.user.get_full_name()}"
       
       @property
       def total_quantity(self):
           """Общее количество товаров в заказе"""
           return sum(item.quantity for item in self.orderitem_set.all())
       
       @property
       def total_price(self):
           """Общая стоимость заказа"""
           return sum(item.get_total_price() for item in self.orderitem_set.all())


   class OrderItem(models.Model):
       """Модель элемента заказа"""
       order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ')
       product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
       quantity = models.PositiveIntegerField(verbose_name='Количество')
       price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за единицу')
       
       class Meta:
           verbose_name = 'Элемент заказа'
           verbose_name_plural = 'Элементы заказа'
       
       def __str__(self):
           return f"{self.product.name} - {self.quantity} шт."
       
       def get_total_price(self):
           """Общая стоимость элемента заказа"""
           return self.quantity * self.price


   class Cart(models.Model):
       """Модель корзины"""
       user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
       product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
       quantity = models.PositiveIntegerField(verbose_name='Количество')
       created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
       updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
       
       class Meta:
           verbose_name = 'Корзина'
           verbose_name_plural = 'Корзины'
           unique_together = ['user', 'product']
       
       def __str__(self):
           return f"{self.user.username} - {self.product.name}"
       
       def get_total_price(self):
           """Общая стоимость элемента корзины"""
           return self.quantity * self.product.price


   @receiver(post_save, sender=Order)
   def update_stock_on_order_confirmation(sender, instance, created, **kwargs):
       """Уменьшает количество товаров на складе при подтверждении заказа"""
       if not created and instance.status == 'confirmed':
           # Проверяем, не был ли заказ уже подтвержден ранее
           if Order.objects.filter(id=instance.id, status='confirmed').exists():
               # Уменьшаем количество товаров на складе
               for item in instance.orderitem_set.all():
                   item.product.stock_quantity -= item.quantity
                   if item.product.stock_quantity < 0:
                       item.product.stock_quantity = 0
                   item.product.save()

Создание миграций
-----------------

После создания всех моделей нужно создать и применить миграции:

.. code-block:: batch

   # Создание миграций для всех приложений
   python manage.py makemigrations

   # Применение миграций
   python manage.py migrate

   # Если нужно создать миграции для конкретного приложения
   python manage.py makemigrations main
   python manage.py makemigrations orders
   python manage.py makemigrations user_auth

Особенности моделей
-------------------

**CustomUser:**
- Наследуется от AbstractUser
- Валидация имен кириллицей
- Валидация логина латиницей
- Уникальный email

**Product:**
- Автоматическая валидация цены и количества
- Автоматическое обновление статуса наличия
- Валидация названия кириллицей

**Order:**
- Сигнал для обновления склада при подтверждении заказа
- Вычисляемые свойства для общей стоимости и количества

**Cart:**
- Уникальная связь пользователь-товар
- Автоматический расчет стоимости

Следующий шаг
-------------

После создания моделей переходите к :doc:`views` чтобы создать представления для работы с нашими данными.

.. note::

   **Важно:** Не забудьте выполнить `makemigrations` и `migrate` после создания моделей!

.. warning::

   При изменении моделей после применения миграций нужно создавать новые миграции!