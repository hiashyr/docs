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

    python manage.py startapp client

Далее создаем все необходимые папки шаблонов и статических файлов

Структура проекта должна выглядеть следующим образом (если каких-то файлов не хватает, то они создадутся в дальнейшем):

.. code-block:: text

   server/
   │   manage.py
   │   db.sqlite3
   │
   ├───client/
   │   ├───migrations/
   │   ├───templates/
   │   │       admin_panel.html
   │   │       application_create.html
   │   │       feedback.html
   │   │       index.html
   │   │       login.html
   │   │       profile_application.html
   │   │       register.html
   │   │       robots.txt
   │   │       sitemap.xml
   │   │   __init__.py
   │   │   admin.py
   │   │   apps.py
   │   │   forms.py
   │   │   models.py
   │   │   tests.py
   │   │   urls.py
   │   │   views.py
   │
   ├───server/
   │   │   __init__.py
   │   │   asgi.py
   │   │   settings.py
   │   │   urls.py
   │   │   wsgi.py
   │
   ├───static/
   │   ├───css/
   │   │       bootstrap.min.css (из папки с бутстрапом)
   │   │       style.css
   │   ├───img/
   │   │       logo.jpg
   │   │       slide-1.jpg
   │   │       slide-2.jpg
   │   │       slide-3.jpg
   │   └───js/
   │           bootstrap.bundle.min.js (из папки с бутстрапом)
   │
   └───templates/
           base.html

В этом моменте следует сделать первый коммит, чтобы зафиксировать структуру проекта и начать отслеживать изменения в коде.

Настройка проекта
-----------------

settings.py
------------

Открываем файл :code:`server/settings.py` и настраиваем проект:

.. code-block:: python

    from pathlib import Path

    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent.parent


    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = 'django-insecure-sb_4twnx6+^5ure(1@3ka8u0(!pqm2bp615hs0k@+4p$_)=1j*'

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True

    ALLOWED_HOSTS = []


    # Application definition

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'client'
    ]

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
            'DIRS': [BASE_DIR / 'templates'],
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
    # https://docs.djangoproject.com/en/6.0/ref/settings/#databases

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


    # Password validation
    # https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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

    AUTH_USER_MODEL = 'client.CustomUser'
    # Internationalization
    # https://docs.djangoproject.com/en/6.0/topics/i18n/

    LANGUAGE_CODE = 'ru-ru'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_TZ = True


    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/6.0/howto/static-files/

    STATIC_URL = 'static/'
    STATICFILES_DIRS = [BASE_DIR / 'static']

    STATIC_ROOT = BASE_DIR / 'staticfiles'  # Папка для collectstatic

    # Кэширование с версионированием файлов
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

models.py
---------

Создаем модели в файле :code:`client/models.py`:

.. code-block:: python

    from django.contrib.auth.models import AbstractUser
    from django.db import models
    from django.conf import settings
    import datetime


    class CustomUser(AbstractUser):
        username = models.CharField(
            max_length=150,
            unique=True,
            verbose_name='Логин'
        )
        first_name = models.CharField(
            max_length=150,
            verbose_name='Имя'
        )
        last_name = models.CharField(
            max_length=150,
            verbose_name='Фамилия'
        )
        patronymic = models.CharField(
            max_length=150,
            verbose_name='Отчество',
            blank=True,
            null=True
        )
        phone = models.CharField(
            max_length=20,
            verbose_name='Телефон'
        )
        email = models.EmailField(
            unique=True,
            verbose_name='Email'
        )

        REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'phone']

        def __str__(self):
            return self.username
        


    class Application(models.Model):
        COURSE_CHOICES = (
            ('algorithms', 'Основы алгоритмизации и программирования'),
            ('web_design', 'Основы веб-дизайна'),
            ('databases', 'Основы проектирования баз данных'),
        )

        PAYMENT_CHOICES = (
            ('cash', 'Наличными'),
            ('phone_transfer', 'Перевод по номеру телефона'),
        )

        #4
        STATUS_CHOICES = (
            ('new', 'Новая'),
            ('in_progress', 'Идет обучение'),
            ('completed', 'Обучение завершено'),
        )

        user = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
            verbose_name='Пользователь'
        )
        course = models.CharField(max_length=50, choices=COURSE_CHOICES, verbose_name='Курс')
        start_date = models.DateField(verbose_name='Дата начала обучения')
        
        payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, verbose_name='Способ оплаты')
        status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Статус')
        feedback = models.TextField(blank=True, null=True, verbose_name='Отзыв')
        created_at = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return f"{self.user.username} - {self.get_course_display()}"
        
        class Meta:
            verbose_name = 'Заявка'
            verbose_name_plural = 'Заявки'

Здесь стоит сделать второй коммит, чтобы зафиксировать создание моделей таблиц баз данных.

После создания моделей выполняем миграции:

.. code-block:: bash

    python manage.py makemigrations
    python manage.py migrate

forms.py
--------

Создаем файл :code:`client/forms.py` с формами:

.. code-block:: python

    import re
    from django import forms
    from django.contrib.auth.forms import UserCreationForm
    from .models import CustomUser, Application
    from django.utils import timezone


    class RegisterForm(UserCreationForm):
        username = forms.CharField(
            label='Логин',
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите логин'
            })
        )
        first_name = forms.CharField(
            label='Имя',
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите имя'
            })
        )
        last_name = forms.CharField(
            label='Фамилия',
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите фамилию'
            })
        )
        patronymic = forms.CharField(
            label='Отчество (необязательно)',
            required=False,
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите отчество'
            })
        )
        phone = forms.CharField(
            label='Телефон',
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '8(XXX)XXX-XX-XX'
            })
        )
        email = forms.EmailField(
            label='Email',
            widget=forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите Email'
            })
        )
        password1 = forms.CharField(
            label='Пароль',
            widget=forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите пароль'
            })
        )
        password2 = forms.CharField(
            label='Подтверждение пароля',
            widget=forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Повторите пароль'
            })
        )

        class Meta:
            model = CustomUser
            fields = (
                'username',
                'password1',
                'password2',
                'first_name',
                'last_name',
                'patronymic',
                'phone',
                'email',
            )

        def clean_username(self):
            username = self.cleaned_data['username']
            if not re.match(r'^[A-Za-z0-9]{6,}$', username):
                raise forms.ValidationError(
                    'Логин должен содержать минимум 6 символов (латиница и цифры)'
                )
            return username

        def clean_first_name(self):
            first_name = self.cleaned_data['first_name']
            if not re.match(r'^[А-Яа-яЁё\-]+$', first_name):
                raise forms.ValidationError(
                    'Имя должно содержать только кириллицу и дефис'
                )
            return first_name

        def clean_last_name(self):
            last_name = self.cleaned_data['last_name']
            if not re.match(r'^[А-Яа-яЁё\-]+$', last_name):
                raise forms.ValidationError(
                    'Фамилия должна содержать только кириллицу и дефис'
                )
            return last_name

        def clean_patronymic(self):
            patronymic = self.cleaned_data.get('patronymic')
            if patronymic and not re.match(r'^[А-Яа-яЁё\-]+$', patronymic):
                raise forms.ValidationError(
                    'Отчество должно содержать только кириллицу и дефис'
                )
            return patronymic

        def clean_phone(self):
            phone = self.cleaned_data['phone']
            if not re.match(r'^8\(\d{3}\)\d{3}-\d{2}-\d{2}$', phone): #8
                raise forms.ValidationError(
                    'Телефон должен быть в формате 8(XXX)XXX-XX-XX'
                )
            return phone
        


    class LoginForm(forms.Form):
        username = forms.CharField(
            label='Логин',
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите логин'
            })
        )
        password = forms.CharField(
            label='Пароль',
            widget=forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите пароль'
            })
        )


    class ApplicationForm(forms.ModelForm):
        start_date = forms.DateField(
            widget=forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date', 
                    'min': timezone.now().date().strftime('%Y-%m-%d'),
                }
            ),
            label='Дата начала обучения'
        )

        class Meta:
            model = Application
            fields = ['course', 'start_date', 'payment_method']
            widgets = {
                'course': forms.Select(attrs={'class': 'form-control'}),
                'payment_method': forms.Select(attrs={'class': 'form-control'}),
            }
            labels = {
                'course': 'Курс',
                'payment_method': 'Способ оплаты',
            }

        def clean_start_date(self):
            start_date = self.cleaned_data['start_date']
            if start_date < timezone.now().date():
                raise forms.ValidationError('Дата начала не может быть в прошлом')
            return start_date
        

    class FeedbackForm(forms.ModelForm):
        class Meta:
            model = Application
            fields = ['feedback']
            widgets = {
                'feedback': forms.Textarea(attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Напишите ваш отзыв о курсе'
                })
            }

views.py
--------

Создаем представления в файле :code:`client/views.py`:

.. code-block:: python

    from django.shortcuts import render, redirect, get_object_or_404
    from .forms import RegisterForm, LoginForm, ApplicationForm, FeedbackForm
    from django.contrib.auth.decorators import login_required, user_passes_test
    from django.contrib import messages 
    from django.core.paginator import Paginator
    from django.contrib.auth import authenticate, login, logout
    from .models import Application

    # Create your views here.
    def index_page(request):
        return render(request, 'index.html')

    def is_admin(user):
        return user.is_authenticated and user.is_superuser

    def login_page(request):
        error = None

        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']

                user = authenticate(
                    request,
                    username=username,
                    password=password
                )

                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    error = 'Неверный логин или пароль'
        else:
            form = LoginForm()

        return render(request, 'login.html', {
            'form': form,
            'error': error
        })

    def register(request):
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.save()
                messages.success(request, 'Регистрация прошла успешно')
                return redirect('login')
        else:
            form = RegisterForm()

        return render(request, 'register.html', {'form': form})

    def logout_func(request):
        logout(request)
        return redirect('home')


    @login_required
    def application_create(request):
        if request.method == 'POST':
            form = ApplicationForm(request.POST)
            if form.is_valid():
                application = form.save(commit=False)
                application.user = request.user
                application.save()
                return redirect('home')
        else:
            form = ApplicationForm()

        return render(request, 'application_create.html', {'form': form})


    @login_required
    def profile(request):
        applications = Application.objects.filter(user=request.user).order_by('-created_at')

        # 2
        
            
        return render(request, 'profile_application.html', {
            'applications': applications,
        })

    @login_required
    def feedback(request, app_id):
        application = get_object_or_404(
            Application,
            id=app_id,
            user=request.user,
            status='completed'
        )

        if request.method == 'POST':
            form = FeedbackForm(request.POST, instance=application)
            if form.is_valid():
                form.save()
                messages.success(request, 'Отзыв успешно сохранён')
                return redirect('profile_application')
        else:
            form = FeedbackForm(instance=application)

        return render(request, 'feedback.html', {
            'application': application,
            'form': form
        })

    @login_required
    @user_passes_test(is_admin)
    def admin_panel(request):
        applications = Application.objects.all().order_by('-created_at')

        status = request.GET.get('status')
        if status:
            applications = applications.filter(status=status)

        paginator = Paginator(applications, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'admin_panel.html', {
            'page_obj': page_obj,
            'status': status,
        })


    @login_required
    @user_passes_test(is_admin)
    def change_application_status(request, app_id):
        application = get_object_or_404(Application, id=app_id)

        if request.method == 'POST':
            new_status = request.POST.get('status')
            if new_status in ['in_progress', 'completed']: #4.
                application.status = new_status
                application.save()
                messages.success(request, 'Статус заявки успешно обновлён')

        return redirect('admin_panel')

    def sitemap_xml(request):
        return render(request, 'sitemap.xml', content_type='application/xml')

    def robots_txt(request):
        return render(request, 'robots.txt', content_type='text/plain')

urls.py
-------

Здесь стоит сделать третий коммит, чтобы зафиксировать создание серверной части.

Настраиваем URL-адреса. Сначала создаем :code:`client/urls.py`:

.. code-block:: python

    from django.urls import path
    from . import views

    urlpatterns = [
        path('', views.index_page, name='home'),
        path('login/', views.login_page, name='login'),
        path('register/', views.register, name='register'),
        path('logout/', views.logout_func, name='logout'),
        path('applicaton-profile/', views.profile, name='profile_application'),
        path('application-create/', views.application_create, name='application_create'),
        path('feedback/<int:app_id>/', views.feedback, name='feedback'),
        path('admin-panel/', views.admin_panel, name='admin_panel'),
        path('admin-panel/change-status/<int:app_id>', views.change_application_status, name='change_status'),

        path('sitemap.xml', views.sitemap_xml, name='sitemap'),
        path('robots.txt', views.robots_txt, name='robots_txt'),

    ]

Затем настраиваем главный :code:`server/urls.py`:

.. code-block:: python

    from django.contrib import admin
    from django.urls import path, include

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', include('client.urls'))
    ]

Шаблоны
-------

base.html
~~~~~~~~~

Базовый шаблон, который наследуют все остальные страницы:

.. code-block:: html

    {% load static %}
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <title>Корочки.есть — Подайте заявку и отслеживайте обучение</title>
        
        <!-- Описание страницы для SEO -->
        <meta name="description" content="Корочки.есть — онлайн-сервис для подачи заявок на курсы и отслеживания статуса обучения. Оставляйте отзывы и управляйте своими заявками.">

        <!-- Ключевые слова -->
        <meta name="keywords" content="корочки, онлайн курсы, заявки на обучение, отзывы, профиль, обучение, админ панель">

        <!-- Bootstrap -->
        <link rel="stylesheet" href="{% static 'css/bootstrap.min.css' %}">

        <!-- Свои стили -->
        <link rel="stylesheet" href="{% static 'css/style.css' %}">
    </head>
    <body>

    <header class="site-header">
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
            <div class="container">
                <a class="navbar-brand d-flex align-items-center" href="/">
                    <div class="brand-logo-wrapper">
                        <img src="{% static 'img/logo.jpg' %}" alt="Логотип" class="brand-logo">
                    </div>
                    Корочки.есть
                </a>

                <button class="navbar-toggler" type="button" data-bs-toggle="collapse"
                        data-bs-target="#mainNavbar">
                    <span class="navbar-toggler-icon"></span>
                </button>

                <div class="collapse navbar-collapse" id="mainNavbar">
                    <ul class="navbar-nav ms-auto mb-2 mb-lg-0">

                        {% if user.is_authenticated %}
                            <li class="nav-item">
                                <a class="nav-link" href="{% url 'home' %}">
                                    Главная
                                </a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link" href="{% url 'profile_application' %}">
                                    Профиль
                                </a>
                            </li>
                            {% if user.is_superuser %}
                                <a class="nav-link text-warning" href="{% url 'admin_panel' %}">
                                    Панель администратора
                                </a>
                            {% endif %}

                            <li class="nav-item">
                                <a class="nav-link" href="{% url 'application_create' %}">
                                    Подать заявку
                                </a>
                            </li>

                            <li class="nav-item">
                                <a class="nav-link text-warning" href="{% url 'logout' %}">
                                    Выйти
                                </a>
                            </li>
                        {% else %}
                            <li class="nav-item">
                                <a class="nav-link" href="{% url 'login' %}">
                                    Вход
                                </a>
                            </li>

                            <li class="nav-item">
                                <a class="nav-link" href="{% url 'register' %}">
                                    Регистрация
                                </a>
                            </li>
                        {% endif %}

                    </ul>
                </div>
            </div>
        </nav>
    </header>

    <main class="container mt-4">
        {% if messages %}
            <div class="container mt-3">
                {% for message in messages %}
                    <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
                        {{ message }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                {% endfor %}
            </div>
            {% endif %}
        {% block content %}
        {% endblock %}
    </main>

    <!-- Bootstrap -->
    <script src="{% static 'js/bootstrap.bundle.min.js' %}"></script>
    </body>
    </html>

В общем далее коммиты можно делтать по каждой странице, но лучше на этих страницах сразу менять мета-теги, и все остальное по теме

admin_panel.html
~~~~~~~~~~~~~~~~

.. code-block:: html

    {% extends 'base.html' %}

    {% block title %}Панель администратора{% endblock %}

    {% block content %}
    <div class="container mt-4">
        <h2 class="mb-3">Панель администратора</h2>

        <form method="get" class="filter-form">
            <select name="status" class="filter-select">
                <option value="">Все заявки</option>
                <option value="new" {% if status == 'new' %}selected{% endif %}>Новые</option>
                <option value="in_progress" {% if status == 'in_progress' %}selected{% endif %}>Идет обучение</option>
                <option value="completed" {% if status == 'completed' %}selected{% endif %}>Обучение завершено</option>
            </select>
            <button type="submit" class="btn-yellow ms-2">Фильтр</button>
        </form>

        {% comment %} #2 {% endcomment %}
            <!-- Вместо текущей формы со статусом добавьте: -->

        {% comment %} #2 {% endcomment %}

        {% for app in page_obj %}
            <div class="profile-card">
                <h5>{{ app.get_course_display }}</h5>
                <p><strong>Пользователь:</strong> {{ app.user.username }}</p>
                <p><strong>Дата начала:</strong> {{ app.start_date }}</p>
                <p><strong>Оплата:</strong> {{ app.get_payment_method_display }}</p>
                <p><strong>Статус:</strong> 
                    {% if app.status == 'new' %}
                        <span class="status-new">Новая</span>
                    {% elif app.status == 'in_progress' %}
                        <span class="status-in-progress">Идет обучение</span>
                    {% else %}
                        <span class="status-completed">Обучение завершено</span>
                    {% endif %}
                </p>

                <form method="post" action="{% url 'change_status' app.id %}" class="status-form">
                    {% csrf_token %}
                    <select name="status" class="filter-select">
                        <option value="in_progress">Идет обучение</option>
                        <option value="completed">Обучение завершено</option>
                    </select>
                    <button type="submit" class="btn-yellow ms-2">Изменить статус</button>
                </form>
            </div>
        {% empty %}
            <p>Заявок нет.</p>
        {% endfor %}

        <nav class="pagination-container">
            <ul class="pagination">
                {% if page_obj.has_previous %}
                    <li class="page-item">
                        <a class="page-link" href="?page={{ page_obj.previous_page_number }}{% if status %}&status={{ status }}{% endif %}">Назад</a>
                    </li>
                {% endif %}

                <li class="page-item active">
                    <span class="page-link">{{ page_obj.number }}</span>
                </li>

                {% if page_obj.has_next %}
                    <li class="page-item">
                        <a class="page-link" href="?page={{ page_obj.next_page_number }}{% if status %}&status={{ status }}{% endif %}">Вперёд</a>
                    </li>
                {% endif %}
            </ul>
        </nav>

        <!-- <nav class="pagination-container mt-3">
            <ul class="pagination">
                {% for i in page_obj.paginator.page_range %}
                    {% if page_obj.number == i %}
                        <li class="page-item active">
                            <span class="page-link">{{ i }}</span>
                        </li>
                    {% else %}
                        <li class="page-item">
                            <a class="page-link" href="?page={{ i }}{% if status %}&status={{ status }}{% endif %}">{{ i }}</a>
                        </li>
                    {% endif %}
                {% endfor %}
            </ul>
        </nav> -->
    </div>
    {% endblock %}

application_create.html
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: html

    {% extends 'base.html' %}

    {% block title %}Подать заявку{% endblock %}

    {% block content %}
    <div class="form-container">
        <h2 class="form-title">Подать заявку на обучение</h2>

        <form method="post" novalidate>
            {% csrf_token %}

            {% for field in form %}
                <div class="form-group">
                    <label class="form-label">{{ field.label }}</label>
                    {{ field }}
                    {% if field.errors %}
                        <div class="text-danger field-error">
                            {{ field.errors|striptags }}
                        </div>
                    {% endif %}
                </div>
            {% endfor %}

            <button type="submit" class="btn btn-register">
                Отправить
            </button>
        </form>
    </div>
    {% endblock %}
    
feedback.html
~~~~~~~~~~~~~

.. code-block:: html

    {% extends 'base.html' %}

    {% block title %}Отзыв{% endblock %}

    {% block content %}
    <div class="container mt-4" style="max-width: 600px;">
        <h3 class="mb-3">Отзыв о курсе</h3>

        <div class="mb-3">
            <strong>Курс:</strong> {{ application.get_course_display }}<br>
            <strong>Дата начала:</strong> {{ application.start_date }}
        </div>

        <form method="post">
            {% csrf_token %}

            <div class="mb-3">
                {{ form.feedback.label_tag }}
                <textarea name="feedback" class="feedback-textarea" rows="4" placeholder="Оставьте ваш отзыв">{{ form.feedback.value }}</textarea>
                {% if form.feedback.errors %}
                    <div class="text-danger mt-1">
                        {{ form.feedback.errors|striptags }}
                    </div>
                {% endif %}
            </div>

            <button type="submit" class="btn-feedback">
                Сохранить отзыв
            </button>
            <a href="{% url 'profile_application' %}" class="btn-feedback" style="background-color:#e5e7eb; color:#111827; border-color:#d1d5db;">
                Назад
            </a>
        </form>
    </div>
    {% endblock %}

    
index.html
~~~~~~~~~~

.. code-block:: html

    {% extends 'base.html' %}
    {% load static %}
    {% block title %}Главная{% endblock %}

    {% block content %}

    <!-- Приветственный блок -->
    <div class="welcome-section text-center">
        <h2 class="welcome-title">Добро пожаловать на платформу</h2>
        <p class="welcome-slogan">«Корочки.есть» — ваш надёжный проводник в мире дополнительного образования</p>
    </div>

    <div id="mainCarousel" class="carousel slide carousel-custom" data-bs-ride="carousel" data-bs-interval="5000">

        <!-- КРУГЛЫЕ ИНДИКАТОРЫ -->
        <div class="carousel-indicators circle-indicators">
            <button type="button" data-bs-target="#mainCarousel" data-bs-slide-to="0" class="active" aria-label="Слайд 1"></button>
            <button type="button" data-bs-target="#mainCarousel" data-bs-slide-to="1" aria-label="Слайд 2"></button>
            <button type="button" data-bs-target="#mainCarousel" data-bs-slide-to="2" aria-label="Слайд 3"></button>
        </div>

        <div class="carousel-inner">
            <!-- Слайд 1 -->
            <div class="carousel-item active">
                <div class="slide-overlay"></div>
                <img src="{% static 'img/slide-1.jpg' %}" class="d-block w-100" alt="Обучение онлайн">
                <div class="carousel-caption modern-caption">
                    <h1>Дополнительное профессиональное образование</h1>
                    <p>Получите востребованные знания онлайн с лучшими преподавателями</p>
                    <a href="#" class="slide-btn">Начать обучение</a>
                </div>
            </div>

            <!-- Слайд 2 -->
            <div class="carousel-item">
                <div class="slide-overlay"></div>
                <img src="{% static 'img/slide-2.jpg' %}" class="d-block w-100" alt="Курсы">
                <div class="carousel-caption modern-caption">
                    <h1>Практические курсы</h1>
                    <p>Алгоритмы, веб-дизайн, базы данных и многое другое</p>
                    <a href="#" class="slide-btn">Выбрать курс</a>
                </div>
            </div>

            <!-- Слайд 3 -->
            <div class="carousel-item">
                <div class="slide-overlay"></div>
                <img src="{% static 'img/slide-3.jpg' %}" class="d-block w-100" alt="Результат">
                <div class="carousel-caption modern-caption">
                    <h1>Результат, подтверждённый документом</h1>
                    <p>Обучение с удобной оплатой и гибкими сроками</p>
                    <a href="#" class="slide-btn">Узнать подробнее</a>
                </div>
            </div>
        </div>
        

        <!-- НОВЫЕ СТРЕЛКИ -->
        <button class="carousel-control-prev new-arrow" type="button" data-bs-target="#mainCarousel" data-bs-slide="prev">
            <span class="arrow-circle" aria-hidden="true">
                <svg class="arrow-icon" viewBox="0 0 24 24" width="24" height="24">
                    <path d="M15 18L9 12L15 6" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
            </span>
            <span class="visually-hidden">Предыдущий</span>
        </button>

        <button class="carousel-control-next new-arrow" type="button" data-bs-target="#mainCarousel" data-bs-slide="next">
            <span class="arrow-circle" aria-hidden="true">
                <svg class="arrow-icon" viewBox="0 0 24 24" width="24" height="24">
                    <path d="M9 18L15 12L9 6" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
            </span>
            <span class="visually-hidden">Следующий</span>
        </button>
    </div>

    <!-- Текст о сайте под слайдером -->
    <div class="about-site">
        <p class="about-text">
            «Корочки.есть» — это современная образовательная платформа, где каждый может получить 
            дополнительное профессиональное образование в удобном онлайн-формате.
        </p>
    </div>

    {% endblock %}

login.html
~~~~~~~~~~

.. code-block:: html

    {% extends 'base.html' %}

    {% block title %}Авторизация{% endblock %}

    {% block content %}
    <div class="form-container">
        <h2 class="form-title">Авторизация</h2>

        <form method="post" novalidate>
            {% csrf_token %}

            {% for field in form %}
                <div class="form-group">
                    <label class="form-label">{{ field.label }}</label>
                    {{ field }}

                    {% if field.errors %}
                        <div class="text-danger field-error">
                            {{ field.errors|striptags }}
                        </div>
                    {% endif %}
                </div>
            {% endfor %}

            {% if error %}
                <div class="text-danger field-error mb-3">
                    {{ error }}
                </div>
            {% endif %}

            <button type="submit" class="btn btn-register">
                Войти
            </button>
        </form>

        <p class="mt-3 text-center">
            Еще не зарегистрированы?
            <a href="{% url 'register' %}" class="link-login">
                Регистрация
            </a>
        </p>
    </div>
    {% endblock %}
    
profile_application.html
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: html

    {% extends 'base.html' %}

    {% block title %}Профиль{% endblock %}

    {% block content %}
    <div class="container mt-4">
        <!-- Блок с информацией о пользователе -->
        <div class="profile-card mb-4">
            <h4>Информация о пользователе</h4>
            <div class="row mt-3">
                <div class="col-md-6">
                    <p><strong>Имя пользователя:</strong> {{ user.username }}</p>
                    <p><strong>Email:</strong> {{ user.email }}</p>
                </div>
                <div class="col-md-6">
                    <p><strong>Имя:</strong> {{ user.first_name|default:"Не указано" }}</p>
                    <p><strong>Фамилия:</strong> {{ user.last_name|default:"Не указано" }}</p>
                </div>
            </div>
        </div>

        <h2>Мои заявки</h2>
        <!-- Блоки с заявками -->
        {% if applications %}
            {% for app in applications %}
                <div class="profile-card">
                    <h5>{{ app.get_course_display }}</h5>
                    <p>Дата начала: {{ app.start_date }}</p>
                    <p>Способ оплаты: {{ app.get_payment_method_display }}</p>
                    <p>Статус:
                        {% if app.status == 'new' %}
                            <span class="status-new">Новая</span>
                        {% elif app.status == 'in_progress' %}
                            <span class="status-in-progress">Идет обучение</span>
                        {% else %}
                            <span class="status-completed">Обучение завершено</span>
                        {% endif %}
                    </p>

                    <!-- Блок с отзывом -->
                    {% if app.feedback %}
                        <div class="feedback-block mt-3 p-3 bg-light rounded">
                            <h6 class="text-primary mb-2">
                                <i class="bi bi-chat-quote-fill"></i> Ваш отзыв:
                            </h6>
                            <p class="mb-0 fst-italic">"{{ app.feedback }}"</p>
                        </div>
                    {% endif %}

                    {% if app.status == 'completed' %}
                        <a href="{% url 'feedback' app.id %}"
                        class="btn-feedback mt-3">
                            {% if app.feedback %}
                                Редактировать отзыв
                            {% else %}
                                Оставить отзыв
                            {% endif %}
                        </a>
                    {% endif %}
                </div>
            {% endfor %}
        {% else %}
            <p>Вы ещё не подавали заявки.</p>
        {% endif %}
    </div>
    {% endblock %}
    
register.html
~~~~~~~~~~~~~

.. code-block:: html

    {% extends 'base.html' %}

    {% block title %}Регистрация{% endblock %}

    {% block content %}
    <div class="form-container">
        <h2 class="form-title">Регистрация</h2>

        <form method="post" novalidate>
            {% csrf_token %}

            {% for field in form %}
                <div class="form-group">
                    <label class="form-label">{{ field.label }}</label>
                    {{ field }}
                    {% if field.errors %}
                        <div class="text-danger field-error">
                            {{ field.errors|striptags }}
                        </div>
                    {% endif %}
                </div>
            {% endfor %}

            <button type="submit" class="btn btn-register">
                Зарегистрироваться
            </button>
        </form>

        <p class="mt-3 text-center">
            Уже зарегистрированы? 
            <a href="{% url 'login' %}" class="link-login">Войти</a>
        </p>
    </div>
    {% endblock %}

robots.txt и sitemap.xml
------------------------

robots.txt
~~~~~~~~~~

.. code-block:: text

    User-agent: *
    Disallow: /admin/
    Disallow: /logout/
    Disallow: /login/
    Disallow: /register/
    Allow: /

    Sitemap: http://127.0.0.1:8000/sitemap.xml

sitemap.xml
~~~~~~~~~~~

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">

        <!-- Главная страница -->
        <url>
            <loc>http://127.0.0.1:8000/</loc>
            <changefreq>daily</changefreq>
            <priority>1.0</priority>
        </url>

        <!-- Страница регистрации -->
        <url>
            <loc>http://127.0.0.1:8000/register/</loc>
            <changefreq>monthly</changefreq>
            <priority>0.8</priority>
        </url>

        <!-- Страница входа -->
        <url>
            <loc>http://127.0.0.1:8000/login/</loc>
            <changefreq>monthly</changefreq>
            <priority>0.8</priority>
        </url>

        <!-- Страница с заявками (профиль) -->
        <url>
            <loc>hhttp://127.0.0.1:8000/profile-application/</loc>
            <changefreq>weekly</changefreq>
            <priority>0.9</priority>
        </url>

        <!-- Панель администратора -->
        <url>
            <loc>http://127.0.0.1:8000/admin-panel/</loc>
            <changefreq>weekly</changefreq>
            <priority>0.7</priority>
        </url>

    </urlset>

CSS стили
---------

Основные стили находятся в файле :code:`static/css/style.css`. Файл содержит:

.. code-block:: css

    * {
    margin: 0;
    box-sizing: border-box;
    }

    body {
        background: linear-gradient(135deg, #e6f0fa, #b8d1e8);
        font-family: 'Segoe UI', Roboto, system-ui, sans-serif;
        min-height: 100vh;
    }

    /* ========== ШАПКА САЙТА ========== */
    .site-header {
        background: linear-gradient(120deg, #0b2b4f, #1e4b6e);
        box-shadow: 0 6px 18px rgba(0, 40, 80, 0.4);
        border-bottom: 3px solid #7ab7e0;
        position: sticky;
        top: 0;
        z-index: 1000;
    }

    .navbar {
        padding: 16px 24px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
    }

    .navbar-brand {
        font-size: 28px;
        font-weight: 800;
        color: #ffffff !important;
        text-decoration: none;
        letter-spacing: 1.2px;
        text-shadow: 0 2px 4px rgba(0, 20, 40, 0.5);
        background: rgba(255, 255, 255, 0.1);
        padding: 6px 18px;
        border-radius: 40px;
        backdrop-filter: blur(2px);
        transition: 0.3s;
    }

    .navbar-brand:hover {
        background: rgba(255, 255, 255, 0.25);
        color: #ffffff;
        transform: scale(1.02);
    }

    .navbar-nav {
        display: flex;
        gap: 10px;
        list-style: none;
        margin: 0;
        padding: 0;
    }

    .nav-item {
        margin: 0;
    }

    .nav-link {
        color: #f0f7ff !important;
        text-decoration: none;
        padding: 8px 20px;
        border-radius: 30px;
        font-weight: 500;
        font-size: 16px;
        transition: 0.25s;
        background: transparent;
        border: 1px solid transparent;
    }

    .nav-link:hover {
        background: rgba(255, 255, 255, 0.2);
        color: #ffffff !important;
        border-color: rgba(255, 255, 255, 0.3);
    }

    /* Активная страница — голубое свечение */
    .nav-link.active-page {
        background: #7ab7e0;
        color: #0b1f2f !important;
        font-weight: 700;
        border: 1px solid #c4e2ff;
        box-shadow: 0 0 12px rgba(122, 183, 224, 0.7);
    }

    .nav-link.text-warning {
        background: rgba(255, 255, 255, 0.15);
        border: 1px solid #c4e2ff;
        color: #ffffff !important;
    }

    .nav-link.text-warning:hover {
        background: #7ab7e0;
        color: #0b1f2f !important;
        border-color: #ffffff;
    }

    /* Обертка для логотипа*/
    .navbar-brand {
        display: flex;
        align-items: center;
        gap: 12px;
        font-size: 28px;
        font-weight: 800;
        color: #ffffff !important;
        text-decoration: none;
        letter-spacing: 1.2px;
        text-shadow: 0 2px 4px rgba(0, 20, 40, 0.5);
        background: rgba(255, 255, 255, 0.1);
        padding: 6px 18px;
        border-radius: 45px;
        backdrop-filter: blur(2px);
        transition: 0.3s;
    }

    /* Контейнер для изображения в кружке */
    .brand-logo-wrapper {
        width: 45px;
        height: 45px;
        border-radius: 50%;
        overflow: hidden;
        flex-shrink: 0;
        background-color: #ffffff;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }

    /* Само изображение */
    .brand-logo {
        width: 100%;
        height: 100%;
        object-fit: cover; /* Изображение заполнит кружок, обрезаясь если нужно */
        display: block;
    }

    @media (max-width: 768px) {
        .brand-logo-wrapper {
            width: 32px;
            height: 32px;
        }
        
        .navbar-brand {
            font-size: 22px;
            padding: 4px 12px;
            gap: 8px;
        }
    }

    /* ========== ОСНОВНОЙ КОНТЕЙНЕР ========== */
    main.container {
        background-color: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(8px);
        border-radius: 28px;
        padding: 36px;
        box-shadow: 0 20px 40px rgba(19, 57, 94, 0.25);
        margin: 36px auto;
        border: 1px solid rgba(255, 255, 255, 0.7);
    }

    /* ========== ПРИВЕТСТВЕННЫЙ БЛОК ========== */
    .welcome-section {
        margin-bottom: 40px;
        padding: 20px 20px 10px 20px;
        position: relative;
    }

    .welcome-title {
        font-size: 42px;
        font-weight: 800;
        color: #0b2b4f;
        margin-bottom: 15px;
        text-shadow: 0 2px 4px rgba(255, 255, 255, 0.8);
        letter-spacing: 1px;
        position: relative;
        display: inline-block;
        padding-bottom: 15px;
    }

    .welcome-title:after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 100px;
        height: 4px;
        background: linear-gradient(90deg, #1e6f9f, #7ab7e0, #1e6f9f);
        border-radius: 4px;
        box-shadow: 0 2px 6px rgba(30, 111, 159, 0.3);
    }

    .welcome-slogan {
        font-size: 24px;
        font-weight: 400;
        color: #1e4a6f;
        max-width: 800px;
        margin: 15px auto 0;
        line-height: 1.5;
        background: rgba(255, 255, 255, 0.7);
        padding: 12px 30px;
        border-radius: 50px;
        backdrop-filter: blur(4px);
        box-shadow: 0 4px 12px rgba(19, 57, 94, 0.1);
        border: 1px solid rgba(122, 183, 224, 0.3);
    }

    /* Адаптация для мобильных */
    @media (max-width: 768px) {
        .welcome-title {
            font-size: 32px;
        }
        
        .welcome-slogan {
            font-size: 18px;
            padding: 10px 20px;
        }
    }

    @media (max-width: 480px) {
        .welcome-title {
            font-size: 26px;
        }
        
        .welcome-slogan {
            font-size: 16px;
            padding: 8px 15px;
        }
    }

    /* ========== КАРУСЕЛЬ ========== */
    .carousel-custom {
        border-radius: 24px;
        overflow: hidden;
        box-shadow: 0 15px 30px rgba(19, 57, 94, 0.3);
        margin-bottom: 30px;
        position: relative;
        border: 2px solid rgba(122, 183, 224, 0.5);
    }

    .carousel-item {
        position: relative;
        height: 500px;
    }

    .carousel-item img {
        height: 500px;
        object-fit: cover;
        filter: brightness(0.7);
    }

    /* Голубое затемнение */
    .slide-overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, 
            rgba(11, 43, 79, 0.8), 
            rgba(30, 111, 159, 0.5));
        z-index: 1;
    }

    /* Текст в голубом стиле */
    .modern-caption {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        text-align: center;
        width: 80%;
        z-index: 2;
        color: #ffffff;
    }

    .modern-caption h1 {
        font-size: 48px;
        font-weight: 800;
        margin-bottom: 20px;
        text-shadow: 0 4px 15px rgba(0, 30, 60, 0.7);
        letter-spacing: 1px;
    }

    .modern-caption p {
        font-size: 22px;
        margin-bottom: 35px;
        opacity: 0.95;
        max-width: 700px;
        margin-left: auto;
        margin-right: auto;
        font-weight: 400;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
    }

    /* Голубая кнопка */
    .slide-btn {
        display: inline-block;
        padding: 16px 40px;
        background: linear-gradient(135deg, #1e6f9f, #3b8fc2);
        color: #ffffff;
        font-size: 20px;
        font-weight: 700;
        text-decoration: none;
        border-radius: 60px;
        transition: all 0.3s ease;
        border: 2px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 20px rgba(30, 111, 159, 0.4);
        letter-spacing: 0.5px;
    }

    .slide-btn:hover {
        background: linear-gradient(135deg, #0b4b73, #1e6f9f);
        transform: translateY(-4px) scale(1.02);
        box-shadow: 0 15px 30px rgba(11, 75, 115, 0.5);
        border-color: rgba(255, 255, 255, 0.6);
    }

    /* ===== КРУГЛЫЕ ИНДИКАТОРЫ ===== */
    .circle-indicators {
        bottom: 25px;
        z-index: 3;
        gap: 10px;
    }

    .circle-indicators button {
        width: 14px !important;
        height: 14px !important;
        border-radius: 50% !important;
        background-color: rgba(255, 255, 255, 0.4) !important;
        border: 2px solid transparent !important;
        margin: 0 6px !important;
        padding: 0 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
    }

    .circle-indicators button.active {
        background-color: #7ab7e0 !important;
        transform: scale(1.3);
        border-color: #ffffff !important;
        box-shadow: 0 0 15px rgba(122, 183, 224, 0.8);
    }

    .circle-indicators button:hover {
        background-color: rgba(122, 183, 224, 0.8) !important;
        transform: scale(1.2);
    }

    /* ===== СТРЕЛКИ В ГОЛУБОМ СТИЛЕ ===== */
    .new-arrow {
        width: 60px !important;
        height: 60px !important;
        top: 50%;
        transform: translateY(-50%);
        opacity: 0;
        transition: all 0.3s ease;
        z-index: 3;
    }

    .carousel-custom:hover .new-arrow {
        opacity: 1;
    }

    .arrow-circle {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 60px;
        height: 60px;
        background: rgba(11, 43, 79, 0.7);
        backdrop-filter: blur(4px);
        border-radius: 50%;
        border: 2px solid rgba(122, 183, 224, 0.7);
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }

    .arrow-icon {
        width: 30px;
        height: 30px;
        color: #7ab7e0;
        transition: all 0.3s ease;
    }

    .new-arrow:hover .arrow-circle {
        background: #1e6f9f;
        border-color: #ffffff;
        transform: scale(1.1);
        box-shadow: 0 0 20px rgba(122, 183, 224, 0.8);
    }

    .new-arrow:hover .arrow-icon {
        color: #ffffff;
        filter: drop-shadow(0 0 5px rgba(255, 255, 255, 0.5));
    }

    .carousel-control-prev.new-arrow {
        left: 20px;
    }

    .carousel-control-next.new-arrow {
        right: 20px;
    }

    css
    /* ========== ТЕКСТ О САЙТЕ ========== */
    .about-site {
        margin-top: 50px;
        margin-bottom: 30px;
        padding: 0 20px;
    }

    .about-text {
        font-size: 18px;
        line-height: 1.8;
        color: #1e3a5f;
        text-align: justify;
        max-width: 1000px;
        margin: 0 auto;
        background: rgba(255, 255, 255, 0.7);
        padding: 30px 40px;
        border-radius: 24px;
        backdrop-filter: blur(4px);
        box-shadow: 0 10px 30px rgba(19, 57, 94, 0.15);
        border: 1px solid rgba(122, 183, 224, 0.3);
        font-weight: 400;
        letter-spacing: 0.3px;
    }

    /* Адаптация для мобильных */
    @media (max-width: 768px) {
        .about-text {
            font-size: 16px;
            line-height: 1.7;
            padding: 20px 25px;
            border-radius: 20px;
        }
    }

    @media (max-width: 480px) {
        .about-text {
            font-size: 15px;
            line-height: 1.6;
            padding: 15px 20px;
            text-align: left; /* На маленьких экранах выравнивание по левому краю удобнее */
        }
    }

    /* ========== ФОРМЫ ========== */
    .form-container {
        max-width: 500px;
        margin: 40px auto;
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(10px);
        padding: 36px;
        border-radius: 32px;
        box-shadow: 0 20px 35px rgba(0, 60, 110, 0.3);
        border: 1px solid rgba(255,255,255,0.8);
    }

    .form-title {
        font-size: 32px;
        font-weight: 800;
        margin-bottom: 28px;
        text-align: center;
        color: #0b2b4f;
        text-shadow: 0 2px 4px rgba(255,255,255,0.7);
    }

    .form-group {
        margin-bottom: 22px;
    }

    .form-label {
        display: block;
        font-size: 16px;
        font-weight: 700;
        margin-bottom: 6px;
        color: #0b2b4f;
    }

    .form-control {
        width: 100%;
        padding: 12px 18px;
        font-size: 16px;
        border-radius: 40px;
        border: 1px solid #c9ddec;
        background: rgba(255,255,255,0.9);
        transition: 0.2s;
    }

    .form-control:focus {
        border-color: #1e6f9f;
        outline: none;
        box-shadow: 0 0 0 3px rgba(30, 111, 159, 0.3);
        background: #ffffff;
    }

    .field-error {
        font-size: 14px;
        margin-top: 6px;
        color: #b13e3e;
        font-weight: 500;
    }

    /* ========== КНОПКИ ========== */
    .btn-register {
        display: inline-block;
        width: 100%;
        padding: 14px 22px;
        font-size: 18px;
        font-weight: 700;
        background: #1e6f9f;
        border: none;
        border-radius: 50px;
        color: #ffffff;
        cursor: pointer;
        transition: 0.25s;
        text-align: center;
        text-decoration: none;
        border: 2px solid #7ab7e0;
    }

    .btn-register:hover {
        background: #0b4b73;
        color: #ffffff;
        transform: scale(1.02);
        box-shadow: 0 8px 18px rgba(0, 70, 120, 0.4);
        border-color: #ffffff;
    }

    .btn-yellow, .btn-feedback {
        display: inline-block;
        padding: 12px 24px;
        font-size: 16px;
        font-weight: 600;
        background: #ffffff;
        color: #0b2b4f;
        border: 2px solid #1e6f9f;
        border-radius: 40px;
        cursor: pointer;
        transition: 0.25s;
        text-decoration: none;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
    }

    .btn-yellow:hover, .btn-feedback:hover {
        background: #1e6f9f;
        color: #ffffff;
        border-color: #ffffff;
        transform: translateY(-2px);
        box-shadow: 0 8px 18px rgba(30, 111, 159, 0.4);
    }

    /* Ссылка в стиле кнопки */
    .link-login {
        color: #1e6f9f;
        font-weight: 700;
        text-decoration: none;
        border-bottom: 2px solid #7ab7e0;
        padding-bottom: 2px;
    }

    .link-login:hover {
        color: #0b2b4f;
        border-bottom-color: #0b2b4f;
    }

    /* ========== КАРТОЧКИ ========== */
    .card, .profile-card {
        background: #ffffff;
        border-radius: 28px;
        box-shadow: 0 12px 30px rgba(30, 111, 159, 0.15);
        padding: 22px;
        transition: 0.25s;
        border: 1px solid rgba(122, 183, 224, 0.4);
    }

    .card:hover, .profile-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 35px rgba(11, 43, 79, 0.25);
        border-color: #7ab7e0;
    }

    .card h5, .profile-card h5 {
        font-size: 20px;
        font-weight: 700;
        color: #0b2b4f;
        margin-bottom: 12px;
    }

    .card p, .profile-card p {
        font-size: 15px;
        color: #1f3a57;
        margin-bottom: 8px;
        line-height: 1.5;
    }

    /* ========== СТАТУСЫ ========== */
    .status-new {
        background: #3b82f6;
        color: #ffffff;
        padding: 4px 14px;
        border-radius: 50px;
        font-size: 13px;
        font-weight: 600;
        display: inline-block;
        box-shadow: 0 2px 6px rgba(59,130,246,0.4);
    }

    .status-in-progress {
        background: #fbbf24;
        color: #0b2b4f;
        padding: 4px 14px;
        border-radius: 50px;
        font-size: 13px;
        font-weight: 600;
        display: inline-block;
        box-shadow: 0 2px 6px rgba(251,191,36,0.5);
    }

    .status-completed {
        background: #10b981;
        color: #ffffff;
        padding: 4px 14px;
        border-radius: 50px;
        font-size: 13px;
        font-weight: 600;
        display: inline-block;
        box-shadow: 0 2px 6px rgba(16,185,129,0.4);
    }

    /* ========== ФИЛЬТРЫ ========== */
    .filter-form {
        margin-bottom: 28px;
        display: flex;
        gap: 20px;
        align-items: center;
        flex-wrap: wrap;
        background: rgba(255,255,255,0.5);
        padding: 18px 22px;
        border-radius: 60px;
        backdrop-filter: blur(4px);
    }

    .filter-select, select {
        padding: 10px 24px;
        border-radius: 40px;
        border: 1px solid #b8d1e8;
        background: #ffffff;
        font-size: 15px;
        font-weight: 500;
        color: #0b2b4f;
        outline: none;
        cursor: pointer;
    }

    .filter-select:focus, select:focus {
        border-color: #1e6f9f;
        box-shadow: 0 0 0 3px rgba(30,111,159,0.3);
    }

    /* ========== ПАГИНАЦИЯ ========== */
    .pagination-container {
        display: flex;
        justify-content: center;
        margin-top: 36px;
    }

    .pagination {
        display: flex;
        gap: 8px;
        list-style: none;
    }

    .pagination .page-link {
        display: block;
        padding: 10px 18px;
        border-radius: 40px;
        background: #ffffff;
        border: 1px solid #b8d1e8;
        text-decoration: none;
        color: #0b2b4f;
        font-weight: 600;
        transition: 0.2s;
    }

    .pagination .page-item.active .page-link {
        background: #1e6f9f;
        color: #ffffff;
        border-color: #1e6f9f;
        box-shadow: 0 4px 10px rgba(30,111,159,0.4);
    }

    .pagination .page-link:hover {
        background: #7ab7e0;
        border-color: #1e6f9f;
        color: #0b1f2f;
        transform: scale(1.05);
    }

    /* ========== ТЕКСТОВОЕ ПОЛЕ ========== */
    .feedback-textarea {
        width: 100%;
        padding: 16px 20px;
        font-size: 16px;
        border-radius: 32px;
        border: 1px solid #c9ddec;
        background: #ffffff;
        margin-bottom: 18px;
        transition: 0.2s;
    }

    .feedback-textarea:focus {
        border-color: #1e6f9f;
        outline: none;
        box-shadow: 0 0 0 3px rgba(30, 111, 159, 0.3);
    }

    /* ========== ЗАГОЛОВКИ ========== */
    h2 {
        color: #0b2b4f;
        font-weight: 800;
        font-size: 32px;
        margin-bottom: 24px;
        position: relative;
        display: inline-block;
    }

    h2:after {
        content: '';
        display: block;
        width: 70px;
        height: 4px;
        background: linear-gradient(90deg, #1e6f9f, #7ab7e0);
        border-radius: 4px;
        margin-top: 8px;
    }

    /* Адаптация */
    @media (max-width: 992px) {
        .carousel-item,
        .carousel-item img {
            height: 450px;
        }
        
        .modern-caption h1 {
            font-size: 38px;
        }
        
        .modern-caption p {
            font-size: 20px;
        }
        
        .slide-btn {
            padding: 14px 35px;
            font-size: 18px;
        }
    }

    @media (max-width: 768px) {
        .carousel-item,
        .carousel-item img {
            height: 400px;
        }
        
        .modern-caption h1 {
            font-size: 30px;
        }
        
        .modern-caption p {
            font-size: 18px;
            margin-bottom: 25px;
        }
        
        .slide-btn {
            padding: 12px 30px;
            font-size: 17px;
        }
        
        .new-arrow {
            width: 50px !important;
            height: 50px !important;
        }
        
        .arrow-circle {
            width: 50px;
            height: 50px;
        }
        
        .arrow-icon {
            width: 24px;
            height: 24px;
        }
        
        .circle-indicators button {
            width: 12px !important;
            height: 12px !important;
        }
    }

    @media (max-width: 576px) {
        .carousel-item,
        .carousel-item img {
            height: 350px;
        }
        
        .modern-caption h1 {
            font-size: 24px;
        }
        
        .modern-caption p {
            font-size: 16px;
            margin-bottom: 20px;
        }
        
        .slide-btn {
            padding: 10px 25px;
            font-size: 15px;
        }
        
        .new-arrow {
            width: 40px !important;
            height: 40px !important;
            opacity: 1;
        }
        
        .arrow-circle {
            width: 40px;
            height: 40px;
        }
        
        .arrow-icon {
            width: 20px;
            height: 20px;
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

3. Откройте браузер и перейдите по адресу: http://127.0.0.1:8000

Особенности проекта
-------------------

Права доступа
~~~~~~~~~~~~~

- Все пользователи могут просматривать главную страницу
- Только авторизованные пользователи могут:
  - Создавать заявки
  - Просматривать свой профиль
  - Оставлять отзывы (только для завершенных курсов)
- Только суперпользователи могут:
  - Доступ к панели администратора
  - Изменять статусы заявок
  - Фильтровать заявки по статусу

SEO оптимизация
~~~~~~~~~~~~~~~

- robots.txt ограничивает доступ к админке и служебным страницам
- sitemap.xml содержит все основные страницы сайта
- Мета-теги description и keywords на всех страницах

Заголовок раздела
-----------------

Пример ЕR-диаграммы:

.. image:: /_static/images/er.png
   :alt: Описание изображения
   :width: 600px
   :height: 400px
   :align: center

Памятка разработчика
====================

.. note::
    Этот раздел содержит быстрые справочные команды и важные напоминания для разработки и деплоя проекта.

Памятка разработчика
====================

Что точно нужно:
----------------

- удалить er-диаграмму
- удалить nado.txt
- заменить на сайте все, чтобы все было по теме
- поменять мета-теги
- поменять фотки на слайдере СРАЗУ
- создать админа ПО БУМАЖКЕ
- какой-либо доп. функционал оставить на самый конец 

1. Создание окружения
---------------------

команда:

.. code-block:: bash

    python -m venv venv

активация:

.. code-block:: bash

    venv\Scripts\activate

.. code-block:: bash

    pip install Django
    pip install Pillow
    pip install django-admin-interface

(Готовая админка admin.py:

.. code-block:: python

    # Импорт стандартных административных модулей Django
    from django.contrib import admin
    from django.contrib.auth.admin import UserAdmin
    from django.contrib.auth.models import Group
    # Импорт модели Theme из admin-interface
    from admin_interface.models import Theme
    # Импорт моделей приложения
    from .models import CustomUser, Application, Review

    # Удаление модели Theme из админки (admin-interface)
    admin.site.unregister(Theme)
    # Удаление модели Group из админки
    admin.site.unregister(Group)

    # Регистрация кастомной модели пользователя в админке
    admin.site.register(CustomUser)
    # Регистрация модели заявок в админке
    admin.site.register(Application)
    # Регистрация модели отзывов в админке
    admin.site.register(Review)

)

.. code-block:: bash

    cd server

2. Фильтрация записей для пользователя
--------------------------------------

файл :code:`profile_application.html`

.. code-block:: html

    <form method="get" class="mb-3">
        <select name="status" class="form-control" onchange="this.form.submit()">
            <option value="">Все заявки</option>
            <option value="new" {% if request.GET.status == 'new' %}selected{% endif %}>
                Новые
            </option>
            <option value="in_progress" {% if request.GET.status == 'in_progress' %}selected{% endif %}>
                Идёт обучение
            </option>
            <option value="completed" {% if request.GET.status == 'completed' %}selected{% endif %}>
                Завершённые
            </option>
        </select>
    </form>

файл :code:`views.py` 

найти "def profile"

.. code-block:: python

    @login_required
    def profile(request):
        applications = Application.objects.filter(user=request.user).order_by('-created_at')
        status = request.GET.get('status')
        if status:
            applications = applications.filter(status=status)

        applications = applications.order_by('-created_at')
            
        return render(request, 'profile_application.html', {
            'applications': applications,
        })

3. Изменение шрифтов
--------------------

в папке :code:`static` создаем папку :code:`fonts`

туда перекидываем файлы шрифтов

в папке :code:`fonts` появиться папка (условно она будет называться так) :code:`Great_Vibes`, потом если открыть эту папку будет файл :code:`GreatVibes-Regular.ttf`

и самое первое, что должно быть написано в :code:`style.css` это:

.. code-block:: css

    @font-face {
        font-family: 'Great_Vibes';
        src: url("../fonts/Great_Vibes/GreatVibes-Regular.ttf");
        font-weight: 400;
    }

а использование его будет так(с 8 строчки):

.. code-block:: css

    body {
        background: linear-gradient(135deg, #e6f0fa, #b8d1e8);
        min-height: 100vh;
        font-family: "Great_Vibes";
        font-weight: 400; 
    }

4. Изменение выборов в models
-----------------------------

файл :code:`models.py`

Сейчас поля выбора содержат одни значение, например: 

.. code-block:: python

    STATUS_CHOICES = (
        ('new', 'Новая'),
        ('in_progress', 'Идет обучение'),
        ('completed', 'Обучение завершено'),
    )

Можно заменить на другие, более универсальные, например:

.. code-block:: python

    STATUS_CHOICES = (
        ('pending', 'Новая'),
        ('processing', 'В работе'),
        ('done', 'Завершена'),
        ('cancelled', 'Отменена'),
    )

тогда в файле :code:`views.py` нужно использовать новые статусы:

.. code-block:: python

    if status in ['pending', 'processing', 'done', 'cancelled']:

5. Выкладывание на гит
----------------------

Чтобы создать репозиторий Git (через документацию):

В само приложение prob2 (не в сервер) добавляем файл :code:`.gitignore` (наполнение его в доке :code:`venv/` и :code:`nado.txt`)

Открыть консоль (…Desktop\prob2\server>) и прописать:

.. code-block:: bash

    git init 
    git status
    git add . 
    git commit -m "start_project"

– создание первого коммита, в конце написать то же самое, только в кавычках :code:`"finish_project"`

Когда я буду создавать второй коммит, то мне нужно будет прописать только:

.. code-block:: bash

    git add .
    git commit -m "finish_project"

6. Создание админа
------------------

Чтобы создать админа(на npm), нужно:

(…Desktop\123\korochki>):

.. code-block:: bash

    python manage.py createsuperuser

Логин: НА ЛИСТЕ

Пароль: НА ЛИСТЕ

Чтобы создать админа(на кастомной), нужно:

.. code-block:: bash

    python manage.py shell

.. code-block:: python

    from main.models import CustomUser
    CustomUser.objects.create_user()

ЭТО ДЛЯ ВОВИНОЙ:

(:code:`korochki/main/admin.py`)

Закомментировать 11 строку :code:`admin.site.unregister(Theme)` чтобы поменять цвета панели администратора

7. Создание миграций
--------------------

.. code-block:: bash

    python manage.py makemigrations И python manage.py migrate

8. Изменение паттерна номера телефона
-------------------------------------

файл :code:`forms.py`

Было: 

.. code-block:: python

    r'^8\(\d{3}\)\d{3}-\d{2}-\d{2}$'
    # 8(XXX)XXX-XX-XX

Стало:

.. code-block:: python

    r'^\+7\(\d{3}\)\d{3}-\d{2}-\d{2}$'
    # +7(XXX)XXX-XX-XX

    r'^\+\d{1,3} \d{3} \d{3} \d{2} \d{2}$'
    # +7 123 456 78 90

    r'^8 \d{3} \d{3} \d{2} \d{2}$'
    # 8 123 456 78 90

    r'^\d{11}$'
    # 81234567890

    r'^8-\d{3}-\d{3}-\d{2}-\d{2}$'
    # 8-123-456-78-90

    r'^8\(\d{3}\) \d{3}-\d{2}-\d{2}$'
    # 8(123) 456-78-90

    r'^[\+\d\s\(\)\-]{10,20}$'
    # +7 (123) 456-78-90

9. Создание и удаление админа
-----------------------------

.. code-block:: bash

    python manage.py createsuperuser

– создание

удаление всех файлов в :code:`migrations` (кроме :code:`__init__.py`) + удаление бд (:code:`db.sqlite3`)

а потом проведение новых миграций

10. Просмотр robots.txt и sitemap.xml
-------------------------------------

(в поисковой строке браузера)

- :code:`http://127.0.0.1:8000/robots.txt`
- :code:`http://127.0.0.1:8000/sitemap.xml`

11. Пример er-диаграммы
-----------------------

Расположение - :code:`static/img/image.png` (удалить после того как сделаю)

ОСНОВНЫЕ таблицы находятся в :code:`models.py`. Есть типы данных: :code:`varchar`(номер страницы, пароль), :code:`boolean`(пользователь(да\нет)), :code:`datetime`(дата записи), :code:`integer`(айди связанной таблицы), :code:`text`(описание). Связи: «Один к одному» (1:1), «Один ко многим» (1:N), «Многие ко многим» (M:N).

12. Добавление новых полей
--------------------------

Открыть файл :code:`models.py`

импорты которые должны быть в начале файла:

.. code-block:: python

    from django.contrib.auth.models import AbstractUser
    from django.db import models
    from django.conf import settings
    import datetime

Найти таблицу :code:`Application`

после строчки (строчка показана ниже) добавить новые поля

.. code-block:: python

    start_date = models.DateField(verbose_name='Дата начала обучения')

    # НОВЫЕ ПОЛЯ
    # время
    start_time = models.TimeField(
        verbose_name='Время начала',
        default=datetime.time(9, 0),  # По умолчанию 9:00
        help_text='Выберите удобное время начала занятий'
    )
    # текст
    comment = models.TextField(
        verbose_name='Комментарий',
        blank=True,
        null=True,
        help_text='Дополнительная информация или пожелания'
    )
    # число
    hours_count = models.PositiveIntegerField(
        verbose_name='Количество часов',
        default=40,
        help_text='Желаемое количество учебных часов'
    )    

Далее открыть файл :code:`forms.py`

импорты которые должны быть в начале файла:

.. code-block:: python

    import re
    from django import forms
    from django.contrib.auth.forms import UserCreationForm
    from .models import CustomUser, Application
    from django.utils import timezone
    import datetime

В этом файле найти форму (:code:`class ApplicationForm`) и сделать, чтобы она выглядела вот так:

.. code-block:: python

    class ApplicationForm(forms.ModelForm):
        start_date = forms.DateField(
            widget=forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date', 
                    'min': timezone.now().date().strftime('%Y-%m-%d'),
                }
            ),
            label='Дата начала обучения'
        )
        
        # НОВЫЕ ПОЛЯ
        start_time = forms.TimeField(
            widget=forms.TimeInput(
                attrs={
                    'class': 'form-control',
                    'type': 'time',
                }
            ),
            label='Время начала',
            initial=datetime.time(9, 0),
            help_text='Выберите удобное время (с 8:00 до 20:00)'
        )
        
        comment = forms.CharField(
            widget=forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3, # Количество строк доступных
                    'placeholder': 'Напишите ваши пожелания, вопросы или дополнительную информацию...',
                }
            ),
            label='Комментарий', # Заголовок
            required=False, # Количество строк доступных
            help_text='Необязательное поле'
        )
        
        hours_count = forms.IntegerField(
            widget=forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': '10', # Мин значение
                    'max': '200', # Макс значение
                    'step': '10', # Кратно 10
                    'placeholder': 'Введите количество часов',
                }
            ),
            label='Количество часов',
            initial=40, # Базовое количество
            help_text='От 10 до 200 часов (кратно 10)'
        )

        class Meta:
            model = Application
            fields = ['course', 'start_date', 'start_time', 'hours_count', 'comment', 'payment_method']
            widgets = {
                'course': forms.Select(attrs={'class': 'form-control'}),
                'payment_method': forms.Select(attrs={'class': 'form-control'}),
            }
            labels = {
                'course': 'Курс',
                'payment_method': 'Способ оплаты',
            }

        def clean_start_date(self):
            start_date = self.cleaned_data['start_date']
            if start_date < timezone.now().date():
                raise forms.ValidationError('Дата начала не может быть в прошлом')
            return start_date
        
        # НОВЫЕ ВАЛИДАЦИИ
        def clean_start_time(self):
            start_time = self.cleaned_data['start_time']
            # Проверяем, что время в рабочем диапазоне (8:00 - 20:00)
            if start_time < datetime.time(8, 0) or start_time > datetime.time(20, 0):
                raise forms.ValidationError('Время должно быть между 8:00 и 20:00')
            return start_time
        
        def clean_hours_count(self):
            hours = self.cleaned_data['hours_count']
            if hours < 10:
                raise forms.ValidationError('Минимальное количество часов - 10')
            if hours > 200:
                raise forms.ValidationError('Максимальное количество часов - 200')
            if hours % 10 != 0:
                raise forms.ValidationError('Количество часов должно быть кратно 10')
            return hours

Далее переходим в :code:`profile_application.html`

Там редактировать блок "Блоки с заявками"

.. code-block:: html

    <!-- Блоки с заявками -->
    {% if applications %}
        {% for app in applications %}
            <div class="profile-card">
                <h5>{{ app.get_course_display }}</h5>
                <p>Дата начала: {{ app.start_date }}</p>
                <p>Время начала: {{ app.start_time|time:"H:i" }}</p>
                <p>Количество часов: {{ app.hours_count }}</p>
                <p>Способ оплаты: {{ app.get_payment_method_display }}</p>
                <p>Статус:
                    {% if app.status == 'new' %}
                        <span class="status-new">Новая</span>
                    {% elif app.status == 'in_progress' %}
                        <span class="status-in-progress">Идет обучение</span>
                    {% else %}
                        <span class="status-completed">Обучение завершено</span>
                    {% endif %}
                </p>

                {% if app.comment %}
                    <p><strong>Комментарий:</strong> {{ app.comment }}</p>
                {% endif %}

Редактировать только его. Дальше блок с отзывами и всё остальное остается как есть.

В файле :code:`admin_panel.html` найти цикл :code:`{% for app in page_obj %}`

Заменить его начало:

.. code-block:: html

    {% for app in page_obj %}
        <div class="profile-card">
            <h5>{{ app.get_course_display }}</h5>
            <p><strong>Пользователь:</strong> {{ app.user.username }} ({{ app.user.email }})</p>
            <p><strong>Дата начала:</strong> {{ app.start_date }}</p>
            <p><strong>Время начала:</strong> {{ app.start_time|time:"H:i" }}</p>
            <p><strong>Количество часов:</strong> {{ app.hours_count }}</p>
            <p><strong>Оплата:</strong> {{ app.get_payment_method_display }}</p>
            
            {% if app.comment %}
                <div class="comment-block mt-2 mb-3 p-3 bg-light rounded">
                    <strong>Комментарий пользователя:</strong>
                    <p class="mb-0 mt-1">{{ app.comment }}</p>
                </div>
            {% endif %}
            
            {% if app.feedback %}
                <div class="feedback-block mt-2 mb-3 p-3 bg-light rounded">
                    <strong>Отзыв пользователя:</strong>
                    <p class="mb-0 mt-1 fst-italic">"{{ app.feedback }}"</p>
                </div>
            {% endif %}

Далее "Статус" (:code:`<p><strong>Статус:</strong>`) и все остальное остаются без изменений.

Создать миграции:

.. code-block:: bash

    python manage.py makemigrations
    python manage.py migrate

13. Для подключение бустрапа
----------------------------

в папке :code:`static` проекта должны быть папки :code:`css` и :code:`js`.

Скачать архив с бутстрапом, в нем найти папку :code:`css`, а в ней :code:`bootstrap.min.css` и перенести этот файл (в папке static) в папку :code:`css` проекта

Найти папку :code:`js`, в ней, :code:`bootstrap.bundle.min.js` и перенести этот файл (в папке static) в папку :code:`js` проекта

в начале файла :code:`base.html` указать:

.. code-block:: html

    <!-- Bootstrap -->
    <link rel="stylesheet" href="{% static 'css/bootstrap.min.css' %}">

в конце файла указать:

.. code-block:: html

    <!-- Bootstrap -->
    <script src="{% static 'js/bootstrap.bundle.min.js' %}"></script>

Чтобы проверить, что бутстрап подключен правильно 

обновить страницу (:code:`ctrl + fn + f5`).

14. Удаление бд
---------------

Чтобы удалить данные с бд нужно:

Удалить файл :code:`db.sqlite3` и все миграции из папки :code:`migrations` (КРОМЕ :code:`__init__.py`!!!)

Провести новые миграции:

.. code-block:: bash

    python manage.py makemigrations
    python manage.py migrate

15. Изменение длины логина
--------------------------

открыть :code:`forms.py` стр.82 там изменить цифру.

16. Добавление слайдов
----------------------

Чтобы добавились слайды в слайдер нужно перенести картинки в папку :code:`static`, а в ней в папку :code:`img` с именами :code:`slide-1.jpg`, :code:`slide-2.jpg` и тд.

.. image:: /_static/images/er.png
   :alt: Альтернативное описание изображения