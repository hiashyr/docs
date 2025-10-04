import os
import sys
from pathlib import Path

# Добавляем пути Django
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Базовые расширения (без autoapi для начала)
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode', 
    'sphinx.ext.napoleon',
    'sphinx.ext.todo',
    'sphinx.ext.graphviz',
]

# Основные настройки
project = 'Проект Django на русском'
copyright = '2025, Irsp-122'
author = 'Irs-122'
release = '1.0.0'

# Язык
language = 'ru'

# Тема
html_theme = 'sphinx_rtd_theme'

# Кастомный CSS для скрытия навигационных кнопок
html_static_path = ['_static']
html_css_files = [
    'custom.css',
]

# Дополнительные настройки
html_show_sourcelink = False
html_show_sphinx = False

# Настройки autodoc
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__'
}

# Отключаем предупреждения о missing imports
autodoc_mock_imports = [
    'django',
    'users',
    'tasks', 
    'api',
    'flower_shop',
    'main',
    'orders'
]

# Если хотите безопасную попытку загрузки Django
try:
    import django
    from django.conf import settings
    
    if not settings.configured:
        settings.configure(
            DEBUG=True,
            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': ':memory:',
                }
            },
            INSTALLED_APPS=[
                'django.contrib.auth',
                'django.contrib.contenttypes',
                'django.contrib.sessions',
            ],
            SECRET_KEY='dummy-for-docs',
            USE_TZ=True,
        )
    
    django.setup()
    print("✅ Django настроен для документации")
except Exception as e:
    print(f"⚠️ Django не настроен: {e}")
    print("📝 Документация будет генерироваться без Django autodoc")