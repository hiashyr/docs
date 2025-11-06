Создание Sitemap.xml
=====================

Что такое Sitemap.xml?
-----------------------

Sitemap.xml - это файл карты сайта, который помогает поисковым системам:

* Находить все страницы вашего сайта
* Быстро индексировать новый контент  
* Понимать структуру и важность страниц
* Отслеживать частоту обновлений

Где создать?
------------

Для простого варианта сойдет поместить файл в директорию static и таким образом можно будет перейти на данную страницу, не указывая urls. Путь будет такой: http://127.0.0.1:8000/static/sitemap.xml

Формат файла
------------

Базовая структура sitemap.xml::

    <?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
        <url>
            <loc>https://example.com/</loc>
            <lastmod>2024-01-20</lastmod>
            <changefreq>weekly</changefreq>
            <priority>1.0</priority>
        </url>
    </urlset>

Обязательные теги
-----------------

``<loc>``
~~~~~~~~~
**URL страницы**
Полный адрес страницы::

    <loc>https://mysite.com/page/</loc>

``<lastmod>``
~~~~~~~~~~~~~
**Дата последнего изменения**
Формат ГГГГ-ММ-ДД::

    <lastmod>2024-01-20</lastmod>

Опциональные теги
-----------------

``<changefreq>``
~~~~~~~~~~~~~~~~
**Частота изменений:**

* ``always`` - постоянно меняется
* ``hourly`` - каждый час
* ``daily`` - ежедневно  
* ``weekly`` - еженедельно
* ``monthly`` - ежемесячно
* ``yearly`` - ежегодно
* ``never`` - никогда не меняется

``<priority>``
~~~~~~~~~~~~~~
**Приоритет страницы (0.0 - 1.0):**

* ``1.0`` - максимальный (главная страница)
* ``0.9`` - очень высокий
* ``0.8`` - высокий (страницы товаров)
* ``0.5`` - средний
* ``0.3`` - низкий

Пример для книг
----------------------------

::

    <?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
        
        <!-- Главная страница -->
        <url>
            <loc>https://bookstore.com/</loc>
            <lastmod>2024-01-20</lastmod>
            <changefreq>weekly</changefreq>
            <priority>1.0</priority>
        </url>
        
        <!-- Каталог книг -->
        <url>
            <loc>https://bookstore.com/books/</loc>
            <lastmod>2024-01-18</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.9</priority>
        </url>
        
        <!-- Страница книги -->
        <url>
            <loc>https://bookstore.com/books/123/</loc>
            <lastmod>2024-01-15</lastmod>
            <changefreq>monthly</changefreq>
            <priority>0.8</priority>
        </url>
        
        <!-- Информационные страницы -->
        <url>
            <loc>https://bookstore.com/about/</loc>
            <lastmod>2024-01-10</lastmod>
            <changefreq>monthly</changefreq>
            <priority>0.6</priority>
        </url>
        
    </urlset>

Что включать в sitemap
~~~~~~~~~~~~~~~~~~~~~~

✅ **Включать:**

* Главная страница
* Страницы категорий
* Страницы товаров/услуг
* Информационные страницы
* Статьи и блог-посты

❌ **Не включать:**

* Страницы с параметрами фильтрации
* Страницы поиска
* Личные кабинеты пользователей
* Корзины покупок
* Административные разделы


robots.txt
==========================

Что такое robots.txt?
---------------------

Robots.txt - это файл с инструкциями для поисковых роботов (ботов), который указывает:

* Какие разделы сайта можно сканировать
* Какие разделы запрещены для индексации  
* Где находится карта сайта (sitemap)
* Скорость обхода (crawl delay)

Расположение файла
------------------

Файл должен находиться в директории статики сайта::

    https://example.com/static/robots.txt

Базовый синтаксис
-----------------

Директива User-agent
~~~~~~~~~~~~~~~~~~~~

Определяет, для каких роботов применяются правила::

    User-agent: *          # Для всех роботов
    User-agent: Googlebot  # Только для Google
    User-agent: Yandex     # Только для Yandex

Директива Allow
~~~~~~~~~~~~~~~

Разрешает доступ к указанным разделам::

    Allow: /               # Разрешить весь сайт
    Allow: /public/        # Разрешить только папку /public/
    Allow: *.html          # Разрешить HTML файлы

Директива Disallow
~~~~~~~~~~~~~~~~~~

Запрещает доступ к указанным разделам::

    Disallow: /admin/      # Запретить папку /admin/
    Disallow: /private/    # Запретить папку /private/
    Disallow: /search      # Запретить страницу поиска

Директива Sitemap
~~~~~~~~~~~~~~~~~

Указывает расположение карты сайта::

    Sitemap: https://example.com/static/sitemap.xml

Директива Crawl-delay
~~~~~~~~~~~~~~~~~~~~~

Устанавливает задержку между запросами (в секундах)::

    Crawl-delay: 2         # Задержка 2 секунды

Примеры конфигураций
--------------------

Базовый пример
~~~~~~~~~~~~~~

::

    User-agent: *
    Allow: /
    Disallow: /admin/
    Disallow: /private/
    
    Sitemap: https://example.com/static/sitemap.xml

Для книг
~~~~~~~~~~~~~~~~~~~~~

::

    User-agent: *
    Allow: /
    
    # Административные разделы
    Disallow: /admin/
    Disallow: /backend/
    Disallow: /control/
    
    # Пользовательские разделы  
    Disallow: /user/
    Disallow: /account/
    Disallow: /profile/
    Disallow: /cart/
    Disallow: /checkout/
    
    # Служебные разделы
    Disallow: /api/
    Disallow: /ajax/
    Disallow: /search/
    
    # Системные папки
    Disallow: /static/admin/
    Disallow: /media/private/
    
    Sitemap: https://bookstore.com/sitemap.xml
    Crawl-delay: 1

Что нужно запрещать
~~~~~~~~~~~~~~~~~~~

* **Административные панели** - ``/admin/``, ``/backend/``
* **Пользовательские данные** - ``/user/``, ``/account/``
* **Корзины покупок** - ``/cart/``, ``/checkout/``
* **Страницы поиска** - ``/search/``, ``/find/``
* **API endpoints** - ``/api/``, ``/ajax/``
* **Системные папки** - ``/tmp/``, ``/cache/``, ``/logs/``

Что не нужно запрещать
~~~~~~~~~~~~~~~~~~~~~~

* **Главная страница** - ``/``
* **Страницы категорий** - ``/books/``, ``/categories/``
* **Страницы товаров** - ``/product/``, ``/item/``
* **Статические ресурсы** - CSS, JS, изображения
* **Информационные страницы** - ``/about/``, ``/contact/``