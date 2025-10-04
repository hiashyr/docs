Создание моделей базы данных
============================

В этом разделе мы создадим модели для нашего приложения. Начнем с кастомной модели пользователя, которая расширяет стандартную модель Django.

Модель CustomUser
-----------------

Модель ``CustomUser`` наследуется от ``AbstractUser`` и добавляет дополнительные поля для хранения расширенной информации о пользователях.

Наследование от AbstractUser
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   class CustomUser(AbstractUser):

Модель наследуется от ``AbstractUser`` - базового класса Django для пользователей. Это дает нам все стандартные поля (username, email, password, etc.) и методы, которые мы можем расширить.

Переопределение стандартных полей
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Поле first_name
~~~~~~~~~~~~~~~

.. code-block:: python

   first_name = models.CharField(
       _('first name'),
       max_length=150,
       null=True,
       blank=True
   )

**Назначение:** Хранит имя пользователя.

**Параметры:**
- ``_('first name')`` - переводимый ярлык для интернационализации
- ``max_length=150`` - максимальная длина 150 символов
- ``null=True`` - разрешает NULL значения в базе данных
- ``blank=True`` - поле может быть пустым в формах

Поле last_name
~~~~~~~~~~~~~~

.. code-block:: python

   last_name = models.CharField(
       _('last name'),
       max_length=150,
       null=True,
       blank=True
   )

**Назначение:** Хранит фамилию пользователя.

**Параметры:**
- Те же параметры, что и у ``first_name`` для согласованности
- Позволяет пользователям не указывать фамилию, если они не хотят

Дополнительные поля пользователя
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Поле phone
~~~~~~~~~~

.. code-block:: python

   phone = models.CharField(
       _('phone number'),
       max_length=20,
       blank=True,
       null=True
   )

**Назначение:** Хранит номер телефона пользователя.

**Параметры:**
- ``max_length=20`` - достаточно для международных номеров
- ``blank=True, null=True`` - поле необязательное
- Используется ``CharField`` так как номер телефона может содержать символы (+, -, пробелы)

Поле address
~~~~~~~~~~~~

.. code-block:: python

   address = models.TextField(
       _('address'),
       blank=True
   )

**Назначение:** Хранит полный адрес пользователя.

**Параметры:**
- ``TextField`` - подходит для длинного текста (адрес может быть многострочным)
- ``blank=True`` - поле необязательное для заполнения
- Не использует ``null=True`` так как TextField предпочитает пустые строки вместо NULL

Поле age
~~~~~~~~

.. code-block:: python

   age = models.IntegerField(
       _('age'),
       null=True,
       blank=True
   )

**Назначение:** Хранит возраст пользователя в годах.

**Параметры:**
- ``IntegerField`` - для целочисленных значений
- ``null=True, blank=True`` - возраст может быть не указан
- Может вычисляться автоматически из ``birth_date``

Поле birth_date
~~~~~~~~~~~~~~~

.. code-block:: python

   birth_date = models.DateField(
       _('birth date'),
       null=True,
       blank=True
   )

**Назначение:** Хранит дату рождения пользователя.

**Параметры:**
- ``DateField`` - специализированное поле для дат
- ``null=True, blank=True`` - необязательное поле
- Позволяет точно хранить дату рождения для различных вычислений

Поле gender
~~~~~~~~~~~

.. code-block:: python

   GENDER_CHOICES = [
       ('male', _('Male')),
       ('female', _('Female')),
       ('other', _('Other')),
   ]
   gender = models.CharField(
       _('gender'),
       max_length=10,
       choices=GENDER_CHOICES,
       blank=True
   )

**Назначение:** Хранит пол пользователя с предопределенными вариантами.

**Параметры:**
- ``choices=GENDER_CHOICES`` - ограничивает ввод предопределенными значениями
- ``max_length=10`` - достаточно для самых длинных вариантов
- ``blank=True`` - пользователь может не указывать пол
- Переводимые варианты для интернационализации

Поле city
~~~~~~~~~

.. code-block:: python

   city = models.CharField(
       _('city'),
       max_length=100,
       blank=True
   )

**Назначение:** Хранит город проживания пользователя.

**Параметры:**
- ``max_length=100`` - достаточно для большинства названий городов
- ``blank=True`` - необязательное поле

Поле country
~~~~~~~~~~~~

.. code-block:: python

   country = models.CharField(
       _('country'),
       max_length=100,
       blank=True
   )

**Назначение:** Хранит страну проживания пользователя.

**Параметры:**
- Аналогично полю ``city``
- Может быть связано со справочником стран в будущем

Поле occupation
~~~~~~~~~~~~~~~

.. code-block:: python

   occupation = models.CharField(
       _('occupation'),
       max_length=100,
       blank=True
   )

**Назначение:** Хранит профессию или род занятий пользователя.

**Параметры:**
- ``max_length=100`` - достаточно для большинства профессий
- ``blank=True`` - необязательное поле

Поле avatar
~~~~~~~~~~~

.. code-block:: python

   avatar = models.ImageField(
       _('avatar'),
       upload_to='avatars/',
       blank=True,
       null=True
   )

**Назначение:** Хранит аватар (изображение профиля) пользователя.

**Параметры:**
- ``ImageField`` - специализированное поле для изображений
- ``upload_to='avatars/'`` - файлы сохраняются в папку avatars/
- ``blank=True, null=True`` - аватар не обязателен
- Требует установки Pillow для работы с изображениями

Настройки модели Meta
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   class Meta:
       verbose_name = _('user')
       verbose_name_plural = _('users')

**Назначение:** Класс Meta содержит метаданные модели.

**Параметры:**
- ``verbose_name`` - человекочитаемое имя в единственном числе
- ``verbose_name_plural`` - человекочитаемое имя во множественном числе
- Оба параметра используют переводимые строки для интернационализации

Методы модели
^^^^^^^^^^^^^

Метод get_full_name
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def get_full_name(self):
       """Возвращает полное имя пользователя."""
       return f'{self.first_name} {self.last_name}'

**Назначение:** Возвращает полное имя пользователя в формате "Имя Фамилия".

**Особенности:**
- Использует f-строки для форматирования
- Возвращает строку с объединением имени и фамилии
- Переопределяет стандартный метод Django

Метод __str__
~~~~~~~~~~~~~

.. code-block:: python

   def __str__(self):
       full_name = self.get_full_name()
       if full_name.strip():
           return full_name
       return self.username

**Назначение:** Определяет строковое представление объекта.

**Логика:**
- Сначала пытается вернуть полное имя
- Если полное имя пустое (состоит только из пробелов), возвращает username
- Гарантирует, что всегда будет непустое строковое представление

Настройка в settings.py
^^^^^^^^^^^^^^^^^^^^^^^

Чтобы Django использовал нашу кастомную модель, нужно добавить в ``settings.py``:

.. code-block:: python

   AUTH_USER_MODEL = 'user_auth.CustomUser'

Эта настройка указывает Django использовать нашу модель вместо стандартной User.

Модель Category
---------------

Модель ``Category`` представляет категории товаров в нашем приложении.

Создание модели
^^^^^^^^^^^^^^^

.. code-block:: python

   class Category(models.Model):

Базовый класс для создания модели базы данных. Каждая категория будет отдельной записью в таблице.

Поле name
^^^^^^^^^

.. code-block:: python

   name = models.CharField(_('name'), max_length=100, blank=True, null=True)

**Назначение:** Хранит название категории.

**Параметры:**
- ``_('name')`` - переводимый ярлык для интернационализации
- ``max_length=100`` - максимальная длина названия 100 символов
- ``blank=True, null=True`` - поле может быть пустым

Поле description
^^^^^^^^^^^^^^^^

.. code-block:: python

   description = models.TextField(_('description'), blank=True, null=True)

**Назначение:** Хранит подробное описание категории.

**Параметры:**
- ``TextField`` - подходит для длинных текстовых описаний
- ``blank=True, null=True`` - описание не обязательно для заполнения

Поле image
^^^^^^^^^^

.. code-block:: python

   image = models.ImageField(_('image'), upload_to='categories/', blank=True, null=True)

**Назначение:** Хранит изображение категории.

**Параметры:**
- ``ImageField`` - поле для загрузки изображений
- ``upload_to='categories/'`` - изображения сохраняются в папку categories/
- ``blank=True, null=True`` - категория может быть без изображения

Настройки модели Meta
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   class Meta:
       verbose_name = _('category')
       verbose_name_plural = _('categories')

**Назначение:** Задает человекочитаемые имена для админ-панели.

**Параметры:**
- ``verbose_name`` - имя в единственном числе ("категория")
- ``verbose_name_plural`` - имя во множественном числе ("категории")

Метод __str__
^^^^^^^^^^^^^

.. code-block:: python

   def __str__(self):
       return self.name or ''

**Назначение:** Определяет строковое представление объекта.

**Логика:**
- Возвращает название категории, если оно есть
- Если название пустое, возвращает пустую строку
- Гарантирует, что метод никогда не вернет None

Модель Product
--------------

Модель ``Product`` представляет товары в нашем приложении. Каждый товар принадлежит к определенной категории.

Создание модели
^^^^^^^^^^^^^^^

.. code-block:: python

   class Product(models.Model):

Базовый класс для создания модели товаров. Каждый товар будет отдельной записью в таблице.

Поле name
^^^^^^^^^

.. code-block:: python

   name = models.CharField(_('name'), max_length=200, blank=True, null=True)

**Назначение:** Хранит название товара.

**Параметры:**
- ``_('name')`` - переводимый ярлык для интернационализации
- ``max_length=200`` - максимальная длина названия 200 символов (больше чем у категории)
- ``blank=True, null=True`` - поле может быть пустым

Поле description
^^^^^^^^^^^^^^^^

.. code-block:: python

   description = models.TextField(_('description'), blank=True, null=True)

**Назначение:** Хранит подробное описание товара.

**Параметры:**
- ``TextField`` - подходит для длинных текстовых описаний товаров
- ``blank=True, null=True`` - описание не обязательно для заполнения

Поле price
^^^^^^^^^^

.. code-block:: python

   price = models.DecimalField(_('price'), max_digits=10, decimal_places=2, blank=True, null=True)

**Назначение:** Хранит цену товара.

**Параметры:**
- ``DecimalField`` - специализированное поле для денежных значений
- ``max_digits=10`` - максимально 10 цифр (включая дробную часть)
- ``decimal_places=2`` - 2 знака после запятой (копейки)
- ``blank=True, null=True`` - цена может быть не указана

Поле image
^^^^^^^^^^

.. code-block:: python

   image = models.ImageField(_('image'), upload_to='products/', blank=True, null=True)

**Назначение:** Хранит изображение товара.

**Параметры:**
- ``ImageField`` - поле для загрузки изображений товаров
- ``upload_to='products/'`` - изображения сохраняются в папку products/
- ``blank=True, null=True`` - товар может быть без изображения

Поле category (ForeignKey)
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name='products')

**Назначение:** Связывает товар с категорией.

**Параметры:**
- ``Category`` - модель, с которой устанавливается связь
- ``on_delete=models.SET_NULL`` - при удалении категории товар остается, но связь обнуляется
- ``blank=True, null=True`` - товар может быть без категории
- ``related_name='products'`` - обратная связь: category.products.all()

Поле created_at
^^^^^^^^^^^^^^^

.. code-block:: python

   created_at = models.DateTimeField(_('created at'), auto_now_add=True)

**Назначение:** Хранит дату и время создания товара.

**Параметры:**
- ``DateTimeField`` - поле для хранения даты и времени
- ``auto_now_add=True`` - автоматически устанавливает текущее время при создании
- Не имеет ``blank=True, null=True`` - всегда заполняется автоматически

Настройки модели Meta
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   class Meta:
       verbose_name = _('product')
       verbose_name_plural = _('products')

**Назначение:** Задает человекочитаемые имена для админ-панели.

**Параметры:**
- ``verbose_name`` - имя в единственном числе ("товар")
- ``verbose_name_plural`` - имя во множественном числе ("товары")

Метод __str__
^^^^^^^^^^^^^

.. code-block:: python

   def __str__(self):
       return self.name or ''

**Назначение:** Определяет строковое представление объекта.

**Логика:**
- Возвращает название товара, если оно есть
- Если название пустое, возвращает пустую строку
- Гарантирует корректное отображение в админ-панели

Модель CartItem
---------------

Модель ``CartItem`` представляет товары в корзине пользователя. Каждая запись соответствует одному товару в корзине с указанием количества.

Создание модели
^^^^^^^^^^^^^^^

.. code-block:: python

   class CartItem(models.Model):

Базовый класс для создания модели элементов корзины. Каждый элемент связывает пользователя с товаром и количеством.

Поле user (ForeignKey)
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='cart_items', blank=True, null=True)

**Назначение:** Связывает элемент корзины с пользователем.

**Параметры:**
- ``CustomUser`` - модель пользователя, с которой устанавливается связь
- ``on_delete=models.CASCADE`` - при удалении пользователя удаляются все его элементы корзины
- ``related_name='cart_items'`` - обратная связь: user.cart_items.all()
- ``blank=True, null=True`` - элемент корзины может быть без пользователя (для гостей)

Поле product (ForeignKey)
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)

**Назначение:** Связывает элемент корзины с товаром.

**Параметры:**
- ``Product`` - модель товара, с которой устанавливается связь
- ``on_delete=models.CASCADE`` - при удалении товара удаляются все связанные элементы корзины
- ``blank=True, null=True`` - элемент корзины может быть без товара

Поле quantity
^^^^^^^^^^^^^

.. code-block:: python

   quantity = models.PositiveIntegerField(_('quantity'), default=1, blank=True, null=True)

**Назначение:** Хранит количество товара в корзине.

**Параметры:**
- ``PositiveIntegerField`` - поле для положительных целых чисел (не может быть отрицательным)
- ``default=1`` - значение по умолчанию 1 товар
- ``blank=True, null=True`` - количество может быть не указано

Поле added_at
^^^^^^^^^^^^^

.. code-block:: python

   added_at = models.DateTimeField(_('added at'), auto_now_add=True)

**Назначение:** Хранит дату и время добавления товара в корзину.

**Параметры:**
- ``DateTimeField`` - поле для хранения даты и времени
- ``auto_now_add=True`` - автоматически устанавливает текущее время при создании
- Полезно для анализа поведения пользователей и очистки старых корзин

Настройки модели Meta
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   class Meta:
       verbose_name = _('cart item')
       verbose_name_plural = _('cart items')

**Назначение:** Задает человекочитаемые имена для админ-панели.

**Параметры:**
- ``verbose_name`` - имя в единственном числе ("элемент корзины")
- ``verbose_name_plural`` - имя во множественном числе ("элементы корзины")

Метод __str__
^^^^^^^^^^^^^

.. code-block:: python

   def __str__(self):
       return f"{self.quantity} x {self.product.name if self.product else ''}"

**Назначение:** Определяет строковое представление объекта.

**Логика:**
- Возвращает строку в формате "количество x название товара"
- Проверяет наличие товара перед обращением к его имени
- Пример: "2 x Роза красная"

Метод get_total
^^^^^^^^^^^^^^^

.. code-block:: python

   def get_total(self):
       if self.product and self.product.price and self.quantity:
           return self.product.price * self.quantity
       return 0

**Назначение:** Вычисляет общую стоимость элемента корзины.

**Логика:**
- Проверяет наличие товара, цены и количества
- Умножает цену товара на количество
- Возвращает 0 если какие-то данные отсутствуют
- Полезно для отображения суммы в корзине

Модель Order
------------

Модель ``Order`` представляет заказы пользователей. Каждый заказ содержит информацию о статусе, доставке и общей стоимости.

Создание модели
^^^^^^^^^^^^^^^

.. code-block:: python

   class Order(models.Model):

Базовый класс для создания модели заказов. Каждый заказ содержит полную информацию о покупке.

Константа ORDER_STATUS_CHOICES
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   ORDER_STATUS_CHOICES = [
       ('pending', _('Pending')),
       ('processing', _('Processing')),
       ('shipped', _('Shipped')),
       ('delivered', _('Delivered')),
       ('cancelled', _('Cancelled')),
   ]

**Назначение:** Определяет возможные статусы заказа.

**Варианты:**
- ``pending`` - ожидает обработки
- ``processing`` - в процессе обработки
- ``shipped`` - отправлен
- ``delivered`` - доставлен
- ``cancelled`` - отменен

Поле user (ForeignKey)
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name='orders', blank=True, null=True)

**Назначение:** Связывает заказ с пользователем.

**Параметры:**
- ``CustomUser`` - модель пользователя
- ``on_delete=models.SET_NULL`` - при удалении пользователя заказ сохраняется, но связь обнуляется
- ``related_name='orders'`` - обратная связь: user.orders.all()
- ``blank=True, null=True`` - заказ может быть без пользователя (гостевой заказ)

Поле status
^^^^^^^^^^^

.. code-block:: python

   status = models.CharField(_('status'), max_length=20, choices=ORDER_STATUS_CHOICES, default='pending', blank=True, null=True)

**Назначение:** Хранит текущий статус заказа.

**Параметры:**
- ``max_length=20`` - достаточно для самых длинных статусов
- ``choices=ORDER_STATUS_CHOICES`` - ограничивает ввод предопределенными статусами
- ``default='pending'`` - новый заказ всегда создается со статусом "ожидает"
- ``blank=True, null=True`` - статус может быть не указан

Поле created_at
^^^^^^^^^^^^^^^

.. code-block:: python

   created_at = models.DateTimeField(_('created at'), auto_now_add=True)

**Назначение:** Хранит дату и время создания заказа.

**Параметры:**
- ``DateTimeField`` - поле для хранения даты и времени
- ``auto_now_add=True`` - автоматически устанавливает текущее время при создании
- Важно для отслеживания истории заказов

Поле shipping_address
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   shipping_address = models.TextField(_('shipping address'), blank=True, null=True)

**Назначение:** Хранит адрес доставки заказа.

**Параметры:**
- ``TextField`` - подходит для длинных адресов
- ``blank=True, null=True`` - адрес может быть не указан (для самовывоза)

Поле phone
^^^^^^^^^^

.. code-block:: python

   phone = models.CharField(_('phone'), max_length=20, blank=True, null=True)

**Назначение:** Хранит контактный телефон для заказа.

**Параметры:**
- ``max_length=20`` - достаточно для международных номеров
- ``blank=True, null=True`` - телефон может быть не указан

Поле email
^^^^^^^^^^

.. code-block:: python

   email = models.EmailField(_('email'), blank=True, null=True)

**Назначение:** Хранит контактный email для заказа.

**Параметры:**
- ``EmailField`` - специализированное поле для email с валидацией формата
- ``blank=True, null=True`` - email может быть не указан

Поле total_amount
^^^^^^^^^^^^^^^^^

.. code-block:: python

   total_amount = models.DecimalField(_('total amount'), max_digits=10, decimal_places=2, blank=True, null=True)

**Назначение:** Хранит общую стоимость заказа.

**Параметры:**
- ``DecimalField`` - поле для денежных значений
- ``max_digits=10, decimal_places=2`` - поддерживает суммы до 99,999,999.99
- ``blank=True, null=True`` - сумма может рассчитываться позже

Настройки модели Meta
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   class Meta:
       verbose_name = _('order')
       verbose_name_plural = _('orders')

**Назначение:** Задает человекочитаемые имена для админ-панели.

**Параметры:**
- ``verbose_name`` - имя в единственном числе ("заказ")
- ``verbose_name_plural`` - имя во множественном числе ("заказы")

Метод __str__
^^^^^^^^^^^^^

.. code-block:: python

   def __str__(self):
       return f"Order #{self.id} - {self.user.username if self.user else ''}"

**Назначение:** Определяет строковое представление объекта.

**Логика:**
- Возвращает строку в формате "Order #номер - имя_пользователя"
- Проверяет наличие пользователя перед обращением к username
- Пример: "Order #15 - john_doe"

Модель OrderItem
----------------

Модель ``OrderItem`` представляет отдельные товары в заказе. Каждая запись связывает заказ с конкретным товаром, его количеством и ценой на момент заказа.

Создание модели
^^^^^^^^^^^^^^^

.. code-block:: python

   class OrderItem(models.Model):

Базовый класс для создания модели элементов заказа. Каждый элемент сохраняет информацию о товаре, его количестве и цене в момент оформления заказа.

Поле order (ForeignKey)
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', blank=True, null=True)

**Назначение:** Связывает элемент заказа с родительским заказом.

**Параметры:**
- ``Order`` - модель заказа, с которой устанавливается связь
- ``on_delete=models.CASCADE`` - при удалении заказа удаляются все его элементы
- ``related_name='items'`` - обратная связь: order.items.all()
- ``blank=True, null=True`` - элемент может существовать без заказа

Поле product (ForeignKey)
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)

**Назначение:** Связывает элемент заказа с товаром.

**Параметры:**
- ``Product`` - модель товара
- ``on_delete=models.SET_NULL`` - при удалении товара элемент заказа сохраняется, но связь обнуляется
- ``blank=True, null=True`` - элемент может быть без товара
- **Важно:** Сохранение элемента даже при удалении товара позволяет вести историю заказов

Поле quantity
^^^^^^^^^^^^^

.. code-block:: python

   quantity = models.PositiveIntegerField(_('quantity'), default=1, blank=True, null=True)

**Назначение:** Хранит количество товара в заказе.

**Параметры:**
- ``PositiveIntegerField`` - поле для положительных целых чисел
- ``default=1`` - значение по умолчанию 1 товар
- ``blank=True, null=True`` - количество может быть не указано

Поле price
^^^^^^^^^^

.. code-block:: python

   price = models.DecimalField(_('price'), max_digits=10, decimal_places=2, blank=True, null=True)

**Назначение:** Хранит цену товара на момент оформления заказа.

**Параметры:**
- ``DecimalField`` - поле для денежных значений
- ``max_digits=10, decimal_places=2`` - поддерживает цены до 99,999,999.99
- ``blank=True, null=True`` - цена может быть не указана
- **Важно:** Сохранение цены отдельно позволяет отслеживать историю изменения цен

Настройки модели Meta
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   class Meta:
       verbose_name = _('order item')
       verbose_name_plural = _('order items')

**Назначение:** Задает человекочитаемые имена для админ-панели.

**Параметры:**
- ``verbose_name`` - имя в единственном числе ("элемент заказа")
- ``verbose_name_plural`` - имя во множественном числе ("элементы заказа")

Метод __str__
^^^^^^^^^^^^^

.. code-block:: python

   def __str__(self):
       return f"{self.quantity} x {self.product.name if self.product else ''}"

**Назначение:** Определяет строковое представление объекта.

**Логика:**
- Возвращает строку в формате "количество x название товара"
- Проверяет наличие товара перед обращением к его имени
- Пример: "2 x Букет роз"

Метод get_total
^^^^^^^^^^^^^^^

.. code-block:: python

   def get_total(self):
       if self.price and self.quantity:
           return self.price * self.quantity
       return 0

**Назначение:** Вычисляет общую стоимость элемента заказа.

**Логика:**
- Умножает сохраненную цену на количество товара
- Возвращает 0 если цена или количество отсутствуют
- **Важно:** Использует сохраненную цену, а не текущую цену товара


Импорт
-----------------

Не забывайте про импорт!
Обычный импорт выглядит таким образом:

.. code-block:: python

    from django.contrib.auth.models import AbstractUser
    from django.db import models
    from django.utils.translation import gettext_lazy as _

Создание миграций
-----------------

После создания модели выполните:

.. code-block:: bash

   python manage.py makemigrations
   python manage.py migrate

.. note::

   **Важно:** Все дополнительные поля сделаны необязательными, чтобы не нарушать работу существующих пользователей при добавлении полей.

.. warning::

   После изменения ``AUTH_USER_MODEL`` сложно вернуться к стандартной модели. Планируйте структуру заранее!