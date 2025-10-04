Views:

.. code-block:: python

    from django.shortcuts import render, redirect, get_object_or_404
    from django.contrib.auth import login, logout
    from django.contrib.auth.backends import ModelBackend
    from django.contrib.auth.decorators import login_required
    from django.db.models import Q
    from .forms import (
        CustomUserCreationForm, 
        PhoneAuthForm,
        EmailAuthForm,
        UsernameAuthForm,
        CartItemQuantityForm,
        OrderForm
    )
    from .models import (
        Category,
        Product,
        CartItem,
        Order,
        OrderItem
    )

    def contacts_view(request):
        return render(request, 'pages/contacts.html')

    def main_page(request):
        # Get popular products for display
        popular_products = Product.objects.all()[:8]
        context = {
            'popular_products': popular_products
        }
        return render(request, 'pages/main_page.html', context)

    def register_view(request):
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST, request.FILES)
            if form.is_valid():
                user = form.save()
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('main_page')
        else:
            form = CustomUserCreationForm()
        return render(request, 'components/register.html', {'form': form})

    def login_view(request):
        auth_type = request.POST.get('auth_type', request.GET.get('tab', 'username'))
        
        if request.method == 'POST':
            if auth_type == 'phone':
                form = PhoneAuthForm(request.POST)
            elif auth_type == 'email':
                form = EmailAuthForm(request.POST)
            else:
                form = UsernameAuthForm(request.POST)
            
            if form.is_valid():
                user = form.get_user()
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('main_page')
        else:
            if auth_type == 'phone':
                form = PhoneAuthForm()
            elif auth_type == 'email':
                form = EmailAuthForm()
            else:
                form = UsernameAuthForm()
        
        return render(request, 'components/login.html', {
            'form': form,
            'active_tab': auth_type
        })

    def logout_view(request):
        logout(request)
        return redirect('main_page')

    # 1. Каталог с фильтрацией
    def catalog_view(request):
        categories = Category.objects.all()
        
        # Получение фильтров из GET-параметров
        category_id = request.GET.get('category')
        search_query = request.GET.get('q')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        
        # Начинаем с полной выборки товаров
        products = Product.objects.all()
        
        # Применяем фильтры
        if category_id:
            products = products.filter(category_id=category_id)
        
        if search_query:
            products = products.filter(
                Q(name__icontains=search_query) | 
                Q(description__icontains=search_query)
            )
        
        if min_price:
            products = products.filter(price__gte=min_price)
        
        if max_price:
            products = products.filter(price__lte=max_price)
        
        context = {
            'categories': categories,
            'products': products,
            'selected_category': category_id,
            'search_query': search_query,
            'min_price': min_price,
            'max_price': max_price
        }
        
        return render(request, 'pages/catalog.html', context)

    def product_detail_view(request, product_id):
        product = get_object_or_404(Product, id=product_id)
        context = {'product': product}
        return render(request, 'pages/product_detail.html', context)

    # 2. Корзина
    @login_required
    def cart_view(request):
        cart_items = CartItem.objects.filter(user=request.user)
        
        # Подсчет общей суммы корзины
        total_amount = sum(item.get_total() for item in cart_items)
        
        context = {
            'cart_items': cart_items,
            'total_amount': total_amount
        }
        
        return render(request, 'pages/cart.html', context)

    @login_required
    def add_to_cart(request, product_id):
        product = get_object_or_404(Product, id=product_id)
        
        # Проверяем, нет ли уже такого товара в корзине
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': 1}
        )
        
        # Если товар уже был в корзине, увеличиваем количество
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        
        return redirect('cart')

    @login_required
    def update_cart_item(request, item_id):
        cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
        
        if request.method == 'POST':
            form = CartItemQuantityForm(request.POST, instance=cart_item)
            if form.is_valid():
                form.save()
        
        return redirect('cart')

    @login_required
    def remove_from_cart(request, item_id):
        cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
        cart_item.delete()
        return redirect('cart')

    # 4. Формирование заказа
    @login_required
    def checkout_view(request):
        cart_items = CartItem.objects.filter(user=request.user)
        if not cart_items.exists():
            return redirect('cart')
        total_amount = sum(item.get_total() for item in cart_items)
        if request.method == 'POST':
            form = OrderForm(request.POST)
            if form.is_valid():
                order = form.save(commit=False)
                order.user = request.user
                order.total_amount = total_amount
                order.save()
                for cart_item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        product=cart_item.product,
                        quantity=cart_item.quantity,
                        price=cart_item.product.price
                    )
                cart_items.delete()
                return redirect('order_success', order_id=order.id)
        else:
            initial_data = {
                'shipping_address': request.user.address,
                'phone': request.user.phone,
                'email': request.user.email
            }
            form = OrderForm(initial=initial_data)
        context = {
            'form': form,
            'cart_items': cart_items,
            'total_amount': total_amount
        }
        return render(request, 'pages/checkout.html', context)

    @login_required
    def order_success_view(request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        
        context = {
            'order': order
        }
        
        return render(request, 'pages/order_success.html', context)

    @login_required
    def orders_view(request):
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        
        context = {
            'orders': orders
        }
        
        return render(request, 'pages/orders.html', context)

    @login_required
    def order_detail_view(request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        order_items = OrderItem.objects.filter(order=order)
        
        context = {
            'order': order,
            'order_items': order_items
        }
        
        return render(request, 'pages/order_detail.html', context)

    @login_required
    def profile_view(request):
        user = request.user
        
        if request.method == 'POST':
            user.first_name = request.POST.get('first_name', user.first_name)
            user.last_name = request.POST.get('last_name', user.last_name)
            user.email = request.POST.get('email', user.email)
            user.phone = request.POST.get('phone', user.phone)
            user.address = request.POST.get('address', user.address)
            user.city = request.POST.get('city', user.city)
            user.country = request.POST.get('country', user.country)
            
            if 'avatar' in request.FILES:
                user.avatar = request.FILES['avatar']
                
            user.save()
            return redirect('profile')
        
        orders = Order.objects.filter(user=user).order_by('-created_at')
        
        context = {
            'user': user,
            'orders': orders
        }
        
        return render(request, 'pages/profile.html', context)

Urls:

.. code-block:: python

    from django.contrib import admin
    from django.urls import path
    from front import views
    from django.conf.urls.static import static
    from django.conf import settings

    urlpatterns = [
        # Администрирование и аутентификация
        path('admin/', admin.site.urls, name='admin'),
        path('', views.main_page, name='main_page'),
        path('register/', views.register_view, name='register'),
        path('login/', views.login_view, name='login'),
        path('logout/', views.logout_view, name='logout'),
        path('profile/', views.profile_view, name='profile'),
        
        # 1. Каталог товаров
        path('catalog/', views.catalog_view, name='catalog'),
        path('product/<int:product_id>/', views.product_detail_view, name='product_detail'),
        
        # 2. Корзина
        path('cart/', views.cart_view, name='cart'),
        path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
        path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
        path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
        
        # 3. Заказы
        path('checkout/', views.checkout_view, name='checkout'),
        path('order/success/<int:order_id>/', views.order_success_view, name='order_success'),
        path('orders/', views.orders_view, name='orders'),
        path('order/<int:order_id>/', views.order_detail_view, name='order_detail'),
        path('contacts/', views.contacts_view, name='contacts'),
    ]

    if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

Models:

.. code-block:: python
    from django.contrib.auth.models import AbstractUser
    from django.db import models
    from django.utils.translation import gettext_lazy as _

    class CustomUser(AbstractUser):
        # Переопределение стандартных полей
        first_name = models.CharField(
            _('first name'),
            max_length=150,
            null=True,
            blank=True
        )
        last_name = models.CharField(
            _('last name'),
            max_length=150,
            null=True,
            blank=True
        )
        
        # Дополнительные поля
        phone = models.CharField(
            _('phone number'),
            max_length=20,
            blank=True,
            null=True
        )
        
        address = models.TextField(
            _('address'),
            blank=True
        )
        
        age = models.IntegerField(
            _('age'),
            null=True,
            blank=True
        )
        
        birth_date = models.DateField(
            _('birth date'),
            null=True,
            blank=True
        )
        
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
        
        city = models.CharField(
            _('city'),
            max_length=100,
            blank=True
        )
        
        country = models.CharField(
            _('country'),
            max_length=100,
            blank=True
        )
        
        occupation = models.CharField(
            _('occupation'),
            max_length=100,
            blank=True
        )
        
        avatar = models.ImageField(
            _('avatar'),
            upload_to='avatars/',
            blank=True,
            null=True
        )
        
        class Meta:
            verbose_name = _('user')
            verbose_name_plural = _('users')
        
        def get_full_name(self):
            """Возвращает полное имя пользователя."""
            return f'{self.first_name} {self.last_name}'
        
        def __str__(self):
            full_name = self.get_full_name()
            if full_name.strip():
                return full_name
            return self.username

    # 1. Модели для каталога
    class Category(models.Model):
        name = models.CharField(_('name'), max_length=100, blank=True, null=True)
        description = models.TextField(_('description'), blank=True, null=True)
        image = models.ImageField(_('image'), upload_to='categories/', blank=True, null=True)
        
        class Meta:
            verbose_name = _('category')
            verbose_name_plural = _('categories')
        
        def __str__(self):
            return self.name or ''

    class Product(models.Model):
        name = models.CharField(_('name'), max_length=200, blank=True, null=True)
        description = models.TextField(_('description'), blank=True, null=True)
        price = models.DecimalField(_('price'), max_digits=10, decimal_places=2, blank=True, null=True)
        image = models.ImageField(_('image'), upload_to='products/', blank=True, null=True)
        category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name='products')
        created_at = models.DateTimeField(_('created at'), auto_now_add=True)
        
        class Meta:
            verbose_name = _('product')
            verbose_name_plural = _('products')
        
        def __str__(self):
            return self.name or ''

    # 2. Модель для корзины
    class CartItem(models.Model):
        user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='cart_items', blank=True, null=True)
        product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
        quantity = models.PositiveIntegerField(_('quantity'), default=1, blank=True, null=True)
        added_at = models.DateTimeField(_('added at'), auto_now_add=True)
        
        class Meta:
            verbose_name = _('cart item')
            verbose_name_plural = _('cart items')
        
        def __str__(self):
            return f"{self.quantity} x {self.product.name if self.product else ''}"
        
        def get_total(self):
            if self.product and self.product.price and self.quantity:
                return self.product.price * self.quantity
            return 0

    # 3. Модели для заказов
    class Order(models.Model):
        ORDER_STATUS_CHOICES = [
            ('pending', _('Pending')),
            ('processing', _('Processing')),
            ('shipped', _('Shipped')),
            ('delivered', _('Delivered')),
            ('cancelled', _('Cancelled')),
        ]
        
        user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name='orders', blank=True, null=True)
        status = models.CharField(_('status'), max_length=20, choices=ORDER_STATUS_CHOICES, default='pending', blank=True, null=True)
        created_at = models.DateTimeField(_('created at'), auto_now_add=True)
        shipping_address = models.TextField(_('shipping address'), blank=True, null=True)
        phone = models.CharField(_('phone'), max_length=20, blank=True, null=True)
        email = models.EmailField(_('email'), blank=True, null=True)
        total_amount = models.DecimalField(_('total amount'), max_digits=10, decimal_places=2, blank=True, null=True)
        
        class Meta:
            verbose_name = _('order')
            verbose_name_plural = _('orders')
        
        def __str__(self):
            return f"Order #{self.id} - {self.user.username if self.user else ''}"

    class OrderItem(models.Model):
        order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', blank=True, null=True)
        product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
        quantity = models.PositiveIntegerField(_('quantity'), default=1, blank=True, null=True)
        price = models.DecimalField(_('price'), max_digits=10, decimal_places=2, blank=True, null=True)
        
        class Meta:
            verbose_name = _('order item')
            verbose_name_plural = _('order items')
        
        def __str__(self):
            return f"{self.quantity} x {self.product.name if self.product else ''}"
        
        def get_total(self):
            if self.price and self.quantity:
                return self.price * self.quantity
            return

forms.py:

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

    class CustomUserCreationForm(UserCreationForm):
        phone = forms.CharField(
            widget=forms.TextInput(attrs={'placeholder': '+7XXXXXXXXXX'}),
            help_text='Введите номер телефона в формате +7XXXXXXXXXX'
        )
        
        class Meta:
            model = CustomUser
            fields = ('username', 'email', 'phone', 'first_name', 'last_name', 
                    'password1', 'password2', 'avatar')
        
        def clean_phone(self):
            phone = self.cleaned_data.get('phone')
            if phone:
                # Проверка формата номера телефона для России
                if not re.match(r'^\+7\d{10}$', phone):
                    raise ValidationError('Номер телефона должен быть в формате +7XXXXXXXXXX')
            return phone

    class PhoneAuthForm(forms.Form):
        phone = forms.CharField(
            widget=forms.TextInput(attrs={'placeholder': '+7XXXXXXXXXX'}),
            help_text='Введите номер телефона в формате +7XXXXXXXXXX'
        )
        password = forms.CharField(widget=forms.PasswordInput)

        def clean_phone(self):
            phone = self.cleaned_data.get('phone')
            if phone:
                # Проверка формата номера телефона для России
                if not re.match(r'^\+7\d{10}$', phone):
                    raise ValidationError('Номер телефона должен быть в формате +7XXXXXXXXXX')
            return phone

        def clean(self):
            cleaned_data = super().clean()
            phone = cleaned_data.get('phone')
            password = cleaned_data.get('password')

            if phone and password:
                self.user = authenticate(phone=phone, password=password)
                if self.user is None:
                    raise forms.ValidationError("Неверный телефон или пароль")
            return cleaned_data

        def get_user(self):
            return getattr(self, 'user', None)

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

    class CategoryForm(forms.ModelForm):
        class Meta:
            model = Category
            fields = ['name', 'description', 'image']

    class ProductForm(forms.ModelForm):
        class Meta:
            model = Product
            fields = ['name', 'description', 'price', 'image', 'category']

    class CartItemForm(forms.ModelForm):
        class Meta:
            model = CartItem
            fields = ['product', 'quantity']

    class CartItemQuantityForm(forms.ModelForm):
        class Meta:
            model = CartItem
            fields = ['quantity']

    class OrderForm(forms.ModelForm):
        phone = forms.CharField(
            widget=forms.TextInput(attrs={'placeholder': '+7XXXXXXXXXX'}),
            help_text='Введите номер телефона в формате +7XXXXXXXXXX'
        )
        class Meta:
            model = Order
            fields = ['shipping_address', 'phone', 'email']
        def clean_phone(self):
            phone = self.cleaned_data.get('phone')
            if phone:
                if not re.match(r'^\+7\d{10}$', phone):
                    raise ValidationError('Номер телефона должен быть в формате +7XXXXXXXXXX')
            return phone

backends.py:

.. code-block:: python

    from django.contrib.auth.backends import ModelBackend
    from django.contrib.auth import get_user_model
    from django.db.models import Q

    User = get_user_model()

    class MultiFieldAuthBackend(ModelBackend):
        def authenticate(self, request, username=None, password=None, **kwargs):
            # Если в kwargs есть email или phone, используем их вместо username
            if 'email' in kwargs:
                username = kwargs.get('email')
                field = 'email'
            elif 'phone' in kwargs:
                username = kwargs.get('phone')
                field = 'phone'
            else:
                field = 'username'

            if username is None or password is None:
                return None
                
            try:
                # Строим запрос на основе используемого поля
                if field == 'phone':
                    # Нормализация телефона (удаление пробелов, скобок, дефисов)
                    clean_phone = ''.join(c for c in username if c.isdigit() or c == '+')
                    user = User.objects.get(phone=clean_phone)
                elif field == 'email':
                    user = User.objects.get(email__iexact=username)
                else:
                    # Если это обычный логин или запрос с неизвестного поля,
                    # пробуем найти по всем полям
                    user = User.objects.get(
                        Q(phone=username) |
                        Q(email__iexact=username) |
                        Q(username=username)
                    )
                    
                if user.check_password(password):
                    return user
            except User.DoesNotExist:
                return None
            except User.MultipleObjectsReturned:
                # Если найдено несколько пользователей, возвращаем None для безопасности
                return None

        def get_user(self, user_id):
            try:
                return User.objects.get(pk=user_id)
            except User.DoesNotExist:
                return None


base.html:

.. code-block:: django

    {% load static %}
    <!DOCTYPE html>
    <html lang="ru" class="h-100">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{% block title %}МОЙ НЕ САМ{% endblock %}</title>
        <link rel="stylesheet" href="{% static 'bootstrap.min.css' %}">
        <link rel="stylesheet" href="{% static 'bootstrap-icons.css' %}">
        <link rel="stylesheet" href="{% static 'styles.css' %}">
        {% block extra_css %}{% endblock %}
    </head>

    <body class="d-flex flex-column h-100">
        {% include 'components/header.html' %}
        
        <main class="flex-grow-1">
            <div class="container mt-4">
                {% block content %}{% endblock %}
            </div>
        </main>
        
        <footer class="footer bg-light py-4 mt-auto">
            <div class="container">
                <div class="row">
                    <div class="col-md-6">
                        <h5>Контакты</h5>
                        <p>Телефон: +7 (123) 456-78-90</p>
                        <p>Email: info@example.com</p>
                    </div>
                    <div class="col-md-6 text-end">
                        <p>&copy; 2025 Магазин "МОЙ НЕ САМ". Все права защищены.</p>
                    </div>
                </div>
            </div>
        </footer>
        
        <script src="{% static 'bootstrap.bundle.min.js' %}"></script>
        {% block scripts %}{% endblock %}
    </body>

    </html>