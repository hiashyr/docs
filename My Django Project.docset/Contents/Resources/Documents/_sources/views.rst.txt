Создание представлений (Views)
==============================

В этом разделе мы создадим представления для нашего приложения ekz. Представления обрабатывают запросы пользователей и возвращают ответы с данными.

Представление главной страницы
-------------------------------

Представление ``main_page`` отвечает за отображение главной страницы приложения.

Код представления
^^^^^^^^^^^^^^^^^

.. code-block:: python

   def main_page(request):
       popular_products = Product.objects.all()[:8]
       context = {
           'popular_products': popular_products
       }
       return render(request, 'pages/main_page.html', context)

Разбор кода
^^^^^^^^^^^

Функция main_page
~~~~~~~~~~~~~~~~~

.. code-block:: python

   def main_page(request):

**Назначение:** Объявление функции представления.

**Параметры:**
- ``request`` - объект HttpRequest, содержащий информацию о запросе пользователя
- Каждое представление Django принимает request первым параметром

Получение популярных товаров
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   popular_products = Product.objects.all()[:8]

**Назначение:** Получает товары для отображения на главной странице.

**Логика:**
- ``Product.objects.all()`` - получает все товары из базы данных
- ``[:8]`` - ограничивает результат первыми 8 товарами
- **Примечание:** В будущем можно добавить логику для определения действительно популярных товаров

Создание контекста
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   context = {
       'popular_products': popular_products
   }

**Назначение:** Подготавливает данные для передачи в шаблон.

**Структура:**
- ``context`` - словарь с данными
- ``'popular_products'`` - ключ, по которому данные будут доступны в шаблоне
- ``popular_products`` - значение (QuerySet с товарами)

Возврат ответа
~~~~~~~~~~~~~~

.. code-block:: python

   return render(request, 'pages/main_page.html', context)

**Назначение:** Возвращает отрендеренный HTML-ответ.

**Параметры:**
- ``request`` - исходный объект запроса
- ``'pages/main_page.html'`` - путь к шаблону
- ``context`` - словарь с данными для шаблона

.. note::

   **Совет:** Для улучшения производительности можно использовать ``select_related()`` или ``prefetch_related()`` если товары связаны с другими моделями.

.. warning::

   Использование ``Product.objects.all()[:8]`` без сортировки может возвращать разные товары при каждом запросе. Рекомендуется добавить сортировку.

Представление регистрации пользователя
--------------------------------------

Представление ``register_view`` обрабатывает регистрацию новых пользователей в системе.

Код представления
^^^^^^^^^^^^^^^^^

.. code-block:: python

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

Разбор кода
^^^^^^^^^^^

Функция register_view
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def register_view(request):

**Назначение:** Объявление функции представления для регистрации.

**Особенности:**
- Обрабатывает как GET (показ формы), так и POST (отправка данных) запросы
- Использует кастомную форму регистрации

Проверка метода запроса
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   if request.method == 'POST':

**Назначение:** Определяет тип HTTP-запроса.

**Логика:**
- ``POST`` - пользователь отправил данные формы
- Любой другой метод (обычно ``GET``) - пользователь запрашивает страницу

Обработка POST-запроса
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   form = CustomUserCreationForm(request.POST, request.FILES)

**Назначение:** Создает форму с данными от пользователя.

**Параметры:**
- ``request.POST`` - данные формы (текстовые поля)
- ``request.FILES`` - загруженные файлы (например, аватар)

Валидация и сохранение формы
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   if form.is_valid():
       user = form.save()

**Назначение:** Проверяет корректность данных и сохраняет пользователя.

**Логика:**
- ``form.is_valid()`` - проверяет все валидаторы формы
- ``form.save()`` - создает нового пользователя в базе данных
- Возвращает созданный объект пользователя

Автоматический вход после регистрации
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   login(request, user, backend='django.contrib.auth.backends.ModelBackend')

**Назначение:** Выполняет вход пользователя сразу после регистрации.

**Параметры:**
- ``request`` - объект запроса
- ``user`` - созданный пользователь
- ``backend`` - указывает бэкенд аутентификации

Редирект после успешной регистрации
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   return redirect('main_page')

**Назначение:** Перенаправляет пользователя на главную страницу.

**Особенности:**
- ``'main_page'`` - имя URL-шаблона из urls.py
- Пользователь сразу попадает в систему

Обработка GET-запроса
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   else:
       form = CustomUserCreationForm()

**Назначение:** Создает пустую форму для отображения.

**Логика:**
- Выполняется когда метод запроса не POST
- Подготавливает чистую форму для заполнения

Возврат ответа с формой
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   return render(request, 'components/register.html', {'form': form})

**Назначение:** Отображает страницу регистрации с формой.

**Параметры:**
- ``'components/register.html'`` - шаблон страницы регистрации
- ``{'form': form}`` - передает форму в контекст шаблона

.. note::

   **Важно:** Указание бэкенда аутентификации необходимо при использовании кастомной модели пользователя.

.. warning::

   Всегда проверяйте метод запроса для разделения логики отображения формы и обработки данных.

Представление входа в систему
------------------------------

Представление ``login_view`` обрабатывает вход пользователей в систему с поддержкой нескольких типов аутентификации.

Код представления
^^^^^^^^^^^^^^^^^

.. code-block:: python

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

Разбор кода
^^^^^^^^^^^

Определение типа аутентификации
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   auth_type = request.POST.get('auth_type', request.GET.get('tab', 'username'))

**Назначение:** Определяет выбранный пользователем тип аутентификации.

**Логика:**
- ``request.POST.get('auth_type')`` - проверяет данные из отправленной формы
- ``request.GET.get('tab')`` - проверяет параметр URL (для вкладок)
- ``'username'`` - значение по умолчанию
- **Приоритет:** POST данные > GET параметры > значение по умолчанию

Обработка POST-запроса
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   if request.method == 'POST':

**Назначение:** Обрабатывает отправку данных формы входа.

Выбор формы по типу аутентификации
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   if auth_type == 'phone':
       form = PhoneAuthForm(request.POST)
   elif auth_type == 'email':
       form = EmailAuthForm(request.POST)
   else:
       form = UsernameAuthForm(request.POST)

**Назначение:** Создает соответствующую форму с данными пользователя.

**Типы аутентификации:**
- ``phone`` - вход по номеру телефона
- ``email`` - вход по email адресу  
- ``username`` - вход по имени пользователя (по умолчанию)

Валидация и аутентификация
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   if form.is_valid():
       user = form.get_user()
       login(request, user, backend='django.contrib.auth.backends.ModelBackend')
       return redirect('main_page')

**Назначение:** Проверяет данные и выполняет вход пользователя.

**Логика:**
- ``form.is_valid()`` - проверяет корректность введенных данных
- ``form.get_user()`` - возвращает объект пользователя после успешной аутентификации
- ``login()`` - создает сессию пользователя
- ``redirect('main_page')`` - перенаправляет на главную страницу

Обработка GET-запроса
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   else:
       if auth_type == 'phone':
           form = PhoneAuthForm()
       elif auth_type == 'email':
           form = EmailAuthForm()
       else:
           form = UsernameAuthForm()

**Назначение:** Создает пустые формы для отображения страницы входа.

**Особенности:**
- Использует тот же ``auth_type`` для согласованности
- Подготавливает правильную форму для выбранного типа аутентификации

Возврат ответа с контекстом
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   return render(request, 'components/login.html', {
       'form': form,
       'active_tab': auth_type
   })

**Назначение:** Отображает страницу входа с формой и активной вкладкой.

**Контекст:**
- ``'form'`` - объект формы для рендеринга
- ``'active_tab'`` - текущий активный тип аутентификации для подсветки вкладки

Преимущества подхода
~~~~~~~~~~~~~~~~~~~

- **Гибкость:** Поддержка нескольких способов входа
- **Удобство:** Сохранение выбранного типа аутентификации между запросами
- **Модульность:** Разделение логики для разных типов аутентификации

.. note::

   **Совет:** Для улучшения UX можно добавить переключение между вкладками без перезагрузки страницы с помощью JavaScript.

.. warning::

   Убедитесь, что все формы аутентификации правильно реализуют метод ``get_user()`` для возврата объекта пользователя.

Представление выхода из системы
-------------------------------

Представление ``logout_view`` обрабатывает выход пользователя из системы.

Код представления
^^^^^^^^^^^^^^^^^

.. code-block:: python

   def logout_view(request):
       logout(request)
       return redirect('main_page')

Разбор кода
^^^^^^^^^^^

Функция logout_view
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def logout_view(request):

**Назначение:** Объявление функции представления для выхода из системы.

**Особенности:**
- Очень простое представление без сложной логики
- Обычно вызывается по GET-запросу (ссылка "Выйти")

Выход из системы
~~~~~~~~~~~~~~~~

.. code-block:: python

   logout(request)

**Назначение:** Завершает сеанс пользователя.

**Действие:**
- Удаляет данные сессии из базы данных
- Очищает cookies в браузере пользователя
- Пользователь больше не считается аутентифицированным

Редирект на главную страницу
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   return redirect('main_page')

**Назначение:** Перенаправляет пользователя после выхода.

**Логика:**
- ``'main_page'`` - имя URL-шаблона главной страницы
- Пользователь попадает на публичную часть сайта
- Можно изменить на любую другую страницу (например, страницу входа)

Особенности реализации
~~~~~~~~~~~~~~~~~~~

**Простота:** Минимальный код без лишней логики

**Безопасность:** 
- Не требует проверки метода запроса
- Безопасно вызывать даже если пользователь уже вышел

**Надежность:** Всегда выполняет перенаправление

Рекомендации по использованию
~~~~~~~~~~~~~~~~~~~

- **Защита CSRF:** Убедитесь, что выход выполняется через POST-запрос или с CSRF-токеном
- **Сообщения:** Можно добавить flash-сообщение о успешном выходе:

.. code-block:: python

   from django.contrib import messages

   def logout_view(request):
       logout(request)
       messages.info(request, 'Вы успешно вышли из системы')
       return redirect('main_page')

- **Логирование:** Для отладки можно добавить логирование:

.. code-block:: python

   import logging

   def logout_view(request):
       logger = logging.getLogger(__name__)
       logger.info(f'User {request.user} logged out')
       logout(request)
       return redirect('main_page')

.. note::

   **Важно:** Функция ``logout()`` безопасна для многократного вызова - она не вызывает ошибок если пользователь уже вышел.

.. warning::

   Для безопасности рекомендуется использовать POST-запросы для выхода из системы, чтобы предотвратить CSRF-атаки.

Представление каталога с фильтрацией
-------------------------------------

Представление ``catalog_view`` отображает каталог товаров с поддержкой фильтрации по категориям, поиска и ценового диапазона.

Код представления
^^^^^^^^^^^^^^^^^

.. code-block:: python

   def catalog_view(request):
       categories = Category.objects.all()
       
       category_id = request.GET.get('category')
       search_query = request.GET.get('q')
       min_price = request.GET.get('min_price')
       max_price = request.GET.get('max_price')
       
       products = Product.objects.all()
       
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

Разбор кода
^^^^^^^^^^^

Получение списка категорий
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   categories = Category.objects.all()

**Назначение:** Получает все категории для отображения в фильтрах.

**Особенности:**
- Используется для построения выпадающего списка категорий
- Всегда загружается, независимо от примененных фильтров

Извлечение GET-параметров
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   category_id = request.GET.get('category')
   search_query = request.GET.get('q')
   min_price = request.GET.get('min_price')
   max_price = request.GET.get('max_price')

**Назначение:** Получает параметры фильтрации из URL.

**Параметры:**
- ``category`` - ID выбранной категории
- ``q`` - поисковый запрос
- ``min_price`` - минимальная цена
- ``max_price`` - максимальная цена
- **Метод:** ``.get()`` возвращает ``None`` если параметр отсутствует

Базовый QuerySet
~~~~~~~~~~~~~~~~

.. code-block:: python

   products = Product.objects.all()

**Назначение:** Создает начальную выборку всех товаров.

**Особенности:**
- Является точкой отсчета для применения фильтров
- QuerySet ленивый - выполнение происходит только при использовании результатов

Фильтрация по категории
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   if category_id:
       products = products.filter(category_id=category_id)

**Назначение:** Фильтрует товары по выбранной категории.

**Логика:**
- Проверяет, что ``category_id`` не ``None``
- Использует ``filter()`` для сужения выборки
- ``category_id`` - прямое указание ID без загрузки объекта Category

Поиск по названию и описанию
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   if search_query:
       products = products.filter(
           Q(name__icontains=search_query) | 
           Q(description__icontains=search_query)
       )

**Назначение:** Выполняет поиск товаров по названию и описанию.

**Особенности:**
- ``Q()`` объекты позволяют строить сложные запросы
- ``|`` - оператор ИЛИ (OR)
- ``icontains`` - регистронезависимое совпадение подстроки
- Ищет как в названии, так и в описании товара

Фильтрация по цене
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   if min_price:
       products = products.filter(price__gte=min_price)
   
   if max_price:
       products = products.filter(price__lte=max_price)

**Назначение:** Фильтрует товары по ценовому диапазону.

**Операторы:**
- ``gte`` - Greater Than or Equal (больше или равно)
- ``lte`` - Less Than or Equal (меньше или равно)
- Можно использовать одновременно для диапазона

Подготовка контекста
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   context = {
       'categories': categories,
       'products': products,
       'selected_category': category_id,
       'search_query': search_query,
       'min_price': min_price,
       'max_price': max_price
   }

**Назначение:** Собирает все данные для передачи в шаблон.

**Структура контекста:**
- ``categories`` - все категории для фильтра
- ``products`` - отфильтрованные товары
- ``selected_category`` - сохраняет выбранную категорию для формы
- ``search_query`` - сохраняет поисковый запрос
- ``min_price, max_price`` - сохраняют значения ценовых фильтров

Возврат ответа
~~~~~~~~~~~~~~

.. code-block:: python

   return render(request, 'pages/catalog.html', context)

**Назначение:** Отображает страницу каталога с примененными фильтрами.

Особенности реализации
~~~~~~~~~~~~~~~~~~~

**Постепенная фильтрация:** Каждый фильтр применяется последовательно к QuerySet

**Сохранение состояния:** Все параметры фильтрации передаются обратно в шаблон

**Гибкость:** Легко добавить новые фильтры без изменения структуры

.. note::

   **Производительность:** Для большого количества товаров рассмотрите использование ``select_related('category')`` для избежания N+1 запросов.

.. warning::

   Фильтрация по цене предполагает, что параметры передаются как числа. Добавьте валидацию для защиты от неверных данных.

Представление детальной страницы товара
----------------------------------------

Представление ``product_detail_view`` отображает подробную информацию о конкретном товаре.

Код представления
^^^^^^^^^^^^^^^^^

.. code-block:: python

   def product_detail_view(request, product_id):
       product = get_object_or_404(Product, id=product_id)
       context = {'product': product}
       return render(request, 'pages/product_detail.html', context)

Разбор кода
^^^^^^^^^^^

Функция с параметром product_id
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def product_detail_view(request, product_id):

**Назначение:** Объявление функции представления с параметром URL.

**Особенности:**
- ``product_id`` - параметр из URL, который передается в функцию
- Обычно извлекается из пути URL, например: ``/products/123/``

Получение товара или 404 ошибка
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   product = get_object_or_404(Product, id=product_id)

**Назначение:** Получает товар по ID или возвращает страницу 404.

**Параметры:**
- ``Product`` - модель для поиска
- ``id=product_id`` - условие поиска по первичному ключу
- **Альтернатива:** ``Product.objects.get(id=product_id)``, но тогда нужно обрабатывать исключение вручную

Преимущества get_object_or_404
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Эквивалентная ручная реализация:
   try:
       product = Product.objects.get(id=product_id)
   except Product.DoesNotExist:
       raise Http404("Товар не существует")

**Сравнение:**
- ``get_object_or_404()`` - более компактная и читаемая запись
- Автоматически генерирует соответствующий HTTP-ответ
- Стандартный Django подход для таких случаев

Представление корзины пользователя
-----------------------------------

Представление ``cart_view`` отображает содержимое корзины текущего пользователя с подсчетом общей суммы.

Код представления
^^^^^^^^^^^^^^^^^

.. code-block:: python

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

Разбор кода
^^^^^^^^^^^

Декоратор login_required
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   @login_required

**Назначение:** Ограничивает доступ к представлению только для авторизованных пользователей.

**Действие:**
- Если пользователь не авторизован, перенаправляет на страницу входа
- После входа возвращает на запрошенную страницу корзины
- **Альтернатива:** Можно использовать ``LoginRequiredMixin`` для класс-базированных представлений

Получение элементов корзины
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   cart_items = CartItem.objects.filter(user=request.user)

**Назначение:** Получает все товары в корзине текущего пользователя.

**Особенности:**
- ``request.user`` - текущий авторизованный пользователь
- ``filter(user=request.user)`` - только элементы корзины этого пользователя
- **Производительность:** Рассмотрите ``select_related('product')`` для избежания N+1 запросов

Подсчет общей суммы
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   total_amount = sum(item.get_total() for item in cart_items)

**Назначение:** Вычисляет общую стоимость всех товаров в корзине.

**Логика:**
- ``item.get_total()`` - вызывает метод модели CartItem для расчета стоимости элемента
- ``sum()`` - встроенная функция Python для суммирования
- **Генератор:** Использует generator expression для эффективного вычисления

Метод get_total() модели CartItem
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # В модели CartItem (напоминание)
   def get_total(self):
       if self.product and self.product.price and self.quantity:
           return self.product.price * self.quantity
       return 0

**Назначение:** Вычисляет стоимость одного элемента корзины.

**Преимущества:**
- Логика расчета инкапсулирована в модели
- Можно переиспользовать в других местах
- Обрабатывает случаи с отсутствующими данными

Подготовка контекста
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   context = {
       'cart_items': cart_items,
       'total_amount': total_amount
   }

**Назначение:** Собирает данные для отображения в корзине.

**Структура:**
- ``cart_items`` - список элементов корзины для отображения в таблице
- ``total_amount`` - общая сумма для отображения в итоговой строке

Возврат ответа
~~~~~~~~~~~~~~

.. code-block:: python

   return render(request, 'pages/cart.html', context)

**Назначение:** Отображает страницу корзины с товарами и общей суммой.

Оптимизации и улучшения
~~~~~~~~~~~~~~

**Оптимизация запросов:**

.. code-block:: python

   @login_required
   def cart_view(request):
       cart_items = CartItem.objects.filter(
           user=request.user
       ).select_related('product')
       
       total_amount = sum(item.get_total() for item in cart_items)
       
       context = {
           'cart_items': cart_items,
           'total_amount': total_amount
       }
       return render(request, 'pages/cart.html', context)

**Добавление проверки пустой корзины:**

.. code-block:: python

   @login_required
   def cart_view(request):
       cart_items = CartItem.objects.filter(user=request.user)
       
       if not cart_items.exists():
           messages.info(request, 'Ваша корзина пуста')
           return redirect('catalog')
       
       total_amount = sum(item.get_total() for item in cart_items)
       
       context = {
           'cart_items': cart_items,
           'total_amount': total_amount
       }
       return render(request, 'pages/cart.html', context)

Особенности реализации
~~~~~~~~~~~~~~~~~~~

**Безопасность:** Доступ только для авторизованных пользователей

**Производительность:** Один запрос к базе данных для получения элементов корзины

**Гибкость:** Легко расширить дополнительной логикой (скидки, доставка и т.д.)

.. note::

   **Совет:** Для больших корзин можно вынести подсчет суммы в базу данных с помощью ``aggregate()``:
   ``total_amount = cart_items.aggregate(total=Sum(F('product__price') * F('quantity')))['total'] or 0``

.. warning::

   Убедитесь, что метод ``get_total()`` в модели CartItem корректно обрабатывает случаи, когда товар или цена отсутствуют.

Представление добавления товара в корзину
------------------------------------------

Представление ``add_to_cart`` добавляет товар в корзину пользователя или увеличивает количество, если товар уже есть.

Код представления
^^^^^^^^^^^^^^^^^

.. code-block:: python

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

Разбор кода
^^^^^^^^^^^

Защита декоратором
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   @login_required

**Назначение:** Гарантирует, что только авторизованные пользователи могут добавлять товары в корзину.

**Важность:** Предотвращает добавление товаров анонимными пользователями

Получение товара
~~~~~~~~~~~~~~~~

.. code-block:: python

   product = get_object_or_404(Product, id=product_id)

**Назначение:** Находит товар по ID или возвращает 404 ошибку.

**Безопасность:** Защищает от добавления несуществующих товаров

Метод get_or_create
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   cart_item, created = CartItem.objects.get_or_create(
       user=request.user,
       product=product,
       defaults={'quantity': 1}
   )

**Назначение:** Находит или создает элемент корзины.

**Параметры:**
- ``user=request.user`` - пользователь для поиска/создания
- ``product=product`` - товар для поиска/создания
- ``defaults={'quantity': 1}`` - значения по умолчанию при создании

**Возвращаемые значения:**
- ``cart_item`` - найденный или созданный объект
- ``created`` - boolean: True если создан новый, False если найден существующий

Логика увеличения количества
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   if not created:
       cart_item.quantity += 1
       cart_item.save()

**Назначение:** Увеличивает количество, если товар уже есть в корзине.

**Условие:** ``not created`` - если объект :ref:`​ <templates_code>` не был создан (уже существовал)

**Действие:**
- Увеличивает количество на 1
- Сохраняет изменения в базе данных

Редирект на корзину
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   return redirect('cart')

**Назначение:** Перенаправляет пользователя на страницу корзины.

**Пользовательский опыт:** Позволяет сразу увидеть добавленный товар

Альтернативные реализации
~~~~~~~~~~~~~~~~~~~

**С обработкой ошибок:**

.. code-block:: python

   @login_required
   def add_to_cart(request, product_id):
       try:
           product = Product.objects.get(id=product_id)
       except Product.DoesNotExist:
           messages.error(request, 'Товар не найден')
           return redirect('catalog')
       
       # Остальная логика...
       return redirect('cart')

**С сообщениями об успехе:**

.. code-block:: python

   @login_required
   def add_to_cart(request, product_id):
       product = get_object_or_404(Product, id=product_id)
       
       cart_item, created = CartItem.objects.get_or_create(
           user=request.user,
           product=product,
           defaults={'quantity': 1}
       )
       
       if not created:
           cart_item.quantity += 1
           cart_item.save()
           messages.success(request, f'Количество "{product.name}" увеличено')
       else:
           messages.success(request, f'Товар "{product.name}" добавлен в корзину')
       
       return redirect('cart')

**С AJAX поддержкой:**

.. code-block:: python

   @login_required
   def add_to_cart(request, product_id):
       if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
           # AJAX запрос - возвращаем JSON
           product = get_object_or_404(Product, id=product_id)
           
           cart_item, created = CartItem.objects.get_or_create(
               user=request.user,
               product=product,
               defaults={'quantity': 1}
           )
           
           if not created:
               cart_item.quantity += 1
               cart_item.save()
           
           return JsonResponse({
               'success': True,
               'message': 'Товар добавлен в корзину',
               'cart_count': CartItem.objects.filter(user=request.user).count()
           })
       
       # Обычный запрос - редирект
       # ... обычная логика

Особенности реализации
~~~~~~~~~~~~~~~~~~~

**Эффективность:** Один запрос к базе для поиска/создания

**Удобство:** Автоматическое увеличение количества существующих товаров

**Надежность:** Обработка несуществующих товаров через 404

.. note::

   **Совет:** Для улучшения UX можно добавить параметр количества:
   ``quantity = request.POST.get('quantity', 1)`` и использовать его в ``defaults``

.. warning::

   Убедитесь, что в модели CartItem установлено ``unique_together`` для полей ``user`` и ``product``, чтобы ``get_or_create`` работал корректно.


Представление обновления количества товара в корзине
-----------------------------------------------------

Представление ``update_cart_item`` обновляет количество конкретного товара в корзине пользователя с использованием формы.

Код представления
^^^^^^^^^^^^^^^^^

.. code-block:: python

   @login_required
   def update_cart_item(request, item_id):
       cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
       
       if request.method == 'POST':
           form = CartItemQuantityForm(request.POST, instance=cart_item)
           if form.is_valid():
               form.save()
       
       return redirect('cart')

Разбор кода
^^^^^^^^^^^

Безопасное получение элемента корзины
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)

**Назначение:** Находит элемент корзины с двойной проверкой безопасности.

**Условия поиска:**
- ``id=item_id`` - по идентификатору элемента
- ``user=request.user`` - принадлежность текущему пользователю
- **Безопасность:** Предотвращает изменение чужих корзин

Проверка метода запроса
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   if request.method == 'POST':

**Назначение:** Обеспечивает, что обновление происходит только через POST-запрос.

**Безопасность:** Защищает от CSRF-атак и случайных изменений

Создание формы с данными
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   form = CartItemQuantityForm(request.POST, instance=cart_item)

**Назначение:** Создает форму с данными от пользователя и привязывает к существующему объекту.

**Параметры:**
- ``request.POST`` - данные из отправленной формы
- ``instance=cart_item`` - объект для обновления (а не создания нового)

Валидация и сохранение
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   if form.is_valid():
       form.save()

**Назначение:** Проверяет данные и сохраняет изменения.

**Логика:**
- ``form.is_valid()`` - проверяет корректность введенного количества
- ``form.save()`` - обновляет объект в базе данных
- **Автоматически:** Применяет все изменения к ``cart_item``

Редирект на корзину
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   return redirect('cart')

**Назначение:** Возвращает пользователя на страницу корзины после обновления.


Представление удаления товара из корзины
-----------------------------------------

Представление ``remove_from_cart`` удаляет конкретный товар из корзины пользователя.

Код представления
^^^^^^^^^^^^^^^^^

.. code-block:: python

   @login_required
   def remove_from_cart(request, item_id):
       cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
       cart_item.delete()
       return redirect('cart')

Разбор кода
^^^^^^^^^^^

Защита доступа
~~~~~~~~~~~~~~

.. code-block:: python

   @login_required

**Назначение:** Ограничивает доступ только для авторизованных пользователей.

**Важность:** Предотвращает удаление товаров из корзины анонимными пользователями

Безопасное получение элемента
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)

**Назначение:** Находит элемент корзины с проверкой принадлежности.

**Условия поиска:**
- ``id=item_id`` - идентификатор элемента корзины
- ``user=request.user`` - принадлежность текущему пользователю
- **Безопасность:** Гарантирует, что пользователь может удалять только свои товары

Удаление элемента
~~~~~~~~~~~~~~~~~

.. code-block:: python

   cart_item.delete()

**Назначение:** Удаляет элемент корзины из базы данных.

**Действие:**
- Выполняет SQL DELETE запрос
- Объект полностью удаляется из базы данных
- **Атомарность:** Операция выполняется как единое целое

Редирект на корзину
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   return redirect('cart')

**Назначение:** Перенаправляет пользователя обратно в корзину.

**Пользовательский опыт:** Позволяет сразу увидеть обновленную корзину без удаленного товара

Альтернативные реализации
~~~~~~~~~~~~~~~~~~~

**С проверкой метода запроса:**

.. code-block:: python

   @login_required
   def remove_from_cart(request, item_id):
       if request.method == 'POST':
           cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
           cart_item.delete()
       return redirect('cart')

**С сообщением об успехе:**

.. code-block:: python

   @login_required
   def remove_from_cart(request, item_id):
       cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
       product_name = cart_item.product.name if cart_item.product else 'Товар'
       cart_item.delete()
       messages.success(request, f'{product_name} удален из корзины')
       return redirect('cart')

Представление страницы контактов
-----------------------------------------

Представление ``contacts_view`` удаляет конкретный товар из корзины пользователя.

Код представления
^^^^^^^^^^^^^^^^^

.. code-block:: python

    def contacts_view(request):
        return render(request, 'pages/contacts.html')

Представление оформления заказа
-------------------------------

Представление ``checkout_view`` обрабатывает процесс оформления заказа из корзины пользователя.

Код представления
^^^^^^^^^^^^^^^^^

.. code-block:: python

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

Разбор кода
^^^^^^^^^^^

Проверка наличия товаров в корзине
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   cart_items = CartItem.objects.filter(user=request.user)
   if not cart_items.exists():
       return redirect('cart')

**Назначение:** Проверяет, что в корзине есть товары для оформления.

**Действие:** Если корзина пуста - перенаправляет обратно в корзину

Подсчет общей суммы
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   total_amount = sum(item.get_total() for item in cart_items)

**Назначение:** Вычисляет общую стоимость заказа на основе товаров в корзине

Обработка POST-запроса (отправка формы)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   if request.method == 'POST':
       form = OrderForm(request.POST)

**Назначение:** Обрабатывает отправленные данные формы заказа

Создание заказа с дополнительными полями
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   order = form.save(commit=False)
   order.user = request.user
   order.total_amount = total_amount
   order.save()

**Назначение:** Создает объект заказа с автоматическим заполнением полей.

**Логика:**
- ``commit=False`` - создает объект без сохранения в БД
- Заполняет ``user`` и ``total_amount`` вручную
- ``order.save()`` - сохраняет заказ в базе данных

Создание элементов заказа
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   for cart_item in cart_items:
       OrderItem.objects.create(
           order=order,
           product=cart_item.product,
           quantity=cart_item.quantity,
           price=cart_item.product.price
       )

**Назначение:** Переносит товары из корзины в заказ.

**Особенности:**
- Сохраняет текущую цену товара на момент заказа
- Создает связь между заказом и товарами

Очистка корзины и редирект
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   cart_items.delete()
   return redirect('order_success', order_id=order.id)

**Назначение:** Удаляет товары из корзины и перенаправляет на страницу успеха

Обработка GET-запроса (показ формы)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   else:
       initial_data = {
           'shipping_address': request.user.address,
           'phone': request.user.phone,
           'email': request.user.email
       }
       form = OrderForm(initial=initial_data)

**Назначение:** Подготавливает форму с предзаполненными данными пользователя.

**Удобство:** Автоматически заполняет адрес, телефон и email из профиля

Отображение страницы оформления
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   context = {
       'form': form,
       'cart_items': cart_items,
       'total_amount': total_amount
   }
   return render(request, 'pages/checkout.html', context)

**Назначение:** Показывает страницу оформления заказа с формой и товарами

Особенности реализации
----------------------

**Целостность данных:** Сохранение цены товара на момент заказа

**Удобство:** Автозаполнение данных пользователя

**Очистка:** Автоматическое удаление товаров из корзины после оформления

.. note::

   **Рекомендация:** Добавьте обработку исключений для случаев, когда товар становится недоступным между добавлением в корзину и оформлением заказа.

.. warning::

   Убедитесь, что метод ``get_total()`` в модели CartItem корректно вычисляет стоимость, так как от этого зависит итоговая сумма заказа.

Представление страницы успешного заказа
----------------------------------------

Представление ``order_success_view`` показывает подтверждение успешно оформленного заказа.

Код представления
^^^^^^^^^^^^^^^^^

.. code-block:: python

   @login_required
   def order_success_view(request, order_id):
       order = get_object_or_404(Order, id=order_id, user=request.user)
       
       context = {
           'order': order
       }
       
       return render(request, 'pages/order_success.html', context)

Разбор кода
^^^^^^^^^^^

Безопасное получение заказа
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   order = get_object_or_404(Order, id=order_id, user=request.user)

**Назначение:** Находит заказ с проверкой принадлежности пользователю.

**Условия:**
- ``id=order_id`` - идентификатор заказа из URL
- ``user=request.user`` - гарантирует, что пользователь видит только свои заказы

Подготовка контекста
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   context = {
       'order': order
   }

**Назначение:** Передает объект заказа в шаблон для отображения деталей

Отображение страницы успеха
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   return render(request, 'pages/order_success.html', context)

**Назначение:** Показывает страницу с подтверждением заказа и его деталями

Особенности реализации
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Безопасность:** Пользователи видят только свои заказы

**Простота:** Минимальный код для отображения информации

**Связь:** Используется после ``checkout_view`` для показа результатов

.. note::

   В шаблоне ``order_success.html`` можно отображать номер заказа, список товаров, общую сумму и контактную информацию.

Представление списка заказов
-----------------------------

Представление ``orders_view`` показывает историю заказов пользователя.

Код представления
^^^^^^^^^^^^^^^^^

.. code-block:: python

   @login_required
   def orders_view(request):
       orders = Order.objects.filter(user=request.user).order_by('-created_at')
       
       context = {
           'orders': orders
       }
       
       return render(request, 'pages/orders.html', context)

Разбор кода
^^^^^^^^^^^

Получение заказов пользователя
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   orders = Order.objects.filter(user=request.user).order_by('-created_at')

**Назначение:** Получает все заказы текущего пользователя.

**Сортировка:** ``-created_at`` - показывает сначала самые новые заказы

Подготовка контекста
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   context = {
       'orders': orders
   }

**Назначение:** Передает список заказов в шаблон для отображения

Отображение страницы заказов
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   return render(request, 'pages/orders.html', context)

**Назначение:** Показывает страницу с историей всех заказов пользователя

Особенности реализации
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Безопасность:** Пользователь видит только свои заказы

**Удобство:** Сортировка по дате создания (новые сверху)

**Производительность:** Один запрос к базе данных

.. note::

   В шаблоне ``orders.html`` можно отображать номер заказа, дату, статус и общую сумму каждого заказа.

Представление детальной страницы заказа
----------------------------------------

Представление ``order_detail_view`` показывает подробную информацию о конкретном заказе.

Код представления
^^^^^^^^^^^^^^^^^

.. code-block:: python

   @login_required
   def order_detail_view(request, order_id):
       order = get_object_or_404(Order, id=order_id, user=request.user)
       order_items = OrderItem.objects.filter(order=order)
       
       context = {
           'order': order,
           'order_items': order_items
       }
       
       return render(request, 'pages/order_detail.html', context)

Разбор кода
^^^^^^^^^^^

Безопасное получение заказа
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   order = get_object_or_404(Order, id=order_id, user=request.user)

**Назначение:** Находит заказ с проверкой принадлежности пользователю.

**Безопасность:** Предотвращает просмотр чужих заказов

Получение элементов заказа
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   order_items = OrderItem.objects.filter(order=order)

**Назначение:** Получает все товары, входящие в этот заказ.

**Связь:** Использует связь между Order и OrderItem

Подготовка контекста
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   context = {
       'order': order,
       'order_items': order_items
   }

**Назначение:** Передает заказ и его товары в шаблон.

**Структура:**
- ``order`` - основная информация о заказе
- ``order_items`` - список товаров в заказе

Отображение детальной страницы
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   return render(request, 'pages/order_detail.html', context)

**Назначение:** Показывает страницу с полной информацией о заказе

Особенности реализации
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Безопасность:** Двойная проверка принадлежности заказа

**Полнота:** Отображает как основную информацию, так и список товаров

**Производительность:** Два запроса к базе данных

.. note::

   Для оптимизации можно использовать ``select_related()`` или ``prefetch_related()`` если нужно загрузить связанные данные о товарах.

Представление профиля пользователя
-----------------------------------

Представление ``profile_view`` отображает и обновляет профиль пользователя.

Код представления
^^^^^^^^^^^^^^^^^

.. code-block:: python

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

Разбор кода
^^^^^^^^^^^

Получение текущего пользователя
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   user = request.user

**Назначение:** Получает объект текущего авторизованного пользователя

Обработка POST-запроса (обновление профиля)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   if request.method == 'POST':

**Назначение:** Обрабатывает отправку формы редактирования профиля

Обновление полей пользователя
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   user.first_name = request.POST.get('first_name', user.first_name)
   user.last_name = request.POST.get('last_name', user.last_name)
   user.email = request.POST.get('email', user.email)
   user.phone = request.POST.get('phone', user.phone)
   user.address = request.POST.get('address', user.address)
   user.city = request.POST.get('city', user.city)
   user.country = request.POST.get('country', user.country)

**Назначение:** Обновляет данные пользователя из формы.

**Логика:** ``request.POST.get('field', user.field)`` - использует новое значение или оставляет старое

Обработка загрузки аватара
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   if 'avatar' in request.FILES:
       user.avatar = request.FILES['avatar']

**Назначение:** Обновляет аватар пользователя если файл был загружен

Сохранение изменений
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   user.save()
   return redirect('profile')

**Назначение:** Сохраняет изменения в базе и обновляет страницу

Получение истории заказов
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   orders = Order.objects.filter(user=user).order_by('-created_at')

**Назначение:** Получает заказы пользователя для отображения в профиле

Подготовка контекста
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   context = {
       'user': user,
       'orders': orders
   }

**Назначение:** Передает данные пользователя и его заказы в шаблон

Отображение страницы профиля
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   return render(request, 'pages/profile.html', context)

**Назначение:** Показывает страницу профиля с формой редактирования и историей заказов

Особенности реализации
~~~~~~~~~~~~~~~~~~~~~~~~~~~ы

**Гибкость:** Позволяет обновлять отдельные поля без потери остальных данных

**Удобство:** Сочетает редактирование профиля и просмотр истории заказов

**Безопасность:** Работает только с текущим пользователем

.. note::

   Для улучшения безопасностаи добавьте валидацию email и проверку уникальности.

.. warning::

   Прямая работа с ``request.POST`` без формы может быть уязвима. Рекомендуется использовать ModelForm для валидации данных.


Импорт
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Не забывайте про импорт!
Обычный импорт выглядит таким образом:

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