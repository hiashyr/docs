Создание проекта
----------------

Для начала нужно создать папку проекта 

Затем открыть ее в прводнике и в пути прописать :code:`cmd` и нажать Enter, после чего эта папка откроется в терминале, в котором мы будем запускать команды.

Далее создаем виртуальное окружение и устанавливаем Django.

Создаем виртуальное окружение командой:

.. code-block:: bash

    python -m venv venv

Активируем окружение:

.. code-block:: bash

    venv\Scripts\activate

Если все сделано правильно, то перед путем будет показываться :code:`(venv)`

Устанавливаем Django, Pillow (для работы с изображениями) и django-admin-interface:

.. code-block:: bash

    pip install Django
    pip install Pillow
    pip install django-admin-interface

Создаем проект командой:

.. code-block:: bash

    django-admin startproject server

Переходим в папку проекта:

.. code-block:: bash

    cd server

Создаем приложение:

.. code-block:: bash

    python manage.py startapp main

Далее создаем все необходимые папки шаблонов и статических файлов

Структура проекта должна выглядеть следующим образом (если каких-то файлов не хватает, то они создадутся в дальнейшем):

.. code-block:: text

   server/
   │
   ├───main/
   │   ├───__pycache__/
   │   ├───migrations/
   │   ├───__init__.py
   │   ├───admin.py
   │   ├───apps.py
   │   ├───forms.py
   │   ├───models.py
   │   ├───tests.py
   │   └───views.py
   │
   ├───server/
   │   ├───__pycache__/
   │   │
   │   ├───static/
   │   │   ├───css/
   │   │   │   └───bootstrap.min.css
   │   │   ├───images/
   │   │   ├───js/
   │   │   │   └───bootstrap.bundle.min.js
   │   │   └───styles.css
   │   │
   │   ├───templates/
   │   │   ├───add_review.html
   │   │   ├───admin_panel.html
   │   │   ├───applications.html
   │   │   ├───base.html
   │   │   ├───create_application.html
   │   │   ├───home.html
   │   │   ├───login.html
   │   │   ├───register.html
   │   │   ├───robots.txt
   │   │   └───sitemap.xml
   │   │
   │   ├───__init__.py
   │   ├───asgi.py
   │   ├───settings.py
   │   ├───urls.py
   │   └───wsgi.py
   │
   └───manage.py

В этом моменте следует сделать первый коммит, чтобы зафиксировать структуру проекта и начать отслеживать изменения в коде.

Настройка проекта
-----------------

settings.py
------------

Открываем файл :code:`server/settings.py` и настраиваем проект:

.. code-block:: python

    import os
    from pathlib import Path

    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent.parent


    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = 'django-insecure-fkolin=&-2i6)t5e8!ykwgj=q56x38piev-0=7vo_78#aqqqxp'

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True

    ALLOWED_HOSTS = []


    # Application definition

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

    X_FRAME_OPTIONS = "SAMEORIGIN"
    SILENCED_SYSTEM_CHECKS = ["security.W019"]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    ROOT_URLCONF = 'server.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(BASE_DIR, 'server/templates')],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]

    WSGI_APPLICATION = 'server.wsgi.application'


    # Database
    # https://docs.djangoproject.com/en/5.2/ref/settings/#databases

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


    # Password validation
    # https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]


    # Internationalization
    # https://docs.djangoproject.com/en/5.2/topics/i18n/

    LANGUAGE_CODE = 'RU-ru'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_TZ = True


    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/5.2/howto/static-files/

    STATIC_URL = 'static/'
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'server', 'static')]
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

    AUTH_USER_MODEL = 'main.CustomUser'

    LOGIN_REDIRECT_URL = '/applications/'
    LOGOUT_REDIRECT_URL = '/'

    # Default primary key field type
    # https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


models.py
---------

Создаем модели в файле :code:`client/models.py`:

.. code-block:: python

    # Импорт модулей Django для работы с моделями
    from django.db import models
    from django.contrib.auth.models import AbstractUser
    from django.core.validators import RegexValidator
    import re

    # Кастомная модель пользователя
    class CustomUser(AbstractUser):
        # Валидатор для логина - только латиница и цифры, минимум 6 символов
        username_validator = RegexValidator(
            regex=r'^[a-zA-Z0-9]{6,}$',
            message='Логин должен содержать только латинские буквы и цифры, минимум 6 символов'
        )
        
        # Валидатор для ФИО - только кириллица и пробелы
        fio_validator = RegexValidator(
            regex=r'^[а-яА-ЯёЁ\s]+$',
            message='ФИО должно содержать только кириллические символы и пробелы'
        )
        
        # Валидатор для телефона - строгий формат 8(XXX)XXX-XX-XX
        phone_validator = RegexValidator(
            regex=r'^8\(\d{3}\)\d{3}-\d{2}-\d{2}$',
            message='Телефон должен быть в формате: 8(XXX)XXX-XX-XX'
        )

        # Поле логина с валидацией и уникальностью
        username = models.CharField(
            max_length=150,
            unique=True,
            verbose_name='Логин',
            error_messages={
                'unique': "Пользователь с таким логином уже существует.",
            },
        )
        # Поле ФИО с валидацией кириллицы
        fio = models.CharField(
            max_length=255,
            validators=[fio_validator],
            verbose_name='ФИО'
        )
        # Поле телефона с валидацией формата
        phone = models.CharField(
            max_length=15,
            validators=[phone_validator],
            verbose_name='Телефон'
        )
        # Поле email с уникальностью
        email = models.EmailField(unique=True, verbose_name='Email')

        # Отключение стандартных полей имени и фамилии
        first_name = None
        last_name = None

        # Поля, обязательные при создании суперпользователя
        REQUIRED_FIELDS = ['email', 'fio', 'phone']

        class Meta:
            verbose_name = 'Пользователь'
            verbose_name_plural = 'Пользователи'

        # Строковое представление пользователя
        def __str__(self):
            return f"{self.fio} ({self.username})"
        
    # Модель заявки на обучение
    class Application(models.Model):
        # Варианты способов оплаты
        PAYMENT_METHOD_CHOICES = [
            ('cash', 'Наличными'),
            ('transfer', 'Переводом по номеру телефона'),
        ]
        
        # Варианты статусов заявки
        STATUS_CHOICES = [
            ('new', 'Новая'),
            ('in_progress', 'Идет обучение'),
            ('completed', 'Обучение завершено'),
        ]

        # Связь с пользователем (один ко многим)
        user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь')
        # Название курса
        course = models.CharField(max_length=50, verbose_name='Курс')
        # Желаемая дата начала обучения
        desired_start_date = models.DateField(verbose_name='Желаемая дата начала обучения')
        # Способ оплаты с выбором из вариантов
        payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name='Способ оплаты')
        # Статус заявки с выбором из вариантов
        status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Статус')
        # Дата создания заявки (автоматически)
        created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
        # Дата обновления заявки (автоматически при сохранении)
        updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

        class Meta:
            verbose_name = 'Заявка'
            verbose_name_plural = 'Заявки'
            # Сортировка по дате создания (новые сверху)
            ordering = ['-created_at']

        # Строковое представление заявки
        def __str__(self):
            return f"Заявка {self.id} - {self.user.fio} - {self.course}"
        

    # Модель отзыва к заявке
    class Review(models.Model):
        # Связь один-к-одному с заявкой
        application = models.OneToOneField(
            Application, 
            on_delete=models.CASCADE, 
            verbose_name='Заявка',
            related_name='review'
        )
        # Текст отзыва
        text = models.TextField(verbose_name='Текст отзыва')
        # Оценка от 1 до 5
        rating = models.IntegerField(
            choices=[(i, i) for i in range(1, 6)],
            verbose_name='Оценка'
        )
        # Дата создания отзыва (автоматически)
        created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

        class Meta:
            verbose_name = 'Отзыв'
            verbose_name_plural = 'Отзывы'

        # Строковое представление отзыва
        def __str__(self):
            return f"Отзыв на заявку {self.application.id}"

Здесь стоит сделать второй коммит, чтобы зафиксировать создание моделей таблиц баз данных.

После создания моделей выполняем миграции:

.. code-block:: bash

    python manage.py makemigrations
    python manage.py migrate

forms.py
--------

Создаем файл :code:`client/forms.py` с формами:

.. code-block:: python

    # Импорт модулей Django для работы с формами
    from django import forms
    from django.contrib.auth.forms import UserCreationForm
    # Импорт моделей приложения
    from .models import CustomUser, Application, Review
    # Импорт модуля для работы с регулярными выражениями
    import re

    # Форма регистрации пользователя
    class CustomUserRegistrationForm(UserCreationForm):
        def __init__(self, *args, **kwargs):
            # Вызов родительского конструктора
            super().__init__(*args, **kwargs)
            
            # Настройка подсказок для полей паролей
            self.fields['password1'].help_text = 'Минимум 8 символов'
            self.fields['password2'].help_text = 'Повторите пароль для подтверждения'
            self.fields['password1'].label = 'Пароль'
            self.fields['password2'].label = 'Подтверждение пароля'
            
            # Настройка подсказок для остальных полей
            self.fields['username'].help_text = 'Только латинские буквы и цифры, не менее 6 символов'
            self.fields['fio'].help_text = 'Только кириллические символы и пробелы'
            self.fields['phone'].help_text = 'Формат: 8(XXX)XXX-XX-XX'
            self.fields['email'].help_text = 'Введите действующий email адрес'
            
            # Настройка сообщений об ошибках для полей паролей
            self.fields['password1'].error_messages = {
                'required': 'Обязательное поле',
            }
            self.fields['password2'].error_messages = {
                'required': 'Обязательное поле',
            }

        # Валидация поля username
        def clean_username(self):
            username = self.cleaned_data['username']
            # Проверка формата логина (только латиница и цифры, минимум 6 символов)
            if not re.match(r'^[a-zA-Z0-9]{6,}$', username):
                raise forms.ValidationError('Логин должен содержать только латинские буквы и цифры, минимум 6 символов')
            
            # Проверка уникальности логина
            if CustomUser.objects.filter(username=username).exists():
                raise forms.ValidationError('Пользователь с таким логином уже существует')
            
            return username

        # Валидация поля fio
        def clean_fio(self):
            fio = self.cleaned_data['fio']
            # Проверка что ФИО содержит только кириллицу и пробелы
            if not re.match(r'^[а-яА-ЯёЁ\s]+$', fio):
                raise forms.ValidationError('ФИО должно содержать только кириллические символы и пробелы')
            return fio

        # Валидация поля phone
        def clean_phone(self):
            phone = self.cleaned_data['phone']
            # Проверка формата телефона
            if not re.match(r'^8\(\d{3}\)\d{3}-\d{2}-\d{2}$', phone):
                raise forms.ValidationError('Телефон должен быть в формате: 8(XXX)XXX-XX-XX')
            
            # Проверка уникальности телефона
            if CustomUser.objects.filter(phone=phone).exists():
                raise forms.ValidationError('Пользователь с таким телефоном уже существует')
            
            return phone

        # Валидация поля email
        def clean_email(self):
            email = self.cleaned_data['email']
            
            # Проверка уникальности email
            if CustomUser.objects.filter(email=email).exists():
                raise forms.ValidationError('Пользователь с таким email уже существует')
            
            return email

        # Общая валидация формы
        def clean(self):
            cleaned_data = super().clean()
            password1 = cleaned_data.get("password1")
            password2 = cleaned_data.get("password2")

            # Проверка совпадения паролей
            if password1 and password2 and password1 != password2:
                raise forms.ValidationError({
                    'password2': 'Пароли не совпадают'
                })

        class Meta:
            model = CustomUser
            fields = ['username', 'fio', 'phone', 'email', 'password1', 'password2']
            widgets = {
                'username': forms.TextInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'Введите логин'
                }),
                'fio': forms.TextInput(attrs={
                    'class': 'form-control', 
                    'placeholder': 'Введите ФИО'
                }),
                'phone': forms.TextInput(attrs={
                    'class': 'form-control',
                    'placeholder': '8(XXX)XXX-XX-XX',
                    'id': 'phone-input'
                }),
                'email': forms.EmailInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'Введите email'
                }),
                'password1': forms.PasswordInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'Введите пароль'
                }),
                'password2': forms.PasswordInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'Повторите пароль'
                }),
            }
            labels = {
                'username': 'Логин',
                'fio': 'ФИО',
                'phone': 'Телефон', 
                'email': 'Email',
                'password1': 'Пароль',
                'password2': 'Подтверждение пароля',
            }
            error_messages = {
                'username': {
                    'required': 'Обязательное поле',
                },
                'fio': {
                    'required': 'Обязательное поле',
                },
                'phone': {
                    'required': 'Обязательное поле',
                },
                'email': {
                    'required': 'Обязательное поле',
                    'invalid': 'Введите корректный email адрес',
                },
            }

    # Форма создания заявки на курс
    class ApplicationForm(forms.ModelForm):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Добавление подсказки для поля даты
            self.fields['desired_start_date'].help_text = 'Формат: ДД.ММ.ГГГГ'
            # Добавляем подсказку для поля курса
            self.fields['course'].help_text = 'Введите название курса'

        class Meta:
            model = Application
            fields = ['course', 'desired_start_date', 'payment_method']
            widgets = {
                'course': forms.TextInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'Введите название курса'
                }),
                'desired_start_date': forms.DateInput(attrs={
                    'class': 'form-control',
                    'type': 'date'
                }),
                'payment_method': forms.Select(attrs={'class': 'form-control'}),
            }
            labels = {
                'course': 'Наименование курса',
                'desired_start_date': 'Желаемая дата начала обучения',
                'payment_method': 'Способ оплаты',
            }
            error_messages = {
                'course': {
                    'required': 'Обязательное поле',
                },
                'desired_start_date': {
                    'required': 'Обязательное поле',
                },
                'payment_method': {
                    'required': 'Обязательное поле',
                },
            }

    # Форма добавления отзыва
    class ReviewForm(forms.ModelForm):
        class Meta:
            model = Review
            fields = ['rating', 'text']
            widgets = {
                'rating': forms.Select(attrs={'class': 'form-control'}),
                'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            }
            labels = {
                'rating': 'Оценка',
                'text': 'Текст отзыва',
            }
            error_messages = {
                'rating': {
                    'required': 'Обязательное поле',
                },
                'text': {
                    'required': 'Обязательное поле',
                },
            }

views.py
--------

Создаем представления в файле :code:`client/views.py`:

.. code-block:: python

    # Импорт модулей Django для работы с представлениями
    from django.shortcuts import render, redirect, get_object_or_404
    from django.contrib.auth import login, logout, authenticate
    from django.contrib.auth.decorators import login_required
    from django.contrib import messages
    from django.http import HttpResponseForbidden
    # Импорт моделей приложения
    from .models import Application, Review
    # Импорт форм приложения
    from .forms import CustomUserRegistrationForm, ApplicationForm, ReviewForm

    # Главная страница сайта
    def home(request):
        return render(request, 'home.html')

    # Обработка регистрации пользователя
    def register(request):
        if request.method == 'POST':
            # Создание формы с данными из POST запроса
            form = CustomUserRegistrationForm(request.POST)
            if form.is_valid():
                # Сохранение пользователя и автоматический вход
                user = form.save()
                login(request, user)
                messages.success(request, 'Регистрация прошла успешно!')
                return redirect('applications')
        else:
            # Создание пустой формы для GET запроса
            form = CustomUserRegistrationForm()
        
        return render(request, 'register.html', {'form': form})

    # Кастомная страница входа в систему
    def custom_login(request):
        if request.method == 'POST':
            # Получение данных из формы
            username = request.POST['username']
            password = request.POST['password']
            # Аутентификация пользователя
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                # Успешный вход
                login(request, user)
                messages.success(request, f'Добро пожаловать, {user.fio}!')
                return redirect('applications')
            else:
                # Ошибка аутентификации
                messages.error(request, 'Неверный логин или пароль')
        
        return render(request, 'login.html')

    # Просмотр заявок пользователя (только для авторизованных)
    @login_required
    def applications(request):
        # Получение всех заявок текущего пользователя
        user_applications = Application.objects.filter(user=request.user).order_by('-created_at')
        return render(request, 'applications.html', {'applications': user_applications})

    # Создание новой заявки (только для авторизованных)
    @login_required
    def create_application(request):
        if request.method == 'POST':
            form = ApplicationForm(request.POST)
            if form.is_valid():
                # Создание заявки без сохранения в БД
                application = form.save(commit=False)
                # Привязка заявки к текущему пользователю
                application.user = request.user
                # Сохранение заявки в БД
                application.save()
                messages.success(request, 'Заявка успешно создана и отправлена на рассмотрение!')
                return redirect('applications')
        else:
            form = ApplicationForm()
        
        return render(request, 'create_application.html', {'form': form})

    # Добавление отзыва к заявке (только для авторизованных)
    @login_required
    def add_review(request, application_id):
        # Получение заявки или 404 ошибка
        application = get_object_or_404(Application, id=application_id, user=request.user)
        
        # Проверка что заявка имеет статус "завершено"
        if application.status != 'completed':
            return HttpResponseForbidden("Отзыв можно оставить только для завершенных курсов")
        
        # Проверка что отзыв еще не оставлен
        if hasattr(application, 'review'):
            messages.error(request, 'Отзыв уже оставлен для этой заявки')
            return redirect('applications')
        
        if request.method == 'POST':
            form = ReviewForm(request.POST)
            if form.is_valid():
                # Создание отзыва без сохранения в БД
                review = form.save(commit=False)
                # Привязка отзыва к заявке
                review.application = application
                # Сохранение отзыва в БД
                review.save()
                messages.success(request, 'Отзыв успешно добавлен!')
                return redirect('applications')
        else:
            form = ReviewForm()
        
        return render(request, 'add_review.html', {'form': form, 'application': application})

    # Выход из системы
    def custom_logout(request):
        logout(request)
        return redirect('home')

    # Генерация robots.txt для SEO
    def robots_txt(request):
        return render(request, 'robots.txt', content_type='text/plain')

    # Генерация sitemap.xml для SEO
    def sitemap_xml(request):
        return render(request, 'sitemap.xml', content_type='application/xml')

    # Кастомная админ-панель для управления заявками
    @login_required
    def admin_panel(request):
        # Проверка прав администратора
        if not request.user.is_staff:
            return HttpResponseForbidden("Доступ запрещен. Требуются права администратора.")
        
        # Получение всех заявок
        applications = Application.objects.all().order_by('-created_at')
        
        # Обработка изменения статуса
        if request.method == 'POST':
            application_id = request.POST.get('application_id')
            new_status = request.POST.get('status')
            
            if application_id and new_status:
                application = get_object_or_404(Application, id=application_id)
                application.status = new_status
                application.save()
                messages.success(request, f'Статус заявки #{application_id} изменен на "{application.get_status_display()}"')
                return redirect('admin_panel')
        
        return render(request, 'admin_panel.html', {'applications': applications})

    # Просмотр деталей заявки для админа
    @login_required
    def admin_application_detail(request, application_id):
        # Проверка прав администратора
        if not request.user.is_staff:
            return HttpResponseForbidden("Доступ запрещен. Требуются права администратора.")
        
        application = get_object_or_404(Application, id=application_id)
        return render(request, 'admin_application_detail.html', {'application': application})

urls.py
-------

Здесь стоит сделать третий коммит, чтобы зафиксировать создание серверной части.

Настраиваем главный :code:`server/urls.py`:

.. code-block:: python

    # Импорт административной панели Django
    from django.contrib import admin
    # Импорт функций для работы с URL
    from django.urls import path
    # Импорт стандартных views аутентификации
    from django.contrib.auth import views as auth_views
    # Импорт views из приложения main
    from main import views

    # Определение URL-шаблонов проекта
    urlpatterns = [
        # URL для административной панели Django
        path('admin/', admin.site.urls),
        
        # Главная страница сайта
        path('', views.home, name='home'),
        
        # URL для аутентификации пользователей
        path('register/', views.register, name='register'),
        path('login/', views.custom_login, name='login'),
        path('logout/', views.custom_logout, name='logout'),
        
        # URL для работы с заявками пользователей
        path('applications/', views.applications, name='applications'),
        path('applications/create/', views.create_application, name='create_application'),
        # URL для добавления отзыва к конкретной заявке
        path('applications/<int:application_id>/review/', views.add_review, name='add_review'),

        # URL для кастомной админ-панели
        path('admin-panel/', views.admin_panel, name='admin_panel'),
        
        # URL для SEO оптимизации
        path('sitemap.xml', views.sitemap_xml, name='sitemap'),
        path('robots.txt', views.robots_txt, name='robots_txt'),
    ]

Шаблоны
-------

base.html
~~~~~~~~~

Базовый шаблон, который наследуют все остальные страницы:

.. code-block:: html

    {# Загрузка статических файлов (CSS, JS, изображения) #}
    {% load static %}

    <!DOCTYPE html>
    <html lang="ru">
    <head>
        {# Базовые мета-теги #}
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        
        {# Блоки для динамического контента страниц #}
        <title>{% block title %}Корочки.есть{% endblock %}</title>
        <meta name="description" content="{% block description %}Онлайн курсы дополнительного профессионального образования{% endblock %}">
        <meta name="keywords" content="{% block keywords %}курсы, обучение, образование{% endblock %}">
        
        {# Подключение Bootstrap CSS локально #}
        <link href="{% static 'css/bootstrap.min.css' %}" rel="stylesheet">
        
        {# Подключение кастомных стилей проекта #}
        <link href="{% static 'styles.css' %}" rel="stylesheet">
    </head>
    <body>
        {# Навигационная панель сайта #}
        <nav class="navbar navbar-expand-lg navbar-dark">
            <div class="container">
                {# Логотип и название сайта #}
                <a class="navbar-brand" href="{% url 'home' %}">Корочки.есть</a>
                
                {# Навигационное меню #}
                <div class="navbar-nav ms-auto">
                    {% if user.is_authenticated %}
                        <a class="nav-link" href="{% url 'applications' %}">Мои заявки</a>
                        <a class="nav-link" href="{% url 'create_application' %}">Подать заявку</a>
                        
                        {% if user.is_staff %}
                            <a class="nav-link" href="{% url 'admin_panel' %}">Админ-панель</a>
                        {% endif %}
                        
                        <a class="nav-link" href="{% url 'logout' %}">Выйти ({{ user.username }})</a>
                    {% else %}
                        <a class="nav-link" href="{% url 'login' %}">Войти</a>
                        <a class="nav-link" href="{% url 'register' %}">Регистрация</a>
                    {% endif %}
                </div>
            </div>
        </nav>

        {# Основной контент страницы #}
        <main class="container mt-4">
            {% block content %}
            {% endblock %}
        </main>

        {# Подключение Bootstrap JavaScript локально #}
        <script src="{% static 'js/bootstrap.bundle.min.js' %}"></script>
    </body>
    </html>

В общем далее коммиты можно делтать по каждой странице, но лучше на этих страницах сразу менять мета-теги, и все остальное по теме

add_review.html
~~~~~~~~~~~~~~~~

.. code-block:: html
    
    {% extends 'base.html' %}

    {% block title %}Отзыв - Корочки.есть{% endblock %}
    {% block description %}Оставьте отзыв о пройденном курсе{% endblock %}
    {% block keywords %}отзыв, оценка, курс, обучение{% endblock %}

    {% block content %}
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="form-container">
                <h2 class="mb-4">Оставить отзыв</h2>

                <div class="card mb-4">
                    <div class="card-body">
                        <h5 class="card-title">Информация о курсе</h5>
                        <p class="mb-1"><strong>Курс:</strong> {{ application.get_course_display }}</p>
                        <p class="mb-1"><strong>Дата начала:</strong> {{ application.desired_start_date|date:"d.m.Y" }}</p>
                        <p class="mb-0"><strong>Способ оплаты:</strong> {{ application.get_payment_method_display }}</p>
                    </div>
                </div>

                <form method="post">
                    {% csrf_token %}
                    
                    {% for field in form %}
                    <div class="mb-3">
                        <label for="{{ field.id_for_label }}" class="form-label">{{ field.label }}</label>
                        {{ field }}
                        {% if field.errors %}
                            <div class="text-danger small mt-1">
                                {% for error in field.errors %}
                                    {{ error }}
                                {% endfor %}
                            </div>
                        {% endif %}
                    </div>
                    {% endfor %}
                    
                    <button type="submit" class="btn btn-primary">Опубликовать отзыв</button>
                    <a href="{% url 'applications' %}" class="btn btn-outline-secondary">Отмена</a>
                </form>
            </div>
        </div>
    </div>
    {% endblock %}

admin_panel.html
~~~~~~~~~~~~~~~~

.. code-block:: html

    {% extends 'base.html' %}
    {% load static %}

    {% block title %}Админ-панель - Управление заявками{% endblock %}
    {% block description %}Управление статусами заявок{% endblock %}

    {% block content %}
    <div class="admin-container">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2 class="fw-bold">Админ-панель управления заявками</h2>
            <a href="{% url 'home' %}" class="btn btn-outline-secondary">На главную</a>
        </div>

        {% if messages %}
            {% for message in messages %}
                <div class="alert alert-{% if message.tags == 'success' %}success{% elif message.tags == 'error' %}warning{% else %}info{% endif %} alert-dismissible fade show" role="alert">
                    {{ message }}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            {% endfor %}
        {% endif %}

        <div class="table-responsive">
            <table class="table admin-table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Пользователь</th>
                        <th>Курс</th>
                        <th>Дата начала</th>
                        <th>Способ оплаты</th>
                        <th>Текущий статус</th>
                        <th>Дата создания</th>
                        <th>Отзыв</th>
                        <th>Действия</th>
                    </tr>
                </thead>
                <tbody>
                    {% for application in applications %}
                    <tr class="application-row 
                        {% if application.status == 'new' %}row-new
                        {% elif application.status == 'in_progress' %}row-progress
                        {% elif application.status == 'completed' %}row-completed{% endif %}">
                        <td><strong>{{ application.id }}</strong></td>
                        <td>
                            <strong>{{ application.user.fio }}</strong><br>
                            <small class="text-muted">{{ application.user.username }}</small>
                        </td>
                        <td>{{ application.get_course_display }}</td>
                        <td>{{ application.desired_start_date|date:"d.m.Y" }}</td>
                        <td>{{ application.get_payment_method_display }}</td>
                        <td>
                            <span class="badge 
                                {% if application.status == 'new' %}badge-new
                                {% elif application.status == 'in_progress' %}badge-progress
                                {% else %}badge-completed{% endif %}">
                                {{ application.get_status_display }}
                            </span>
                        </td>
                        <td>{{ application.created_at|date:"d.m.Y H:i" }}</td>
                        <td>
                            {% if application.review %}
                                <button type="button" class="btn btn-sm btn-review" data-bs-toggle="modal" data-bs-target="#reviewModal{{ application.id }}">
                                    Показать отзыв
                                </button>
                            {% else %}
                                <span class="text-muted">Нет отзыва</span>
                            {% endif %}
                        </td>
                        <td>
                            <button type="button" class="btn btn-sm btn-change-status" data-bs-toggle="modal" data-bs-target="#statusModal{{ application.id }}">
                                Изменить статус
                            </button>
                        </td>
                    </tr>

                    <!-- Модальное окно для изменения статуса -->
                    <div class="modal fade admin-modal" id="statusModal{{ application.id }}" tabindex="-1">
                        <div class="modal-dialog modal-dialog-centered">
                            <div class="modal-content">
                                <div class="modal-header">
                                    <h5 class="modal-title">Изменение статуса заявки #{{ application.id }}</h5>
                                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                                </div>
                                <form method="post">
                                    {% csrf_token %}
                                    <div class="modal-body">
                                        <input type="hidden" name="application_id" value="{{ application.id }}">
                                        <div class="mb-3">
                                            <label class="form-label">Текущий статус:</label>
                                            <p class="fw-bold mb-0">{{ application.get_status_display }}</p>
                                        </div>
                                        <div class="mb-3">
                                            <label for="status{{ application.id }}" class="form-label">Новый статус:</label>
                                            <select name="status" id="status{{ application.id }}" class="form-select" required>
                                                <option value="new" {% if application.status == 'new' %}selected{% endif %}>Новая</option>
                                                <option value="in_progress" {% if application.status == 'in_progress' %}selected{% endif %}>Идет обучение</option>
                                                <option value="completed" {% if application.status == 'completed' %}selected{% endif %}>Обучение завершено</option>
                                            </select>
                                        </div>
                                    </div>
                                    <div class="modal-footer">
                                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Отмена</button>
                                        <button type="submit" class="btn btn-primary">Сохранить изменения</button>
                                    </div>
                                </form>
                            </div>
                        </div>
                    </div>

                    <!-- Модальное окно для просмотра отзыва -->
                    {% if application.review %}
                    <div class="modal fade admin-modal" id="reviewModal{{ application.id }}" tabindex="-1">
                        <div class="modal-dialog modal-dialog-centered">
                            <div class="modal-content">
                                <div class="modal-header">
                                    <h5 class="modal-title">Отзыв на заявку #{{ application.id }}</h5>
                                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                                </div>
                                <div class="modal-body">
                                    <div class="mb-3">
                                        <strong>Оценка:</strong>
                                        <div class="mt-1">
                                            <span class="ms-2">({{ application.review.rating }}/5)</span>
                                        </div>
                                    </div>
                                    <div>
                                        <strong>Текст отзыва:</strong>
                                        <div class="mt-2 p-3 bg-light rounded review-content">
                                            {{ application.review.text }}
                                        </div>
                                    </div>
                                    <div class="text-muted mt-3">
                                        <small>Дата отзыва: {{ application.review.created_at|date:"d.m.Y H:i:s" }}</small>
                                    </div>
                                </div>
                                <div class="modal-footer">
                                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                                </div>
                            </div>
                        </div>
                    </div>
                    {% endif %}

                    {% empty %}
                    <tr>
                        <td colspan="9" class="text-center py-4">
                            <p class="text-muted mb-0">Нет заявок для отображения</p>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
    {% endblock %}

applications.html
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: html

    {% extends 'base.html' %}
    {% load static %}

    {% block title %}Мои заявки - Корочки.есть{% endblock %}
    {% block description %}Просмотр ваших заявок на обучение и отзывов{% endblock %}
    {% block keywords %}заявки, обучение, отзывы, статусы{% endblock %}

    {% block content %}
    {# Заголовок страницы с кнопкой создания новой заявки #}
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h2 class="fw-bold">Мои заявки</h2>
        <a href="{% url 'create_application' %}" class="btn btn-primary">
            Новая заявка
        </a>
    </div>

    {# Проверка наличия заявок у пользователя #}
    {% if applications %}
        <div class="row justify-content-center">
            <div class="col-lg-8">
                {# Цикл по всем заявкам пользователя - теперь в одну колонку #}
                {% for application in applications %}
                    <div class="mb-4">
                        {# Карточка заявки с динамическими классами в зависимости от статуса #}
                        <div class="card application-card 
                            {% if application.status == 'new' %}application-new
                            {% elif application.status == 'in_progress' %}application-in-progress
                            {% elif application.status == 'completed' %}application-completed{% endif %}">
                            <div class="card-body">
                                {# Заголовок карточки с названием курса и статусом #}
                                <div class="d-flex justify-content-between align-items-center mb-3">
                                    <h4 class="card-title mb-0">{{ application.get_course_display }}</h4>
                                    <span class="badge 
                                        {% if application.status == 'new' %}bg-success
                                        {% elif application.status == 'in_progress' %}bg-warning
                                        {% else %}bg-secondary{% endif %}">
                                        {{ application.get_status_display }}
                                    </span>
                                </div>
                                
                                {# Детальная информация о заявке в виде сетки #}
                                <div class="row g-3 mb-3">
                                    <div class="col-sm-4">
                                        <div class="d-flex align-items-center text-muted">
                                            <span class="me-2">Дата</span>
                                            <small>Начало: {{ application.desired_start_date|date:"d.m.Y" }}</small>
                                        </div>
                                    </div>
                                    <div class="col-sm-4">
                                        <div class="d-flex align-items-center text-muted">
                                            <span class="me-2">Оплата</span>
                                            <small>{{ application.get_payment_method_display }}</small>
                                        </div>
                                    </div>
                                    <div class="col-sm-4">
                                        <div class="d-flex align-items-center text-muted">
                                            <span class="me-2">Время</span>
                                            <small>Подана: {{ application.created_at|date:"d.m.Y" }}</small>
                                        </div>
                                    </div>
                                </div>
                                
                                {# Блок для отзывов (только для завершенных заявок) #}
                                {% if application.status == 'completed' %}
                                    <div class="mt-3 pt-3 border-top">
                                        {% if application.review %}
                                            <div class="alert alert-info mb-0">
                                                <div class="d-flex align-items-center mb-2">
                                                    <strong class="me-2">Ваш отзыв:</strong>
                                                    <span>Оценка: {{ application.review.rating }}/5</span>
                                                </div>
                                                <p class="mb-0">{{ application.review.text }}</p>
                                            </div>
                                        {% else %}
                                            <a href="{% url 'add_review' application.id %}" class="btn btn-outline-primary btn-sm">
                                                Оставить отзыв
                                            </a>
                                        {% endif %}
                                    </div>
                                {% endif %}
                            </div>
                        </div>
                    </div>
                {% endfor %}
            </div>
        </div>
    {% else %}
        {# Сообщение при отсутствии заявок #}
        <div class="text-center py-5">
            <h4 class="fw-bold">У вас пока нет заявок</h4>
            <p class="text-muted mb-4">Подайте первую заявку на обучение!</p>
            <a href="{% url 'create_application' %}" class="btn btn-primary btn-lg px-5">Подать заявку</a>
        </div>
    {% endif %}
    {% endblock %}
    
create_application.html
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: html

    {% extends 'base.html' %}

    {% block title %}Подача заявки - Корочки.есть{% endblock %}
    {% block description %}Подайте заявку на онлайн курс обучения{% endblock %}
    {% block keywords %}заявка, курс, обучение, подать{% endblock %}

    {% block content %}
    <div class="form-container">
        <h2>Подача заявки на курс</h2>
        
        <form method="post">
            {% csrf_token %}
            {{ form.as_p }}
            <div class="d-grid gap-2">
                <button type="submit" class="btn btn-primary btn-lg">Отправить заявку</button>
            </div>
        </form>
    </div>
    {% endblock %}

home.html
~~~~~~~~~~

.. code-block:: html

    {# Наследование от базового шаблона #}
    {% extends 'base.html' %}
    {# Загрузка статических файлов #}
    {% load static %}

    {# Мета-теги для SEO #}
    {% block title %}Главная - Корочки.есть{% endblock %}
    {% block description %}Запишитесь на онлайн курсы программирования, веб-дизайна и баз данных. Официальные документы.{% endblock %}
    {% block keywords %}курсы, программирование, веб-дизайн, базы данных, обучение{% endblock %}

    {% block content %}
    {# Основной заголовок и приветствие #}
    <div class="row">
        <div class="col-12 text-center mb-5">
            <h1 class="display-4">Добро пожаловать на портал "Корочки.есть"</h1>
            <p class="lead">Онлайн курсы дополнительного профессионального образования</p>
            
            {# Разные кнопки для авторизованных и неавторизованных пользователей #}
            {% if not user.is_authenticated %}
                <div class="mt-4">
                    <a href="{% url 'register' %}" class="btn btn-primary btn-lg me-3">Начать обучение</a>
                    <a href="{% url 'login' %}" class="btn btn-outline-primary btn-lg">Войти в систему</a>
                </div>
            {% else %}
                <div class="mt-4">
                    <a href="{% url 'create_application' %}" class="btn btn-success btn-lg me-3">Подать заявку на курс</a>
                    <a href="{% url 'applications' %}" class="btn btn-outline-success btn-lg">Мои заявки</a>
                </div>
            {% endif %}
        </div>
    </div>

    {# Слайдер с курсами #}
    <div class="row justify-content-center">
        {# Контейнер слайдера с ограничением ширины #}
        <div class="col-12 col-lg-10 col-xl-8">
            <div id="courseSlider" class="carousel slide" data-bs-ride="carousel">
                {# Индикаторы слайдов (точки внизу) #}
                <div class="carousel-indicators">
                    <button type="button" data-bs-target="#courseSlider" data-bs-slide-to="0" class="active"></button>
                    <button type="button" data-bs-target="#courseSlider" data-bs-slide-to="1"></button>
                    <button type="button" data-bs-target="#courseSlider" data-bs-slide-to="2"></button>
                    <button type="button" data-bs-target="#courseSlider" data-bs-slide-to="3"></button>
                </div>
                
                {# Контейнер слайдов #}
                <div class="carousel-inner rounded">
                    {# Слайд 1 - Программирование #}
                    <div class="carousel-item active">
                        <img src="{% static 'images/slide1.jpg' %}" class="d-block w-100 slider-image" alt="Курсы программирования">
                        <div class="carousel-caption d-none d-md-block">
                            <h5>Основы алгоритмизации и программирования</h5>
                            <p>Научитесь основам программирования и созданию алгоритмов</p>
                        </div>
                    </div>
                    {# Слайд 2 - Веб-дизайн #}
                    <div class="carousel-item">
                        <img src="{% static 'images/slide2.jpg' %}" class="d-block w-100 slider-image" alt="Веб-дизайн">
                        <div class="carousel-caption d-none d-md-block">
                            <h5>Основы веб-дизайна</h5>
                            <p>Освойте современные тенденции в создании веб-интерфейсов</p>
                        </div>
                    </div>
                    {# Слайд 3 - Базы данных #}
                    <div class="carousel-item">
                        <img src="{% static 'images/slide3.jpg' %}" class="d-block w-100 slider-image" alt="Базы данных">
                        <div class="carousel-caption d-none d-md-block">
                            <h5>Основы проектирования баз данных</h5>
                            <p>Изучите принципы проектирования и работы с базами данных</p>
                        </div>
                    </div>
                    {# Слайд 4 - Документы #}
                    <div class="carousel-item">
                        <img src="{% static 'images/slide4.jpg' %}" class="d-block w-100 slider-image" alt="Дипломы">
                        <div class="carousel-caption d-none d-md-block">
                            <h5>Получите документы об образовании</h5>
                            <p>Официальные документы после успешного завершения курсов</p>
                        </div>
                    </div>
                </div>
                
                {# Кнопки переключения слайдов #}
                <button class="carousel-control-prev" type="button" data-bs-target="#courseSlider" data-bs-slide="prev">
                    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                    <span class="visually-hidden">Предыдущий</span>
                </button>
                <button class="carousel-control-next" type="button" data-bs-target="#courseSlider" data-bs-slide="next">
                    <span class="carousel-control-next-icon" aria-hidden="true"></span>
                    <span class="visually-hidden">Следующий</span>
                </button>
            </div>
        </div>
    </div>

    {# Блок с информацией о курсах #}
    <div class="row mt-5">
        {# Карточка курса 1 - Алгоритмизация #}
        <div class="col-md-4 mb-4">
            <div class="card h-100">
                <div class="card-body text-center">
                    <h5 class="card-title"> Основы алгоритмизации</h5>
                    <p class="card-text">Изучите основы программирования, алгоритмы и структуры данных. Подходит для начинающих.</p>
                </div>
            </div>
        </div>
        {# Карточка курса 2 - Веб-дизайн #}
        <div class="col-md-4 mb-4">
            <div class="card h-100">
                <div class="card-body text-center">
                    <h5 class="card-title"> Веб-дизайн</h5>
                    <p class="card-text">Освойте создание современных веб-интерфейсов, UX/UI дизайн и работу с графикой.</p>
                </div>
            </div>
        </div>
        {# Карточка курса 3 - Базы данных #}
        <div class="col-md-4 mb-4">
            <div class="card h-100">
                <div class="card-body text-center">
                    <h5 class="card-title"> Базы данных</h5>
                    <p class="card-text">Научитесь проектировать и работать с базами данных, писать SQL запросы.</p>
                </div>
            </div>
        </div>
    </div>
    {% endblock %}

    {# Блок для JavaScript кода #}
    {% block scripts %}
    <script>
        // Автопереключение слайдов каждые 3 секунды
        document.addEventListener('DOMContentLoaded', function() {
            var myCarousel = document.getElementById('courseSlider');
            var carousel = new bootstrap.Carousel(myCarousel, {
                interval: 3000,
                wrap: true
            });
        });
    </script>
    {% endblock %}

login.html
~~~~~~~~~~

.. code-block:: html

    {% extends 'base.html' %}

    {% block title %}Вход - Корочки.есть{% endblock %}
    {% block description %}Войдите в свой аккаунт для доступа к курсам{% endblock %}
    {% block keywords %}вход, авторизация, аккаунт{% endblock %}

    {% block content %}
    <div class="form-container">
        <h2>Авторизация</h2>

        {% if messages %}
            {% for message in messages %}
                <div class="alert alert-danger">{{ message }}</div>
            {% endfor %}
        {% endif %}

        <form method="post">
            {% csrf_token %}
            
            <div class="mb-4">
                <label for="username" class="form-label">Логин</label>
                <input type="text" class="form-control" id="username" name="username" placeholder="Введите ваш логин" required>
            </div>
            
            <div class="mb-4">
                <label for="password" class="form-label">Пароль</label>
                <input type="password" class="form-control" id="password" name="password" placeholder="Введите ваш пароль" required>
            </div>
            
            <button type="submit" class="btn btn-primary w-100 mb-3">Войти</button>
        </form>
        
        <div class="text-center mt-4">
            <p class="mb-0">Нет аккаунта? <a href="{% url 'register' %}" class="text-primary fw-bold">Регистрация</a></p>
        </div>
    </div>
    {% endblock %}
    
register.html
~~~~~~~~~~~~~

.. code-block:: html

    {% extends 'base.html' %}

    {% block title %}Регистрация - Корочки.есть{% endblock %}
    {% block description %}Создайте аккаунт для доступа к онлайн курсам{% endblock %}
    {% block keywords %}регистрация, аккаунт, запись на курсы{% endblock %}

    {% block content %}
    <div class="form-container">
        <h2>Регистрация</h2>

        <form method="post">
            {% csrf_token %}
            
            {% for field in form %}
            <div class="mb-3">
                <label for="{{ field.id_for_label }}" class="form-label">{{ field.label }}</label>
                {{ field }}
                {% if field.help_text %}
                    <div class="form-text text-muted small">{{ field.help_text }}</div>
                {% endif %}
                {% if field.errors %}
                    <div class="text-danger small mt-1">
                        {% for error in field.errors %}
                            {{ error }}
                        {% endfor %}
                    </div>
                {% endif %}
            </div>
            {% endfor %}
            
            <button type="submit" class="btn btn-primary w-100 mb-3">Создать пользователя</button>
        </form>
        
        <div class="text-center mt-4">
            <p class="mb-0">Уже есть аккаунт? <a href="{% url 'login' %}" class="text-primary fw-bold">Войти</a></p>
        </div>
    </div>

    <script>
    // Маска для телефона в формате 8(XXX)XXX-XX-XX
    document.addEventListener('DOMContentLoaded', function() {
        const phoneInput = document.getElementById('id_phone'); // Убедитесь, что ID совпадает с вашим полем формы
        if(phoneInput) {
            phoneInput.addEventListener('input', function(e) {
                let x = e.target.value.replace(/\D/g, '').match(/(\d{0,1})(\d{0,3})(\d{0,3})(\d{0,2})(\d{0,2})/);
                e.target.value = !x[2] ? x[1] : x[1] + '(' + x[2] + (x[3] ? ')' + x[3] : '') + (x[4] ? '-' + x[4] : '') + (x[5] ? '-' + x[5] : '');
            });
        }
    });
    </script>
    {% endblock %}

robots.txt и sitemap.xml
------------------------

robots.txt
~~~~~~~~~~

.. code-block:: text

    User-agent: *
    Allow: /
    Disallow: /admin/
    Disallow: /logout/

    Sitemap: http://127.0.0.1:8000/sitemap.xml

sitemap.xml
~~~~~~~~~~~

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
        <!-- Главная страница -->
        <url>
            <loc>http://127.0.0.1:8000/</loc>
            <lastmod>{% now "Y-m-d" %}</lastmod>
            <changefreq>daily</changefreq>
            <priority>1.0</priority>
        </url>
        
        <!-- Регистрация -->
        <url>
            <loc>http://127.0.0.1:8000/register/</loc>
            <lastmod>{% now "Y-m-d" %}</lastmod>
            <changefreq>monthly</changefreq>
            <priority>0.8</priority>
        </url>
        
        <!-- Вход -->
        <url>
            <loc>http://127.0.0.1:8000/login/</loc>
            <lastmod>{% now "Y-m-d" %}</lastmod>
            <changefreq>monthly</changefreq>
            <priority>0.7</priority>
        </url>
        
        <!-- Заявки -->
        <url>
            <loc>http://127.0.0.1:8000/applications/</loc>
            <lastmod>{% now "Y-m-d" %}</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.6</priority>
        </url>
        
        <!-- Создание заявки -->
        <url>
            <loc>http://127.0.0.1:8000/applications/create/</loc>
            <lastmod>{% now "Y-m-d" %}</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.6</priority>
        </url>
    </urlset>

CSS стили
---------

Основные стили находятся в файле :code:`static/css/style.css`. Файл содержит:

.. code-block:: css

    /* ===== ЦВЕТОВАЯ ПАЛИТРА ===== */
    :root {
        /* Основные цвета */
        --primary-blue: #168cc2;
        --primary-dark: #168cc2;
        --accent-green: #168cc2;
        --accent-orange: #ffffff;
        
        /* Нейтральные цвета */
        --light-gray: #f8f9fa;
        --medium-gray: #e9ecef;
        --dark-gray: #6c757d;
        --text-dark: #343a40;
        
        /* Статусы */
        --status-new: #168cc2;
        --status-progress: #ffc107;
        --status-completed: #6c757d;
    }

    /* ===== ОБЩИЕ СТИЛИ ===== */
    body {
        background-color: var(--light-gray);
        color: var(--text-dark);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        display: flex;
        flex-direction: column;
        min-height: 100vh;
    }

    main.container {
        flex: 1;
    }

    /* ===== НАВИГАЦИЯ ===== */
    .navbar {
        background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary-blue) 100%);
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        padding: 1rem 0;
    }

    .navbar-brand {
        font-weight: 700;
        font-size: 1.5rem;
        letter-spacing: -0.5px;
    }

    .nav-link {
        font-weight: 500;
        transition: color 0.3s ease;
        position: relative;
        padding: 0.5rem 1rem !important;
    }

    .nav-link:hover {
        color: var(--accent-orange) !important;
    }

    .navbar-nav .nav-link::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 1rem;
        right: 1rem;
        height: 2px;
        background-color: var(--accent-orange);
        transform: scaleX(0);
        transition: transform 0.3s ease;
    }

    .navbar-nav .nav-link:hover::after {
        transform: scaleX(1);
    }

    /* ===== КНОПКИ ===== */
    .btn {
        border-radius: 30px !important;
        padding: 0.6rem 1.5rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        border: none !important;
        position: relative;
        overflow: hidden;
        z-index: 1;
    }

    .btn::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, rgba(255,255,255,0.2), rgba(255,255,255,0));
        transition: left 0.3s ease;
        z-index: -1;
    }

    .btn:hover::before {
        left: 100%;
    }

    .btn-primary {
        background: linear-gradient(135deg, var(--primary-dark), var(--primary-blue));
        box-shadow: 0 4px 15px rgba(44, 90, 160, 0.3);
    }

    .btn-primary:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(44, 90, 160, 0.4);
    }

    .btn-success {
        background: linear-gradient(135deg, #168cc2, var(--accent-green));
    }

    .btn-outline-primary {
        background: transparent !important;
        border: 2px solid var(--primary-blue) !important;
        color: var(--primary-blue) !important;
    }

    .btn-outline-primary:hover {
        background: var(--primary-blue) !important;
        color: white !important;
    }

    .btn-outline-success {
        border: 2px solid var(--accent-green) !important;
        color: var(--accent-green) !important;
    }

    .btn-outline-success:hover {
        background: var(--accent-green) !important;
        color: white !important;
    }

    .btn-lg {
        padding: 0.8rem 2rem !important;
        font-size: 1.1rem !important;
    }

    /* ===== КАРТОЧКИ ===== */
    .card {
        border: none !important;
        border-radius: 15px !important;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08) !important;
        transition: transform 0.3s ease, box-shadow 0.3s ease !important;
        overflow: hidden;
    }

    .card:hover {
        transform: translateY(-5px) !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15) !important;
    }

    /* ===== ФОРМЫ ===== */
    .form-container {
        max-width: 500px;
        margin: 2rem auto;
        background: white;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        padding: 2.5rem;
    }

    .form-container h2 {
        text-align: center;
        margin-bottom: 2rem;
        color: var(--primary-dark);
        font-weight: 700;
    }

    .form-control {
        border: 2px solid var(--medium-gray) !important;
        border-radius: 12px !important;
        padding: 12px 15px !important;
        transition: all 0.3s ease !important;
    }

    .form-control:focus {
        border-color: var(--primary-blue) !important;
        box-shadow: 0 0 0 0.2rem rgba(44, 90, 160, 0.15) !important;
    }

    .form-label {
        font-weight: 600;
        color: var(--primary-dark);
        margin-bottom: 0.5rem;
    }

    /* Стили для вывода форм как параграфов (в create_application) */
    form p {
        margin-bottom: 1.5rem;
    }

    form p label {
        display: block;
        font-weight: 600;
        color: var(--primary-dark);
        margin-bottom: 0.5rem;
    }

    form p input,
    form p select,
    form p textarea {
        width: 100%;
        border: 2px solid var(--medium-gray);
        border-radius: 12px;
        padding: 12px 15px;
        transition: all 0.3s ease;
    }

    form p input:focus,
    form p select:focus,
    form p textarea:focus {
        border-color: var(--primary-blue);
        outline: none;
        box-shadow: 0 0 0 0.2rem rgba(44, 90, 160, 0.15);
    }

    /* ===== СТАТУСЫ ЗАЯВОК ===== */
    .application-card {
        border-left: none !important;
        position: relative;
    }

    .application-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
    }

    .application-new::before {
        background-color: var(--status-new);
    }

    .application-in-progress::before {
        background-color: var(--status-progress);
    }

    .application-completed::before {
        background-color: var(--status-completed);
    }

    .badge.bg-success { 
        background: linear-gradient(135deg, #28a745, #34ce57) !important; 
        padding: 0.5em 1em !important;
        border-radius: 20px !important;
        font-weight: 500 !important;
    }

    .badge.bg-warning { 
        background: linear-gradient(135deg, #ffc107, #ffdb6d) !important; 
        color: #856404 !important;
        padding: 0.5em 1em !important;
        border-radius: 20px !important;
        font-weight: 500 !important;
    }

    .badge.bg-secondary { 
        background: linear-gradient(135deg, #6c757d, #8f979f) !important; 
        padding: 0.5em 1em !important;
        border-radius: 20px !important;
        font-weight: 500 !important;
    }

    /* ===== ФУТЕР ===== */
    .footer {
        background-color: var(--primary-dark);
        color: white;
        margin-top: 4rem;
        padding: 2rem 0;
    }

    /* ===== УТИЛИТЫ ===== */
    .text-primary { 
        color: var(--primary-blue) !important; 
    }

    .bg-primary { 
        background-color: var(--primary-blue) !important; 
    }

    .border-primary { 
        border-color: var(--primary-blue) !important; 
    }

    /* Алерты */
    .alert-success {
        background: linear-gradient(135deg, rgba(40, 167, 69, 0.1), rgba(40, 167, 69, 0.2));
        border: none;
        border-left: 4px solid var(--accent-green);
        color: #155724;
        border-radius: 8px;
    }

    .alert-warning {
        background: linear-gradient(135deg, rgba(253, 126, 20, 0.1), rgba(253, 126, 20, 0.2));
        border: none;
        border-left: 4px solid var(--accent-orange);
        color: #856404;
        border-radius: 8px;
    }

    .alert-info {
        background: linear-gradient(135deg, rgba(23, 162, 184, 0.1), rgba(23, 162, 184, 0.2));
        border: none;
        border-left: 4px solid #17a2b8;
        color: #0c5460;
        border-radius: 8px;
    }

    /* ===== СЛАЙДЕР ===== */
    .slider-container {
        max-width: 900px !important;
        margin: 0 auto !important;
    }

    .carousel {
        border-radius: 20px !important;
        overflow: hidden !important;
        box-shadow: 0 15px 30px rgba(0,0,0,0.15) !important;
        position: relative;
    }

    .slider-image {
        height: 450px !important;
        object-fit: cover !important;
        width: 100% !important;
        transition: transform 0.5s ease;
    }

    .carousel-item:hover .slider-image {
        transform: scale(1.05);
    }

    /* Затемнение для лучшей читаемости текста */
    .carousel-item::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(to bottom, rgba(0,0,0,0.2), rgba(0,0,0,0.5));
        pointer-events: none;
    }

    .carousel-caption {
        text-align: left !important;
        bottom: 30px !important;
        left: 30px !important;
        right: 30px !important;
        padding: 20px !important;
        background: none !important;
        backdrop-filter: none !important;
        transform: none !important;
        width: auto !important;
    }

    .carousel-caption h5 {
        color: white !important;
        font-weight: 700 !important;
        margin-bottom: 10px !important;
        font-size: 2rem !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }

    .carousel-caption p {
        color: #f8f9fa !important;
        margin-bottom: 0 !important;
        font-size: 1.2rem !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
        opacity: 0.9;
    }

    /* Современные кнопки навигации */
    .carousel-control-prev,
    .carousel-control-next {
        width: 50px !important;
        height: 50px !important;
        background: white !important;
        border-radius: 50% !important;
        top: 50% !important;
        transform: translateY(-50%) scale(0.8) !important;
        margin: 0 20px !important;
        opacity: 0 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
    }

    .carousel:hover .carousel-control-prev,
    .carousel:hover .carousel-control-next {
        opacity: 1 !important;
        transform: translateY(-50%) scale(1) !important;
    }

    .carousel-control-prev:hover,
    .carousel-control-next:hover {
        background: var(--primary-blue) !important;
        transform: translateY(-50%) scale(1.1) !important;
        box-shadow: 0 6px 20px rgba(0,0,0,0.3) !important;
    }

    .carousel-control-prev {
        left: 20px !important;
    }

    .carousel-control-next {
        right: 20px !important;
    }

    .carousel-control-prev-icon,
    .carousel-control-next-icon {
        width: 25px !important;
        height: 25px !important;
        background-size: 25px 25px !important;
        filter: invert(1) !important;
    }

    .carousel-control-prev:hover .carousel-control-prev-icon,
    .carousel-control-next:hover .carousel-control-next-icon {
        filter: brightness(0) invert(1) !important;
    }

    /* Индикаторы (прогресс-бар) */
    .carousel-indicators {
        bottom: 20px !important;
        margin-bottom: 0 !important;
        gap: 8px;
    }

    .carousel-indicators button {
        width: 40px !important;
        height: 4px !important;
        border-radius: 4px !important;
        background-color: rgba(255,255,255,0.5) !important;
        border: none !important;
        margin: 0 !important;
        transition: all 0.3s ease !important;
    }

    .carousel-indicators button.active {
        width: 60px !important;
        background-color: white !important;
    }

    /* ===== АДАПТИВНОСТЬ ===== */
    @media (max-width: 768px) {
        .slider-image {
            height: 350px !important;
        }
        
        .carousel-caption h5 {
            font-size: 1.5rem !important;
        }
        
        .carousel-caption p {
            font-size: 1rem !important;
        }
        
        .carousel-control-prev,
        .carousel-control-next {
            width: 40px !important;
            height: 40px !important;
            margin: 0 10px !important;
            opacity: 1 !important;
            transform: translateY(-50%) scale(1) !important;
        }
        
        .form-container {
            margin: 1rem;
            padding: 1.5rem;
        }
        
        .btn-lg {
            width: 100%;
            margin-bottom: 10px;
        }
        
        .d-flex.justify-content-center .btn-lg {
            margin-bottom: 0;
            margin-right: 10px;
        }
        .d-flex.justify-content-center .btn-lg:last-child {
            margin-right: 0;
        }
    }

    @media (max-width: 390px) {
        .slider-image {
            height: 250px !important;
        }
        
        .carousel-caption {
            bottom: 15px !important;
            left: 15px !important;
            right: 15px !important;
            padding: 10px !important;
        }
        
        .carousel-caption h5 {
            font-size: 1.2rem !important;
        }
        
        .carousel-caption p {
            font-size: 0.9rem !important;
        }
        
        .carousel-indicators button {
            width: 30px !important;
        }
        
        .carousel-indicators button.active {
            width: 45px !important;
        }
        
        .navbar-brand {
            font-size: 1.3rem !important;
        }

    }

    /* ===== АДМИН-ПАНЕЛЬ ===== */
    .admin-container {
        max-width: 1400px;
        margin: 0 auto;
        background: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    }

    .admin-table {
        margin-bottom: 0;
    }

    .admin-table thead th {
        background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary-blue) 100%);
        color: white;
        border: none;
        padding: 1rem;
        font-weight: 600;
    }

    .admin-table tbody td {
        padding: 1rem;
        vertical-align: middle;
        border-bottom: 1px solid var(--medium-gray);
    }

    .admin-table tbody tr:hover {
        background-color: var(--light-gray);
        transition: background-color 0.3s ease;
    }

    /* Строки с разными статусами */
    .row-new {
        border-left: 4px solid var(--status-new);
    }

    .row-progress {
        border-left: 4px solid var(--status-progress);
    }

    .row-completed {
        border-left: 4px solid var(--status-completed);
    }

    /* Бейджи статусов для админки */
    .badge-new {
        background: linear-gradient(135deg, var(--status-new), var(--primary-blue)) !important;
        color: white;
        padding: 0.5em 1em;
        border-radius: 20px;
        font-weight: 500;
    }

    .badge-progress {
        background: linear-gradient(135deg, var(--status-progress), #ffdb6d) !important;
        color: #856404;
        padding: 0.5em 1em;
        border-radius: 20px;
        font-weight: 500;
    }

    .badge-completed {
        background: linear-gradient(135deg, var(--status-completed), #8f979f) !important;
        color: white;
        padding: 0.5em 1em;
        border-radius: 20px;
        font-weight: 500;
    }

    /* Кнопки админ-панели */
    .btn-review {
        background: linear-gradient(135deg, #17a2b8, #138496);
        color: white;
        border-radius: 30px;
        padding: 0.4rem 1rem;
        font-size: 0.85rem;
        font-weight: 600;
        transition: all 0.3s ease;
        border: none;
    }

    .btn-review:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(23, 162, 184, 0.3);
        color: white;
    }

    .btn-change-status {
        background: linear-gradient(135deg, var(--primary-dark), var(--primary-blue));
        color: white;
        border-radius: 30px;
        padding: 0.4rem 1rem;
        font-size: 0.85rem;
        font-weight: 600;
        transition: all 0.3s ease;
        border: none;
    }

    .btn-change-status:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(44, 90, 160, 0.3);
        color: white;
    }

    /* Стили для модальных окон админки */
    .admin-modal .modal-content {
        border-radius: 20px;
        border: none;
        box-shadow: 0 15px 40px rgba(0,0,0,0.15);
    }

    .admin-modal .modal-header {
        background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary-blue) 100%);
        color: white;
        border-radius: 20px 20px 0 0;
    }

    .admin-modal .modal-header .btn-close {
        filter: brightness(0) invert(1);
    }

    .admin-modal .modal-title {
        font-weight: 700;
    }

    .admin-modal .form-select {
        border: 2px solid var(--medium-gray);
        border-radius: 12px;
        padding: 10px 15px;
        transition: all 0.3s ease;
    }

    .admin-modal .form-select:focus {
        border-color: var(--primary-blue);
        box-shadow: 0 0 0 0.2rem rgba(44, 90, 160, 0.15);
        outline: none;
    }

    /* Стиль для отзыва в модальном окне */
    .review-content {
        background: linear-gradient(135deg, rgba(23, 162, 184, 0.1), rgba(23, 162, 184, 0.2)) !important;
    }

    .star-filled {
        color: #ffc107;
        font-size: 1.2rem;
    }

    .star-empty {
        color: var(--dark-gray);
        font-size: 1.2rem;
    }

    /* Адаптивность админ-панели */
    @media (max-width: 768px) {
        .admin-container {
            padding: 1rem;
            margin: 0.5rem;
        }
        
        .admin-table thead th {
            font-size: 0.85rem;
            padding: 0.75rem;
        }
        
        .admin-table tbody td {
            font-size: 0.85rem;
            padding: 0.75rem;
        }
        
        .btn-review,
        .btn-change-status {
            padding: 0.3rem 0.75rem;
            font-size: 0.75rem;
        }
    }

    @media (max-width: 576px) {
        .admin-table {
            font-size: 0.8rem;
        }
        
        .admin-table thead th,
        .admin-table tbody td {
            padding: 0.5rem;
        }
        
        .btn-review,
        .btn-change-status {
            display: block;
            width: 100%;
            margin-bottom: 5px;
        }
        
        .btn-review:last-child,
        .btn-change-status:last-child {
            margin-bottom: 0;
        }
        
        td .btn-review,
        td .btn-change-status {
            margin: 2px 0;
        }
    }

Запуск проекта
--------------

1. Создайте суперпользователя:

.. code-block:: bash

    python manage.py createsuperuser

2. Запустите сервер разработки:

.. code-block:: bash

    python manage.py runserver

3. Откройте браузер и перейдите по адресу: http://127.0.0.1:8000/