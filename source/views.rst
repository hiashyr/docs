Создание представлений (Views)
==============================

В этом разделе мы создадим представления для нашего магазина цветов. Представления обрабатывают запросы пользователей и возвращают ответы. У нас есть три приложения с разными типами представлений.

Представления для основного приложения (main)
---------------------------------------------

Эти представления отвечают за отображение страниц магазина: главная, каталог, товары, контакты.

**main/views.py:**

.. code-block:: python
   :linenos:

   from django.shortcuts import render, get_object_or_404
   from django.db.models import Q
   from .models import Product, Category, SliderImage, Contact


   def home(request):
       """Главная страница"""
       slider_images = SliderImage.objects.filter(is_active=True).order_by('order')
       popular_products = Product.objects.filter(is_available=True).order_by('-created_at')[:4]
       context = {
           'slider_images': slider_images,
           'popular_products': popular_products,
       }
       return render(request, 'main/home.html', context)


   def catalog(request):
       """Страница каталога"""
       products = Product.objects.filter(is_available=True)
       categories = Category.objects.all()
       
       # Фильтрация по категории
       category_id = request.GET.get('category')
       if category_id:
           products = products.filter(category_id=category_id)
       
       # Сортировка
       sort_by = request.GET.get('sort')
       if sort_by == 'year':
           products = products.order_by('-year')
       elif sort_by == 'name':
           products = products.order_by('name')
       elif sort_by == 'price':
           products = products.order_by('price')
       else:
           products = products.order_by('-created_at')  # По умолчанию по новизне
       
       context = {
           'products': products,
           'categories': categories,
           'current_category': category_id,
           'current_sort': sort_by,
       }
       return render(request, 'main/catalog.html', context)


   def product_detail(request, product_id):
       """Страница товара"""
       product = get_object_or_404(Product, id=product_id, is_available=True)
       similar_products = Product.objects.filter(
           category=product.category, 
           is_available=True
       ).exclude(id=product.id)[:4]
       
       context = {
           'product': product,
           'similar_products': similar_products,
       }
       return render(request, 'main/product_detail.html', context)


   def contacts(request):
       """Страница контактов"""
       contact_info = Contact.objects.first()
       context = {
           'contact_info': contact_info,
       }
       return render(request, 'main/contacts.html', context)

Особенности представлений main:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- **home**: Отображает слайдер и популярные товары
- **catalog**: Поддерживает фильтрацию по категориям и сортировку
- **product_detail**: Показывает детальную информацию о товаре и похожие товары
- **contacts**: Отображает контактную информацию

Представления для приложения заказов (orders)
---------------------------------------------

Эти представления управляют корзиной и заказами.

**orders/views.py:**

.. code-block:: python
   :linenos:

   from django.shortcuts import render, redirect, get_object_or_404
   from django.contrib.auth.decorators import login_required
   from django.contrib import messages
   from django.http import JsonResponse
   from django.views.decorators.http import require_http_methods
   from django.db import transaction
   from .models import Cart, Order, OrderItem
   from .forms import OrderConfirmationForm, OrderStatusForm
   from main.models import Product


   @login_required
   def cart_view(request):
       """Корзина пользователя"""
       cart_items = Cart.objects.filter(user=request.user)
       total_price = sum(item.get_total_price() for item in cart_items)
       
       context = {
           'cart_items': cart_items,
           'total_price': total_price,
       }
       return render(request, 'orders/cart.html', context)


   @login_required
   @require_http_methods(["POST"])
   def add_to_cart(request, product_id):
       """Добавление товара в корзину"""
       product = get_object_or_404(Product, id=product_id, is_available=True)
       quantity = int(request.POST.get('quantity', 1))
       
       if quantity > product.stock_quantity:
           return JsonResponse({
               'success': False, 
               'message': f'Недостаточно товара на складе. Доступно: {product.stock_quantity}'
           })
       
       cart_item, created = Cart.objects.get_or_create(
           user=request.user,
           product=product,
           defaults={'quantity': quantity}
       )
       
       if not created:
           if cart_item.quantity + quantity > product.stock_quantity:
               return JsonResponse({
                   'success': False,
                   'message': f'Недостаточно товара на складе. Доступно: {product.stock_quantity}'
               })
           cart_item.quantity += quantity
           cart_item.save()
       
       return JsonResponse({
           'success': True,
           'message': 'Товар добавлен в корзину'
       })


   @login_required
   @require_http_methods(["POST"])
   def update_cart_item(request, cart_item_id):
       """Обновление количества товара в корзине"""
       cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
       quantity = int(request.POST.get('quantity', 1))
       
       if quantity <= 0:
           cart_item.delete()
           return JsonResponse({'success': True, 'message': 'Товар удален из корзины'})
       
       if quantity > cart_item.product.stock_quantity:
           return JsonResponse({
               'success': False,
               'message': f'Недостаточно товара на складе. Доступно: {cart_item.product.stock_quantity}'
           })
       
       cart_item.quantity = quantity
       cart_item.save()
       
       return JsonResponse({'success': True, 'message': 'Количество обновлено'})


   @login_required
   @require_http_methods(["POST"])
   def remove_from_cart(request, cart_item_id):
       """Удаление товара из корзины"""
       cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
       cart_item.delete()
       return JsonResponse({'success': True, 'message': 'Товар удален из корзины'})


   @login_required
   def checkout(request):
       """Оформление заказа"""
       cart_items = Cart.objects.filter(user=request.user)
       
       if not cart_items.exists():
           messages.warning(request, 'Корзина пуста')
           return redirect('cart')
       
       if request.method == 'POST':
           form = OrderConfirmationForm(request.user, request.POST)
           if form.is_valid():
               with transaction.atomic():
                   # Создаем заказ
                   order = Order.objects.create(user=request.user)
                   
                   # Добавляем товары в заказ
                   for cart_item in cart_items:
                       OrderItem.objects.create(
                           order=order,
                           product=cart_item.product,
                           quantity=cart_item.quantity,
                           price=cart_item.product.price
                       )
                       
                       # НЕ уменьшаем количество на складе - это будет происходить только при подтверждении заказа
                   
                   # Очищаем корзину
                   cart_items.delete()
                   
                   messages.success(request, 'Заказ успешно оформлен!')
                   return JsonResponse({'success': True, 'message': 'Заказ успешно оформлен!', 'redirect': '/auth/profile/'})
       else:
           form = OrderConfirmationForm(request.user)
       
       total_price = sum(item.get_total_price() for item in cart_items)
       
       context = {
           'form': form,
           'cart_items': cart_items,
           'total_price': total_price,
       }
       return render(request, 'orders/checkout.html', context)


   @login_required
   @require_http_methods(["POST"])
   def cancel_order(request, order_id):
       """Отмена заказа пользователем"""
       order = get_object_or_404(Order, id=order_id, user=request.user, status='new')
       
       with transaction.atomic():
           # Возвращаем товары на склад
           for item in order.orderitem_set.all():
               item.product.stock_quantity += item.quantity
               item.product.save()
           
           # Отменяем заказ
           order.status = 'cancelled'
           order.cancellation_reason = 'Отменен пользователем'
           order.save()
       
       messages.success(request, 'Заказ отменен')
       return redirect('profile')

Особенности представлений orders:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- **cart_view**: Показывает содержимое корзины
- **add_to_cart**: AJAX-функция для добавления товаров
- **update_cart_item**: AJAX-функция для обновления количества
- **remove_from_cart**: AJAX-функция для удаления товаров
- **checkout**: Оформление заказа с транзакцией
- **cancel_order**: Отмена заказа с возвратом товаров на склад

Представления для аутентификации (user_auth)
--------------------------------------------

Эти представления управляют регистрацией, авторизацией и профилем пользователя.

**user_auth/views.py:**

.. code-block:: python
   :linenos:

   from django.shortcuts import render, redirect
   from django.contrib.auth import login, logout
   from django.contrib.auth.decorators import login_required
   from django.contrib import messages
   from django.http import JsonResponse
   from django.views.decorators.csrf import csrf_exempt
   from django.views.decorators.http import require_http_methods
   from .forms import RegistrationForm, LoginForm


   def register_view(request):
       """Регистрация пользователя"""
       if request.method == 'POST':
           form = RegistrationForm(request.POST)
           if form.is_valid():
               user = form.save()
               login(request, user)
               messages.success(request, 'Регистрация прошла успешно!')
               return redirect('home')
           # Ошибки валидации будут показаны в форме
       else:
           form = RegistrationForm()
       
       return render(request, 'user_auth/register.html', {'form': form})


   def login_view(request):
       """Авторизация пользователя"""
       if request.method == 'POST':
           form = LoginForm(data=request.POST)
           if form.is_valid():
               user = form.get_user()
               login(request, user)
               messages.success(request, 'Вы успешно авторизованы!')
               return redirect('home')
           # Ошибки валидации будут показаны в форме
       else:
           form = LoginForm()
       
       return render(request, 'user_auth/login.html', {'form': form})


   def logout_view(request):
       """Выход из системы"""
       logout(request)
       messages.info(request, 'Вы вышли из системы')
       return redirect('home')


   @login_required
   def profile(request):
       """Личный кабинет пользователя"""
       from orders.models import Order
       
       orders = Order.objects.filter(user=request.user).order_by('-created_at')
       
       context = {
           'orders': orders,
       }
       return render(request, 'user_auth/profile.html', context)

Особенности представлений user_auth:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- **register_view**: Регистрация с автоматическим входом
- **login_view**: Авторизация с сообщениями
- **logout_view**: Выход с редиректом
- **profile**: Личный кабинет с историей заказов

Декораторы и их назначение
--------------------------

.. list-table:: Декораторы Django
   :header-rows: 1
   :widths: 30 70

   * - Декоратор
     - Назначение
   * - ``@login_required``
     - Требует авторизации пользователя
   * - ``@require_http_methods(["POST"])``
     - Ограничивает доступ только для POST запросов
   * - ``@csrf_exempt``
     - Отключает CSRF защиту (используется осторожно!)

Типы представлений
------------------

**Функциональные представления:**
- Простые в понимании
- Прямолинейная логика
- Идеальны для простых страниц

**AJAX-представления:**
- Возвращают JSON ответы
- Используются для динамических операций
- Пример: добавление в корзину

**Представления с формами:**
- Обрабатывают данные форм
- Валидируют ввод пользователя
- Пример: оформление заказа

Следующий шаг
-------------

После создания представлений переходите к :doc:`templates` чтобы создать HTML шаблоны для наших страниц.

.. note::

   **Совет:** Используйте декораторы для защиты представлений и ограничения методов!

.. warning::

   Всегда используйте `transaction.atomic()` при работе с несколькими операциями с базой данных!