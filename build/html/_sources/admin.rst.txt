Админка Django (admin.py)
^^^^^^^^^^^^^^^^^^^^^^^^^^

Основные концепции
===================

``admin.py`` используется для настройки административного интерфейса Django. Он позволяет:
- Регистрировать модели для отображения в админке
- Кастомизировать внешний вид и поведение моделей
- Добавлять поиск, фильтрацию и действия
- Контролировать права доступа

1. Базовая регистрация модели
------------------------------

.. code-block:: python
   :linenos:

   from django.contrib import admin
   from .models import Product
   
   admin.site.register(Product)

**Объяснение:** Минимальный код для добавления модели Product в админку. Django создаст стандартный интерфейс для CRUD операций.

2. Кастомизация через ModelAdmin
--------------------------------

.. code-block:: python
   :linenos:

   from django.contrib import admin
   from .models import Product
   
   class ProductAdmin(admin.ModelAdmin):
       list_display = ['name', 'price', 'in_stock', 'created_at']
       list_filter = ['category', 'in_stock']
       search_fields = ['name', 'description']
       ordering = ['-created_at']
   
   admin.site.register(Product, ProductAdmin)

**Объяснение:** ``ModelAdmin`` позволяет кастомизировать отображение модели. ``list_display`` - поля в списке, ``list_filter`` - фильтры справа, ``search_fields`` - поиск по указанным полям, ``ordering`` - сортировка.

3. Декоратор @admin.register
-----------------------------

.. code-block:: python
   :linenos:

   from django.contrib import admin
   from .models import Category, Product
   
   @admin.register(Category)
   class CategoryAdmin(admin.ModelAdmin):
       list_display = ['name', 'product_count']
   
   @admin.register(Product)
   class ProductAdmin(admin.ModelAdmin):
       list_display = ['name', 'category', 'price']

**Объяснение:** Декоратор ``@admin.register`` - современный способ регистрации моделей. Декоратор принимает модель как аргумент и связывает её с классом ModelAdmin.

4. Раздельная регистрация и кастомизация
-----------------------------------------

.. code-block:: python
   :linenos:

   # Способ 1: Регистрация с кастомизацией сразу
   admin.site.register(Product, ProductAdmin)
   
   # Способ 2: Создание экземпляра ModelAdmin
   admin.site.register(Product, admin.ModelAdmin)
   
   # Способ 3: Декоратор (рекомендуется)
   @admin.register(Product)
   class ProductAdmin(admin.ModelAdmin):
       pass

**Объяснение:** Django предлагает несколько способов регистрации моделей. Декоратор наиболее читаемый и рекомендуется для нового кода.

5. Удаление регистрации (unregister)
-------------------------------------

.. code-block:: python
   :linenos:

   from django.contrib import admin
   from django.contrib.auth.models import User, Group
   
   # Удаление стандартных моделей Django
   admin.site.unregister(User)
   admin.site.unregister(Group)
   
   # Регистрация с кастомизацией
   @admin.register(User)
   class CustomUserAdmin(admin.ModelAdmin):
       list_display = ['username', 'email', 'is_staff']

**Объяснение:** ``unregister()`` удаляет модель из админки. Полезно для удаления стандартных моделей (User, Group) перед их кастомизированной перерегистрацией.

6. Групповая регистрация
-------------------------

.. code-block:: python
   :linenos:

   from django.contrib import admin
   from .models import Author, Book, Publisher
   
   # Регистрация нескольких моделей с одним ModelAdmin
   class BaseAdmin(admin.ModelAdmin):
       list_per_page = 20
       save_on_top = True
   
   admin.site.register([Author, Book, Publisher], BaseAdmin)

**Объяснение:** Можно зарегистрировать несколько моделей одновременно, передав список. Все модели получат одинаковую конфигурацию ModelAdmin.

7. Встроенные редакторы (inlines)
----------------------------------

.. code-block:: python
   :linenos:

   from django.contrib import admin
   from .models import Author, Book
   
   class BookInline(admin.TabularInline):
       model = Book
       extra = 1
   
   @admin.register(Author)
   class AuthorAdmin(admin.ModelAdmin):
       inlines = [BookInline]
       list_display = ['name', 'book_count']

**Объяснение:** ``TabularInline`` и ``StackedInline`` позволяют редактировать связанные модели на странице родительской модели. ``extra`` определяет количество пустых форм.

8. Административные действия
-----------------------------

.. code-block:: python
   :linenos:

   @admin.register(Product)
   class ProductAdmin(admin.ModelAdmin):
       actions = ['make_inactive']
       
       def make_inactive(self, request, queryset):
           queryset.update(in_stock=False)
           self.message_user(request, f"{queryset.count()} products deactivated")
       make_inactive.short_description = "Mark selected as inactive"

**Объяснение:** Кастомные действия позволяют выполнять операции с выбранными объектами. ``queryset`` содержит выбранные объекты, ``request`` - HTTP запрос.

9. Права доступа и безопасность
--------------------------------

.. code-block:: python
   :linenos:

   @admin.register(Product)
   class ProductAdmin(admin.ModelAdmin):
       # Кто может видеть модель
       def has_module_permission(self, request):
           return request.user.is_staff
       
       # Кто может добавлять объекты
       def has_add_permission(self, request):
           return request.user.is_superuser
       
       # Кто может изменять объекты
       def has_change_permission(self, request, obj=None):
           if obj and obj.created_by == request.user:
               return True
           return request.user.is_superuser

**Объяснение:** Методы ``has_*_permission`` контролируют права доступа на уровне модели и объектов. Полезно для сложных систем прав.

10. Кастомизация форм в админке
--------------------------------

.. code-block:: python
   :linenos:

   from django import forms
   from .models import Product
   
   class ProductAdminForm(forms.ModelForm):
       class Meta:
           model = Product
           fields = '__all__'
           widgets = {
               'description': forms.Textarea(attrs={'rows': 4}),
           }
   
   @admin.register(Product)
   class ProductAdmin(admin.ModelAdmin):
       form = ProductAdminForm
       fieldsets = (
           ('Основное', {'fields': ('name', 'price')}),
           ('Дополнительно', {'fields': ('category', 'description')}),
       )

**Объяснение:** ``form`` позволяет использовать кастомную форму в админке. ``fieldsets`` организует поля в логические группы с заголовками.

11. Переопределение шаблонов админки
-------------------------------------

.. code-block:: python
   :linenos:

   @admin.register(Product)
   class ProductAdmin(admin.ModelAdmin):
       change_list_template = 'admin/myapp/change_list.html'
       change_form_template = 'admin/myapp/change_form.html'
       
       class Media:
           css = {'all': ('admin/css/custom.css',)}
           js = ('admin/js/custom.js',)

**Объяснение:** ``change_*_template`` переопределяют стандартные шаблоны. Класс ``Media`` добавляет кастомные CSS/JS файлы.

Регистрация и удаление (register/unregister) - подробнее
========================================================

Паттерн unregister/register
---------------------------

.. code-block:: python
   :linenos:

   # 1. Удаляем стандартную регистрацию
   admin.site.unregister(User)
   
   # 2. Регистрируем с кастомизацией
   @admin.register(User)
   class CustomUserAdmin(UserAdmin):
       list_display = ['username', 'email', 'first_name', 'last_name', 'is_active']
       
       # Добавляем кастомное поле в форму
       fieldsets = (
           (None, {'fields': ('username', 'password')}),
           ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
           ('Custom field', {'fields': ('custom_field',)}),
       )

**Объяснение:** Этот паттерн используется для расширения или изменения поведения стандартных моделей Django (User, Group, Permission).

Динамическая регистрация
------------------------

.. code-block:: python
   :linenos:

   from django.apps import apps
   
   # Автоматическая регистрация всех моделей приложения
   for model in apps.get_app_config('myapp').get_models():
       admin.site.register(model)
   
   # Исключение определенных моделей
   EXCLUDE_MODELS = ['AuditLog', 'SystemConfig']
   app_models = apps.get_app_config('myapp').get_models()
   
   for model in app_models:
       if model.__name__ not in EXCLUDE_MODELS:
           admin.site.register(model)

**Объяснение:** Автоматическая регистрация всех моделей приложения. Полезно для больших приложений или плагинов.


13. Использование библиотек
-------------------------------------

Для настройки стилизации admin-панели можно использовать библиотеки. В данном случае будет использоваться библиотека django-admin-interface

Для ее установки используется команда:

.. code-block:: bash
    
    pip install django-admin-interface

Далее нам нужно внести изменения в setting.py, добавив в INSTALLED_APPS необходимые приложения. Теперь список будет выглядеть следущим образом:

.. code-block:: python

    INSTALLED_APPS = [
        "admin_interface",
        "colorfield",
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'main'
    ]

Также нужно после массива добавить пару строк кода:

.. code-block:: python

    X_FRAME_OPTIONS = "SAMEORIGIN"
    SILENCED_SYSTEM_CHECKS = ["security.W019"]

Далее нужно промигрироваться и собрать статические файлы командой:

.. code-block:: bash
    
    python manage.py collectstatic --clear