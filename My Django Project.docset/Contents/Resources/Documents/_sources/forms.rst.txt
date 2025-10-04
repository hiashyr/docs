Работа с формами в Django
=========================

В этом разделе мы подробно разберем создание и использование форм в Django приложении. Формы - это мощный инструмент для валидации пользовательского ввода, обработки данных и взаимодействия с моделями.

Основные концепции форм в Django
--------------------------------

**Django формы** выполняют три основные функции:
1. **Подготовка HTML** - генерация HTML-разметки для полей ввода
2. **Валидация данных** - проверка корректности введенных пользователем данных
3. **Обработка данных** - преобразование и сохранение данных в базу

Класс CustomUserCreationForm
----------------------------

.. code-block:: python

   class CustomUserCreationForm(UserCreationForm):
       phone = forms.CharField(
           widget=forms.TextInput(attrs={'placeholder': '+7XXXXXXXXXX'}),
           help_text='Введите номер телефона в формате +7XXXXXXXXXX'
       )
       
       class Meta:
           model = CustomUser
           fields = ('username', 'email', 'phone', 'first_name', 'last_name', 
                    'password1', 'password2', 'avatar')

**Наследование:** Класс наследуется от ``UserCreationForm`` - стандартной формы Django для создания пользователей, что дает нам готовую логику для работы с паролями.

**Дополнительное поле:** Добавлено поле ``phone`` с кастомными атрибутами:
- ``widget=forms.TextInput`` - определяет тип HTML-инпута
- ``attrs={'placeholder': '+7XXXXXXXXXX'}`` - добавляет атрибут placeholder для подсказки
- ``help_text`` - текст помощи, отображаемый под полем

**Метакласс Meta:** Определяет связь с моделью ``CustomUser`` и перечисляет поля, которые должны отображаться в форме.

Метод clean_phone для валидации номера телефона
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

       def clean_phone(self):
           phone = self.cleaned_data.get('phone')
           if phone:
               # Проверка формата номера телефона для России
               if not re.match(r'^\+7\d{10}$', phone):
                   raise ValidationError('Номер телефона должен быть в формате +7XXXXXXXXXX')
           return phone

**Назначение:** Кастомный метод валидации для поля ``phone``.

**Логика работы:**
1. Получает значение поля из ``cleaned_data``
2. Проверяет наличие значения
3. Использует регулярное выражение ``r'^\+7\d{10}$'`` для проверки формата
4. Если формат не соответствует - выбрасывает ``ValidationError``
5. Возвращает валидное значение

Класс PhoneAuthForm для аутентификации по телефону
---------------------------------------------------

.. code-block:: python

   class PhoneAuthForm(forms.Form):
       phone = forms.CharField(
           widget=forms.TextInput(attrs={'placeholder': '+7XXXXXXXXXX'}),
           help_text='Введите номер телефона в формате +7XXXXXXXXXX'
       )
       password = forms.CharField(widget=forms.PasswordInput)

**Базовая форма:** Наследуется от ``forms.Form`` (не связана с конкретной моделью).

**Поля формы:**
- ``phone`` - текстовое поле с подсказкой о формате
- ``password`` - поле пароля с виджетом ``PasswordInput`` (скрывает ввод)

Метод clean для комплексной валидации
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

       def clean(self):
           cleaned_data = super().clean()
           phone = cleaned_data.get('phone')
           password = cleaned_data.get('password')

           if phone and password:
               self.user = authenticate(phone=phone, password=password)
               if self.user is None:
                   raise forms.ValidationError("Неверный телефон или пароль")
           return cleaned_data

**Назначение:** Метод ``clean()`` выполняет валидацию, которая зависит от нескольких полей.

**Логика работы:**
1. Вызывает родительский ``clean()`` для базовой валидации
2. Получает значения полей ``phone`` и ``password``
3. Если оба поля заполнены - пытается аутентифицировать пользователя
4. Если аутентификация неудачна - выбрасывает ошибку
5. Сохраняет объект пользователя в атрибуте ``self.user``

Метод get_user для получения пользователя
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

       def get_user(self):
           return getattr(self, 'user', None)

**Утилитарный метод:** Возвращает аутентифицированного пользователя или ``None`` если аутентификация не выполнена.

Классы EmailAuthForm и UsernameAuthForm
----------------------------------------

.. code-block:: python

   class EmailAuthForm(forms.Form):
       email = forms.EmailField()
       password = forms.CharField(widget=forms.PasswordInput)

       def clean(self):
           cleaned_data = super().clean()
           email = cleaned_data.get('email')
           password = cleaned_data.get('password')

           if email and password:
               self.user = authenticate(email=email, password=password)
               if self.user is None:
                   raise forms.ValidationError("Неверный email или пароль")
           return cleaned_data

       def get_user(self):
           return getattr(self, 'user', None)

**Особенности EmailAuthForm:**
- Использует ``EmailField()`` с автоматической валидацией email формата
- Аутентификация происходит по полю ``email``

.. code-block:: python

   class UsernameAuthForm(forms.Form):
       username = forms.CharField()
       password = forms.CharField(widget=forms.PasswordInput)

       def clean(self):
           cleaned_data = super().clean()
           username = cleaned_data.get('username')
           password = cleaned_data.get('password')

           if username and password:
               self.user = authenticate(username=username, password=password)
               if self.user is None:
                   raise forms.ValidationError("Неверный логин или пароль")
           return cleaned_data

       def get_user(self):
           return getattr(self, 'user', None)

**Особенности UsernameAuthForm:**
- Стандартная аутентификация по имени пользователя
- Использует поле ``username`` для поиска пользователя

Формы для работы с моделями (ModelForm)
----------------------------------------

Класс CategoryForm
^^^^^^^^^^^^^^^^^^

.. code-block:: python

   class CategoryForm(forms.ModelForm):
       class Meta:
           model = Category
           fields = ['name', 'description', 'image']

**ModelForm:** Наследуется от ``forms.ModelForm``, автоматически создает поля на основе модели.

**Автоматизация:** Django автоматически:
- Создает соответствующие поля формы на основе полей модели
- Применяет валидаторы модели
- Обрабатывает сохранение в базу данных

Класс ProductForm
^^^^^^^^^^^^^^^^^

.. code-block:: python

   class ProductForm(forms.ModelForm):
       class Meta:
           model = Product
           fields = ['name', 'description', 'price', 'image', 'category']

**Поля товара:** Форма включает все основные поля модели Product для создания и редактирования товаров.

Классы CartItemForm и CartItemQuantityForm
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   class CartItemForm(forms.ModelForm):
       class Meta:
           model = CartItem
           fields = ['product', 'quantity']

   class CartItemQuantityForm(forms.ModelForm):
       class Meta:
           model = CartItem
           fields = ['quantity']

**Специализация:** 
- ``CartItemForm`` - для полного управления элементами корзины
- ``CartItemQuantityForm`` - специализированная форма только для изменения количества

Класс OrderForm для оформления заказов
---------------------------------------

.. code-block:: python

   class OrderForm(forms.ModelForm):
       phone = forms.CharField(
           widget=forms.TextInput(attrs={'placeholder': '+7XXXXXXXXXX'}),
           help_text='Введите номер телефона в формате +7XXXXXXXXXX'
       )
       class Meta:
           model = Order
           fields = ['shipping_address', 'phone', 'email']

**Переопределение поля:** Поле ``phone`` переопределено для добавления кастомных атрибутов, хотя оно уже существует в модели.

Метод clean_phone для OrderForm
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

       def clean_phone(self):
           phone = self.cleaned_data.get('phone')
           if phone:
               if not re.match(r'^\+7\d{10}$', phone):
                   raise ValidationError('Номер телефона должен быть в формате +7XXXXXXXXXX')
           return phone

**Консистентность:** Использует ту же логику валидации, что и в ``CustomUserCreationForm`` для обеспечения единообразия данных.

Принципы работы валидации в Django формах
-----------------------------------------

**Уровни валидации:**
1. **Валидация поля** - методы ``clean_<fieldname>()``
2. **Валидация формы** - метод ``clean()`` для проверки нескольких полей
3. **Валидация модели** - автоматически применяется при сохранении

**Очередность выполнения:**
1. Валидация отдельных полей (методы ``clean_<fieldname>``)
2. Валидация всей формы (метод ``clean()``)
3. Если есть ошибки - форма не считается валидной

Использование форм в представлениях
-----------------------------------

.. code-block:: python

   # В представлении
   if request.method == 'POST':
       form = CustomUserCreationForm(request.POST, request.FILES)
       if form.is_valid():
           user = form.save()  # Автоматическое сохранение для ModelForm
           login(request, user)
           return redirect('main_page')

**Обработка файлов:** ``request.FILES`` передается для обработки загружаемых файлов (аватарки, изображения товаров).

**Проверка валидности:** ``form.is_valid()`` запускает всю цепочку валидации.

**Сохранение:** ``form.save()`` для ModelForm автоматически создает/обновляет объект в базе данных.

.. note::

   Все формы используют перевод ``gettext_lazy as _`` для поддержки интернационализации, хотя в текущей реализации переводные строки не используются.

.. warning::

   Регулярное выражение для телефона ``r'^\+7\d{10}$'`` предполагает строгий российский формат. Для международной поддержки потребуется более гибкая валидация.

Импорт
-----------------

Не забывайте про импорт!
Обычный импорт выглядит таким образом:

.. code-block:: python

    from django import forms
    from django.contrib.auth import authenticate
    from django.contrib.auth.forms import UserCreationForm
    from django.core.exceptions import ValidationError
    import re
    from .models import (
        CustomUser, Product, Category, CartItem, Order
    )
    from django.utils.translation import gettext_lazy as _