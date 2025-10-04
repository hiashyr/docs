Настройка админ-панели Django
==============================

В этом разделе мы настроим административную панель Django для удобного управления данными нашего приложения. Админка предоставляет интерфейс для CRUD операций (Create, Read, Update, Delete) с моделями.

Основной файл admin.py
----------------------

Файл ``front/admin.py`` содержит регистрацию моделей и кастомизацию интерфейса административной панели.

Импорт моделей и модулей администрирования
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from django.contrib import admin
   from django.contrib.auth.admin import UserAdmin
   from .models import (
       CustomUser, 
       Category,
       Product,
       CartItem,
       Order,
       OrderItem,
   )

Импортируются стандартные классы администрирования Django и все модели приложения, которые нужно зарегистрировать в админ-панели.

Кастомизация админ-класса для пользователя
------------------------------------------

.. code-block:: python

   class CustomUserAdmin(UserAdmin):

Класс ``CustomUserAdmin`` наследуется от ``UserAdmin`` - стандартного административного класса Django для управления пользователями. Это позволяет сохранить всю базовую функциональность и добавить кастомные поля.

Настройка отображения списка пользователей
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

       list_display = ('username', 'email', 'first_name', 'last_name', 'phone', 'is_staff')

**list_display:** Определяет какие поля отображаются в списке пользователей в админ-панели. Добавлено поле ``phone`` для отображения номера телефона.

Настройка поиска
^^^^^^^^^^^^^^^^

.. code-block:: python

       search_fields = ('username', 'email', 'first_name', 'last_name', 'phone')

**search_fields:** Поля по которым осуществляется поиск в админ-панели. Включено поле ``phone`` для поиска по номеру телефона.

Настройка сортировки
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

       ordering = ('username',)

**ordering:** Определяет порядок сортировки по умолчанию. Пользователи сортируются по имени пользователя в алфавитном порядке.

Кастомизация формы редактирования пользователя
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

       fieldsets = (
           (None, {'fields': ('username', 'password')}),
           ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone')}),
           ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
           ('Important dates', {'fields': ('last_login', 'date_joined')}),
           ('Additional info', {'fields': ('address', 'age', 'birth_date', 'gender', 'city', 'country', 'occupation', 'avatar')}),
       )

**fieldsets:** Группирует поля в логические секции для удобства редактирования:

- **None** - базовые поля (username, password)
- **Personal info** - персональная информация
- **Permissions** - права доступа и группы
- **Important dates** - важные даты (системные)
- **Additional info** - дополнительные поля кастомной модели

Регистрация кастомного пользователя
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   admin.site.register(CustomUser, CustomUserAdmin)

Регистрирует модель ``CustomUser`` с кастомным административным классом ``CustomUserAdmin``.

Регистрация модели Category с декоратором
-----------------------------------------

.. code-block:: python

   # Register Category
   @admin.register(Category)
   class CategoryAdmin(admin.ModelAdmin):

Альтернативный способ регистрации моделей с использованием декоратора ``@admin.register()``. Более современный и читаемый подход.

Базовая настройка CategoryAdmin
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

       list_display = ('name',)
       search_fields = ('name',)

**Минимальная конфигурация:** Для модели Category используется базовая настройка с отображением имени и возможностью поиска по названию.

Регистрация модели Product
--------------------------

.. code-block:: python

   # Register Product
   @admin.register(Product)
   class ProductAdmin(admin.ModelAdmin):
       list_display = ('name', 'category', 'price', 'created_at')
       list_filter = ('category',)
       search_fields = ('name', 'description')

Настройка отображения товаров
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**list_display:** Отображает название товара, категорию, цену и дату создания.

**list_filter:** Добавляет фильтр по категориям в правую панель админки.

**search_fields:** Позволяет искать товары по названию и описанию.

Регистрация модели CartItem
---------------------------

.. code-block:: python

   # Register CartItem
   @admin.register(CartItem)
   class CartItemAdmin(admin.ModelAdmin):
       list_display = ('user', 'product', 'quantity')
       list_filter = ('user',)

Настройка элементов корзины
^^^^^^^^^^^^^^^^^^^^^^^^^^^

**list_display:** Показывает пользователя, товар и количество.

**list_filter:** Фильтр по пользователям для быстрого поиска корзин конкретных пользователей.

Регистрация модели Order
------------------------

.. code-block:: python

   # Register Order
   @admin.register(Order)
   class OrderAdmin(admin.ModelAdmin):
       list_display = ('user', 'status', 'total_amount', 'created_at')
       list_filter = ('status', 'created_at')
       search_fields = ('user__username', 'shipping_address')

Настройка управления заказами
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**list_display:** Отображает пользователя, статус заказа, общую сумму и дату создания.

**list_filter:** Двойной фильтр - по статусу заказа и дате создания.

**search_fields:** Поиск по имени пользователя (через связь ``user__username``) и адресу доставки.

Регистрация модели OrderItem
----------------------------

.. code-block:: python

   # Register OrderItem
   @admin.register(OrderItem)
   class OrderItemAdmin(admin.ModelAdmin):
       list_display = ('order', 'product', 'quantity', 'price')
       list_filter = ('order',)

Настройка элементов заказа
^^^^^^^^^^^^^^^^^^^^^^^^^^

**list_display:** Показывает заказ, товар, количество и цену.

**list_filter:** Фильтр по заказам для группировки элементов.

Принципы организации админ-панели
---------------------------------

**Логическая группировка:** Модели сгруппированы по функциональности:
- Пользователи и аутентификация
- Каталог товаров (Category, Product)
- Корзина и заказы (CartItem, Order, OrderItem)

**Оптимальная производительность:** Использование ``list_filter`` и ``search_fields`` улучшает пользовательский опыт при работе с большими объемами данных.

**Безопасность:** Сохранены все стандартные проверки прав доступа Django.

Доступ к админ-панели
---------------------

После настройки административная панель доступна по адресу:
``http://localhost:8000/admin/``

Для доступа необходимо создать суперпользователя:

.. code-block:: bash

   python manage.py createsuperuser

Рекомендации по улучшению
-------------------------

**Inline администрирование:** Для моделей со связями можно использовать ``TabularInline`` или ``StackedInline``:

.. code-block:: python

   class OrderItemInline(admin.TabularInline):
       model = OrderItem
       extra = 1

   class OrderAdmin(admin.ModelAdmin):
       inlines = [OrderItemInline]

**Кастомные действия:** Добавление массовых операций:

.. code-block:: python

   def make_confirmed(modeladmin, request, queryset):
       queryset.update(status='confirmed')
   make_confirmed.short_description = "Подтвердить выбранные заказы"

   class OrderAdmin(admin.ModelAdmin):
       actions = [make_confirmed]

**Визуальные улучшения:** Использование ``list_display_links``, ``readonly_fields``, ``prepopulated_fields``.

.. note::

   Админ-панель Django автоматически обеспечивает проверку прав доступа based на роли пользователя (staff, superuser).

.. warning::

   Не забывайте выполнять миграции после добавления новых полей в модели: ``python manage.py makemigrations && python manage.py migrate``